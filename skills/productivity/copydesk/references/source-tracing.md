# Source Tracing

Use when the user asks for a traced draft or a source-bound rewrite risks adding unsupported mechanisms, criteria, or certainty. An ordinary diff and source comparison are enough for many edits. Tracing is useful when a reader or editor needs to inspect where added context came from.

## Traced draft

Write the draft with a trace marker at the end of every block (paragraph, bullet, table row, caption). The marker names where the block's content came from:

| Marker | Meaning |
|---|---|
| `[src L12-L15]` | Restates lines 12 to 15 of the source; several ranges separated by commas |
| `[src §2.3]` | Restates a section when the source has no usable line numbers |
| `[background]` | General knowledge the source does not state, kept out of the document's premises |
| `[assumption: <what>]` | The writer's own assumption, named |
| `[user: <instruction>]` | Content the user asked for that the source lacks, such as an ordering or a status word |

A block with no marker is untraced. Put reasoning in the text where the reader needs it; a trace marker records its source or assumption without substituting for the explanation. The source's own decision status travels with the marker: a feasibility the source calls unconfirmed stays unconfirmed in the block that cites it.

Run `python3 scripts/trace_check.py <traced.md>`. It lists untraced blocks and counts markers by kind; a document whose `[background]` or `[assumption]` count is high relative to `[src]` is telling the reader that most of it did not come from the source, and the writer decides what to do about that before stripping. The script never passes or fails the document.

## Clean copy

`python3 scripts/trace_check.py <traced.md> --strip <clean.md>` writes the copy the reader sees, with markers removed and nothing else changed. Deliver the clean copy; keep the traced copy beside the source for the user's review and for the next revision. The script removes markers without rewriting surrounding text; inspect the clean copy before delivery.

## Revision

Revise the traced copy and regenerate its clean copy. When changing structure, update markers to follow the claims they support. For a local correction or an explicit verbatim constraint, `python3 scripts/protected_diff.py <previous-clean> <revised-clean> --allow "<corrected heading>"` can locate unintended changes. A broad revision is judged by meaning and the protected passages, not by literal retention of every block. Supply the trace or diff report when requested or when it helps resolve a material editorial question.

## When not to trace

A document written from many sources and the writer's own analysis, a chat answer, a PR body from a diff the reviewer can read, or a document the user edits live in a shared page. Tracing costs one pass; use it where invention has been the failure.
