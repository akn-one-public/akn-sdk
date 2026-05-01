from __future__ import annotations

import asyncio
import os
from typing import Any

from dotenv import load_dotenv

from akn_sdk.config import SDKConfig
from akn_sdk.node import AKNNode

try:
    from google.adk.agents import Agent  # type: ignore
except Exception:  # pragma: no cover - optional import for starter runtime
    Agent = None


def _require_env(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _safe_float(value: str | None, fallback: float) -> float:
    try:
        return float(value) if value is not None else fallback
    except (TypeError, ValueError):
        return fallback


def _extract_question(payload: dict[str, Any]) -> str:
    question = payload.get("question")
    if isinstance(question, str) and question.strip():
        return question.strip()
    return "No explicit question text provided."


class ADKAdapter:
    """
    Thin adapter so this starter remains easy to customize.

    Replace `run` with your project-specific ADK execution path if your chosen
    ADK API shape differs from this minimal starter.
    """

    def __init__(self) -> None:
        if Agent is None:
            raise RuntimeError(
                "google-adk is not installed. Run `pip install -r requirements.txt` first."
            )
        self.agent = Agent(
            name="akn-adk-starter",
            instruction=(
                "You are an external analysis helper integrated with AKN. "
                "Return concise and clear answers."
            ),
        )

    async def run(self, question: str) -> str:
        if hasattr(self.agent, "run_async"):
            result = await self.agent.run_async(question)  # type: ignore[attr-defined]
        else:
            result = self.agent.run(question)  # type: ignore[attr-defined]

        if isinstance(result, str):
            return result
        return str(result)


async def main() -> None:
    load_dotenv()

    config = SDKConfig(
        gateway_url=(os.getenv("AKN_GATEWAY_URL") or "http://localhost:8000").strip(),
        api_key=_require_env("AKN_API_KEY"),
        agent_id=_require_env("AKN_AGENT_ID"),
        agent_key=_require_env("AKN_AGENT_KEY"),
        wallet_path=(os.getenv("AKN_WALLET_PATH") or "./agent_wallet.json").strip(),
        auto_reconnect=(os.getenv("AKN_AUTO_RECONNECT") or "true").strip().lower() not in {"0", "false", "no"},
    )
    default_confidence = _safe_float(os.getenv("AKN_DEFAULT_CONFIDENCE"), 0.9)

    node = AKNNode(config)
    adk = ADKAdapter()

    async def on_query(event: dict[str, Any]) -> None:
        query_id = str(event.get("query_id") or "").strip()
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        question = _extract_question(payload)

        print(f"[NEW_QUERY] query_id={query_id} question={question}")
        answer_text = await adk.run(question)

        await node.respond(
            query_id=query_id,
            answer={"text": answer_text},
            confidence=default_confidence,
            message_type="ANSWER",
        )

    node.on_query(on_query)

    print(f"Starting Google ADK external agent for agent_id={config.agent_id}")
    print(f"Gateway={config.gateway_url} auto_reconnect={config.auto_reconnect}")
    await node.listen()


if __name__ == "__main__":
    asyncio.run(main())
