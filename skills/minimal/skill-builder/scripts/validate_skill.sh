#!/usr/bin/env bash
# Compatibility entry point. No implicit dependency installation.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${SKILL_BUILDER_PYTHON:-python3}"
if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "SETUP: Python 3.10+ is required; select it with SKILL_BUILDER_PYTHON." >&2
  exit 2
fi
exec "$python_bin" "$here/validate_skill.py" "$@"
