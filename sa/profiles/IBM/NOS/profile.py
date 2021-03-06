# ---------------------------------------------------------------------
# Vendor: IBM
# OS:     NOS
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# import re
# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "IBM.NOS"

    pattern_more = [(rb"^--More--", b"\n")]
    pattern_prompt = rb"^\S+?#"
    pattern_unprivileged_prompt = rb"^\S+?>"
    pattern_syntax_error = rb"% Invalid input detected at"
    command_disable_pager = "terminal-length 0"
    command_super = b"enable"
    command_exit = "exit"
    command_save_config = "copy running-config startup-config\n"
    requires_netmask_conversion = True
    convert_mac = BaseProfile.convert_mac_to_cisco
    config_volatile = [r"^ntp message\-digest\-key .*?^", r"^access user .*?^"]
