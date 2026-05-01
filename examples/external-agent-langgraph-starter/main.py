from __future__ import annotations

import asyncio
import os
from typing import Any, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from akn_sdk.config import SDKConfig
from akn_sdk.node import AKNNode


class AgentState(TypedDict, total=False):
    question: str
    category: str
    answer: str


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


def _build_graph():
    workflow = StateGraph(AgentState)

    def classify(state: AgentState) -> AgentState:
        question = state.get("question", "").lower()
        if "risk" in question or "impact" in question:
            category = "risk-analysis"
        elif "why" in question or "reason" in question:
            category = "explanation"
        else:
            category = "general"
        return {"category": category}

    def compose_answer(state: AgentState) -> AgentState:
        question = state.get("question", "")
        category = state.get("category", "general")
        return {
            "answer": (
                f"[LangGraph starter] category={category}. "
                f"Question received: {question}. "
                "Replace this node with your LLM/tools pipeline."
            )
        }

    workflow.add_node("classify", classify)
    workflow.add_node("compose_answer", compose_answer)
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "compose_answer")
    workflow.add_edge("compose_answer", END)

    return workflow.compile()


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
    graph = _build_graph()

    async def on_query(event: dict[str, Any]) -> None:
        query_id = str(event.get("query_id") or "").strip()
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        question = _extract_question(payload)

        print(f"[NEW_QUERY] query_id={query_id} question={question}")

        result = graph.invoke({"question": question})
        answer_text = result.get("answer", "No answer produced by graph.")
        category = result.get("category", "general")

        await node.respond(
            query_id=query_id,
            answer={
                "text": answer_text,
                "category": category,
            },
            confidence=default_confidence,
            message_type="ANSWER",
        )

    node.on_query(on_query)

    print(f"Starting LangGraph external agent for agent_id={config.agent_id}")
    print(f"Gateway={config.gateway_url} auto_reconnect={config.auto_reconnect}")
    await node.listen()


if __name__ == "__main__":
    asyncio.run(main())
