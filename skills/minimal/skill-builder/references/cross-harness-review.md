# Cross-Harness Review Gate

Use this after reading the target skill and every resource needed for its normal path. The [validator contract](validation.md) covers metadata syntax, links, and symlinks; this gate adds what portability needs.

## Package Gate

- Optional standard metadata follows the documented format, and every native field has a target adapter.
- The first description sentence distinguishes the trigger from adjacent skills.
- SKILL.md contains the normal path, authority, evidence, output, and real gotchas without generic competence scaffolding.
- The normal path makes the use of each required resource clear. Reference depth and size are reviewed for retrieval cost, not treated as universal runtime limits.
- Commands work from the documented location and do not assume a harness-only environment variable or built-in tool.
- A script handles deterministic work, has explicit failures, and passes its documented invocation; contextual judgment remains model-native.

## Prompt Gate

- Outcome and completion criteria are explicit.
- Review, diagnose, or report does not imply edits; build, fix, or change allows in-scope local work and non-destructive validation.
- Required facts, artifacts, evidence, caveats, and actions are protected from generic brevity.
- Contextual choices use decision rules; exact commands are reserved for fragile or safety-critical operations.
- Progress and completion claims require current evidence.
- No hidden-reasoning, scratchpad, reflection-transcript, or chain-of-thought request remains.
- Parallelism is justified by task shape and has a sequential fallback.

## Adapter Gate

- `/name`, `$name`, install paths, optional metadata, hooks, approval rules, built-in tool names, and environment substitutions are outside the portable body unless the skill is explicitly harness-specific.
- Claude-only and Codex-only adapters are labeled and do not contradict the core.
- Side-effect safety still holds when optional invocation policy is absent.
- Model names, effort, pro or ultra modes, and cost routing live in a dedicated routing skill or dated maintenance reference.

## Evaluation Matrix

Run this only for an explicitly requested model comparison; it is not a prerequisite for ordinary skill work, and the verification levels in SKILL.md govern. Ordinary maintenance completes with the package, prompt, and adapter gates above; unavailable model runs are a limitation, not a blocker or a reason to create fixtures.

When requested, use the same representative repository state, artifacts, prompts, effort, and rubric in both primary targets, and record tool availability and effort settings. For an existing skill, compare the target model and harness without the skill, with the current skill, and with the candidate.

Use at least two positive triggers, two adjacent negative triggers, and these behavior cases:

| Case | Expected evidence |
| --- | --- |
| Normal execution | Required artifact and validation pass |
| Review-only request | Findings with no unrequested mutation |
| Missing prerequisite | Smallest fallback or explicit blocker |
| Tool or script failure | Faithful failure, bounded retry, no false completion |
| Long or parallel path | Grounded phase updates, ownership, sequential fallback |

Run each case in the intended Codex and Claude Code model pair. Record an unavailable cell instead of extrapolating. Structural validation cannot substitute for behavioral testing, and a Claude Code pass cannot stand in for a Codex pass.

For a requested model-era migration comparison:

1. Freeze representative tasks and success criteria.
2. Run each primary model and harness pair without the skill and with the current skill before editing.
3. Remove redundant scaffolding, contradictions, irrelevant tools, and generic style rules.
4. Add the smallest instruction that fixes a reproduced failure.
5. Re-run the same tasks after each bounded edit group.
6. Report untested models, harnesses, effort settings, and side-effect modes.

Do not change the model, effort, prompt, tools, and evaluator simultaneously; a passing result would not identify which change helped.

## Acceptance

Accept a change only when it fixes a reproduced structural, authority, trigger, or behavioral defect without weakening the other target. A smaller candidate wins only after required behavior and evidence still pass, and is preferred on a tie. Do not edit a skill merely to standardize headings, insert model names, or mirror every sentence from a provider guide.

Report per skill:

- `pass`: portable core and adapters already satisfy the gate;
- `changed`: accepted patch and its evidence;
- `split`: harness-specific behavior moved out of the core;
- `untested`: model and harness behavior that static checks cannot prove.
