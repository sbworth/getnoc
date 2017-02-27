# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Clickhouse models
##----------------------------------------------------------------------
## Copyright (C) 2007-2016 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import time
## Third-party modules
import six
## NOC modules
from fields import BaseField
from noc.core.clickhouse.connect import connection
from noc.core.bi.query import to_sql, escape_field

__all__ = ["Model"]


class ModelBase(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        cls._fields = {}
        cls._meta = ModelMeta(
            engine=getattr(cls.Meta, "engine", None),
            db_table=getattr(cls.Meta, "db_table", None),
            description=getattr(cls.Meta, "description", None),
            tags=getattr(cls.Meta, "tags", None),
        )
        for k in attrs:
            if isinstance(attrs[k], BaseField):
                cls._fields[k] = attrs[k]
                cls._fields[k].name = k
        cls._fields_order = sorted(
            cls._fields, key=lambda x: cls._fields[x].field_number
        )
        return cls


class ModelMeta(object):
    def __init__(self, engine=None, db_table=None, description=None,
                 tags=None):
        self.engine = engine
        self.db_table = db_table
        self.description = description
        self.tags = tags


class Model(six.with_metaclass(ModelBase)):
    class Meta:
        engine = None
        db_table = None
        description = None
        tags = None

    def __init__(self, **kwargs):
        self.values = kwargs

    @classmethod
    def get_create_sql(cls):
        r = ["CREATE TABLE IF NOT EXISTS %s (" % cls._meta.db_table]
        r += [",\n".join(cls._fields[f].get_create_sql() for f in cls._fields_order)]
        r += [") ENGINE = %s;" % cls._meta.engine.get_create_sql()]
        return "\n".join(r)

    @classmethod
    def to_tsv(cls, **kwargs):
        return "\t".join(
            cls._fields[f].to_tsv(kwargs[f]) for f in cls._fields_order
        ) + "\n"

    @classmethod
    def ensure_table(cls):
        ch = connection()
        if not ch.has_table(cls._meta.db_table):
            # Create new table
            ch.execute(post=cls.get_create_sql())
        else:
            # Alter when necessary
            existing = {}
            for name, type in ch.execute(
                """
                SELECT name, type
                FROM system.columns
                WHERE
                  database=%s
                  AND table=%s
                """,
                [ch.DB, cls._meta.db_table]
            ):
                existing[name] = type
            after = None
            for f in cls._fields_order:
                if f not in existing:
                    ch.execute(post="ALTER TABLE %s ADD COLUMN %s AFTER %s" % (
                        cls._meta.db_table, cls._fields[f].get_create_sql(), after))
                after = f

    @classmethod
    def get_model_class(cls, name):
        """
        Returns model class referred by name
        @todo: Process custom/
        :param name:
        :return:
        """
        m = __import__("noc.core.bi.models.%s" % name, {}, {}, "*")
        for a in dir(m):
            o = getattr(m, a)
            if not hasattr(o, "_meta"):
                continue
            if getattr(o._meta, "db_table", None) == name:
                return o
        return None

    @classmethod
    def transform_query(cls, query, user):
        """
        Transform query, possibly applying access restrictions
        :param query:
        :param user:
        :return: query dict or None if access denied
        """
        return query

    @classmethod
    def query(cls, query, user=None):
        """
        Execute query and return result
        :param query: dict of
            "fields": list of dicts
                *expr -- field expression
                *alias -- resulting name
                *group -- nth field in GROUP BY expression, starting from 0
                *order -- nth field in ORDER BY expression, starting from 0
                *desc -- sort in descending order, if true
            "filter": expression
            "limit": N -- limit to N rows
            "offset": N -- skip first N rows
            "sample": 0.0-1.0 -- randomly select rows
            @todo: group by
            @todo: order by
        :return:
        """
        # Get field expressions
        fields = query.get("fields", [])
        if not fields:
            return None
        transformed_query = cls.transform_query(query, user)
        fields_x = []
        aliases = []
        group_by = {}
        order_by = {}
        for i, f in enumerate(fields):
            if isinstance(f["expr"], six.string_types):
                default_alias = f["expr"]
                f["expr"] = {"$field": f["expr"]}
            else:
                default_alias = "f%04d" % i
            alias = f.get("alias", default_alias)
            if not f.get("hide"):
                aliases += [alias]
                fields_x += ["%s AS %s" % (to_sql(f["expr"]), escape_field(alias))]
            if "group" in f:
                group_by[int(f["group"])] = alias
            if "order" in f:
                if "desc" in f and f["desc"]:
                    order_by[int(f["order"])] = "%s DESC" % alias
                else:
                    order_by[int(f["order"])] = alias
        if transformed_query is None:
            # Access denied
            r = []
            dt = 0.0
            sql = ["SELECT %s FROM %s WHERE 0 = 1" % (", ".join(fields_x), cls._meta.db_table)]
        else:
            # Get where expressions
            filter_x = to_sql(transformed_query.get("filter", {}))
            # Generate SQL
            sql = ["SELECT "]
            sql += [", ".join(fields_x)]
            sql += ["FROM %s" % cls._meta.db_table]
            sample = query.get("sample")
            if sample:
                sql += ["SAMPLE %s" % float(sample)]
            if filter_x:
                sql += ["WHERE %s" % filter_x]
            # GROUP BY
            if group_by:
                sql += ["GROUP BY %s" % ", ".join(group_by[v] for v in sorted(group_by))]
            # ORDER BY
            if order_by:
                sql += ["ORDER BY %s" % ", ".join(order_by[v] for v in sorted(order_by))]
            # LIMIT
            if "limit" in query:
                if "offset" in query:
                    sql += ["LIMIT %d, %d" % (query["offset"], query["limit"])]
                else:
                    sql += ["LIMIT %d" % query["limit"]]
            sql = " ".join(sql)
            # Execute query
            ch = connection()
            t0 = time.time()
            r = ch.execute(sql)
            dt = time.time() - t0
        return {
            "fields": aliases,
            "result": r,
            "duration": dt,
            "sql": sql
        }
