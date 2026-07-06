# Delegation Patterns

Use these as patterns, not scripts. The lead agent should adapt the number of
agents, depth, and output contract to the user's budget and the task's stakes.

## Pattern A: Breadth Research

Use for web research, tool discovery, market scans, ecosystem mapping, and
"what exists?" questions.

First wave:

- Official/source-of-truth lane: specs, docs, standards, vendor pages, papers.
- Adoption lane: GitHub repos, package stats, issues, community usage, examples.
- Skeptic lane: maintenance risk, slop signals, security, dated advice, hype.

Lead synthesis:

- Separate "what is real" from "what is popular" and "what is worth adopting."
- Rank candidates by evidence quality, not by how often they appeared.
- Launch a second wave only for short-listed candidates or unresolved conflicts.

## Pattern B: Literature Or Evidence Review

Use for papers, technical reports, policy, medical/legal/financial-adjacent
background work, or any claim where source quality dominates quantity.

First wave:

- Primary-source extractor: read papers, laws, standards, or official releases.
- Method critic: inspect methodology, sample, assumptions, confounders.
- Applicability analyst: decide what transfers to the user's actual context.

Lead synthesis:

- Maintain a claim table: claim, source, evidence strength, caveat, relevance.
- Prefer a small number of strong sources over a pile of shallow summaries.
- Mark dates and version boundaries.

## Pattern C: Value Judgment Or Strategy

Use when the user asks "should I?", "is this worth it?", "which path?", or
needs a recommendation under uncertainty.

First wave:

- Advocate: strongest case for option A or action.
- Skeptic: strongest case against it, failure modes, opportunity cost.
- Operator: practical execution cost, reversibility, sequencing, constraints.
- Optional outsider: a different time horizon, stakeholder, or domain lens.

Lead synthesis:

- Do not average the opinions. Identify decisive evidence and decision rules.
- Surface trade-offs, reversibility, downside cap, and information value.
- Give a recommendation with confidence and the condition that would change it.

## Pattern D: Codebase Exploration

Use before implementation when the codebase has multiple unknown areas.

First wave:

- Architecture explorer: where the change belongs and key dependencies.
- Test explorer: existing test shape, fixtures, likely verification route.
- Risk explorer: hidden contracts, generated files, migrations, compatibility.

Lead synthesis:

- Convert findings into an implementation map and disjoint write scopes.
- Avoid sending multiple explorers through the same files unless they have
  different questions.

## Pattern E: Parallel Implementation

Use only when write scopes can be separated cleanly.

First wave:

- Worker A owns module/screen/package X.
- Worker B owns module/screen/package Y.
- Worker C owns tests/docs/verification, if it can proceed independently.

Worker packet must include:

- Owned files or modules.
- Files/modules not to touch.
- Required tests or proof.
- Reminder that other agents may be editing the repo and user changes must not
  be reverted.

Lead synthesis:

- Review diffs quickly as workers finish.
- Integrate in dependency order.
- Run whole-system verification after merging worker outputs.

## Pattern F: Adversarial Review

Use after a plan, implementation, or research synthesis exists.

Review lanes:

- Correctness: behavioral bugs, unsupported claims, missing edge cases.
- Security/safety: data exposure, destructive operations, policy risk.
- User-fit: does this solve the real user request or just the literal prompt?
- Quality: maintainability, readability, naturalness, design taste, evidence.

Lead synthesis:

- Fix material findings first.
- Reject vague nits or style churn that lacks consequence.
- If reviewers disagree, decide by impact and evidence, not reviewer confidence.

## Pattern G: Long-Running Or Multi-Wave Work

Use when one wave cannot reasonably finish the user's goal.

State to preserve between waves:

- Objective and non-goals.
- Decisions already made.
- Evidence accepted.
- Open questions.
- Agents used and what they covered.
- Next wave purpose.

Follow-up waves should be narrower than the first wave. If they become broader,
the lead agent probably synthesized too early or framed the original task too
loosely.
