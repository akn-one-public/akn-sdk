from ..protocol.envelope import build_envelope
from ..protocol.signer import canonicalize


async def submit_validation(http_client, key_manager, agent_id, target_id, score):
    payload = {
        "target_id": target_id,
        "score": score,
    }

    envelope = build_envelope(agent_id, payload)
    envelope["signature"] = key_manager.sign(canonicalize(payload))

    return http_client.post("/validations/", envelope)
