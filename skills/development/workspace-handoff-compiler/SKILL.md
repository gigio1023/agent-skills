---
name: workspace-handoff-compiler
description: >-
  Use when a work session is ending and a successor AI must continue it, or when
  someone asks for a handoff, context pack, session handoff, or to "continue across
  sessions" / "인계" / "이어서 작업" / "다음 AI에게 넘겨줘". Compiles prior plan/work/result
  artifacts into a `handoff.md` and a `context-pack.json` with source-priority conflict
  resolution and evidence-based status. NOT for producing plan.md/progress.md/result.md
  during active delivery (use workspace-delivery-orchestrator).
---

# Workspace Handoff Compiler

Compile whatever a prior session produced into two successor-facing artifacts: a human-readable `handoff.md` and a machine-readable `context-pack.json`. Status is evidence-based: never claim more than the proof supports.

## Workflow

1. Gather available artifacts for plan, execution, validation, and outcomes. Optionally index them with `scripts/build_handoff_index.py` (see Tooling).
2. Apply source precedence and conflict handling from `references/handoff-source-priority.md`.
3. Evaluate completion confidence with `references/handoff-quality-gate.md`.
4. Decide continuation mode with `references/continuation-mode.md`.
5. Generate outputs:
   - `handoff.md` for human continuation, starting from `assets/templates/handoff.template.md`.
   - `context-pack.json` following `references/context-pack-schema.md`, starting from `assets/templates/context-pack.template.json`.
6. Keep facts, inferences, and unknowns separate in both outputs.
7. Do not claim `complete` without required evidence. If evidence is missing or conflicting, degrade to `partial` or `blocked` and list the missing proof.
8. Validate before publishing (see Tooling). Both files must pass single-file checks AND the cross-file parity check.

## Status Vocabulary

There is one closed status set, defined in `references/context-pack-schema.md` (Status Vocabulary). Do not re-list or invent values here:

- Per-task / objective rows: `not_started | in_progress | blocked | done`.
- Overall handoff: `complete | partial | blocked`.

Both `handoff.md` and `context-pack.json` MUST use the same overall status value.

## Output Requirements

- `handoff.md` includes:
  - objective, completed work, remaining work, blockers, risks, and first next actions.
  - an evidence reference for every completion claim.
  - a continuation plan with the `continuation_mode` value (see below).
- `context-pack.json` includes:
  - normalized machine-readable state and dependency graph.
  - ownership, constraints, and verification status.
  - the same overall status as `handoff.md`.

## Continuation Mode

`continuation_mode` is a runtime-agnostic recommendation about the SHAPE of remaining work, not a hard requirement to spawn anything. Values: `parallel_recommended` and `sequential_sufficient`. Full judgment rule and the sequential fallback live in `references/continuation-mode.md`.

Parallelism is a universal judgment call, not a harness-specific MUST: when work splits into independent streams that benefit from parallelism, use the harness's parallel-execution capability aggressively; when a single linear session is more effective, do that. Always probe for a native parallel-execution capability first (illustrative examples: Claude Code workflows or subagents, Codex threads). If none exists, run sequentially and say so in the handoff.

When the work is multi-track (more than one independent stream, owner, or repository), record the role map and write-ownership boundaries so the successor can split safely. Single-track work may leave those empty.

## Gotchas

Behavioral pitfalls to avoid when compiling. These are stack-neutral.

- Claiming `complete` without evidence. A status is only as strong as its proof. If there is no command output, test log, or repository diff backing a completion, downgrade to `partial` or `blocked` and enumerate the missing proof. The parity check fails a completed claim that has no passing verification entry.
- Copying conflicting source artifacts verbatim. When `plan.md`, `progress.md`, and `result.md` disagree, do not paste all versions and let the successor sort it out. Resolve with `references/handoff-source-priority.md` (higher-priority source wins; ties break by newer timestamp, then explicit path/command/line), and record the resolution as a decision or conflict entry.
- Inventing status not backed by proof. Do not infer `done` from a hopeful narrative or from memory. Unverified items are `not_started`, `in_progress`, or `blocked`, never `done`.
- The cold-handoff case (zero artifacts). When no plan/progress/result files exist, do not emit an empty or fabricated handoff. Compile from the live repository state (`git status`, `git diff`, commit log, changed files) plus any conversation memory, label every memory-only claim as unverified, and set overall status to `partial` at most until proof is gathered.

## Tooling

All scripts are plain Python 3 (standard library only). Run with the project's Python interpreter; no install step is required. Paths below are relative to this skill directory; use forward slashes.

- `scripts/build_handoff_index.py <artifact_dir>` builds an evidence index from delivery artifacts. The directory is optional and may be given either positionally (`build_handoff_index.py <artifact_dir>`) or as an option (`build_handoff_index.py --dir <artifact_dir>`); both default to the current directory.
- `scripts/validate_handoff_md.py <handoff.md>` checks required handoff sections (single file).
- `scripts/validate_context_pack.py <context-pack.json>` checks required keys, types, and enum values (single file).
- `scripts/validate_handoff_parity.py <handoff.md> <context-pack.json>` checks cross-file parity: the overall status in both files matches, and every completed claim has a passing verification entry. Run this after the two single-file validators pass.

## References

One level deep, read on demand:

- `references/handoff-source-priority.md`: source precedence and conflict resolution.
- `references/handoff-quality-gate.md`: required checks and status rules before publishing.
- `references/context-pack-schema.md`: `context-pack.json` schema and the single-source Status Vocabulary.
- `references/continuation-mode.md`: continuation-mode judgment rule and sequential fallback.
