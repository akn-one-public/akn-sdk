# akn_sdk/actions/subscribe.py

async def subscribe(http_client, agent_id, domain, concept):
    return http_client.post(
        "/subscriptions/",
        {
            "agent_id": agent_id,
            "domain": domain,
            "concept": concept
        }
    )