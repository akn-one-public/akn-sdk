# akn_sdk/identity/wallet.py

import json
import os
from pathlib import Path
from .key_manager import KeyManager


class Wallet:
    """
    Deterministic Agent Wallet

    - Always synced with provided agent_key
    - Overwrites stale key
    - Never auto-generates keys
    """

    def __init__(self, path: str):
        self.path = Path(os.path.expanduser(path))

    def load_or_sync(self, agent_key: str) -> KeyManager:
        """
        Ensure wallet file matches provided agent_key.
        """

        self.path.parent.mkdir(parents=True, exist_ok=True)

        if self.path.exists():
            with open(self.path, "r") as f:
                data = json.load(f)

            existing_key = data.get("agent_key")

            # Overwrite if mismatch
            if existing_key != agent_key:
                with open(self.path, "w") as f:
                    json.dump({"agent_key": agent_key}, f, indent=2)
        else:
            # Create new wallet file
            with open(self.path, "w") as f:
                json.dump({"agent_key": agent_key}, f, indent=2)

        return KeyManager(agent_key)