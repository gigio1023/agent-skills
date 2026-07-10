---
name: pdf-page-count
description: >
  Use when the user asks for the page count of an existing PDF, whether a PDF
  meets an exact/minimum/maximum page limit, or the numeric page-count result
  for another workflow. Triggers on "PDF pages", "page count", "몇 페이지",
  and "분량 제한 확인". NOT for creating, editing, rendering, or visually
  reviewing a PDF; use the PDF skill for those tasks.
---

# PDF Page Count

Return the PDF's numeric page count and, when a limit was supplied, an explicit
pass/fail comparison. Do not edit or rebuild the document unless the user also
requested that separate work.

## Quick Start

1. Resolve the exact PDF path and confirm the file exists.
2. Run the bundled counter from this skill directory:

   ```bash
   python3 scripts/count_pdf_pages.py <path-to-pdf>
   ```

3. Treat exit code `0` plus a single integer on stdout as success. Exit code `2`
   means none of the available backends could determine the count; report the
   dependency/error message instead of guessing.
4. Compare the integer to the user's rule:
   - maximum `N`: pass when `count <= N`;
   - minimum `N`: pass when `count >= N`;
   - exact `N`: pass when `count == N`.

## Output Contract

Report the file, page count, limit if any, and result. When over or under the
limit, include the exact difference. Example: `27 pages; maximum 25; fail by 2
pages.` Keep any requested caveat or next action, but omit backend narration on
success.

If another task changed the source document, count the rebuilt output PDF, not
the stale pre-edit artifact. If no rebuilt PDF exists, state that the count is
for the currently supplied file.

## Gotchas

- Do not infer pages from filename, file size, source-document pagination, or a
  viewer thumbnail count.
- Encrypted or malformed PDFs may fail every backend. Surface the failure; do
  not report zero pages.
- The script tries `pypdf`, `PyPDF2`, `pdfinfo`, then macOS `mdls`. If no backend
  works, install `pypdf` or provide `pdfinfo` rather than rewriting the script
  during the counting task.
- A request to check a limit does not authorize layout compression or content
  cuts. Offer or perform PDF editing only when asked.
