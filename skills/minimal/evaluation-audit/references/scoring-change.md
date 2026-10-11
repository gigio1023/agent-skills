# Scoring Change

Read this when the audited artifact changes a scorer, a metric, answer extraction, verdict parsing, or code that consumes a grader's output. Paraphrased from Inspect Evals' verify-scoring-change skill; the revision is in [sources](sources.md).

## Receipts

Every claim about how the evaluation framework behaves cites the installed version (file and line) or a probe's output. A claim without a receipt stays out of the verdict. Read the eval's changelog and the scorer's history before judging, because whether a branch is reachable or a zero was deliberate is answered there, not in the diff.

## The three questions

1. **The bug exists.** Reproduce it at the base revision through the shipped task wiring or a test that exercises it: hand-built scores fed to the metric, a canned grader reply, or the output said to be misparsed. A stub of the code under review is not a reproduction. A refactor has no bug, so run old and new side by side for parity.
2. **The fix removes it.** Run the same inputs at the changed revision and record both outputs side by side. If the change fixes a different bug from the one described, say which.
3. **What else moves.**
   - Decide reachability first. A guard the framework never reaches moves nothing; a denominator that can empty in a healthy run moves numbers.
   - Run at least one case in each direction. A claim that numbers can only fall needs a test.
   - For extraction or parsing changes, rescore prior real outputs at both revisions, after confirming that the base revision reproduces the stored scores.
   - When a return becomes a raise, count how often the new branch fires over the dataset.
   - A moved number needs a declared version change and a changelog line naming the metric and its direction.

## Exclusions and swallowed errors

- List every path that yields an excluded or unscored value and what it means. "The grader failed" and "the grader was not consulted" are different facts; sharing one value silently drops a group from the denominator. Model-attributed reasons (invalid format, refusal, no response) stay in the denominator. Instrument reasons (grader or scoring failure) are exclusions.
- Before applying that rule, find who wrote the artifact being scored. If the system under test was told to write it, a missing or malformed file is the system's failure.
- When a parser becomes more tolerant, probe an unclosed tag, a missing closing fence, a fence inside a string, trailing prose, a nested block, and a case variant. Tolerance that lets a refusal count as the target behavior is a new false-positive channel.
- Search the changed code and its callees for broad exception handlers that return a constant, zero fallbacks in functions that divide, and comparisons with a correct value that have no unscored branch. A zero that a test asserts on purpose is a decision; one that nothing asserts is a defect, and it blocks when the change makes it reachable.

## Tests pin both sides

In a scratch worktree, never the owner's checkout, reverse-apply the change's source diff against its merge base and run its tests. The failures count the behaviors the tests pin. A test that patches the function under review pins nothing. Also list any existing test that passes before the change and fails after it. Confirm that a correct zero still reports zero for a parse miss, a raised API error, and a genuine negative verdict.

If questions 1 or 2 cannot be run, the verdict is hold with those rows unverified. Probes on stored outputs or canned replies are cheap; probes that make new model calls follow the skill's authority rules.
