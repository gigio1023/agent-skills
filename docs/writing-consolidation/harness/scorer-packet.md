# Scoring mission

## Objective
Score the documents in this workspace against `rubric.md` without knowing which writing-skill version produced each one. Done when `scores.md` exists with one table per arm and a three-sentence comparison.

## Inputs
- `rubric.md`: the items to count. Use the correction-tracking items a–h for Task 1 and the PR-table judgment for Task 2.
- `source-report.md`: the source the documents were written from. Item (d) counts only facts, names, numbers, causal claims, and mechanism absent from this file.
- `arms/<label>/`: one directory per arm, labeled with neutral letters. Each holds draft.md, r1.md, r2.md, r3.md, pr-body.md, pr-body-r1.md.
- `corrections.md`: the three correction requests, so you can judge scope (item h) and the kept section (item f).

## Method
1. Read `source-report.md` once before any document.
2. For each arm and each of draft, r1, r2, r3: count items a–e and g per document, quoting each counted sentence. For f, state whether the kept section is byte-identical, partly lost, or lost, and list what was lost. For h, count blocks changed outside the correction's scope in r2 and r3.
3. Count (b) only for sentences that record the author's diligence; a condition that changes how a number is read, or a distinction between observation and inference, is not (b).
4. Score the PR tables: rows are real comparisons, no constant column, cells short, figure against the real base. Rate 상/중/하 with one reason.
5. Write `scores.md`: one table per arm (item | draft | r1 | r2 | r3 | quotations), then three sentences comparing the arms on the items where they differ most.

## Scope and authority
Read-only outside `scores.md`. No network. Do not guess which arm is which, and do not reward or penalize length. Same standard for every arm; if you change how you count midway, recount the earlier arms.

## Response contract
Final response: the path of `scores.md` and the three comparison sentences. Nothing else.
