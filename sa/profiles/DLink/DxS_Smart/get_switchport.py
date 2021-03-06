# ---------------------------------------------------------------------
# DLink.DxS_Smart.get_switchport
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from builtins import range

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetswitchport import IGetSwitchport
from noc.core.snmp.render import render_bin


class Script(BaseScript):
    name = "DLink.DxS_Smart.get_switchport"
    interface = IGetSwitchport

    def execute_snmp(self):
        r = []

        # Get interafces status
        interface_status = {}
        for s in self.scripts.get_interface_status():
            interface_status[s["interface"]] = s["status"]

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

        # Make a list of tags for each interface or portchannel
        port_vlans = {}
        pmib = self.profile.get_pmib(self.scripts.get_version())
        if pmib is None:
            raise NotImplementedError()
        oid1 = pmib + ".7.6.1.1"
        oid2 = pmib + ".7.6.1.2"
        oid3 = pmib + ".7.6.1.4"
        # For DXS-1210-10TS
        if pmib == "1.3.6.1.4.1.171.10.139.2.1":
            oid1 = pmib + ".4.2.2.1.1"
            oid2 = pmib + ".4.2.2.1.3"
            oid3 = pmib + ".4.2.2.1.4"
        for v in self.snmp.get_tables(
            [oid1, oid2, oid3],
            bulk=True,
            display_hints={
                oid2: render_bin,
                oid3: render_bin,
            },
        ):
            tagged = v[2]
            untagged = v[3]
            s = hex2bin(untagged)
            un = []
            for i in range(len(s)):
                if s[i] == "1":
                    oid = "1.3.6.1.2.1.31.1.1.1.1." + str(i + 1)
                    iface = self.snmp.get(oid, cached=True)
                    if iface[:6] == "Slot0/":
                        iface = iface[6:]
                    if iface not in port_vlans:
                        port_vlans.update({iface: {"tagged": [], "untagged": ""}})
                    port_vlans[iface]["untagged"] = v[0]
                    un += [str(i + 1)]
            s = hex2bin(tagged)
            for i in range(len(s)):
                if s[i] == "1" and str(i + 1) not in un:
                    oid = "1.3.6.1.2.1.31.1.1.1.1." + str(i + 1)
                    iface = self.snmp.get(oid, cached=True)
                    if iface[:6] == "Slot0/":
                        iface = iface[6:]
                    if iface not in port_vlans:
                        port_vlans.update({iface: {"tagged": [], "untagged": ""}})
                    port_vlans[iface]["tagged"].append(v[0])
            # Get switchport description
        port_descr = {}
        for iface, description in self.snmp.join_tables(
            "1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.31.1.1.1.18"
        ):
            if (
                iface[:3] == "Aux"
                or iface[:4] == "Vlan"
                or iface[:11] == "InLoopBack"
                or iface == "System"
            ):
                continue
            if iface[:6] == "Slot0/":
                iface = iface[6:]
            port_descr.update({iface: description})
            # Get switchport data and overall result
        write = False
        for name in interface_status:
            if interface_status.get(name):
                status = True
            else:
                status = False
            if name in port_descr:
                description = port_descr[name]
                if not description:
                    description = ""
            else:
                description = ""
            members = []
            write = True
            if write:
                if name not in port_vlans:
                    tagged = []
                else:
                    tagged = port_vlans[name]["tagged"]
            swp = {
                "status": status,
                "description": description,
                "802.1Q Enabled": len(port_vlans.get(name, "")) > 0,
                "802.1ad Tunnel": "False",
                "tagged": tagged,
            }
            if name in port_vlans:
                if port_vlans[name]["untagged"]:
                    swp["untagged"] = port_vlans[name]["untagged"]
            swp["interface"] = name
            swp["members"] = members
            r.append(swp)
            write = False
        return r
