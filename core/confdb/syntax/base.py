# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ConfDB Syntax
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from .system.base import SYSTEM_SYNTAX
from .interfaces.base import INTERFACES_SYNTAX
from .protocols.base import PROTOCOLS_SYNTAX
from .virtualrouter.base import VIRTUAL_ROUTER_SYNTAX
from .hints import HINTS_SYNTAX

SYNTAX = [SYSTEM_SYNTAX, INTERFACES_SYNTAX, PROTOCOLS_SYNTAX, VIRTUAL_ROUTER_SYNTAX, HINTS_SYNTAX]