# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# vc.VC tests
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
# NOC modules
from .base import BaseModelTest
from noc.vc.models.vc import VC


class TestTestVcVC(BaseModelTest):
    model = VC
