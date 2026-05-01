# Maintainer Content Checklist

This checklist helps maintainers keep the public `akn-sdk` repository aligned
with the source monorepo.

## 1) Python SDK Package

Copy the full `sdk/python` folder contents:

- `pyproject.toml`
- `README.md`
- `scripts/release_pypi.sh`
- `akn_sdk/**`

Do not publish transient build artifacts:

- `build/`
- `dist/`
- `*.egg-info/`
- `.venv/`

## 2) External Agent Starters

Copy these starter folders from `website/examples`:

- `external-agent-starter`
- `external-agent-langgraph-starter`
- `external-agent-google-adk-starter`
- `external-agent-strands-starter`

Each starter should include:

- `README.md`
- `main.py`
- `env.example`
- `requirements.txt`

## 3) Public Docs

Include a short examples index doc in public repo docs:

- starter purpose
- who should use each starter
- quickstart commands
- SDK install from PyPI

## 4) Security Review Before Publish

- Remove any private/internal URLs.
- Remove personal access tokens and credentials.
- Confirm only public-safe contact/support links.

## 5) Public Repo Metadata

In GitHub repository settings, configure:

- Description: `Python SDK and framework starter examples for Agent Knowledge Network (AKN).`
- Website: `https://akn.one/docs/v1`
- Topics: `python`, `sdk`, `agent-framework`, `langgraph`, `google-adk`, `strands`, `ai`
