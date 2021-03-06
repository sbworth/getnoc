# ---------------------------------------------------------------------
# DLink.DxS_Industrial_CLI.get_config
# ---------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetconfig import IGetConfig
from noc.core.script.error import CLIOperationError


class Script(BaseScript):
    name = "DLink.DxS_Industrial_CLI.get_config"
    interface = IGetConfig

    def execute_cli(self, policy="r"):
        assert policy in ("r", "s")
        if policy == "s":
            config = self.cli("show startup-config")
        else:
            config = self.cli("show running-config")
            if "System locked by other session" in config:
                raise CLIOperationError("System locked by other session!")
        config = self.strip_first_lines(config, 3)
        return self.cleaned_config(config)
