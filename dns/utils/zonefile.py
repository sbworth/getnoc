# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# BIND-compatible zonefile generator
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import six

# NOC modules
from noc.dns.utils.rr import RR
from noc.core.comp import smart_text

HEADER = """;;
;; %s
;; WARNING: Auto-generated zone file
;; Do not edit manually
;; Generated by NOC (http://getnoc.com)
;;"""

FOOTER = """;;
;; End of auto-generated zone
;;
"""


class ZoneFile(object):
    TABSTOP = 8
    MAX_TXT = 128

    def __init__(self, data):
        records = data.get("records", [])
        if not records:
            raise ValueError("Zone must contain SOA record")
        self.zone = data["name"]
        if RR(zone=self.zone, **records[0]).type != "SOA":
            raise ValueError("First record must be SOA")
        self.records = [RR(zone=self.zone, **r) for r in records]

    def to_idna(self, n):
        if isinstance(n, unicode):
            return n.lower().encode("idna")
        elif isinstance(n, six.string_types):
            return smart_text(n, "utf-8").lower().encode("idna")
        else:
            return n

    def from_idna(self, s):
        if not s or not self.is_idna(s):
            return s
        if isinstance(s, unicode):
            return s.encode("utf-8").decode("idna")
        else:
            return smart_text(s, "idna").encode("utf-8")

    def is_idna(self, s):
        return "xn--" in s

    def get_text(self):
        primary, contact, serial, refresh, retry, expire, ttl = self.records[0].rdata.split()
        serial = int(serial)
        refresh = int(refresh)
        retry = int(retry)
        expire = int(expire)
        ttl = int(ttl)
        if "@" in contact:
            contact = contact.replace("@", ".")
        if not contact.endswith("."):
            contact += "."

        suffix = self.to_idna(self.zone + ".")
        nsuffix = "." + suffix
        lnsuffix = len(nsuffix)

        # SOA
        z = [
            HEADER % self.from_idna(self.zone),
            """$ORIGIN %(domain)s.
$TTL %(ttl)d
@ IN SOA %(primary)s %(contact)s (
    %(serial)d ; serial
    %(refresh)d       ; refresh (%(pretty_refresh)s)
    %(retry)d        ; retry (%(pretty_retry)s)
    %(expire)d      ; expire (%(pretty_expire)s)
    %(ttl)d       ; minimum (%(pretty_ttl)s)
    )"""
            % {
                "domain": self.zone,
                "primary": primary,
                "contact": contact,
                "serial": serial,
                "ttl": ttl,
                "pretty_ttl": self.pretty_time(ttl),
                "refresh": refresh,
                "pretty_refresh": self.pretty_time(refresh),
                "retry": retry,
                "pretty_retry": self.pretty_time(retry),
                "expire": expire,
                "pretty_expire": self.pretty_time(expire),
            },
        ]
        # Add records
        rr = []
        for r in self.records[1:]:
            name = r.name
            content = r.rdata
            if r.type == "CNAME" and r.rdata.endswith(nsuffix):
                # Strip domain from content
                content = content[:-lnsuffix]
            if r.priority:
                content = "%s %s" % (r.priority, content)
            rr += [(name, r.type, content)]
        # prepare mask for 3-column format
        if rr:
            l1 = max(len(r[0]) for r in rr)
            l2 = max(len(r[1]) for r in rr)
            # Ceil to boundary of 4
            l1 = (l1 // self.TABSTOP + 1) * self.TABSTOP
            l2 = (l2 // self.TABSTOP + 1) * self.TABSTOP
        else:
            l1 = self.TABSTOP
            l2 = self.TABSTOP
        mask = "%%-%ds%%-%ds%%s" % (l1, l2)
        txt_cmask = "%s%%s" % (" " * l1)
        # Add RRs
        for r in rr:
            if self.is_idna(r[0]):
                z += ["; %s" % self.from_idna(r[0])]
            if r[1] == "TXT":
                content = self.split_txt(r[2])
                z += [mask % (r[0], r[1], content.pop(0))]
                for c in content:
                    z += [txt_cmask % c]
            else:
                z += [mask % tuple(r)]
        z += [FOOTER]
        return "\n".join(z)

    @staticmethod
    def pretty_time(t):
        """
        Format seconds to human-readable time for comments
        :param t:
        :return:
        """
        if not t:
            return "zero"
        T = ["week", "day", "hour", "min", "sec"]
        W = [604800, 86400, 3600, 60, 1]
        r = []
        for w in W:
            rr = t // w
            t -= rr * w
            r += [rr]
        z = []
        for rr, t in zip(r, T):
            if rr > 1:
                z += ["%d %ss" % (rr, t)]
            elif rr > 0:
                z += ["%d %s" % (rr, t)]
        return " ".join(z)

    @classmethod
    def split_txt(cls, value):
        """
        Split TXT to up-to MAX_TXT parts
        :param value:
        :return:
        """
        if len(value) <= cls.MAX_TXT:
            if not value[0] == '"':
                value = '"%s"' % value
            return [value]
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        v = ["("]
        while value:
            v += ['"%s"' % value[: cls.MAX_TXT]]
            value = value[cls.MAX_TXT :]
        v += [")"]
        return v
