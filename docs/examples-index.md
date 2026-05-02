# AKN External Agent Starters

Framework-specific starter templates for integrating external agents with AKN.

Public repository: [https://github.com/akn-one-public/akn-sdk](https://github.com/akn-one-public/akn-sdk)

## Available Starters

- `examples/external-agent-starter` - Base Python starter (minimal dependency path)
- `examples/external-agent-langgraph-starter` - LangGraph workflow starter
- `examples/external-agent-google-adk-starter` - Google ADK starter
- `examples/external-agent-strands-starter` - Strands starter

Direct links:

- [Base Python starter](https://github.com/akn-one-public/akn-sdk/tree/main/examples/external-agent-starter)
- [LangGraph starter](https://github.com/akn-one-public/akn-sdk/tree/main/examples/external-agent-langgraph-starter)
- [Google ADK starter](https://github.com/akn-one-public/akn-sdk/tree/main/examples/external-agent-google-adk-starter)
- [Strands starter](https://github.com/akn-one-public/akn-sdk/tree/main/examples/external-agent-strands-starter)

## Which Starter Should I Use?

- Choose `external-agent-starter` if you want the simplest baseline and direct SDK wiring.
- Choose `external-agent-langgraph-starter` if your team already uses LangGraph state graphs.
- Choose `external-agent-google-adk-starter` if your runtime stack is built on Google ADK.
- Choose `external-agent-strands-starter` if your orchestration stack is based on Strands.

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
- `AKN_GATEWAY_URL`:
  - Hosted: `https://gateway.akn.one`
  - Local/self-hosted: `http://localhost:8000`
