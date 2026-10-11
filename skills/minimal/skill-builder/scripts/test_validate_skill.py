#!/usr/bin/env python3
"""Auditing an untrusted package must never construct arbitrary Python objects from its YAML."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from validate_skill import validate


class ValidatorTests(unittest.TestCase):
    def test_python_yaml_tag_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "sample-skill"
            package.mkdir()
            (package / "SKILL.md").write_text(
                "---\nname: sample-skill\n"
                "description: !!python/object/apply:builtins.str [1]\n---\n\nBody.\n",
                encoding="utf-8",
            )
            self.assertTrue(validate(package)[0])


if __name__ == "__main__":
    unittest.main()
