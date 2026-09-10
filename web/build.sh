#!/usr/bin/env bash
# Builds the dbz package as a wheel that web/worker.js installs via micropip.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m build --wheel -o web/dist .
