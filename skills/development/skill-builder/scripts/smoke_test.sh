#!/usr/bin/env bash
# Run local validator regression tests and validate this package.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${SKILL_BUILDER_PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1
"$python_bin" "$here/test_validate_skill.py"
bash "$here/validate_skill.sh" "$(cd "$here/.." && pwd)"
