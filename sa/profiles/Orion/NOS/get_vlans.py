# ---------------------------------------------------------------------
# Orion.NOS.get_vlans
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetvlans import IGetVlans


class Script(BaseScript):
    name = "Orion.NOS.get_vlans"
    interface = IGetVlans

    rx_vlan = re.compile(r"^\s*(?P<vlan_id>\d+)\s+(?P<name>\S+)", re.MULTILINE)
    rx_vlan_beta = re.compile(r"^VLAN ID: (?P<vlan_id>\d+)\s*\nName: (?P<name>\S+)", re.MULTILINE)

    def execute_cli(self):
        r = []
        if self.is_beta:
            for match in self.rx_vlan_beta.finditer(self.cli("show vlan detail", cached=True)):
                if match.group("vlan_id") == "1":
                    continue
                r += [match.groupdict()]
            return r

        for match in self.rx_vlan.finditer(self.cli("show vlan")):
            if match.group("vlan_id") == "1":
                continue
            r += [match.groupdict()]
        return r
