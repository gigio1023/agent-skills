# Deep Interview Evaluation

- Date: 2026-07-10
- Model: GPT-5.6 Sol
- Harness: Codex CLI 0.144.0, ephemeral, read-only
- Effort: low

The baseline and candidate used identical user prompts. Candidate runs received
only the proposed `SKILL.md` as additional instructions.

## First-Turn Comparisons

| Case | Baseline | Candidate | Result |
| --- | --- | --- | --- |
| Sparse expense-tracker idea | Asked five questions in one numbered batch | Asked one root-problem question with four mutually exclusive frames | Clear improvement |
| Rich notes with settled constraints | Preserved the constraints but asked twelve questions at once | Produced an eight-item context-first synthesis and asked one correction question | Clear improvement |

Representative baseline failure: the sparse case opened with questions numbered
`1` through `5`; the rich case opened with questions numbered `1` through `12`.
The candidate obeyed the one-question contract in both cases and did not begin
implementation.

## Trigger Boundary

The candidate classified both near-miss requests correctly:

- mock behavioral job interview: `DO_NOT_ACTIVATE`;
- summarize into a spec without questions: `DO_NOT_ACTIVATE`.

## Structural Checks

- portable frontmatter and referenced-path validation: pass;
- package discovery with `npx skills add . --list`: pass;
- discovered skill count: 20;
- `deep-interview` appears as an installable skill.

The brownfield and early-stop cases remain in the reusable evaluation suite for
future multi-turn or repository-fixture regression runs.
