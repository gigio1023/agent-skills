#!/usr/bin/env python3
"""journal.py must only append: a second entry never rewrites earlier bytes. Run: python3 scripts/test_journal.py"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "journal.py"


def run(*args: str) -> int:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True).returncode


def test_append_is_append_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        j = Path(tmp) / "journal.md"
        assert run("--path", str(j), "append", "--kind", "idea", "--title", "Problem A", "--field", "why=x") == 0
        first = j.read_bytes()
        assert run("--path", str(j), "append", "--kind", "prediction", "--title", "Proj", "--field", "decision=continue") == 0
        after = j.read_bytes()
        assert after.startswith(first), "earlier bytes were rewritten"
        assert b"Proj" in after[len(first):], "second entry was not appended"


if __name__ == "__main__":
    test_append_is_append_only()
    print("ok  test_append_is_append_only")
