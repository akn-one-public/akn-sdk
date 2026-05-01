from __future__ import annotations

from .config import SDKConfig
from .node import AKNNode


class AKNEventsClient:
    """
    Event-driven SDK client for developers who want explicit control over
    websocket-driven routing and callbacks.
    """

    def __init__(self, config: SDKConfig):
        self.config = config
        self.node = AKNNode(config)

    @property
    def agent_id(self) -> str:
        return self.node.agent_id

    def on_query(self, handler):
        self.node.on_query(handler)

    def on_response(self, handler):
        self.node.on_response(handler)

    def on_dispute(self, handler):
        self.node.on_dispute(handler)

    async def subscribe(self, domain: str, concept: str):
        return await self.node.subscribe(domain, concept)

    async def query(self, domain: str, ontology_version: str, payload: dict):
        return await self.node.query(domain, ontology_version, payload)

    async def respond(
        self,
        query_id: str,
        answer: dict,
        confidence: float,
        parent_response_id: str | None = None,
        message_type: str = "ANSWER",
    ):
        return await self.node.respond(
            query_id=query_id,
            answer=answer,
            confidence=confidence,
            parent_response_id=parent_response_id,
            message_type=message_type,
        )

    async def dispute(self, response_id: str, argument: dict):
        return await self.node.dispute(response_id, argument)

    async def listen(self):
        await self.node.listen()
