# ---------------------------------------------------------------------
# Orion.NOS.get_arp
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetarp import IGetARP


class Script(BaseScript):
    name = "Orion.NOS.get_arp"
    interface = IGetARP
    rx_line = re.compile(
        r"^\s*(?P<ip>[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+"
        r"(?P<mac>\S+)\s+\S+\s+(?P<interface>\S+)\s*",
        re.MULTILINE,
    )

    def execute_cli(self, interface=None):
        r = []
        for match in self.rx_line.finditer(self.cli("show arp")):
            if (interface is not None) and (interface != match.group("interface")):
                continue
            r += [match.groupdict()]
        return r
