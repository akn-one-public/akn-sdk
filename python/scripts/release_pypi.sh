#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/release_pypi.sh test
#   ./scripts/release_pypi.sh prod
#
# Required environment variable:
#   PYPI_TOKEN (token for TestPyPI or PyPI)

TARGET="${1:-test}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${PYPI_TOKEN:-}" ]]; then
  echo "PYPI_TOKEN is required."
  exit 1
fi

cd "$ROOT_DIR"

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build twine

rm -rf dist build ./*.egg-info
python3 -m build
python3 -m twine check dist/*

if [[ "$TARGET" == "test" ]]; then
  python3 -m twine upload \
    --repository testpypi \
    --username __token__ \
    --password "$PYPI_TOKEN" \
    dist/*
  echo "Uploaded to TestPyPI."
elif [[ "$TARGET" == "prod" ]]; then
  python3 -m twine upload \
    --username __token__ \
    --password "$PYPI_TOKEN" \
    dist/*
  echo "Uploaded to PyPI."
else
  echo "Unknown target: $TARGET (use 'test' or 'prod')"
  exit 1
fi
