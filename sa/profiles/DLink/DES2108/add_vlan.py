# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DES2108.add_vlan
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from __future__ import with_statement
import noc.sa.script
from noc.sa.interfaces import IAddVlan

class Script(noc.sa.script.Script):
    name="DLink.DES2108.add_vlan"
    implements=[IAddVlan]
    def execute(self,vlan_id,name,tagged_ports):
        with self.configure():
            self.cli("create vlan tag %d desc %s"%(vlan_id,name))
            if tagged_ports:
                for port in tagged_ports:
                    self.cli("config vlan vid %d add tagged %s"%(vlan_id,port))
        self.save_config()
        return True
