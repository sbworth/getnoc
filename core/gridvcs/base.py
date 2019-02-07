# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# GridVCS
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import datetime
import difflib
import zlib
# Third-party modules
import pymongo
import gridfs
import gridfs.errors
from mercurial.mdiff import patch
import bsdiff4
# NOC modules
from noc.lib.nosql import get_db, ObjectId
from .revision import Revision


class GridVCS(object):
    T_FILE = "F"
    T_BDIFF = "b"
    T_BSDIFF4 = "B"
    ENCODING = "utf-8"
    DEFAULT_COMPRESS = "z"

    def __init__(self, repo):
        self.fs = gridfs.GridFS(
            get_db(), collection="noc.gridvcs.%s" % repo)
        self.files = self.fs._GridFS__files

    def get_delta(self, src, dst):
        """
        Calculate strings delta
        :param src: Source string
        :param dst: Destination string
        :return: (<type>, delta)
        """
        delta = bsdiff4.diff(src, dst)
        if len(delta) >= len(dst):
            return self.T_FILE, dst
        return self.T_BSDIFF4, delta

    def apply_delta(self, type, src, delta):
        """
        Apply delta
        :param type: Delta type
        :param src: Source string
        :param delta: Delta
        :return: Patched string
        """
        return getattr(self, "apply_delta_%s" % type)(src, delta)

    def apply_delta_F(self, src, delta):
        """
        Raw string
        :param src:
        :param delta:
        :return:
        """
        return delta

    def apply_delta_b(self, src, delta):
        """
        Mercurial bdiff
        :param src:
        :param delta:
        :return:
        """
        return patch(src, delta)

    def apply_delta_B(self, src, delta):
        """
        BSDIFF4 diff
        :param src:
        :param delta:
        :return:
        """
        return bsdiff4.patch(src, delta)

    def compress(self, data, method=None):
        if method:
            return getattr(self, "compress_%s" % method)(data)
        return data

    def decompress(self, data, method=None):
        if method:
            return getattr(self, "decompress_%s" % method)(data)
        return data

    def compress_z(self, data):
        return zlib.compress(data)

    def decompress_z(self, data):
        return zlib.decompress(data)

    def put(self, object, data, ts=None):
        """
        Save data
        :param object: Object id
        :param data: Data to store
        :param ts: Timestamp
        :return:
        """
        if self.fs.exists(object=object):
            # Save delta
            try:
                # Get old version
                with self.fs.get_last_version(object=object, ft=self.T_FILE) as f:
                    old_data = self.decompress(f.read(), f._file.get("c"))
                # Check data has been changed
                if data == old_data:
                    return False
                # Calculate reverse delta
                dt, delta = self.get_delta(data, old_data)
                delta = self.compress(delta, self.DEFAULT_COMPRESS)
                # Save delta
                self.fs.put(
                    delta, object=object, ts=f.ts, ft=dt,
                    encoding=self.ENCODING, c=self.DEFAULT_COMPRESS
                )
                # Remove old version
                self.fs.delete(f._id)
            except gridfs.errors.NoFile:
                pass
        # Save new version
        ts = ts or datetime.datetime.now()
        self.fs.put(
            self.compress(data, self.DEFAULT_COMPRESS),
            object=object,
            ts=ts, ft=self.T_FILE,
            encoding=self.ENCODING,
            c=self.DEFAULT_COMPRESS
        )
        return True

    def get(self, object, revision=None):
        """
        Get data
        :param object:
        :param revision:
        :return:
        """
        if not revision:
            try:
                with self.fs.get_last_version(object=object, ft=self.T_FILE) as f:
                    return self.decompress(f.read(), f._file.get("c"))
            except gridfs.errors.NoFile:
                return None
        else:
            data = None
            for r in self.iter_revisions(object, reverse=True):
                with self.fs.get(r.id) as f:
                    delta = self.decompress(f.read(), f._file.get("c"))
                data = self.apply_delta(r.ft, data, delta)
                if r.id == revision.id:
                    break
            return data

    def delete(self, object):
        """
        Delete object's data and history
        :param object:
        :return:
        """
        for r in self.iter_revisions(object):
            self.fs.delete(r.id)

    def iter_revisions(self, object, reverse=False):
        """
        Get object's revision
        :param object:
        :return: List of Revisions
        """
        d = pymongo.DESCENDING if reverse else pymongo.ASCENDING
        for r in self.files.find({"object": object}).sort("ts", d):
            yield Revision(r["_id"], r["ts"], r["ft"], r.get("c"), r["length"])

    def find_revision(self, object, revision):
        """
        :param object:
        :param revision: Revision id
        :return:
        """
        r = self.files.find_one({
            "object": object,
            "_id": ObjectId(revision)
        })
        if r:
            return Revision(r["_id"], r["ts"], r["ft"], r.get("c"), r["length"])
        else:
            return None

    def diff(self, object, rev1, rev2):
        """
        Get unified diff between revisions
        :param object:
        :param rev1:
        :param rev2:
        :return:
        """
        src = self.get(object, rev1)
        dst = self.get(object, rev2)
        return "\n".join(
            difflib.unified_diff(
                src.splitlines(),
                dst.splitlines(),
                lineterm=""
            )
        )

    def ensure_collection(self):
        self.files.ensure_index([("object", 1), ("ft", 1)])