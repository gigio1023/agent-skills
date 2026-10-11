"""The changed, added, and retention numbers of protected_diff.py are reported in harness results
(docs/writing-consolidation/harness/auto_measures.py); each expected value is a hand count."""

from __future__ import annotations

import unittest

from protected_diff import build_report


class TestProtectedDiff(unittest.TestCase):
    def setUp(self) -> None:
        self.previous = (
            "# Title\n"
            "\n"
            "Intro paragraph that must survive any revision untouched.\n"
            "\n"
            "## Results\n"
            "\n"
            "The results paragraph will be corrected in this revision.\n"
            "\n"
            "## Appendix\n"
            "\n"
            "Appendix content that is allowed to change freely.\n"
        )

    def test_edited_protected_block_is_reported_as_changed(self) -> None:
        revised = self.previous.replace(
            "The results paragraph will be corrected in this revision.",
            "The results paragraph has now been corrected with new numbers.",
        )
        report = build_report(self.previous, revised, [], [])
        self.assertIn("CHANGED OUTSIDE ALLOWED SCOPE (1)", report)

    def test_allowed_scope_edit_is_not_reported_as_changed_or_added(self) -> None:
        revised = self.previous.replace(
            "Appendix content that is allowed to change freely.",
            "Appendix content is now completely different and rewritten.",
        )
        report = build_report(self.previous, revised, ["Appendix"], [])
        self.assertIn("CHANGED OUTSIDE ALLOWED SCOPE (0)", report)
        self.assertIn("ADDED OUTSIDE ALLOWED SCOPE (0)", report)

    def test_added_block_outside_scope_is_reported(self) -> None:
        # Appending a heading plus a paragraph adds two new blocks, both outside any allowed scope.
        revised = self.previous + "\n## New Section\n\nA brand new block outside any scope.\n"
        report = build_report(self.previous, revised, [], [])
        self.assertIn("ADDED OUTSIDE ALLOWED SCOPE (2)", report)

    def test_summary_reports_retention_ratio(self) -> None:
        report = build_report(self.previous, self.previous, [], [])
        self.assertIn("retention ratio of protected blocks: 1.00", report)


if __name__ == "__main__":
    unittest.main()
