#!/usr/bin/env python3
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import trace_check  # noqa: E402

DOC = """# Title

First paragraph restating the source. [src L1-L4]

Second paragraph with nothing.

- item one [src §2]
- item two [background]
- item three

| a | b |
|---|---|
| 1 | 2 | [src L9]
| 3 | 4 |

```
code [src L99]
```

Last line. [assumption: the run used defaults]
"""


class AnalyzeTests(unittest.TestCase):
    def test_untraced_and_counts(self):
        untraced, counts = trace_check.analyze(DOC)
        heads = [h for _, h in untraced]
        self.assertEqual(len(untraced), 3, heads)
        self.assertTrue(any(h.startswith("Second paragraph") for h in heads))
        self.assertTrue(any(h.startswith("- item three") for h in heads))
        self.assertTrue(any(h.startswith("| 3 | 4 |") for h in heads))
        self.assertEqual(counts, {"src": 3, "background": 1, "assumption": 1, "user": 0})

    def test_code_and_headings_ignored(self):
        untraced, _ = trace_check.analyze("# H\n\n```\nplain\n```\n")
        self.assertEqual(untraced, [])


class StripTests(unittest.TestCase):
    def test_strip_removes_only_markers(self):
        clean = trace_check.strip(DOC)
        outside_code = clean.replace("code [src L99]", "")
        self.assertNotIn("[src", outside_code)
        self.assertNotIn("[background]", outside_code)
        self.assertNotIn("[assumption", outside_code)
        self.assertIn("First paragraph restating the source.", clean)
        self.assertIn("code [src L99]", clean)  # code fences are untouched
        self.assertIn("| 1 | 2 |", clean)
        self.assertEqual(clean.count("\n"), DOC.count("\n"))


if __name__ == "__main__":
    unittest.main()
