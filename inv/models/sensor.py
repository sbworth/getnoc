# ----------------------------------------------------------------------
# Sensor model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
from threading import Lock
import operator
import datetime
from typing import Dict, Optional, Iterable, List

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, IntField, LongField, ListField, DateTimeField, DictField
import cachetools

# NOC modules
from noc.core.wf.decorator import workflow
from noc.core.bi.decorator import bi_sync
from noc.core.mongo.fields import PlainReferenceField, ForeignKeyField
from noc.main.models.label import Label
from noc.inv.models.object import Object
from noc.sa.models.managedobject import ManagedObject
from noc.pm.models.measurementunits import MeasurementUnits
from noc.pm.models.agent import Agent
from noc.wf.models.state import State
from .sensorprofile import SensorProfile

SOURCES = {"objectmodel", "asset", "etl", "manual"}

id_lock = Lock()
logger = logging.getLogger(__name__)

MODBUS_FORMAT = ["i16_be", "u16_be"]
for dt in ["i32", "u32", "f32"]:
    for df in ["be", "le", "bs", "ls"]:
        MODBUS_FORMAT.append(f"{dt}_{df}")


@Label.dynamic_classification(profile_model_id="inv.SensorProfile")
@Label.model
@bi_sync
@workflow
class Sensor(Document):
    meta = {
        "collection": "sensors",
        "strict": False,
        "auto_create_index": False,
        "indexes": ["agent", "managed_object", "object", "labels", "effective_labels"],
    }

    profile = PlainReferenceField(SensorProfile, default=SensorProfile.get_default_profile)
    object = PlainReferenceField(Object)
    managed_object = ForeignKeyField(ManagedObject)
    agent = PlainReferenceField(Agent)
    # Dynamic Profile Classification
    dynamic_classification_policy = StringField(
        choices=[("P", "Profile"), ("R", "By Rule"), ("D", "Disable")],
        default="P",
    )
    local_id = StringField()
    state = PlainReferenceField(State)
    units = PlainReferenceField(MeasurementUnits)
    label = StringField()
    dashboard_label = StringField()
    # Sources that find sensor
    sources = ListField(StringField(choices=list(SOURCES)))
    # Timestamp of last seen
    last_seen = DateTimeField()
    # Timestamp expired
    expired = DateTimeField()
    # Timestamp of first discovery
    first_discovered = DateTimeField(default=datetime.datetime.now)
    protocol = StringField(choices=["modbus_rtu", "modbus_ascii", "modbus_tcp", "snmp", "ipmi"])
    modbus_register = IntField()
    modbus_format = StringField(choices=MODBUS_FORMAT)
    snmp_oid = StringField()
    ipmi_id = StringField()
    bi_id = LongField(unique=True)
    # Labels
    labels = ListField(StringField())
    effective_labels = ListField(StringField())
    extra_labels = DictField()

    _id_cache = cachetools.TTLCache(maxsize=100, ttl=60)
    _bi_id_cache = cachetools.TTLCache(maxsize=100, ttl=60)

    def __str__(self):
        if self.object:
            return f"{self.object}: {self.local_id}"
        elif self.managed_object:
            return f"{self.managed_object}: {self.local_id}"
        return f"{self.units}: {self.local_id}"

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id):
        return Sensor.objects.filter(id=id).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_bi_id_cache"), lock=lambda _: id_lock)
    def get_by_bi_id(cls, id):
        return Sensor.objects.filter(bi_id=id).first()

    def clean(self):
        if self.extra_labels:
            self.labels += [
                ll
                for ll in Label.merge_labels(self.extra_labels.values())
                if Sensor.can_set_label(ll)
            ]

    @property
    def munits(self) -> MeasurementUnits:
        """
        Get effective units
        :return:
        """
        return self.profile.units or self.units

    def seen(self, source: Optional[str] = None):
        """
        Seen sensor
        """
        if source and source in SOURCES:
            self.sources = list(set(self.sources or []).union(set([source])))
            self._get_collection().update_one({"_id": self.id}, {"$addToSet": {"sources": source}})
        self.fire_event("seen")
        self.touch()  # Worflow expired

    def unseen(self, source: Optional[str] = None):
        """
        Unseen sensor
        """
        logger.info(
            "[%s|%s] Sensor is missed '%s'",
            self.object.name if self.object else "-",
            "-",
            self.local_id,
        )
        if source and source in SOURCES:
            self.sources = list(set(self.sources or []) - set([source]))
            self._get_collection().update_one({"_id": self.id}, {"$pull": {"sources": source}})
        elif not source:
            # For empty source, clean sources
            self.sources = []
            self._get_collection().update_one({"_id": self.id}, {"$set": {"sources": []}})
        if not self.sources:
            # source - None, set sensor to missed
            self.fire_event("missed")
            self.touch()

    def get_dynamic_classification_policy(self):
        if self.dynamic_classification_policy == "P":
            return self.profile.dynamic_classification_policy
        return self.dynamic_classification_policy

    @classmethod
    def can_set_label(cls, label):
        return Label.get_effective_setting(label, setting="enable_sensor")

    @classmethod
    def iter_effective_labels(cls, instance: "Sensor") -> Iterable[List[str]]:
        yield list(instance.labels or [])
        if instance.profile.labels:
            yield list(instance.profile.labels)
        yield Label.get_effective_regex_labels("sensor_local_id", instance.local_id)
        if instance.object:
            yield list(instance.object.effective_labels)
            mo_id = instance.object.get_data("management", "managed_object")
            if mo_id:
                mo = ManagedObject.get_by_id(mo_id)
                if mo:
                    yield list(mo.effective_labels)
        if instance.managed_object:
            yield list(instance.managed_object.effective_labels)


def sync_object(obj: "Object") -> None:
    """
    Synchronize sensors with object model
    :param obj:
    :return:
    """
    # Get existing sensors
    obj_sensors: Dict[str, Sensor] = {s.local_id: s for s in Sensor.objects.filter(object=obj.id)}
    logger.info("[%s] Sync sensor for ojbect", obj)
    m_proto = [
        d.value for d in obj.get_effective_data() if d.interface == "modbus" and d.attr == "type"
    ] or ["rtu"]
    agent = obj.get_effective_agent()
    mo = obj.get_data("management", "managed_object")
    if mo:
        mo = ManagedObject.get_by_id(mo)
    # Create new sensors
    for sensor in obj.model.sensors:
        if sensor.name in obj_sensors:
            s = obj_sensors.pop(sensor.name)
        else:
            logger.info(
                "[%s|%s] Creating new sensor '%s'", obj.name if obj else "-", "-", sensor.name
            )
            s = Sensor(
                profile=SensorProfile.get_default_profile(),
                object=obj,
                local_id=sensor.name,
            )
        if s.agent != agent:
            s.agent = agent
        if s.managed_object != mo:
            s.managed_object = mo
        if s.units != sensor.units:
            s.units = sensor.units
        if s.label != sensor.description:
            s.label = sensor.description
        # Get sensor protocol
        if sensor.modbus_register:
            if not m_proto:
                continue
            s.protocol = "modbus_%s" % m_proto[0].lower()
            s.modbus_register = sensor.modbus_register
            s.modbus_format = sensor.modbus_format or "u16_be"
        elif sensor.snmp_oid:
            s.protocol = "snmp"
            s.snmp_oid = sensor.snmp_oid
        else:
            logger.info(
                "[%s|%s] Unknown sensor protocol '%s'",
                obj.name if obj else "-",
                "-",
                sensor.name,
            )
        s.save()
        s.seen("objectmodel")
    # Notify missed sensors
    for s in sorted(obj_sensors):
        sensor = obj_sensors[s]
        sensor.unseen(source="objectmodel")
