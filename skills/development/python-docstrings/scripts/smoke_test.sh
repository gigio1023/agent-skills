#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
guard="$script_dir/verify_doc_only_diff.py"
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

git -C "$tmp_dir" init -q
git -C "$tmp_dir" config user.name "Smoke Test"
git -C "$tmp_dir" config user.email "smoke@example.invalid"

cat > "$tmp_dir/sample.py" <<'PY'
def add(left: int, right: int) -> int:
    return left + right
PY

cat > "$tmp_dir/directive.py" <<'PY'
unused = 1  # noqa: F841
PY

git -C "$tmp_dir" add sample.py directive.py
git -C "$tmp_dir" commit -qm "fixture"

cat > "$tmp_dir/sample.py" <<'PY'
def add(left: int, right: int) -> int:
    """Return the sum of two integers."""

    # Keep arithmetic explicit for callers reading generated source.
    return left + right
PY

(
    cd "$tmp_dir"
    python3 "$guard" --base HEAD sample.py
)

cat > "$tmp_dir/sample.py" <<'PY'
def add(left: int, right: int) -> int:
    """Return the difference between two integers."""

    return left - right
PY

if (
    cd "$tmp_dir"
    python3 "$guard" --base HEAD sample.py >/dev/null 2>&1
); then
    echo "expected executable change to fail" >&2
    exit 1
fi

cat > "$tmp_dir/directive.py" <<'PY'
unused = 1  # noqa: F842
PY

if (
    cd "$tmp_dir"
    python3 "$guard" --base HEAD directive.py >/dev/null 2>&1
); then
    echo "expected semantic directive change to fail" >&2
    exit 1
fi

echo "OK: doc-only diff guard smoke tests passed"
