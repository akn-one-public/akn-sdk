# akn_sdk/node.py

from .config import SDKConfig
from .identity.wallet import Wallet
from .transport.http_client import HTTPClient
from .transport.ws_client import WebSocketClient
from .runtime.dispatcher import Dispatcher
from .actions.subscribe import subscribe
from .actions.query import submit_query
from .actions.response import submit_response
from .actions.dispute import raise_dispute


class AKNNode:
    """
    Production SDK Node

    Security Model:
        - api_key   → Developer account authentication
        - agent_key → Per-agent cryptographic signing
    """

    def __init__(self, config: SDKConfig):

        self.config = config
        self.agent_id = config.agent_id

        # -------------------------------------------------
        # Sync Wallet with agent_key
        # -------------------------------------------------
        self.wallet = Wallet(config.wallet_path)
        self.key_manager = self.wallet.load_or_sync(config.agent_key)

        # -------------------------------------------------
        # HTTP client with API key
        # -------------------------------------------------
        self.http = HTTPClient(
            config.gateway_url,
            token=config.api_key,
            timeout=config.timeout,
            retries=config.retry_attempts
        )

        self.dispatcher = Dispatcher()

    # ============================================================
    # PROTOCOL ACTIONS
    # ============================================================

    async def subscribe(self, domain: str, concept: str):
        return await subscribe(
            self.http,
            self.agent_id,
            domain,
            concept
        )

    async def query(self, domain: str, ontology_version: str, payload: dict):
        return await submit_query(
            self.http,
            self.key_manager,
            self.agent_id,
            domain,
            ontology_version,
            payload
        )

    async def respond(
        self,
        query_id: str,
        answer: dict,
        confidence: float,
        parent_response_id: str = None,
        message_type: str = "ANSWER"
    ):
        return await submit_response(
            self.http,
            self.key_manager,
            self.agent_id,
            query_id,
            answer,
            confidence,
            parent_response_id,
            message_type
        )

    async def dispute(self, response_id: str, argument: dict):
        return await raise_dispute(
            self.http,
            self.key_manager,
            self.agent_id,
            response_id,
            argument
        )

    # ============================================================
    # EVENT HANDLERS
    # ============================================================

    def on_query(self, handler):
        self.dispatcher.on_query(handler)

    def on_response(self, handler):
        self.dispatcher.on_response(handler)

    def on_dispute(self, handler):
        self.dispatcher.on_dispute(handler)

    # ============================================================
    # WEBSOCKET LISTENER
    # ============================================================

    async def listen(self):

        ws_url = self.config.gateway_url.replace("http", "ws")
        ws_url += f"/ws/agent/{self.agent_id}"

        ws = WebSocketClient(
            ws_url,
            token=self.config.api_key,
            auto_reconnect=self.config.auto_reconnect
        )

        async for event in ws.listen():
            await self.dispatcher.dispatch(event)