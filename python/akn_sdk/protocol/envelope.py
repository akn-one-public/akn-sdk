# akn_sdk/protocol/envelope.py

import uuid
from datetime import datetime, timezone


def build_envelope(agent_id: str, payload: dict, protocol_version="0.1.0"):
    return {
        "protocol_version": protocol_version,
        "message_id": str(uuid.uuid4()),
        "agent_id": agent_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }