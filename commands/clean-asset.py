# ---------------------------------------------------------------------
# ./noc clean-asset
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.management.base import BaseCommand
from noc.inv.models.resourcegroup import ResourceGroup
from noc.inv.models.object import Object


class Command(BaseCommand):
    help = "Clean asset"

    def handle(self, *args, **options):
        clean = set()
        for expr in args:
            for obj in ResourceGroup.get_objects_from_expression(expr, model_id="sa.ManagedObject"):
                if obj.id in clean:
                    continue  # Already cleaned
                self.clean_managed_object(obj)
                clean.add(obj.id)

    def clean_managed_object(self, object):
        for o in Object.objects.filter(
            data__match={"interface": "management", "attr": "managed_object", "value": object.id}
        ):
            self.clean_obj(o)

    def clean_obj(self, obj):
        print("Cleaning %s %s (%s)" % (obj.model.name, obj.name, obj.id))
        # Clean children
        for o in Object.objects.filter(container=obj.id):
            self.clean_obj(o)
        # Clean inner connections
        for name, remote, remote_name in obj.iter_connections("i"):
            self.clean_obj(remote)
        obj.delete()


if __name__ == "__main__":
    Command().run()
