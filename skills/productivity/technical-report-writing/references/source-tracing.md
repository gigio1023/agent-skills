# Source Tracing

Read this when a document is rewritten from one source (a report, a transcript, a diff, a paper), or when the user asks for a traced draft. Blind comparisons of writer versions (docs/writing-consolidation/harness) left one weakness that rules did not remove: drafts add mechanism from general knowledge, firm an unconfirmed feasibility into a fact, or attach a selection criterion the source never stated. Tracing makes each sentence's origin visible before the reader sees the clean copy.

## Traced draft

Write the draft with a trace marker at the end of every block (paragraph, bullet, table row, caption). The marker names where the block's content came from:

| Marker | Meaning |
|---|---|
| `[src L12-L15]` | Restates lines 12 to 15 of the source; several ranges separated by commas |
| `[src §2.3]` | Restates a section when the source has no usable line numbers |
| `[background]` | General knowledge the source does not state, kept out of the document's premises |
| `[assumption: <what>]` | The writer's own assumption, named |
| `[user: <instruction>]` | Content the user asked for that the source lacks, such as an ordering or a status word |

A block with no marker is untraced. A marker never carries a reason or an argument; if the block needs one, the block is wrong, not the marker. The source's own decision status travels with the marker: a feasibility the source calls unconfirmed stays unconfirmed in the block that cites it.

Run `python3 scripts/trace_check.py <traced.md>`. It lists untraced blocks and counts markers by kind; a document whose `[background]` or `[assumption]` count is high relative to `[src]` is telling the reader that most of it did not come from the source, and the writer decides what to do about that before stripping. The script never passes or fails the document.

## Clean copy

`python3 scripts/trace_check.py <traced.md> --strip <clean.md>` writes the copy the reader sees, with markers removed and nothing else changed. Deliver the clean copy; keep the traced copy beside the source for the user's review and for the next revision. Never hand-strip: the two copies must differ only in markers.

## Revision

A revision of a traced document edits the traced copy, keeps every untouched block byte-identical marker included, and strips again. Together with `python3 scripts/protected_diff.py <previous-clean> <revised-clean> --allow "<corrected heading>"`, the user can see both what moved and where each moved sentence came from. Attach the protected_diff summary to the delivery of a revision when the user asked for it or when the revision touched more than the named scope.

## When not to trace

A document written from many sources and the writer's own analysis, a chat answer, a PR body from a diff the reviewer can read, or a document the user edits live in a shared page. Tracing costs one pass; use it where invention has been the failure.
