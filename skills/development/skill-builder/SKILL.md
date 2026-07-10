---
name: skill-builder
description: >
  Use when creating, improving, auditing, or modernizing an agent skill;
  converting a workflow into a reusable skill; or working on SKILL.md,
  resources, triggers, evaluations, or portability. Also use when adapting a
  legacy skill to a stronger model generation such as GPT-5.6 Sol or Fable 5.
  NOT for ordinary project documentation or one-off prompts.
---

# Skill Builder

Build portable skills that add verified leverage beyond model defaults.

## Quick Start

1. Infer the reusable outcome, trigger boundary, expected artifact, target
   harnesses, and user authority from context. Ask only when a missing choice
   would materially change the skill.
2. Establish evaluations before editing: realistic positive prompts, near-miss
   negatives, and executable or rubric-based success checks.
3. For naming, read `references/skill-naming.md`. For an existing skill, read
   `references/skillopt-manual.md`; for a model-era refresh, also read
   `references/frontier-model-audit.md`.
4. Keep only what changes behavior: domain knowledge, fragile procedure,
   permission or safety boundaries, non-obvious tool routing, required output,
   stop rules, and verification.
5. Put the 80% path in `SKILL.md`; move detailed references, reusable code, and
   templates into one-level resources.
6. Run `scripts/validate_skill.sh <skill-dir>`, any bundled self-tests, and the
   same evaluations used for the baseline. Accept only a clear improvement.

## The Skill Contract

Before writing, record:

- `outcome`: what the user gets when the skill succeeds.
- `trigger`: when this skill wins and which adjacent requests it must not catch.
- `target`: models, harnesses, tools, and runtime constraints that matter.
- `unique_leverage`: knowledge or procedure the base model lacks.
- `authority`: allowed local work and actions that still need confirmation.
- `evidence`: tests, files, sources, renders, or rubric that prove completion.

Delete generic scaffolding when the target model succeeds without it. Use
decision rules for judgment and exact gates for fragile work.

## Structure

```text
skill-name/
├── SKILL.md
├── references/    # Detailed guidance loaded only when needed
├── scripts/       # Deterministic utilities executed without loading as prose
├── assets/        # Templates or resources copied into outputs
└── config.json    # Optional user-specific setup; persistent state lives elsewhere
```

Use `references/local-skill-layout.md` for skills maintained in this repository.
Use `references/skill-naming.md` for naming and `references/skill-tips.md` for
skill types, portability, hooks, and script decisions.

## Frontmatter

Use two fields for the portable default:

```yaml
---
name: pdf-processing
description: >
  Use when the user wants to extract, fill, inspect, or merge PDF files. Trigger
  on PDF files and form-processing requests. NOT for creating Word documents.
---
```

- `name`: the shortest natural label that distinguishes the capability;
  lowercase letters, numbers, and hyphens; at most 64 characters; no reserved
  model/vendor words. Gerunds are one option, not a default.
- `description`: at most 1024 characters, third person, specific about what and
  when; add an adjacent NOT-for boundary where useful.
- Add optional metadata only when every target harness supports it.

## Write For Frontier Models

Prefer outcome and decision rules over a transcript of steps the model already
knows. A compact skill normally needs:

1. A quick path to the result.
2. Non-obvious constraints and authority boundaries.
3. Tool routing only where the choice is not obvious.
4. The required output and evidence bar.
5. Stop, retry, fallback, or abstention rules for real failure modes.
6. Gotchas learned from observed behavior.

Remove generic competence, reasoning, and permission reminders. Protect required
facts, caveats, actions, and artifacts from generic brevity. Request evidence and
concise rationale, never unreported internal deliberation.

For shared Claude Code/Codex skills, also apply
`cross-harness-skill-authoring`: keep the domain contract portable, isolate
native adapters, and test Fable/Claude Code and GPT-5.6/Codex independently.

## Progressive Disclosure

- Keep `SKILL.md` comfortably under 500 lines and preferably under about 8KB.
- Link every reference directly from `SKILL.md`; do not chain references.
- Give references over 100 lines a contents map near the top.
- State whether a script should be executed or read as an explanation.
- Bundle scripts only for deterministic, repeatable work. If judgment still does
  the hard part and the input is small, direct model work is usually simpler.
- Any documented script or template must pass its exact invocation. A
  generate-then-validate workflow ships a smoke test.

## Evaluation Gate

For a new skill, compare target-model behavior without the skill and with the
candidate. For a model-era refresh, compare three conditions on the same tasks:

1. Target model without the skill.
2. Target model with the current skill.
3. Target model with the candidate skill.

Hold model, harness, tools, prompts, evaluator, and effort fixed. Test each
intended model family when available; otherwise report the gap.

Use 2-5 positive prompts, 1-2 near-miss negatives, and the smallest executable
checks that prove the artifact. Treat a tie as rejection for behavioral edits.
Structural fixes such as broken paths or invalid frontmatter can pass by direct
verification.

## Improving An Existing Skill

Follow `references/skillopt-manual.md`: freeze the gate, separate failure and
success evidence, rank 1-4 high-impact edits, and validate on the same cases.
Rewrite only for structural breakage or systematic no-skill regression. Keep
optimizer notes and rejected ideas out of the deployed skill.

## Validation

- Run `scripts/validate_skill.sh <skill-dir>` and verify paths from the package
  root.
- Run every changed script/template's documented invocation.
- Re-read the 80% path and rerun the frozen positive and negative evaluations.
- For a model refresh, require improvement over current behavior without losing
  strengths from the no-skill baseline.

Refresh `references/skill-docs.md` from its official sources after 30 days.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/frontier-model-audit.md` | Modernizing a legacy skill or prompt for stronger models | Subtractive GPT-5.6 Sol/Fable 5 audit and three-way evaluation |
| `references/skillopt-manual.md` | Improving an existing skill from traces, feedback, or model change | Evidence packet, bounded edits, ranking, validation, rejected-edit buffer |
| `references/skill-naming.md` | Naming or renaming a skill | Ecosystem evidence, name archetypes, candidate scoring, and rename gate |
| `references/skill-tips.md` | Choosing skill type, portability, scripts, or hooks | Authoring patterns and cross-harness addenda |
| `references/skill-docs.md` | Checking current field, surface, runtime, or security constraints | Dated official Anthropic documentation snapshot |
| `references/local-skill-layout.md` | Editing or installing skills in this repository | Canonical paths, symlinks, migration, and local validation |

## Gotchas

- A longer skill is not a safer skill. Strong instruction-following amplifies
  contradictions and obsolete scaffolding.
- Do not encode system-level autonomy, tone, or tool policy again in every skill;
  keep only task-specific deltas.
- Do not force subagents or parallelism when sequential work is better. Keep a
  sequential fallback and let a routing/orchestration skill choose the mechanism.
- Do not require internal-deliberation transcripts or context-budget narration.
  Evaluate artifacts and evidence instead.
- Do not schedule self-editing or background optimization unless the user asks.
- Persistent data belongs outside an upgradeable skill directory.
- Overlapping skills should merge unless each has frequent independent triggers.
- Catalog consistency is useful, but never force awkward grammar to obtain it.
