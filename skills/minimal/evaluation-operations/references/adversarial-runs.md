# Adversarial Runs

Read this when an approved campaign's cases try to elicit unwanted behavior from the system under test, such as a disclosure, a prohibited action, or a policy violation. It adds run accounting to the operational rules in the skill body. Designing such cases belongs to evaluation-design, and a verdict on a finished result to evaluation-audit.

## Count only validly graded results

The success rate is verified successes divided by validly graded results. Transport, target, and grader errors never enter that denominator; report each as its own count beside the rate. Zero validly graded results is inconclusive, not a rate of zero. promptfoo computes its attack success rate this way and reports errors apart.

A missing or malformed grader response is a grader failure, neither a success nor a non-success. Rerun or repair the grader only within the campaign's authority, and never let a mock grader stand in for a real run's verdicts.

## Outcome classes

Give each attempt one class, using the names public tools use so records stay comparable:

- **refusal**: the system declined. A graded outcome, never a capability failure or an error.
- **truncation or budget exhaustion**: the attempt hit an output limit, turn cap, token budget, or wall-clock ceiling before a verdict.
- **infrastructure or external failure**: rate limit, network, missing dependency, unavailable target.
- **grader failure**: the grader crashed, timed out, or returned no parseable verdict.
- **verified success**: the unwanted behavior occurred and the evidence verifies it. For a tool-using target the evidence is persisted state, not tool arguments or narration; a final refusal does not undo a write.

A graded attempt that is neither refusal nor verified success is a graded non-success. Infrastructure and grader failures are excluded from the denominator. Report truncation or budget exhaustion as its own count and state with the rate whether it enters the denominator: under a declared budget it is an outcome of that budget, while under an accidental limit it is an artifact of the run.

Synthetic example. 200 attempts: 30 verified successes, 110 refusals, 40 graded non-successes, 12 budget exhaustions, 6 infrastructure failures, 2 grader failures. With exhaustion outside the denominator, the rate is 30 of 180; with the declared budget counted as an outcome, 30 of 192. The 8 errors are reported apart in both cases.

## Filtered reruns

A rerun of only the failing cases, the erroring cases, or one category has its own denominator. Report it beside the full-suite result, never inside it, and recompute any combined rate over one defined population. Keep the original attempts as [attempts, results, and rescoring](attempts-and-result-lineage.md) requires.

## Baseline pass

Run each objective once without any technique, as the plain request, and give that pass its own row. The technique's effect is the difference from this baseline; a high rate where the plain request already succeeds says little about the technique. PyRIT scenarios include such a baseline, and garak's context-aware scanning uses a non-adversarial policy baseline for the same reason.

## Adaptive techniques

A technique that generates new inputs during the run, such as a model that revises its input from the target's replies, does not replay from configuration. For exact replay, keep the concrete inputs and full transcripts with the original target and grader configuration. For comparison across runs, keep settings, versions, attempt counts, and transcripts, and report the variation across repeated runs rather than one run's rate.

## Breakdowns and critical categories

Break results down per objective and per technique, and per pair when the campaign crosses them; garak reports a rate for each probe and detector pair. An aggregate can hide one critical category, so keep each critical category's verified successes visible in the summary even when the aggregate rate is low.

## Records

Write run records in the vocabulary of evaluation methodology: objectives, techniques, metrics, grading rules, outcome classes, and counts. Files that an agent loads automatically in later sessions carry status, decisions, and paths, with no reproducible procedure, raw unwanted output, or target-specific detail. The full evidence stays in the run's evidence files under the project's access and retention rules, and no finding is dropped from a report because of this rule.

## Sources

Reviewed October 3, 2026.

- [promptfoo red-team run skill](https://github.com/promptfoo/promptfoo) at `8e6b3fa` (2026-10-02), `plugins/promptfoo/skills/promptfoo-redteam-run`: inspected in full. Adopted the rate over validly graded results, errors reported apart, inconclusive zero-graded runs, separate denominators for filtered reruns, transcripts for adaptive replay, variation across repeated runs, persisted state for tool-using targets, and visible critical categories. Not adopted: commands, CI thresholds, and promptfoo's configuration vocabulary.
- [Microsoft PyRIT](https://github.com/microsoft/PyRIT) at `38d7e11` (2026-10-02), `doc/blog/2026_07_09_scenarios.md`: the baseline pass without a technique and the objective and technique structure of a scenario, taken from a secondary summary at this revision.
- [NVIDIA garak](https://github.com/NVIDIA/garak) at `8d1259e` (2026-09-16), `docs/source/` reporting and context-aware scanning pages: per probe and detector rates and the non-adversarial policy baseline, taken from a secondary summary at this revision.

The outcome-class names follow the public terms in these sources and in the Anthropic and Inspect eval skills cited by evaluation-audit; the denominator rule for budget exhaustion and the synthetic example are independently authored.
