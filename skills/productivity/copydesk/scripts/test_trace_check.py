#!/usr/bin/env python3
"""--strip writes the copy the reader gets: only markers may disappear."""
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
