# ---------------------------------------------------------------------
# Vendor: Cisco
# OS:     SANOS
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Cisco.SANOS"

    pattern_more = [(rb"^ --More--", b"\n"), (rb"(?:\?|interfaces)\s*\[confirm\]", b"\n")]
    pattern_unprivileged_prompt = rb"^\S+?>"
    pattern_syntax_error = rb"% invalid command detected at"
    command_disable_pager = "terminal length 0"
    command_super = b"enable"
    command_enter_config = "configure terminal"
    command_leave_config = "end"
    command_exit = "exit"
    command_save_config = "copy running-config startup-config\n"
    pattern_prompt = rb"^(?P<hostname>[a-zA-Z0-9/.]\S{0,35})(?:[-_\d\w]+)?(?:\(config[^\)]*\))?#"
    can_strip_hostname_to = 20
    requires_netmask_conversion = True
    convert_mac = BaseProfile.convert_mac_to_cisco

    def convert_interface_name(self, interface):
        il = interface.lower()
        if il.startswith("iscsi"):
            return "iscsi %s" % interface[5:].strip()
        if il.startswith("sup-fc"):
            return il.strip()
        if il.startswith("mgmt"):
            return il.strip()
        return self.convert_interface_name_cisco(interface)
