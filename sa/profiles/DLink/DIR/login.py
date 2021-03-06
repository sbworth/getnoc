# ---------------------------------------------------------------------
# DLink.DIR.login
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.ilogin import ILogin


class Script(BaseScript):
    """
    Try to log in
    """

    name = "DLink.DIR.login"
    interface = ILogin
    requires = []

    def execute(self):
        try:
            self.http.get("/")
            return {"result": True, "message": ""}
        except Exception as e:
            return {"result": False, "message": str(e)}
