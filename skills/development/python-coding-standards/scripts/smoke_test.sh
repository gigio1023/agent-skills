#!/usr/bin/env bash
# Exercises verify_doc_only_diff.py on fixed fixtures. Each case commits a base
# file in a fresh repository, overwrites it, and checks the guard's verdict.
# The expected verdicts come from what the tools honor (Ruff, ty, pyrefly,
# coverage, PEP 484), not from the guard's own code.
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
guard="$script_dir/verify_doc_only_diff.py"
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

failures=0

# run_case <name> <expected: pass|fail> <base-file> <current-file>
run_case() {
    local name=$1 expected=$2 base_file=$3 current_file=$4
    local repo="$tmp_dir/$name"
    mkdir -p "$repo"
    git -C "$repo" init -q
    git -C "$repo" config user.name "Smoke Test"
    git -C "$repo" config user.email "smoke@example.invalid"
    cp "$base_file" "$repo/target.py"
    git -C "$repo" add target.py
    git -C "$repo" commit -qm "fixture"
    cp "$current_file" "$repo/target.py"
    local rc=0
    (cd "$repo" && python3 "$guard" --base HEAD target.py >/dev/null 2>"$repo/stderr") || rc=$?
    if [ "$expected" = pass ] && [ "$rc" -ne 0 ]; then
        echo "FAIL: $name expected pass, guard exit $rc: $(cat "$repo/stderr")" >&2
        failures=$((failures + 1))
    elif [ "$expected" = fail ] && [ "$rc" -ne 1 ]; then
        echo "FAIL: $name expected exit 1, guard exit $rc: $(cat "$repo/stderr")" >&2
        failures=$((failures + 1))
    else
        echo "ok: $name ($expected)"
    fi
}

fx="$tmp_dir/fixtures"
mkdir -p "$fx"

# Docstring and rationale comment added: pass.
cat > "$fx/add_base.py" <<'PY'
def add(left: int, right: int) -> int:
    return left + right
PY
cat > "$fx/add_doc.py" <<'PY'
def add(left: int, right: int) -> int:
    """Return the sum of two integers."""

    # Keep arithmetic explicit for callers reading generated source.
    return left + right
PY
run_case docstring_and_comment pass "$fx/add_base.py" "$fx/add_doc.py"

# Executable change hidden behind a docstring edit: fail.
cat > "$fx/add_subtract.py" <<'PY'
def add(left: int, right: int) -> int:
    """Return the difference between two integers."""

    return left - right
PY
run_case executable_change fail "$fx/add_base.py" "$fx/add_subtract.py"

# A noqa code edited in place: fail.
cat > "$fx/noqa_base.py" <<'PY'
unused = 1  # noqa: F841
PY
cat > "$fx/noqa_changed.py" <<'PY'
unused = 1  # noqa: F842
PY
run_case noqa_code_changed fail "$fx/noqa_base.py" "$fx/noqa_changed.py"

# A type-checker suppression replaced by prose: fail (ty and pyrefly forms).
for checker in ty pyrefly; do
    cat > "$fx/${checker}_base.py" <<PY
value: int = "text"  # ${checker}: ignore[invalid-assignment]
PY
    cat > "$fx/${checker}_removed.py" <<'PY'
value: int = "text"  # Fixture value kept for the type-checker test.
PY
    run_case "${checker}_suppression_removed" fail "$fx/${checker}_base.py" "$fx/${checker}_removed.py"
done

# Docstring added above a later "# type: ignore" line: pass. ast.TypeIgnore
# carries its line number as a field, so parsing type comments into the tree
# reported this as an executable change.
cat > "$fx/type_ignore_base.py" <<'PY'
def scale(value: int) -> int:
    return value * 2


result: int = scale("3")  # type: ignore[arg-type]
PY
cat > "$fx/type_ignore_doc.py" <<'PY'
def scale(value: int) -> int:
    """Return ``value`` doubled.

    Callers pass counts, never negative sizes.
    """
    return value * 2


result: int = scale("3")  # type: ignore[arg-type]
PY
run_case docstring_above_type_ignore pass "$fx/type_ignore_base.py" "$fx/type_ignore_doc.py"

# Protocol stub "..." replaced by a docstring: pass; both bodies are empty at runtime.
cat > "$fx/protocol_base.py" <<'PY'
from typing import Protocol


class Sink(Protocol):
    def write(self, data: bytes) -> None: ...
PY
cat > "$fx/protocol_doc.py" <<'PY'
from typing import Protocol


class Sink(Protocol):
    def write(self, data: bytes) -> None:
        """Accept one chunk; implementations must not retain ``data``."""
PY
run_case protocol_stub_docstring pass "$fx/protocol_base.py" "$fx/protocol_doc.py"

# Prose comments that merely start with "Type:" or "Coverage:": pass.
cat > "$fx/prose_base.py" <<'PY'
def parse(raw: str) -> str:
    return raw.strip()
PY
cat > "$fx/prose_capitalized.py" <<'PY'
def parse(raw: str) -> str:
    # Type: RFC 3339 timestamp text; the caller validates the format.
    # Coverage: exercised by the CLI integration run.
    return raw.strip()
PY
run_case capitalized_prose_comments pass "$fx/prose_base.py" "$fx/prose_capitalized.py"

# A lowercase own-line "# type:" comment is a PEP 484 type comment, so adding
# one is reported as a directive change rather than a syntax error.
cat > "$fx/prose_type_comment.py" <<'PY'
def parse(raw: str) -> str:
    # type: plain text, never bytes; the caller decodes first.
    return raw.strip()
PY
run_case lowercase_type_comment_added fail "$fx/prose_base.py" "$fx/prose_type_comment.py"

# A noqa after explanatory prose in the same comment is still honored by Ruff: fail when removed.
cat > "$fx/trailing_noqa_base.py" <<'PY'
import os  # imported for its side effect # noqa: F401
PY
cat > "$fx/trailing_noqa_removed.py" <<'PY'
import os  # imported for its side effect
PY
run_case noqa_after_prose_removed fail "$fx/trailing_noqa_base.py" "$fx/trailing_noqa_removed.py"

# "# flake8: noqa" is a file-level Ruff suppression: fail when replaced.
cat > "$fx/flake8_base.py" <<'PY'
# flake8: noqa
import os
PY
cat > "$fx/flake8_removed.py" <<'PY'
# Module kept for import compatibility.
import os
PY
run_case flake8_noqa_removed fail "$fx/flake8_base.py" "$fx/flake8_removed.py"

# coverage.py pragma variants: fail when removed.
cat > "$fx/pragma_base.py" <<'PY'
def check(flag: bool) -> int:
    if flag:  # pragma: no branch
        return 1
    return 0  # pragma: nocover
PY
cat > "$fx/pragma_removed.py" <<'PY'
def check(flag: bool) -> int:
    if flag:  # flag is always set by the CLI
        return 1
    return 0  # unreachable from the CLI
PY
run_case pragma_variants_removed fail "$fx/pragma_base.py" "$fx/pragma_removed.py"

if [ "$failures" -ne 0 ]; then
    echo "$failures smoke test case(s) failed" >&2
    exit 1
fi
echo "OK: doc-only diff guard smoke tests passed"
