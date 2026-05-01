# akn_sdk/actions/response.py

from ..protocol.envelope import build_envelope
from ..protocol.signer import canonicalize


async def submit_response(
    http_client,
    key_manager,
    agent_id,
    query_id,
    answer,
    confidence,
    parent_response_id=None,
    message_type="ANSWER"
):

    payload = {
        "query_id": query_id,
        "answer": answer,
        "confidence": confidence,
        "parent_response_id": parent_response_id,
        "message_type": message_type,
    }

    envelope = build_envelope(agent_id, payload)
    envelope["signature"] = key_manager.sign(canonicalize(payload))

    return http_client.post("/responses/", envelope)