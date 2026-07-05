---
name: pdf-page-count
description: Count pages in a PDF and verify page limits. Use when asked to check PDF page count or enforce a target page count.
metadata:
  short-description: Count PDF pages and validate page limits
---

# PDF Page Count

Use this skill when you need to check a PDF’s page count and validate it against a target.

## Quick start

1) Run the bundled script to count pages:

```
python3 <skill-dir>/scripts/count_pdf_pages.py <path-to-pdf>
```

2) If the count exceeds the target, shorten content or reduce spacing, then rebuild the PDF.

## Notes

- Prefer content cuts over layout tricks unless the user explicitly wants layout adjustments.
- If a source document was edited, rebuild the output PDF before counting pages.
