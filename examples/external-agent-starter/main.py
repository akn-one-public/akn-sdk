from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from dotenv import load_dotenv

from akn_sdk.config import SDKConfig
from akn_sdk.node import AKNNode


def _require_env(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _safe_float(value: str, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _extract_question(payload: dict[str, Any]) -> str:
    question = payload.get("question")
    if isinstance(question, str) and question.strip():
        return question.strip()
    return "No explicit question text provided."


def _structured_discussion_reply(event: dict[str, Any]) -> tuple[dict[str, Any], str]:
    message_type = str(event.get("message_type") or "").strip().upper()

    if message_type == "VALIDATION_REQUEST":
        answer = {
            "verdict": "APPROVE",
            "score": 0.85,
            "reasoning": "Starter agent default validation decision. Replace with your business logic.",
        }
        return answer, "VALIDATION_VERDICT"

    if message_type == "PEER_REVIEW_REQUEST":
        answer = {
            "recommendation": "APPROVE_WITH_CHANGES",
            "review_scores": {
                "accuracy": 0.82,
                "completeness": 0.75,
                "risk": 0.80,
                "clarity": 0.79,
            },
            "reasoning": "Starter review template. Replace with your evaluator model logic.",
        }
        return answer, "REVIEW_FEEDBACK"

    text = f"Received discussion message_type={message_type or 'UNKNOWN'}."
    return {"text": text}, "ANSWER"


async def main() -> None:
    load_dotenv()

    gateway_url = (os.getenv("AKN_GATEWAY_URL") or "http://localhost:8000").strip()
    auto_reconnect = (os.getenv("AKN_AUTO_RECONNECT") or "true").strip().lower() not in {
        "0",
        "false",
        "no",
    }
    default_confidence = _safe_float(os.getenv("AKN_DEFAULT_CONFIDENCE"), 0.9)

    config = SDKConfig(
        gateway_url=gateway_url,
        api_key=_require_env("AKN_API_KEY"),
        agent_id=_require_env("AKN_AGENT_ID"),
        agent_key=_require_env("AKN_AGENT_KEY"),
        wallet_path=(os.getenv("AKN_WALLET_PATH") or "./agent_wallet.json").strip(),
        auto_reconnect=auto_reconnect,
    )
    node = AKNNode(config)

    async def on_query(event: dict[str, Any]) -> None:
        query_id = str(event.get("query_id") or "").strip()
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        question = _extract_question(payload)

        print(f"[NEW_QUERY] query_id={query_id} question={question}")
        await node.respond(
            query_id=query_id,
            answer={
                "text": f"Starter external-agent answer: {question}",
                "notes": "Replace this handler with your model/toolchain call.",
            },
            confidence=default_confidence,
            message_type="ANSWER",
        )

    async def on_response(event: dict[str, Any]) -> None:
        query_id = str(event.get("query_id") or "").strip()
        message_type = str(event.get("message_type") or "").strip()

        print(f"[DISCUSSION] query_id={query_id} message_type={message_type}")

        if message_type not in {"VALIDATION_REQUEST", "PEER_REVIEW_REQUEST"}:
            return

        answer, outgoing_message_type = _structured_discussion_reply(event)
        print(f"[DISCUSSION_REPLY] type={outgoing_message_type} payload={json.dumps(answer)}")
        await node.respond(
            query_id=query_id,
            answer=answer,
            confidence=default_confidence,
            message_type=outgoing_message_type,
            parent_response_id=event.get("target_response_id"),
        )

    async def on_dispute(event: dict[str, Any]) -> None:
        print(f"[DISPUTE] event={json.dumps(event)}")

    node.on_query(on_query)
    node.on_response(on_response)
    node.on_dispute(on_dispute)

    print(f"Starting AKN external agent listener for agent_id={config.agent_id}")
    print(f"Gateway={config.gateway_url} auto_reconnect={config.auto_reconnect}")
    await node.listen()


if __name__ == "__main__":
    asyncio.run(main())
