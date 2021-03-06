# ---------------------------------------------------------------------
# IGetSLAProbe
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.interface.base import BaseInterface
from .base import (
    DictListParameter,
    StringParameter,
    BooleanParameter,
    IntParameter,
    LabelListParameter,
)


class IGetSLAProbes(BaseInterface):
    """
    name: Probe name. Pair of (<name>, <group>) must be unique per object
    description: Probe description
    type: Probe type
    target: Probe target, i.e address or URL depending on probe
    hw_timestamp: Hardware timestamps usage
    group: Name of group of probes (owner for IOS, probe name for JUNOS etc)
    tags: Additional tags
    """

    returns = DictListParameter(
        attrs={
            "group": StringParameter(required=True, default=""),
            "name": StringParameter(),
            "description": StringParameter(required=False),
            # SLA Probe operational status
            # True - Active
            # False - NonOperational
            "status": BooleanParameter(default=True),
            # VRF Name
            "vrf": StringParameter(required=False),
            # TOS
            "tos": IntParameter(required=False),
            "type": StringParameter(
                choices=[
                    "icmp-echo",
                    "path-jitter",
                    "udp-jitter",
                    "udp-echo",
                    "tcp-connect",
                    "http-get",
                    "dns",
                    "ftp",
                    "dhcp",
                    "owamp",  # One-Way Active Measurement Protocol (RFC4656)
                    "twamp",  # Two-Way Active Measurement Protocol (RFC5357)
                ]
            ),
            "target": StringParameter(),
            "hw_timestamp": BooleanParameter(default=False),
            # Custom field
            "tags": LabelListParameter(required=False, default_scope="noc::sla::tag"),
        }
    )
