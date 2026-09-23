"""Unit tests for protected_diff.py: an edited protected block must be caught, an
untouched one must stay quiet, and an edit inside an allowed scope must be waved through."""

from __future__ import annotations

import unittest

from protected_diff import build_report, split_blocks


class TestBlockSplitting(unittest.TestCase):
    def test_fenced_code_with_blank_line_is_one_block(self) -> None:
        text = "```\nline one\n\nline two\n```\n"
        blocks = split_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].kind, "code")

    def test_table_rows_stay_one_block(self) -> None:
        text = "| a | b |\n| --- | --- |\n| 1 | 2 |\n"
        blocks = split_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].kind, "table")


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
        self.assertIn("The results paragraph will be corrected", report)

    def test_untouched_protected_block_is_not_reported(self) -> None:
        revised = self.previous.replace(
            "The results paragraph will be corrected in this revision.",
            "The results paragraph has now been corrected with new numbers.",
        )
        report = build_report(self.previous, revised, [], [])
        self.assertNotIn("Intro paragraph that must survive", report)

    def test_allowed_scope_edit_is_not_reported_as_changed_or_added(self) -> None:
        revised = self.previous.replace(
            "Appendix content that is allowed to change freely.",
            "Appendix content is now completely different and rewritten.",
        )
        report = build_report(self.previous, revised, ["Appendix"], [])
        self.assertIn("CHANGED OUTSIDE ALLOWED SCOPE (0)", report)
        self.assertIn("ADDED OUTSIDE ALLOWED SCOPE (0)", report)

    def test_allow_lines_covers_an_edit_by_line_range(self) -> None:
        revised = self.previous.replace(
            "The results paragraph will be corrected in this revision.",
            "The results paragraph has now been corrected with new numbers.",
        )
        # line 7 in `previous` is the Results paragraph.
        report = build_report(self.previous, revised, [], [(6, 8)])
        self.assertIn("CHANGED OUTSIDE ALLOWED SCOPE (0)", report)

    def test_added_block_outside_scope_is_reported(self) -> None:
        # Appending a heading plus a paragraph adds two new blocks, both outside any allowed scope.
        revised = self.previous + "\n## New Section\n\nA brand new block outside any scope.\n"
        report = build_report(self.previous, revised, [], [])
        self.assertIn("ADDED OUTSIDE ALLOWED SCOPE (2)", report)
        self.assertIn("A brand new block outside any scope.", report)

    def test_removed_categories_counts_by_kind(self) -> None:
        revised = self.previous.replace("## Appendix\n\nAppendix content that is allowed to change freely.\n", "")
        report = build_report(self.previous, revised, [], [])
        self.assertIn("heading: 1", report)
        self.assertIn("prose: 1", report)

    def test_summary_reports_retention_ratio(self) -> None:
        report = build_report(self.previous, self.previous, [], [])
        self.assertIn("retention ratio of protected blocks: 1.00", report)


class TestMainExitsZero(unittest.TestCase):
    def test_cli_runs_and_exits_zero(self) -> None:
        import io
        from contextlib import redirect_stdout

        import protected_diff

        with open("/tmp/_pd_prev.md", "w", encoding="utf-8") as f:
            f.write("Paragraph one.\n\nParagraph two.\n")
        with open("/tmp/_pd_rev.md", "w", encoding="utf-8") as f:
            f.write("Paragraph one edited.\n\nParagraph two.\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = protected_diff.main(["/tmp/_pd_prev.md", "/tmp/_pd_rev.md"])
        self.assertEqual(exit_code, 0)
        self.assertIn("SUMMARY", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
