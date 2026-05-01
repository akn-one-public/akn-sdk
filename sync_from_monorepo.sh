#!/usr/bin/env bash
set -euo pipefail

# Sync public-safe SDK content from monorepo into this staging folder.
# Run from: akn-github/akn-sdk

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SDK_SRC="$ROOT_DIR/sdk/python"
EXAMPLES_SRC="$ROOT_DIR/website/examples"
DEST_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$DEST_DIR/python"
mkdir -p "$DEST_DIR/examples"

rsync -av --delete \
  --exclude 'dist/' \
  --exclude 'build/' \
  --exclude '*.egg-info/' \
  --exclude '.venv/' \
  "$SDK_SRC/" "$DEST_DIR/python/"

for starter in \
  external-agent-starter \
  external-agent-langgraph-starter \
  external-agent-google-adk-starter \
  external-agent-strands-starter
do
  mkdir -p "$DEST_DIR/examples/$starter"
  rsync -av --delete "$EXAMPLES_SRC/$starter/" "$DEST_DIR/examples/$starter/"
done

echo "Sync complete."
echo "Staged SDK path: $DEST_DIR/python"
echo "Staged examples path: $DEST_DIR/examples"
