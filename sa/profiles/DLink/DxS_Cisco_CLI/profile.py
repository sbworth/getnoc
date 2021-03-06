# ---------------------------------------------------------------------
# Vendor: DLink
# OS:     DxS_Cisco_CLI
# ---------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "DLink.DxS_Cisco_CLI"

    pattern_more = [(b"^ --More-- ", b"b")]
    pattern_unprivileged_prompt = rb"^\S+?>"
    pattern_syntax_error = rb"% Invalid input detected at"
    command_disable_pager = "terminal length 0"
    command_super = b"enable"
    command_enter_config = "configure terminal"
    command_leave_config = "exit"
    command_save_config = "copy running-config startup-config\n"
    pattern_prompt = rb"^(?P<hostname>\S+?)#"
    # Don't sure. Below this line obtained from Cisco.IOS profile
    requires_netmask_conversion = True
    convert_mac = BaseProfile.convert_mac_to_cisco
    convert_interface_name = BaseProfile.convert_interface_name_cisco
    config_volatile = ["^ntp clock-period .*?^"]

    def generate_prefix_list(self, name, pl):
        """
        Generate prefix list _name_. pl is a list of (prefix, min_len, max_len)
        """
        me = "ip prefix-list %s permit %%s" % name
        mne = "ip prefix-list %s permit %%s le %%d" % name
        r = ["no ip prefix-list %s" % name]
        for prefix, min_len, max_len in pl:
            if min_len == max_len:
                r += [me % prefix]
            else:
                r += [mne % (prefix, max_len)]
        return "\n".join(r)
