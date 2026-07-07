#!/usr/bin/env bash
# Unix wrapper for the cross-platform Python entrypoint.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${PYTHON:-}" ]]; then
  PYTHON_BIN="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "python not found" >&2
  exit 3
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/gen.py" "$@"
