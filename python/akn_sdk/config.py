# akn_sdk/config.py

from dataclasses import dataclass


@dataclass
class SDKConfig:
    """
    SDK Configuration

    Required:
        - gateway_url
        - agent_id
        - api_key        (developer account key)
        - agent_key      (per-agent signing key)
        - wallet_path
    """

    gateway_url: str
    agent_id: str
    api_key: str
    agent_key: str
    wallet_path: str

    timeout: int = 10
    retry_attempts: int = 5
    auto_reconnect: bool = True
    verify_signatures: bool = True
    debug: bool = False

    def __post_init__(self):
        self.gateway_url = self.gateway_url.rstrip("/")

        if not self.agent_id:
            raise ValueError("agent_id is required")

        if not self.api_key:
            raise ValueError("api_key is required")

        if not self.agent_key:
            raise ValueError("agent_key is required")

        if not self.wallet_path:
            raise ValueError("wallet_path is required")