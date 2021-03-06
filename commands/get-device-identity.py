# ----------------------------------------------------------------------
# Service command
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import argparse

# NOC modules
from noc.core.management.base import BaseCommand
from noc.core.mongo.connection import connect
from noc.inv.models.resourcegroup import ResourceGroup
from noc.core.mib import mib
from noc.core.error import NOCError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "devices",
            nargs=argparse.REMAINDER,
            help="Device or selector list. Selectors starts with @",
        )

    def handle(self, devices, *args, **options):
        devs = set()
        connect()
        for d in devices:
            try:
                devs |= set(
                    ResourceGroup.get_objects_from_expression(d, model_id="sa.ManagedObject")
                )
            except ResourceGroup.DoesNotExist:
                self.die("Invalid object '%s'" % d)
        self.stdout.write("profile,platform,oid,value\n")
        for o in sorted(devs, key=lambda x: x.name):
            if "get_snmp_get" not in o.scripts:
                continue
            if o.platform:
                platform = o.platform.full_name
            else:
                try:
                    v = o.scripts.get_version()
                except AttributeError:
                    v = {"platform": "Unknown"}
                platform = v["platform"]
            # sysObjectID
            try:
                v = o.scripts.get_snmp_get(oid=mib["SNMPv2-MIB::sysObjectID.0"])
            except NOCError:
                continue
            self.stdout.write(
                "%s,%s,%s,%s\n" % (o.profile.name, platform, "SNMPv2-MIB::sysObjectID.0", v)
            )


if __name__ == "__main__":
    Command().run()
