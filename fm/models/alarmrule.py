# ---------------------------------------------------------------------
# AlarmGroup model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import operator
from threading import Lock

# Third-party modules
import cachetools
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField,
    BooleanField,
    ListField,
    LongField,
    ReferenceField,
    EmbeddedDocumentField,
)

# NOC modules
from noc.core.mongo.fields import PlainReferenceField, ForeignKeyField
from noc.main.models.label import Label
from noc.main.models.notificationgroup import NotificationGroup
from noc.main.models.handler import Handler
from noc.core.bi.decorator import bi_sync
from .alarmclass import AlarmClass


id_lock = Lock()


class Match(EmbeddedDocument):
    labels = ListField(StringField())
    alarm_class = ReferenceField(AlarmClass)
    reference_re = StringField()

    def __str__(self):
        return f'{", ".join(self.labels)}, {self.alarm_class or ""}/{self.reference_re}'

    def get_labels(self):
        return list(Label.objects.filter(name__in=self.labels))


class Group(EmbeddedDocument):
    # Group Alarm reference Template
    reference_template = StringField(default="")
    # Group Alarm Class (Group by default)
    alarm_class = PlainReferenceField(AlarmClass)
    # Group Title template
    title_template = StringField()

    def __str__(self):
        return f'{self.alarm_class or ""}/{self.title_template or ""}: {self.reference_template}'


class Action(EmbeddedDocument):
    when = StringField(
        default="raise",
        choices=[
            ("raise", "When raise alarm"),
            ("clear", "When clear alarm"),
        ],
    )
    policy = StringField(
        default="continue",
        choices=[
            ("continue", "Continue processed"),
            ("drop", "Drop Alarm"),
            ("rewrite", "Rewrite Alarm Class"),
        ],
    )
    handler = PlainReferenceField(Handler)
    notification_group = ForeignKeyField(NotificationGroup, required=False)
    alarm_class = PlainReferenceField(AlarmClass)

    def __str__(self):
        return f"{self.when}: {self.policy}"


@bi_sync
class AlarmRule(Document):
    meta = {
        "collection": "alarmrules",
        "strict": False,
        "auto_create_index": False,
        "indexes": ["match.labels", ("match.alarm_class", "match.labels")],
    }

    name = StringField(unique=True)
    description = StringField()
    is_active = BooleanField(default=True)
    #
    match = ListField(EmbeddedDocumentField(Match))
    #
    groups = ListField(EmbeddedDocumentField(Group))
    #
    actions = ListField(EmbeddedDocumentField(Action))
    # BI ID
    bi_id = LongField(unique=True)

    _id_cache = cachetools.TTLCache(maxsize=100, ttl=60)
    _name_cache = cachetools.TTLCache(maxsize=100, ttl=60)
    _bi_id_cache = cachetools.TTLCache(maxsize=100, ttl=60)

    DEFAULT_AC_NAME = "Group"

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id) -> "AlarmRule":
        return AlarmRule.objects.filter(id=id).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_name_cache"), lock=lambda _: id_lock)
    def get_by_name(cls, name) -> "AlarmRule":
        return AlarmRule.objects.filter(name=name).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_bi_id_cache"), lock=lambda _: id_lock)
    def get_by_bi_id(cls, id) -> "AlarmRule":
        return AlarmRule.objects.filter(bi_id=id).first()