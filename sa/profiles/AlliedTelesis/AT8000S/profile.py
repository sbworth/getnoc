# ---------------------------------------------------------------------
# Vendor: Allied Telesis
# OS:     AT8000S
# ---------------------------------------------------------------------
# Copyright (C) 2007-2010 The NOC Project
# coded by azhur
# See LICENSE for details
# ---------------------------------------------------------------------


from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "AlliedTelesis.AT8000S"

    pattern_unprivileged_prompt = rb"^\S+?>"
    pattern_prompt = rb"^\S+?#"
    pattern_more = [
        (rb"^More: <space>,  Quit: q, One line: <return>", b" "),
        (rb"^.*?\[Yes/press any key for no\]\.*", b"Y"),
    ]
    command_super = b"enable"
    command_enter_config = "configure"
    command_leave_config = "end"
    command_save_config = "copy running-config startup-config"
    command_disable_pager = "terminal datadump"
    config_volatile = [
        r"^\s*(?P<day>3[01]|[0-2]{0,1}\d)-(?P<month>Jan|Feb|Mar|Apr|May|"
        r"Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(?P<year>\d{4}) "
        r"(?P<time>\d\d:\d\d:\d\d) %\W*"
    ]
