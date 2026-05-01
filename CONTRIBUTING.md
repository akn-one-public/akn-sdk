# Contributing to AKN SDK

Thanks for your interest in improving AKN SDK.

## Development Setup

1. Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install SDK in editable mode:

```bash
pip install -e ./python
```

3. Run an example starter:

```bash
cd examples/external-agent-starter
pip install -r requirements.txt
python3 main.py
```

## Pull Request Guidelines

- Keep changes focused and minimal.
- Update documentation for public-facing behavior changes.
- Avoid including secrets, private URLs, or environment credentials.
- Include clear PR titles and context about the change impact.

## Versioning

- Use semantic versioning for SDK releases.
- Update `python/pyproject.toml` version and `CHANGELOG.md` in the same PR.
