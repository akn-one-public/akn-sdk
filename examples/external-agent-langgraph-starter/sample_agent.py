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
    answer: str


def _required(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def _extract_question(payload: dict[str, Any]) -> str:
    question = payload.get("question")
    if isinstance(question, str) and question.strip():
        return question.strip()
    return "No question provided."


def _build_graph():
    workflow = StateGraph(AgentState)

    def compose_answer(state: AgentState) -> AgentState:
        question = state.get("question", "")
        return {"answer": f"[LangGraph sample] {question}"}

    workflow.add_node("compose_answer", compose_answer)
    workflow.set_entry_point("compose_answer")
    workflow.add_edge("compose_answer", END)
    return workflow.compile()


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
    graph = _build_graph()

    async def on_query(event: dict[str, Any]) -> None:
        query_id = str(event.get("query_id") or "").strip()
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        question = _extract_question(payload)
        result = graph.invoke({"question": question})

        await node.respond(
            query_id=query_id,
            answer={"text": result.get("answer", "No answer produced.")},
            confidence=0.9,
            message_type="ANSWER",
        )

    node.on_query(on_query)
    await node.listen()


if __name__ == "__main__":
    asyncio.run(main())
