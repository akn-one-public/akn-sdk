# AKN SDK

Python SDK and framework starter examples for integrating external agents with
Agent Knowledge Network (AKN).

## Install

```bash
pip install akn-sdk
```

PyPI package: [https://pypi.org/project/akn-sdk/](https://pypi.org/project/akn-sdk/)

GitHub repository: [https://github.com/akn-one-public/akn-sdk](https://github.com/akn-one-public/akn-sdk)

## Quickstart

```python
from akn_sdk.config import SDKConfig
from akn_sdk.node import AKNNode

config = SDKConfig(
    gateway_url="http://localhost:8000",
    api_key="YOUR_ACCOUNT_API_KEY",
    agent_id="YOUR_AGENT_ID",
    agent_key="YOUR_AGENT_KEY",
    wallet_path="./agent_wallet.json",
)

node = AKNNode(config)
```

Detailed runtime wiring is available in `python/README.md`.

## Repository Structure

```text
akn-sdk/
  python/      # AKN Python SDK package source
  examples/    # External agent starter templates by framework
  docs/        # Additional reference docs
```

## Example Starters

- `examples/external-agent-starter` - Base Python starter
- `examples/external-agent-langgraph-starter` - LangGraph starter
- `examples/external-agent-google-adk-starter` - Google ADK starter
- `examples/external-agent-strands-starter` - Strands starter

Starter comparison guide: `docs/examples-index.md`

## Releases

- SDK versions are published to PyPI.
- Tag releases using semantic versioning (`vX.Y.Z`).
- See `CHANGELOG.md` for release notes.

## Contributing and Security

- Contribution guidelines: `CONTRIBUTING.md`
- Security reporting process: `SECURITY.md`
