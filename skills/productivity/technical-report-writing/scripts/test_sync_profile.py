#!/usr/bin/env python3
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sync_profile  # noqa: E402

PROFILE = "# Writing Profile\n\nLine one.\n"
NEW_PROFILE = "# Writing Profile\n\nLine one.\nLine two.\n"


class RenderTests(unittest.TestCase):
    def test_appends_block_when_markers_missing(self):
        out = sync_profile.render("# Agents\n\nRule.\n", PROFILE)
        self.assertTrue(out.startswith("# Agents\n\nRule.\n\n<!-- writing-profile:start -->\n"))
        self.assertTrue(out.endswith("Line one.\n<!-- writing-profile:end -->\n"))

    def test_replaces_only_the_block(self):
        first = sync_profile.render("# Agents\n\nRule.\n", PROFILE) + "\n# After\n\nKept.\n"
        second = sync_profile.render(first, NEW_PROFILE)
        self.assertIn("Line two.\n<!-- writing-profile:end -->\n\n# After\n\nKept.\n", second)
        self.assertEqual(second.count(sync_profile.START), 1)
        self.assertNotIn("Line one.\n<!-- writing-profile:end", second)

    def test_idempotent(self):
        once = sync_profile.render("", PROFILE)
        self.assertEqual(sync_profile.render(once, PROFILE), once)

    def test_unpaired_markers_rejected(self):
        with self.assertRaises(ValueError):
            sync_profile.render("<!-- writing-profile:start -->\nx\n", PROFILE)


class CliTests(unittest.TestCase):
    def test_check_reports_drift_then_update_fixes_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = pathlib.Path(tmp, "profile.md")
            src.write_text(PROFILE)
            target = pathlib.Path(tmp, "AGENTS.md")
            target.write_text("# Agents\n")
            cmd = [sys.executable, str(HERE / "sync_profile.py"), str(target), "--source", str(src)]
            self.assertEqual(subprocess.run(cmd + ["--check"], capture_output=True).returncode, 1)
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(cmd + ["--check"], capture_output=True).returncode, 0)
            self.assertIn("Line one.", target.read_text())


if __name__ == "__main__":
    unittest.main()
