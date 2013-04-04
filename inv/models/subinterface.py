## -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## SubInterface model
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.nosql import (Document, PlainReferenceField,
                           ForeignKeyField, StringField, BooleanField,
                           ListField, IntField)
from forwardinginstance import ForwardingInstance
from interface import Interface
from noc.sa.models import ManagedObject
from noc.sa.interfaces.igetinterfaces import IGetInterfaces


SUBINTERFACE_AFI = (
    IGetInterfaces.returns
    .element.attrs["interfaces"]
    .element.attrs["subinterfaces"]
    .element.attrs["enabled_afi"].element.choices)

SUBINTERFACE_PROTOCOLS = (
    IGetInterfaces.returns
    .element.attrs["interfaces"]
    .element.attrs["subinterfaces"]
    .element.attrs["enabled_protocols"].element.choices)


class SubInterface(Document):
    meta = {
        "collection": "noc.subinterfaces",
        "allow_inheritance": False,
        "indexes": [
            ("managed_object", "ifindex"),
            "interface", "managed_object",
            "untagged_vlan", "tagged_vlans",
            "enabled_afi"
        ]
    }
    interface = PlainReferenceField(Interface)
    managed_object = ForeignKeyField(ManagedObject)
    forwarding_instance = PlainReferenceField(
        ForwardingInstance, required=False)
    name = StringField()
    description = StringField(required=False)
    mac = StringField(required=False)
    vlan_ids = ListField(IntField(), default=[])
    enabled_afi = ListField(StringField(
        choices=[(x, x) for x in SUBINTERFACE_AFI]
    ), default=[])
    ipv4_addresses = ListField(StringField(), default=[])
    ipv6_addresses = ListField(StringField(), default=[])
    iso_addresses = ListField(StringField(), default=[])
    enabled_protocols = ListField(StringField(
        choices=[(x, x) for x in SUBINTERFACE_PROTOCOLS]
    ), default=[])
    untagged_vlan = IntField(required=False)
    tagged_vlans = ListField(IntField(), default=[])
    # ip_unnumbered_subinterface
    ifindex = IntField(required=False)

    def __unicode__(self):
        return "%s %s" % (self.interface.managed_object.name, self.name)
