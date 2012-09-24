# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_version test
## Auto-generated by manage.py debug-script at 2011-03-01 18:35:25
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_version_Test(ScriptTestCase):
    script="EdgeCore.ES.get_version"
    vendor="EdgeCore"
    platform='ES3510'
    version='1.1.0.29'
    input={}
    result={'attributes': {'HW version': 'R01', 'Serial Number': '935000844'},
 'platform': 'ES3510',
 'vendor': 'EdgeCore',
 'version': '1.1.0.29'}
    motd=' \n\n      CLI session with the ES3510 is opened.\n      To end the CLI session, enter [Exit].\n\n'
    cli={
## 'show version'
'show version': """show version
 Serial Number:           935000844
 Service Tag:             
 Hardware Version:        R01
 EPLD Version:            0.00
 Number of Ports:         10
 Main Power Status:       Up
 Loader Version:          1.0.0.2
 Boot ROM Version:        1.0.0.5
 Operation Code Version:  1.1.0.29
""", 
'terminal length 0':  "terminal length 0\n      ^\n% Invalid input detected at '^' marker.\n", 
## 'show system'
'show system': """show system
System Description: Layer2+ Fast Ethernet Standalone Switch ES3510
System OID String: 1.3.6.1.4.1.259.8.1.5
System Information
 System Up Time:          9 days, 22 hours, 17 minutes, and 31.79 seconds
 System Name:             10.202.128.2
 System Location:         [NONE]
 System Contact:          [NONE]
 MAC Address (Unit1):     00-12-CF-DF-A4-10
 Web Server:              Enabled
 Web Server Port:         80
 Web Secure Server:       Enabled
 Web Secure Server Port:  443
 Telnet Server:           Enable
 Telnet Server Port:      23
 Authentication Login:     Local RADIUS None
 Authentication Enabled:    Local RADIUS None
 Jumbo Frame:             Disabled 

 POST Result:              
DUMMY Test 1 ................. PASS
UART Loopback Test ........... PASS
DRAM Test .................... PASS
Switch Int Loopback Test ..... PASS

Done All Pass.""", 
}
    snmp_get={'1.3.6.1.2.1.1.1.0': 'Layer2+ Fast Ethernet Standalone Switch ES3510',
 '1.3.6.1.2.1.1.2.0': '(1, 3, 6, 1, 4, 1, 259, 8, 1, 5)',
 '1.3.6.1.4.1.259.8.1.5.1.1.3.1.6.1': '1.1.0.29'}
    snmp_getnext={}
    http_get = {}

