# ---------------------------------------------------------------------
# Vendor: D-Link
# OS:     DES21xx
# Compatible:
# ---------------------------------------------------------------------
# Copyright (C) 2007-2011 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "DLink.DES21xx"

    pattern_prompt = rb"^\S+?>"
    command_exit = "logout"
    command_save_config = "save"
    config_volatile = ["^%.*?$"]
    telnet_slow_send_password = True
    command_submit = b"\r"
