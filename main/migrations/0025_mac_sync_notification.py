# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# mac sync notification
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db


class Migration(object):
    def forwards(self):
        if db.execute("SELECT COUNT(*) FROM main_systemnotification WHERE name=%s", ["ip.sync_macs"])[0][0] == 0:
            db.execute("INSERT INTO main_systemnotification(name) VALUES(%s)", ["ip.sync_macs"])

    def backwards(self):
        pass
