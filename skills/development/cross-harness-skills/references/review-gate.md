# Cross-Harness Review Gate

Use this checklist after reading the target skill and every resource needed for its normal path.

## Package Gate

- `name` and `description` are the only shared frontmatter keys.
- The first description sentence distinguishes the trigger from adjacent skills.
- `SKILL.md` contains the normal path, authority, evidence, output, and real gotchas without generic competence scaffolding.
- Every linked path exists, references are one level deep, and long references have a contents map.
- Commands work from the documented location and do not assume a harness-only environment variable or built-in tool.
- A script handles deterministic work, has explicit failures, and passes its documented invocation; contextual judgment remains model-native.

## Prompt Gate

- Outcome and completion criteria are explicit.
- Review/diagnose/report does not imply edits; build/fix/change allows in-scope local work and non-destructive validation.
- Required facts, artifacts, evidence, caveats, and actions are protected from generic brevity.
- Contextual choices use decision rules; exact commands are reserved for fragile or safety-critical operations.
- Progress and completion claims require current evidence.
- No hidden-reasoning, scratchpad, reflection-transcript, or chain-of-thought request remains.
- Parallelism is justified by task shape and has a sequential fallback.

## Adapter Gate

- `/name`, `$name`, install paths, optional metadata, hooks, approval rules, built-in tool names, and environment substitutions are outside the portable body unless the skill is explicitly harness-specific.
- Claude-only and Codex-only adapters are labeled and do not contradict the core.
- Side-effect safety still holds when optional invocation policy is absent.
- Model names, effort, pro/ultra modes, and cost routing live in a dedicated routing skill or dated maintenance reference.

## Evaluation Matrix

Use this matrix only for an explicitly requested model comparison. Ordinary skill maintenance completes with the applicable package, prompt, and adapter checks above; unavailable model runs are a limitation, not a blocker or a reason to create fixtures.

Use at least two positive triggers, two adjacent negative triggers, and these behavior cases:

| Case | Expected evidence |
| --- | --- |
| Normal execution | Required artifact and validation pass |
| Review-only request | Findings with no unrequested mutation |
| Missing prerequisite | Smallest fallback or explicit blocker |
| Tool or script failure | Faithful failure, bounded retry, no false completion |
| Long or parallel path | Grounded phase updates, ownership, sequential fallback |

Run each case in the intended Codex and Claude Code model pair. For an existing skill, compare no-skill, current, and candidate conditions with the same fixture, effort, and rubric. Record an unavailable cell instead of extrapolating.

## Acceptance

Accept a change only when it fixes a reproduced structural, authority, trigger, or behavioral defect without weakening the other target. Prefer the smaller candidate on a tie. Do not edit a skill merely to standardize headings, insert model names, or mirror every sentence from a provider guide.

Report per skill:

- `pass`: portable core and adapters already satisfy the gate;
- `changed`: accepted patch and its evidence;
- `split`: harness-specific behavior moved out of the core;
- `untested`: model/harness behavior that static checks cannot prove.
