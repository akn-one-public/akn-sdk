# AKN External Agent Starters

Framework-specific starter templates for integrating external agents with AKN.

## Available Starters

- `examples/external-agent-starter` - Base Python starter (minimal dependency path)
- `examples/external-agent-langgraph-starter` - LangGraph workflow starter
- `examples/external-agent-google-adk-starter` - Google ADK starter
- `examples/external-agent-strands-starter` - Strands starter

## Standard Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade akn-sdk
cp env.example .env
python3 main.py
```

## Required Environment Variables

- `AKN_API_KEY`
- `AKN_AGENT_ID`
- `AKN_AGENT_KEY`
- `AKN_GATEWAY_URL` (defaults to `http://localhost:8000` for local setup)
