# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# HP.Comware.get_arp
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules
import re

# NOC modules
from noc.sa.interfaces.igetarp import IGetARP
from noc.core.script.base import BaseScript


class Script(BaseScript):
    name = "HP.Comware.get_arp"
    interface = IGetARP

    rx_arp_line = re.compile(
        r"^(?P<ip>\d+\.\S+)\s+(?P<mac>[0-9a-f]\S+)\s+\d*\s+.{3}\s+" r"(?P<interface>\S+)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )

    def execute(self):
        return self.cli("display arp", list_re=self.rx_arp_line)
