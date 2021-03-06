# ----------------------------------------------------------------------
# SendRequest
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
from typing import Any, Optional, List, Dict

# Third-party modules
from pydantic import BaseModel, root_validator


class SendRequestItem(BaseModel):
    ts: datetime.datetime
    labels: Optional[List[str]]
    service: int
    collector: str
    metrics: Dict[str, Any]

    @root_validator(pre=True)
    def build_metrics(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        r: Dict[str, Any] = {f: values[f] for f in cls.__fields__ if f in values and f != "metrics"}
        r["metrics"] = {f: values[f] for f in values if f not in cls.__fields__}
        return r


class SendRequest(BaseModel):
    __root__: List[SendRequestItem]
