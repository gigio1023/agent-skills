#!/usr/bin/env python3
"""Regression tests for package linting; no model/service execution."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_skill import validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "sample-skill"
        self.package.mkdir()

    def write(self, frontmatter=None, body="Count the requested widgets."):
        frontmatter = frontmatter or (
            "name: sample-skill\ndescription: Use when counting widgets."
        )
        (self.package / "SKILL.md").write_text(
            f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8"
        )

    def test_minimal_without_gotchas(self):
        self.write()
        self.assertEqual(validate(self.package), ([], []))

    def test_standard_metadata_and_valid_yaml(self):
        self.write("""# A valid YAML comment
name: sample-skill
description: "Use when a \\"quoted\\" word appears."
license: MIT
compatibility: Python 3.10+
metadata:
  author: example
  version: "1.0"
allowed-tools: Read Bash(git:*)
""")
        errors, warnings = validate(self.package)
        self.assertEqual(errors, [])
        self.assertTrue(any("experimental" in w for w in warnings))
        self.write("name: sample-skill\ndescription: 'Use when it''s useful.'")
        self.assertEqual(validate(self.package)[0], [])

    def test_lengths_are_not_byte_limits(self):
        self.write(body="é" * 9000)
        self.assertEqual(validate(self.package), ([], []))
        self.write(body="ordinary line\n" * 501)
        errors, warnings = validate(self.package)
        self.assertEqual(errors, [])
        self.assertTrue(any("advisory" in w for w in warnings))

    def test_field_boundaries(self):
        for length, valid in [(1024, True), (1025, False)]:
            with self.subTest(description_length=length):
                self.write("name: sample-skill\ndescription: " + "é" * length)
                self.assertEqual(not validate(self.package)[0], valid)
        for length, valid in [(500, True), (501, False)]:
            with self.subTest(compatibility_length=length):
                self.write("name: sample-skill\ndescription: Widgets.\ncompatibility: " + "x" * length)
                self.assertEqual(not validate(self.package)[0], valid)

    def test_invalid_metadata(self):
        cases = [
            "name: Other\ndescription: Widgets.",
            "name: other-name\ndescription: Widgets.",
            "name: sample--skill\ndescription: Widgets.",
            "name: sample-skill\nname: sample-skill\ndescription: Widgets.",
            "name: sample-skill\ndescription: null",
            "name: sample-skill\ndescription: true",
            "name: sample-skill\ndescription: 123",
            "name: sample-skill\ndescription: [widgets]",
            "name: sample-skill\ndescription: Use when: invalid",
            "name: sample-skill\ndescription: >\nnot indented",
            "name: sample-skill\ndescription: >\n    first\n  invalid",
            "name: sample-skill\ndescription: *missing",
            'name: sample-skill\ndescription: "invalid \\q"',
            "name: sample-skill\ndescription: 'it's broken'",
            "name: sample-skill\ndescription: Widgets.\nmetadata:\n  version: 1",
            "name: sample-skill\ndescription: Widgets.\nmetadata:\n  x: a\n  x: b",
            "name: sample-skill\ndescription: Widgets.\nlicense: [MIT]",
            "name: sample-skill\ndescription: Widgets.\nallowed-tools: [Read]",
            "name: sample-skill\ndescription: !!python/object/apply:builtins.str [1]",
        ]
        for metadata in cases:
            with self.subTest(metadata=metadata):
                self.write(metadata)
                self.assertTrue(validate(self.package)[0])

    def test_frontmatter_delimiters_and_encoding(self):
        entry = self.package / "SKILL.md"
        for text in ["", "# No metadata", "---\nname: sample-skill"]:
            entry.write_text(text)
            self.assertTrue(validate(self.package)[0])
        entry.write_bytes(b"\xff")
        self.assertTrue(validate(self.package)[0])

    def test_native_fields_are_advisory(self):
        self.write("name: sample-skill\ndescription: Widgets.\ncontext: fork\nhooks: {}")
        errors, warnings = validate(self.package)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 2)

    def test_target_specific_restrictions(self):
        self.write("name: sample-skill\ndescription: 'Use <tag>widgets</tag>.'")
        self.assertEqual(validate(self.package)[0], [])
        self.assertTrue(validate(self.package, "claude-code")[0])
        self.package = self.package.rename(self.package.with_name("claude-helper"))
        self.write("name: claude-helper\ndescription: Widgets.")
        self.assertEqual(validate(self.package)[0], [])
        self.assertTrue(validate(self.package, "claude-code")[0])

    def test_cross_links_and_long_reference(self):
        refs = self.package / "references"
        refs.mkdir()
        self.write(body="Read [first](references/first.md).")
        (refs / "first.md").write_text("[second](second.md)\n" + "detail\n" * 110)
        (refs / "second.md").write_text("[entry](../SKILL.md)")
        errors, warnings = validate(self.package)
        self.assertEqual(errors, [])
        self.assertTrue(any("contents" in w for w in warnings))
        (refs / "second.md").unlink()
        errors, warnings = validate(self.package)
        self.assertEqual(errors, [])
        self.assertTrue(any("missing resource" in w for w in warnings))

    def test_resource_forms(self):
        assets = self.package / "assets"
        assets.mkdir()
        (assets / "my file.txt").write_text("fixture")
        self.write(body='[a](<assets/my file.txt>)\n[b][b]\n[b]: assets/my%20file.txt\n'
                        '[remote](https://example.invalid/not-fetched)\n[anchor](#here)')
        self.assertEqual(validate(self.package)[0], [])
        self.write(body="Use `scripts/missing.py`.")
        errors, warnings = validate(self.package)
        self.assertEqual(errors, [])
        self.assertTrue(any("missing resource" in w for w in warnings))
        self.write(body="[required script](scripts/missing.py)")
        self.assertTrue(validate(self.package)[0])
        self.write(body="Use `scripts/missing.py`; [required](scripts/missing.py).")
        self.assertTrue(validate(self.package)[0])

    def test_code_examples_are_not_real_links(self):
        self.write(body="````markdown\n```text\n[example](missing.md)\n```\n````\n"
                        "`[example](missing.md)`")
        self.assertEqual(validate(self.package)[0], [])

    def test_escape_and_symlink(self):
        self.write(body="[outside](../outside.md)")
        self.assertTrue(any("escapes" in e for e in validate(self.package)[0]))
        self.write()
        outside = self.package.parent / "outside.md"
        outside.write_text("not part of the package")
        (self.package / "linked.md").symlink_to(outside)
        self.assertTrue(any("symlink escapes" in e for e in validate(self.package)[0]))

    def test_warning_is_not_failure(self):
        self.write(body="TODO: inspect this wording.")
        command = ["bash", str(Path(__file__).with_name("validate_skill.sh")), str(self.package)]
        result = subprocess.run(command, capture_output=True, text=True,
                                env={**os.environ, "SKILL_BUILDER_PYTHON": sys.executable})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN:", result.stdout)
        self.assertIn("OK:", result.stdout)

    def test_missing_dependency_has_setup_exit(self):
        result = subprocess.run(
            [sys.executable, "-S", str(Path(__file__).with_name("validate_skill.py"))],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("SETUP:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
