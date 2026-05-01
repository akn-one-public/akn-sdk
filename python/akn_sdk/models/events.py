# akn_sdk/models/events.py

from pydantic import BaseModel
from typing import Optional, Dict, Any


class BaseEvent(BaseModel):
    type: str
    protocol_version: Optional[str]
    agent_id: Optional[str]


class QueryEvent(BaseEvent):
    query_id: str
    payload: Dict[str, Any]


class ResponseEvent(BaseEvent):
    response_id: str
    query_id: str
    payload: Dict[str, Any]


class DisputeEvent(BaseEvent):
    dispute_id: str
    response_id: str
    payload: Dict[str, Any]