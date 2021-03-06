# ---------------------------------------------------------------------
# MaintenanceType
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, BooleanField

# NOC modules
from noc.core.model.decorator import on_delete_check


@on_delete_check(check=[("maintenance.Maintenance", "type")])
class MaintenanceType(Document):
    meta = {
        "collection": "noc.maintenancetype",
        "strict": False,
        "auto_create_index": False,
        "legacy_collections": ["noc.maintainancetype"],
    }

    name = StringField(unique=True)
    description = StringField()
    suppress_alarms = BooleanField()
    card_template = StringField()

    def __str__(self):
        return self.name
