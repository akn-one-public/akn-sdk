# akn_sdk/actions/register.py

async def register_agent(http_client, agent_name, public_key):
    return http_client.post(
        "/agents/register",
        {
            "agent_name": agent_name,
            "public_key": public_key
        }
    )