# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## ExtApplication implementation
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Django moules
from django.core import serializers
#from django.http import HttpResponse
from django.utils.encoding import is_protected_type
from django.http import HttpResponse
from django.utils.simplejson.decoder import JSONDecoder
from django.utils.simplejson.encoder import JSONEncoder
## NOC modules
from extapplication import ExtApplication, view


class ExtModelApplication(ExtApplication):
    model = None  # Django model to expose
    
    pk_field_name = None  # Set by constructor
    
    # REST return codes and messages
    OK = 200
    CREATED = 201
    DELETED = 204
    BAD_REQUEST = 400
    FORBIDDEN = 401
    NOT_FOUND = 404
    DUPLICATE_ENTRY = 409
    NOT_HERE = 410
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    THROTTLED = 503
    
    ignored_params = ["_dc"]
    page_param = "__page"
    start_param = "__start"
    limit_param = "__limit"
    sort_param = "__sort"
    format_param = "__format"  # List output format

    def __init__(self, *args, **kwargs):
        super(ExtModelApplication, self).__init__(*args, **kwargs)
        self.pk_field_name = self.model._meta.pk.name

    def queryset(self, request):
        return self.model.objects.all()

    def deserialize(self, data):
        return JSONDecoder(encoding="utf8").decode(data)

    def response(self, content="", status=200):
        if not isinstance(content, basestring):
            return HttpResponse(JSONEncoder(ensure_ascii=False).encode(content),
                               mimetype="text/json; charset=utf-8",
                               status=status)
        else:
            return HttpResponse(content,
                               mimetype="text/plain; charset=utf-8",
                               status=status)

    def cleaned_query(self, q):
        q = q.copy()
        for p in self.ignored_params:
            if p in q:
                del q[p]
        for p in (self.limit_param, self.page_param, self.start_param,
            self.format_param, self.sort_param):
            if p in q:
                del q[p]
        return q

    def instance_to_dict(self, o):
        r = {}
        for f in o._meta.local_fields:
            if f.rel is None:
                r[f.name] = f._get_val_from_obj(o)
            else:
                r[f.name] = getattr(o, f.name)._get_pk_val()
        return r

    @view(method=["GET"], url="^$", access="read", api=True)
    def api_list(self, request):
        """
        Returns a list of available objects
        """
        q = dict(request.GET.items())
        limit = q.get(self.limit_param)
        page = q.get(self.page_param)
        start = q.get(self.start_param)
        format = q.get(self.format_param)
        ordering = []
        if format == "ext" and self.sort_param in q:
            for r in self.deserialize(q[self.sort_param]):
                if r["direction"] == "DESC":
                    ordering += ["-%s" % r["property"]]
                else:
                    ordering += [r["property"]]
        q = self.cleaned_query(q)
        data = self.queryset(request).filter(**q)
        # Apply sorting
        if ordering:
            data = data.order_by(*ordering)
        if format == "ext":
            total = data.count()
        if start is not None and limit is not None:
            data = data[int(start):int(start) + int(limit)]
        out = [self.instance_to_dict(o) for o in data]
        if format == "ext":
            out = {
                "total": total,
                "success": True,
                "data": out
            }
        return self.response(out, status=self.OK)

    @view(method=["POST"], url="^$", access="create", api=True)
    def api_create(self, request):
        try:
            attrs = self.deserialize(request.raw_post_data)
        except ValueError, why:
            return self.response(str(why), status=self.BAD_REQUEST)
        try:
            o = self.queryset(request).get(**attrs)
            return self.response(status=self.DUPLICATE_ENTRY)
        except self.model.MultipleObjectsReturned:
            return self.response(status=self.DUPLICATE_ENTRY)
        except self.model.DoesNotExist:
            o = self.model(**attrs)
            o.save()
            return self.response(self.instance_to_dict(o), status=self.CREATED)

    @view(method=["GET"], url="^(?P<id>\d+)/", access="read", api=True)
    def api_read(self, request, id):
        """
        Returns dict with object's fields and values
        """
        try:
            o = self.queryset(request).get(id=int(id))
        except self.model.DoesNotExist:
            return HttpResponse("", status=self.NOT_FOUND)
        return self.response(self.instance_to_dict(o), status=self.OK)

    @view(method=["PUT"], url="^(?P<id>\d+)/", access="update", api=True)
    def api_update(self, request, id):
        try:
            attrs = self.deserialize(request.raw_post_data)
        except ValueError, why:
            return self.response(str(why), status=self.BAD_REQUEST)
        try:
            o = self.queryset(request).get(id=int(id))
        except self.model.DoesNotExist:
            return HttpResponse("", status=self.NOT_FOUND)
        for k, v in attrs.items():
            setattr(o, k, v)
        o.save()
        return self.response(status=self.OK)

    @view(method=["DELETE"], url="^(?P<id>\d+)/", access="delete", api=True)
    def api_delete(self, request, id):
        try:
            o = self.queryset(request).get(id=int(id))
        except self.model.DoesNotExist:
            return HttpResponse("", status=self.NOT_FOUND)
        o.delete()
        return HttpResponse(status=self.DELETED)
