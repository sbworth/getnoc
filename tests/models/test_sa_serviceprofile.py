# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# sa.ServiceProfile tests
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
# NOC modules
from .base import BaseDocumentTest
from noc.sa.models.serviceprofile import ServiceProfile


class TestSaServiceProfile(BaseDocumentTest):
    model = ServiceProfile
