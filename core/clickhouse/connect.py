# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Clickhouse connection
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import os
import urllib
# Third-party modules
import six
# NOC modules
from noc.core.http.client import fetch_sync
from noc.config import config


class ClickhouseError(Exception):
    pass


class ClickhouseClient(object):
    def __init__(self, host=None, port=None):
        self.host = host or config.clickhouse.addresses[0].host
        self.port = port or config.clickhouse.addresses[0].port

    def execute(self, sql=None, args=None, nodb=False, post=None):
        def q(v):
            # @todo: quote dates
            if isinstance(v, six.string_types):
                return "'%s'" % (v.replace("\\", "\\\\").replace("'", "\\'"))
            else:
                return str(v)

        qs = []
        if not nodb:
            qs += ["database=%s" % config.clickhouse.db]
        if sql:
            if args:
                sql = sql % tuple(q(v) for v in args)
            if post:
                qs += ["query=%s" % urllib.quote(sql.encode('utf8'))]
            else:
                post = sql.encode('utf8')
        url = "http://%s:%s/?%s" % (self.HOST, self.PORT, "&".join(qs))
        code, headers, body = fetch_sync(
            url,
            method="POST",
            body=post,
            connect_timeout=self.config.clickhouse.connect_timeout,
            request_timeout=self.config.clickhouse.request_timeout
        )
        if code != 200:
            raise ClickhouseError("%s: %s" % (code, body))
        return [
            row.split("\t") for row in body.splitlines()
        ]

    def ensure_db(self):
        self.execute(
            post="CREATE DATABASE IF NOT EXISTS %s;" % config.clickhouse.db,
            nodb=True
        )

    def has_table(self, name):
        r = self.execute("""
            SELECT COUNT(*)
            FROM system.tables
            WHERE
              database=%s
              AND name = %s
        """, [config.clickhouse.db, name])
        return r and r[0][0] == "1"


def connection(host=None, port=None):
    return ClickhouseClient(host=port, port=port)
