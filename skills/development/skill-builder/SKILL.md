---
name: skill-builder
description: >
  Use when creating, improving, auditing, or modernizing an agent skill;
  converting a workflow into a reusable skill; or working on SKILL.md,
  resources, triggers, packaging, or portability. Also use when adapting a
  legacy skill to a stronger model generation such as GPT-5.6 Sol or Fable 5.
  NOT for ordinary project documentation or one-off prompts.
---

# Skill Builder

Build portable skills that add verified leverage beyond model defaults.

## Quick Start

1. Infer the reusable outcome, trigger boundary, expected artifact, target
   harnesses, and user authority from context. Ask only when a missing choice
   would materially change the skill.
2. Inspect the existing package and linked resources before changing
   it. Use real user feedback or observed failures when they exist; do not invent
   an evaluation program as a prerequisite.
3. For naming, read `references/skill-naming.md`. For a model-era refresh, read
   `references/frontier-model-audit.md`.
4. Keep only what changes behavior: domain knowledge, fragile procedure,
   permission or safety boundaries, non-obvious tool routing, required output,
   stop rules, and verification.
5. Put the 80% path in `SKILL.md`; move detailed references, reusable code, and
   templates into one-level resources.
6. Run `scripts/validate_skill.sh <skill-dir>` and every changed script or
   template's documented smoke invocation. Report any check that cannot run.

## The Skill Contract

Before writing, record:

- `outcome`: what the user gets when the skill succeeds.
- `trigger`: when this skill wins and which adjacent requests it must not catch.
- `target`: models, harnesses, tools, and runtime constraints that matter.
- `unique_leverage`: knowledge or procedure the base model lacks.
- `authority`: allowed local work and actions that still need confirmation.
- `verification`: direct checks for changed files, links, scripts, templates, or
  package discovery that establish the requested artifact is usable.

Delete generic scaffolding when the target model succeeds without it. Use
decision rules for judgment and deterministic checks for fragile work.

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
4. The required output and verification bar.
5. Stop, retry, fallback, or abstention rules for real failure modes.
6. Gotchas learned from observed behavior.

Remove generic competence, reasoning, and permission reminders. Protect required
facts, caveats, actions, and artifacts from generic brevity. Request evidence and
concise rationale, never unreported internal deliberation.

For shared Claude Code/Codex skills, also apply
`cross-harness-skills`: keep the domain contract portable, isolate
native adapters, and keep correctness independent of either harness's optional
metadata. Do not inherit model-comparison or evaluation-matrix requirements
unless the user explicitly requests them.

## Progressive Disclosure

- Keep `SKILL.md` comfortably under 500 lines and preferably under about 8KB.
- Link every reference directly from `SKILL.md`; do not chain references.
- Give references over 100 lines a contents map near the top.
- State whether a script should be executed or read as an explanation.
- Bundle scripts only for deterministic, repeatable work. If judgment still does
  the hard part and the input is small, direct model work is usually simpler.
- Any documented script or template must pass its exact invocation. A
  generate-then-validate workflow ships a smoke test.

## Scope Discipline

- Do not create evaluation suites, prompt cases, benchmarks, baselines,
  candidate comparisons, scoring rubrics, scorecards, or persistent results
  files unless the user explicitly asks for them.
- Do not launch extra model sessions solely to compare skill variants. Real
  usage feedback may inform a change without becoming a permanent evaluation
  artifact.
- Validate the artifact directly: frontmatter, referenced paths, package
  discovery, and the exact invocation of scripts or templates changed in the
  request. Documentation-only changes need no synthetic behavior trial.

## Improving An Existing Skill

Read the current skill and its directly linked resources, identify the smallest
change that addresses the user's request or an observed failure, and preserve
working behavior outside that scope. Prefer 1-4 focused edits. Rewrite only for
structural breakage; keep maintenance notes and discarded alternatives out of
the deployed skill.

## Validation

- Run `scripts/validate_skill.sh <skill-dir>` and verify paths from the package
  root.
- Run every changed script/template's documented invocation.
- Re-read the normal path and confirm references, examples, and installation
  instructions still agree with the changed contract.
- Use existing repository checks when they are already part of the project; do
  not add an evaluation framework to validate an ordinary skill edit.

Refresh `references/skill-docs.md` from its official sources after 30 days.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/frontier-model-audit.md` | Modernizing a legacy skill or prompt for stronger models | Subtractive GPT-5.6 Sol/Fable 5 audit without benchmark scaffolding |
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
  Report observable artifacts and checks instead.
- Do not schedule self-editing or background optimization unless the user asks.
- Persistent data belongs outside an upgradeable skill directory.
- Overlapping skills should merge unless each has frequent independent triggers.
- Catalog consistency is useful, but never force awkward grammar to obtain it.
