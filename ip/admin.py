# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## admin.py
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from django.contrib import admin
from django import forms
from noc.ip.models import VRFGroup,VRF,IPv4BlockAccess,IPv4Block,IPv4Address,IPv4AddressRange
from noc.peer.models import AS
from noc.lib.ip import cmp_ip
##
## Admin for VRFGroup
##
class VRFGroupAdmin(admin.ModelAdmin):
    list_display=["name","unique_addresses","description"]
    search_fields=["name"]
##
## Admin or VRF
##
class VRFAdmin(admin.ModelAdmin):
    list_display=["rd","name","vrf_group","description"]
    search_fields=["name","rd"]
    list_filter=["vrf_group"]
    def save_model(self, request, obj, form, change):
        vrf=form.save()
        # Create 0.0.0.0/0 prefix if not exists
        try:
            IPv4Block.objects.get(vrf=vrf,prefix="0.0.0.0/0")
        except IPv4Block.DoesNotExist:
            IPv4Block(vrf=vrf,prefix="0.0.0.0/0",description="root",asn=AS.default_as(),modified_by=request.user).save()
##
## Admin for IPv4BlockAccess
##
class IPv4BlockAccessAdmin(admin.ModelAdmin):
    list_display=["user","vrf","prefix"]
    list_filter=["user","vrf"]
    search_fields=["user","prefix"]
##
##
##
class IPv4AddressRangeAdminForm(forms.ModelForm):
    class Meta:
        model=IPv4AddressRange
    def clean(self):
        try:
            instance=self.instance
        except:
            instance=None
        vrf=self.cleaned_data["vrf"]
        from_ip=self.cleaned_data["from_ip"]
        to_ip=self.cleaned_data["to_ip"]
        if cmp_ip(from_ip,to_ip)>0:
            raise forms.ValidationError("'To IP' must be not less than 'From IP'")
        # Check for lock status
        if self.cleaned_data["is_locked"]==False and self.cleaned_data["fqdn_action"]!="N":
            raise forms.ValidationError("Need to lock range for FQDN Action")
        if self.cleaned_data["fqdn_action"] in ["G","D"] and not self.cleaned_data["fqdn_action_parameter"]:
            raise forms.ValidationError("FQDN Action Parameter required")
        # Check for overlapped ranges
        ro=list(IPv4AddressRange.get_range_overlap(vrf,from_ip,to_ip,instance)[:10])
        if ro:
            raise forms.ValidationError("Range overlaps with %s"%",".join([unicode(r) for r in ro]))
        # Check for overlapped blocks
        bo=list(IPv4AddressRange.get_block_overlap(vrf,from_ip,to_ip)[:10])
        if bo:
            raise forms.ValidationError("Range overlaps with blocks %s"%",".join([unicode(r) for r in bo]))
        return self.cleaned_data

class IPv4AddressRangeAdmin(admin.ModelAdmin):
    form=IPv4AddressRangeAdminForm
    list_display=["name","vrf","from_ip","to_ip","is_locked","fqdn_action","fqdn_action_parameter"]
    list_filter=["is_locked","vrf"]
    search_fields=["name"]

admin.site.register(VRFGroup,VRFGroupAdmin)
admin.site.register(VRF,VRFAdmin)
admin.site.register(IPv4BlockAccess,IPv4BlockAccessAdmin)
admin.site.register(IPv4AddressRange, IPv4AddressRangeAdmin)