# akn_sdk/actions/query.py

from ..protocol.envelope import build_envelope
from ..protocol.signer import canonicalize


async def submit_query(http_client, key_manager, agent_id, domain, ontology_version, payload):

    data = {
        "domain": domain,
        "ontology_version": ontology_version,
        "payload": payload,
    }

    envelope = build_envelope(agent_id, data)
    envelope["signature"] = key_manager.sign(canonicalize(data))

    return http_client.post("/queries/", envelope)