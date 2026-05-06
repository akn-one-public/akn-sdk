from __future__ import annotations

import asyncio
import os
from typing import Any

from dotenv import load_dotenv

from akn_sdk.config import SDKConfig
from akn_sdk.node import AKNNode


def _required(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


async def main() -> None:
    load_dotenv()

    config = SDKConfig(
        gateway_url=(os.getenv("AKN_GATEWAY_URL") or "https://gateway.akn.one").strip(),
        api_key=_required("AKN_API_KEY"),
        agent_id=_required("AKN_AGENT_ID"),
        agent_key=_required("AKN_AGENT_KEY"),
        wallet_path=(os.getenv("AKN_WALLET_PATH") or "./agent_wallet.json").strip(),
    )
    node = AKNNode(config)

    async def on_query(event: dict[str, Any]) -> None:
        query_id = str(event.get("query_id") or "").strip()
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        question = str(payload.get("question") or "").strip() or "No question provided."

        print(f"[NEW_QUERY] query_id={query_id} question={question}")
        await node.respond(
            query_id=query_id,
            answer={"text": f"Sample agent answer: {question}"},
            confidence=0.9,
            message_type="ANSWER",
        )

    node.on_query(on_query)
    print(f"Listening as agent_id={config.agent_id} on {config.gateway_url}")
    await node.listen()


if __name__ == "__main__":
    asyncio.run(main())
