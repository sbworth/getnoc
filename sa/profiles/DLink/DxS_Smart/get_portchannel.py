# ---------------------------------------------------------------------
# DLink.DxS_Smart.get_portchannel
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from builtins import range

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetportchannel import IGetPortchannel
from noc.core.snmp.render import render_bin


class Script(BaseScript):
    name = "DLink.DxS_Smart.get_portchannel"
    cache = True
    interface = IGetPortchannel

    def execute_snmp(self):
        r = []

        def hex2bin(ports):
            bin = [
                "0000",
                "0001",
                "0010",
                "0011",
                "0100",
                "0101",
                "0110",
                "0111",
                "1000",
                "1001",
                "1010",
                "1011",
                "1100",
                "1101",
                "1110",
                "1111",
            ]
            ports = ["%02x" % c for c in ports]
            p = ""
            for c in ports:
                for i in range(len(c)):
                    p += bin[int(c[i], 16)]
            return p

        pmib = self.profile.get_pmib(self.scripts.get_version())
        if pmib is None:
            raise NotImplementedError()
        for v in self.snmp.get_tables(
            [
                pmib + ".8.1.3.1.1",
                pmib + ".8.1.3.1.2",
                pmib + ".8.1.3.1.3",
            ],
            bulk=True,
            display_hints={
                pmib + ".8.1.3.1.2": render_bin,
            },
        ):
            oid = pmib + ".8.1.3.1.1." + str(v[1])
            port = self.snmp.get(oid, cached=True)  # IF-MIB
            if not port:
                oid = "1.3.6.1.2.1.2.2.1.2." + str(v[1])
                port = self.snmp.get(oid, cached=True)
            s = hex2bin(v[2])
            members = []
            for i in range(len(s)):
                if s[i] == "1":
                    oid = "1.3.6.1.2.1.31.1.1.1.1." + str(i + 1)
                    iface = self.snmp.get(oid, cached=True)  # IF-MIB
                    if not iface:
                        oid = "1.3.6.1.2.1.2.2.1.2." + str(i + 1)
                        iface = self.snmp.get(oid, cached=True)
                    members.append(iface)
            r.append(
                {
                    "interface": "T" + str(port),
                    "type": "L" if int(v[3]) == 1 else "S",
                    "members": members,
                }
            )
        return r
