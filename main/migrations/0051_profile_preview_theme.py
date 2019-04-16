# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# profile preview theme
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db
from django.db import models


class Migration(object):
    def forwards(self):
        db.add_column(
            "main_userprofile", "preview_theme",
            models.CharField("Preview Theme", max_length=32, null=True, blank=True)
        )

    def backwards(self):
        db.drop_column("main_userprofile", "preview_theme_id")
