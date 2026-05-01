# akn_sdk/actions/dispute.py

from ..protocol.envelope import build_envelope
from ..protocol.signer import canonicalize


async def raise_dispute(http_client, key_manager, agent_id, response_id, argument):

    payload = {
        "response_id": response_id,
        "argument": argument,
    }

    envelope = build_envelope(agent_id, payload)
    envelope["signature"] = key_manager.sign(canonicalize(payload))

    return http_client.post("/disputes/", envelope)