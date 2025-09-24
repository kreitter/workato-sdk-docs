#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed."
  echo "macOS:   brew install uv"
  echo "Docs:    https://docs.astral.sh/uv/"
  exit 1
fi

# Default action: fetch/build docs
uv run python scripts/fetch_workato_docs.py "$@"
