# ---------------------------------------------------------------------
# Vendor: HP, 3Com
# OS:     1910, BaseLine
# ---------------------------------------------------------------------
# Copyright (C) 2007-2013 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.profile.base import BaseProfile

# from noc.sa.models import ManagedObject


class Profile(BaseProfile):
    name = "HP.1910"

    pattern_password = rb"^(Password:|Please input password:)"
    pattern_more = [
        (rb"^\s+---- More ----$", b" "),
        (rb"The current configuration will be written to the device. Are you sure? [Y/N]:", b"Y"),
        (rb"(To leave the existing filename unchanged, press the enter key):", b"\n"),
        (rb"flash:/startup.cfg exists, overwrite? [Y/N]:", b"Y"),
    ]
    pattern_prompt = rb"^[<\[]\S+[>\]]"
    pattern_syntax_error = rb"^\s+% (Unrecognized|Incomplete) command found at '\^' position.$"
    command_save_config = "save"
    command_enter_config = "system-view"
    command_leave_config = "return"
    command_exit = "quit"
    convert_interface_name = BaseProfile.convert_interface_name_cisco

    def setup_session(self, script):
        # Yuo may change password instead 512900
        # script.cli("_cmdline-mode on\nY\n512900\nsystem-view\n")
        script.cli("_cmdline-mode on\nY\n512900")
        """
        obj = ManagedObject.objects.get()
        passwd = obj.super_password()
        script.cli("_cmdline-mode on\nY\n" + passwd)
        """
