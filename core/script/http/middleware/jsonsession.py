# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# JSONSession middleware
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
# NOC modules
from .base import BaseMiddleware


class JSONSessionMiddleware(BaseMiddleware):
    """
    Append session_id: XXXXX to body.
    `session_id` name may be changed via `session_param`
    """
    name = "jsonsession"

    def __init__(self, http, session_param="session_id"):
        super(JSONSessionMiddleware, self).__init__(http)
        self.session_param = session_param

    def process_post(self, url, body, headers):
        if self.http.session_id and isinstance(body, dict):
            body[self.session_param] = self.http.session_id
        return url, body, headers

    def process_put(self, url, body, headers):
        return self.process_post(url, body, headers)