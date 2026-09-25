#!/usr/bin/env python3
"""sync_profile.py rewrites a user's instruction file: text outside the marker block must survive."""
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sync_profile  # noqa: E402

PROFILE = "# Writing Profile\n\nLine one.\n"
NEW_PROFILE = "# Writing Profile\n\nLine one.\nLine two.\n"


class RenderTests(unittest.TestCase):
    def test_text_outside_the_block_survives(self):
        first = sync_profile.render("# Agents\n\nRule.\n", PROFILE) + "\n# After\n\nKept.\n"
        second = sync_profile.render(first, NEW_PROFILE)
        self.assertTrue(second.startswith("# Agents\n\nRule.\n"))
        self.assertTrue(second.endswith("\n# After\n\nKept.\n"))
        self.assertIn("Line two.", second)

    def test_unpaired_markers_rejected(self):
        with self.assertRaises(ValueError):
            sync_profile.render("<!-- writing-profile:start -->\nx\n", PROFILE)


if __name__ == "__main__":
    unittest.main()
