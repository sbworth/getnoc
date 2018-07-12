# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# vc.VCType tests
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
# NOC modules
from .base import BaseModelTest
from noc.vc.models.vctype import VCType


class TestTestVcVCType(BaseModelTest):
    model = VCType
