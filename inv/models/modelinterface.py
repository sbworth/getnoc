# ---------------------------------------------------------------------
# ModelInterface model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import os
from threading import Lock
import operator
from typing import Optional

# Third-party modules
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField,
    BooleanField,
    ListField,
    EmbeddedDocumentField,
    UUIDField,
)
import cachetools

# NOC modules
from .error import ModelDataError
from noc.core.copy import deep_copy
from noc.core.escape import json_escape as q
from noc.core.validators import is_objectid
from noc.sa.interfaces.base import (
    StringParameter,
    BooleanParameter,
    FloatParameter,
    IntParameter,
    StringListParameter,
)

id_lock = Lock()


T_MAP = {
    "str": StringParameter(),
    "int": IntParameter(),
    "float": FloatParameter(),
    "bool": BooleanParameter(),
    "strlist": StringListParameter(),
}

A_TYPE = ["str", "int", "float", "bool", "objectid", "ref", "strlist"]


class ModelInterfaceAttr(EmbeddedDocument):
    meta = {"strict": False, "auto_create_index": False}
    name = StringField()
    type = StringField(choices=[(t, t) for t in A_TYPE])
    description = StringField()
    required = BooleanField(default=False)
    is_const = BooleanField(default=False)
    # default
    # ref

    def __str__(self):
        return self.name

    def __eq__(self, v):
        return (
            self.name == v.name
            and self.type == v.type
            and self.description == v.description
            and self.required == v.required
            and self.is_const == v.is_const
        )

    def _clean(self, value):
        return getattr(self, "clean_%s" % self.type)(value)

    def clean_str(self, value):
        return value

    def clean_int(self, value):
        return int(value)

    def clean_float(self, value):
        if isinstance(value, str):
            return float(value.replace(",", "."))
        else:
            return float(value)

    def clean_bool(self, value):
        value = value.lower()
        if value in ("yes", "y", "t", "true"):
            return True
        try:
            v = int(value)
            return v != 0
        except ValueError:
            return False

    def clean_objectid(self, value):
        value = value.lower()
        if is_objectid(value):
            return value
        raise ValueError(f"Value {value} is not ObjectID")


class ModelInterface(Document):
    """
    Equipment vendor
    """

    meta = {
        "collection": "noc.modelinterfaces",
        "strict": False,
        "auto_create_index": False,
        "json_collection": "inv.modelinterfaces",
        "json_unique_fields": ["uuid", "name"],
    }

    name = StringField(unique=True)
    description = StringField()
    attrs = ListField(EmbeddedDocumentField(ModelInterfaceAttr))
    uuid = UUIDField(binary=True)

    _id_cache = cachetools.TTLCache(1000, 10)
    _name_cache = cachetools.TTLCache(1000, 10)

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id) -> Optional["ModelInterface"]:
        return ModelInterface.objects.filter(id=id).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_name_cache"), lock=lambda _: id_lock)
    def get_by_name(cls, name: str) -> Optional["ModelInterface"]:
        return ModelInterface.objects.filter(name=name).first()

    def get_attr(self, name):
        for a in self.attrs:
            if a.name == name:
                return a
        return None

    def to_json(self) -> str:
        ar = []
        for a in self.attrs:
            r = ["        {"]
            r += ['            "name": "%s",' % q(a.name)]
            r += ['            "type": "%s",' % q(a.type)]
            r += ['            "description": "%s",' % q(a.description)]
            r += ['            "required": %s,' % q(a.required)]
            r += ['            "is_const": %s' % q(a.is_const)]
            r += ["        }"]
            ar += ["\n".join(r)]
        r = [
            "{",
            '    "name": "%s",' % q(self.name),
            '    "$collection": "%s",' % self._meta["json_collection"],
            '    "uuid": "%s",' % str(self.uuid),
            '    "description": "%s",' % q(self.description),
            '    "attrs": [',
            ",\n".join(ar),
            "    ]",
            "}",
        ]
        return "\n".join(r) + "\n"

    def get_json_path(self) -> str:
        p = [n.strip() for n in self.name.split("|")]
        return os.path.join(*p) + ".json"

    @classmethod
    def clean_data(cls, data):
        """
        Convert types accoding to interface
        """
        d = deep_copy(data)
        for i_name in d:
            mi = ModelInterface.objects.filter(name=i_name).first()
            if not mi:
                raise ModelDataError("Unknown interface '%s'" % i_name)
            v = d[i_name]
            for a in mi.attrs:
                if a.name in v:
                    vv = v[a.name]
                    if a.type == "strlist":
                        if isinstance(vv, str):
                            vv = [vv]
                        r = set()
                        for x in vv:
                            r.update(x.split(","))
                        vv = [x.strip() for x in sorted(r) if x.strip()]
                    v[a.name] = T_MAP[a.type].clean(vv)
        return d

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_interface_attr(cls, interface, key):
        mi = ModelInterface.objects.filter(name=interface).first()
        if not mi:
            raise ModelDataError("Invalid interface '%s'" % interface)
        attr = mi.get_attr(key)
        if not attr:
            raise ModelDataError("Invalid attribute '%s.%s'" % (interface, key))
        return attr
