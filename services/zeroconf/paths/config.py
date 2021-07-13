# ----------------------------------------------------------------------
# config endpoint
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Optional, List
from http import HTTPStatus

# Third-party modules
from fastapi import APIRouter, Query, HTTPException

# NOC modules
from ..models.zk import ZkConfig
from ..util import find_agent, get_config

router = APIRouter()


@router.get("/api/zeroconf/config", response_model=ZkConfig)
def config(
    agent_id: Optional[str] = None,
    serial: Optional[str] = None,
    mac: Optional[List[str]] = Query(None),
    ip: Optional[List[str]] = Query(None),
):
    agent = find_agent(agent_id=agent_id, serial=serial, mac=mac, ip=ip)
    if not agent:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    if agent.profile.update_addresses:
        agent.update_addresses(serial=serial, mac=mac, ip=ip)
    return get_config(agent)