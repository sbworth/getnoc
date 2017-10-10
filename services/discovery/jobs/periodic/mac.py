# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# MAC Check
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import time
from functools import reduce
# NOC modules
from noc.inv.models.interfaceprofile import InterfaceProfile
from noc.services.discovery.jobs.base import DiscoveryCheck
from noc.core.perf import metrics
from noc.core.mac import MAC


class MACCheck(DiscoveryCheck):
    """
    MAC discovery
    """
    name = "mac"
    required_script = "get_mac_address_table"

    METRIC_FIELDS = "mac.date.ts.managed_object.mac" \
                    ".interface.interface_profile.segment.vlan.is_uni"

    def handler(self):
        # Build filter policy
        if self.object.object_profile.mac_collect_all:
            mf = self.filter_all
        else:
            mf = []
            self.allowed_vlans = set()
            # Filter by interface profile
            if self.object.object_profile.mac_collect_interface_profile:
                mf += [self.filter_interface_profile]
            # Filter by management vlan
            if self.object.object_profile.mac_collect_management:
                vlan = self.object.segment.get_management_vlan()
                if vlan:
                    self.allowed_vlans.add(vlan)
            # Filter by multicast vlan
            if self.object.object_profile.mac_collect_multicast:
                vlan = self.object.segment.get_multicast_vlan()
                if vlan:
                    self.allowed_vlans.add(vlan)
            # Filter by VC Filter (not implemented yet)
            if self.object.object_profile.mac_collect_vcfilter:
                self.logger.info("VC Filters are not implemented yet")
            # Apply VLAN filter
            if self.allowed_vlans:
                mf += [self.filter_vlan]
            if not mf:
                self.logger.info("MAC collection is not enabled by any policy")
                return
            mf = reduce(lambda x, y: x or y, mf)
        # Collect macs
        now = time.localtime()
        date = time.strftime("%Y-%m-%d", now)
        ts = time.strftime("%Y-%m-%d %H:%M:%S", now)
        unknown_interfaces = set()
        total_macs = 0
        processed_macs = 0
        data = []
        mo_bi_id = str(self.object.bi_id)
        seg_bi_id = str(self.object.segment.bi_id)
        # Collect and process MACs
        result = self.object.scripts.get_mac_address_table()
        for v in result:
            total_macs += 1
            if v["type"] != "D" or not v["interfaces"]:
                continue
            ifname = str(v["interfaces"][0])
            iface = self.get_interface_by_name(ifname)
            if not iface:
                unknown_interfaces.add(ifname)
                continue  # Interface not found
            if not mf(iface, v["vlan_id"], v["mac"]):
                continue
            ifprofile = iface.get_profile()
            data += ["\t".join((
                date,  # date
                ts,  # ts
                mo_bi_id,  # managed_object
                str(int(MAC(v["mac"]))),  # mac
                ifname,  # interface
                str(ifprofile.bi_id),  # interface_profile
                seg_bi_id,  # segment
                str(v.get("vlan_id", 0)),  # vlan
                "1" if ifprofile.is_uni else "0"  # is_uni
            ))]
            processed_macs += 1
        if unknown_interfaces:
            self.logger.info(
                "Ignoring unknown interfaces: %s",
                ", ".join(unknown_interfaces))
        metrics["discovery_mac_total_macs"] += total_macs
        metrics["discovery_mac_processed_macs"] += processed_macs
        metrics["discovery_mac_ignored_macs"] += total_macs - processed_macs
        if data:
            self.logger.info("%d MAC addresses are collected. Sending",
                             processed_macs)
            self.service.register_metrics(
                self.METRIC_FIELDS,
                data
            )
        else:
            self.logger.info("No MAC addresses collected")

    def filter_all(self, interface, vlan, mac):
        return True

    def filter_interface_profile(self, interface, vlan, mac):
        return interface.get_profile().mac_discovery_policy != "e"

    def filter_vlan(self, interface, vlan, mac):
        return vlan in self.allowed_vlans
