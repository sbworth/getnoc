# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Angtel.Topaz.get_interface_status
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfacestatus import IGetInterfaceStatus


class Script(BaseScript):
    name = "Angtel.Topaz.get_interface_status"
    interface = IGetInterfaceStatus
    cache = True

    rx_port = re.compile(
        r"^(?P<port>(?:Fa|Gi|Te|Po)\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+"
        r"(?P<oper_status>Up|Down|Not Present)",
        re.MULTILINE | re.IGNORECASE,
    )

    def execute_cli(self, interface=None):
        r = []
        v = self.cli("show interfaces status", cached=True)
        for match in self.rx_port.finditer(v):
            if (interface is not None) and (interface == match.group("port")):
                return [
                    {"interface": match.group("port"), "status": match.group("oper_status") == "Up"}
                ]
            r += [{"interface": match.group("port"), "status": match.group("oper_status") == "Up"}]
        return r
