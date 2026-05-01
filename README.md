# AKN SDK (Public Repo Staging)

This folder defines the intended public repository structure for `akn-sdk`.

## Public Repo Goals

- Provide installable Python SDK (`pip install akn-sdk`)
- Provide framework-specific external agent starters
- Keep docs production-quality and public-safe

## Suggested Public Repository Layout

```text
akn-sdk/
  python/
    pyproject.toml
    README.md
    scripts/
    akn_sdk/
  examples/
    external-agent-starter/
    external-agent-langgraph-starter/
    external-agent-google-adk-starter/
    external-agent-strands-starter/
  docs/
    examples-index.md
  CHANGELOG.md
  LICENSE
```

## Source Mapping (Current Monorepo)

- SDK source: `sdk/python`
- Example starters: `website/examples`
- Docs references: `website/frontend/src/pages`

## Staging Sync Script

Use `sync_from_monorepo.sh` to populate this staging area with latest SDK and
starter example content before uploading to public GitHub:

```bash
cd akn-github/akn-sdk
bash sync_from_monorepo.sh
```

## Release Checklist

1. Ensure `python/pyproject.toml` version is bumped.
2. Build and validate package in virtual environment:
   - `python -m build`
   - `python -m twine check dist/*`
3. Upload to TestPyPI, validate install.
4. Upload to PyPI.
