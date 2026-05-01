from __future__ import annotations

import asyncio
import time
from typing import Any

from .config import SDKConfig
from .node import AKNNode
from .transport.ws_client import WebSocketClient


class AKNSychClient:
    """
    Synchronous convenience client on top of the async AKN event model.

    This class hides websocket/listener setup for developers who prefer
    request/response style APIs.
    """

    RESPONSE_MESSAGE_TYPES = {
        "ANSWER",
        "REVISION",
        "REBUTTAL",
        "SUPPORT",
        "CLARIFICATION",
        "VALIDATION_VERDICT",
        "REVIEW_FEEDBACK",
    }

    def __init__(self, config: SDKConfig):
        self.config = config
        self.node = AKNNode(config)

    @property
    def agent_id(self) -> str:
        return self.node.agent_id

    async def _wait_for_query_events(
        self,
        query_id: str,
        *,
        timeout_seconds: float,
        min_responses: int,
    ) -> list[dict[str, Any]]:
        ws_url = self.config.gateway_url.replace("http", "ws")
        ws_url += f"/ws/agent/{self.agent_id}"
        ws = WebSocketClient(
            ws_url,
            token=self.config.api_key,
            auto_reconnect=self.config.auto_reconnect,
        )

        deadline = time.monotonic() + max(1.0, timeout_seconds)
        collected: list[dict[str, Any]] = []
        response_count = 0

        iterator = ws.listen().__aiter__()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            try:
                event = await asyncio.wait_for(iterator.__anext__(), timeout=remaining)
            except asyncio.TimeoutError:
                break
            except StopAsyncIteration:
                break

            if str(event.get("query_id") or "").strip() != query_id:
                continue

            collected.append(event)

            if (
                str(event.get("type") or "").strip().upper() == "DISCUSSION_MESSAGE"
                and str(event.get("message_type") or "").strip().upper()
                in self.RESPONSE_MESSAGE_TYPES
            ):
                response_count += 1
                if response_count >= max(1, min_responses):
                    break

        return collected

    async def ask_async(
        self,
        *,
        domain: str,
        ontology_version: str,
        question: str,
        concepts: list[str] | None = None,
        relationships: list[dict] | None = None,
        supporting_context: str | None = None,
        mode: str = "ask_network",
        candidate_answer: dict | str | None = None,
        review_dimensions: list[str] | None = None,
        timeout_seconds: float = 45.0,
        min_responses: int = 1,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "question": (question or "").strip(),
            "concepts": concepts or [],
            "relationships": relationships or [],
            "mode": (mode or "ask_network").strip(),
        }
        if supporting_context:
            payload["supporting_context"] = supporting_context
        if candidate_answer is not None:
            payload["candidate_answer"] = candidate_answer
        if review_dimensions is not None:
            payload["review_dimensions"] = review_dimensions

        submit_result = await self.node.query(
            domain=domain,
            ontology_version=ontology_version,
            payload=payload,
        )
        query_id = str(submit_result.get("query_id") or "").strip()
        if not query_id:
            raise RuntimeError("AKN did not return query_id")

        events = await self._wait_for_query_events(
            query_id,
            timeout_seconds=timeout_seconds,
            min_responses=min_responses,
        )
        responses = [
            event
            for event in events
            if str(event.get("type") or "").strip().upper() == "DISCUSSION_MESSAGE"
            and str(event.get("message_type") or "").strip().upper() in self.RESPONSE_MESSAGE_TYPES
        ]

        return {
            "query_id": query_id,
            "submit_result": submit_result,
            "events": events,
            "responses": responses,
            "response_count": len(responses),
            "timed_out": len(responses) < max(1, min_responses),
        }

    def ask(self, **kwargs) -> dict[str, Any]:
        try:
            asyncio.get_running_loop()
            raise RuntimeError(
                "ask() cannot run inside an active event loop. "
                "Use `await ask_async(...)` instead."
            )
        except RuntimeError as exc:
            if "cannot run inside an active event loop" in str(exc):
                raise
        return asyncio.run(self.ask_async(**kwargs))
