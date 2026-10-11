# Worked Example: A Web-Navigation Agent Hunch

A synthetic critique of one hunch. Paths, numbers, and dates are invented to show the shape and depth; the depth fits a hunch someone is about to spend a week on.

The user writes: "I think if the agent writes a full plan before its first action, it'll finish a lot more of the long tasks. Poke holes in this."

## Critique

**Claim tested:** Having the web-navigation agent write an explicit step plan before its first action raises success on the long-task split (tasks needing 15 or more actions) by at least ten points, compared with the current agent at the same model and step limit. "A lot more" is read as ten points or more; correct it if you meant otherwise.

**Steelman:** Long tasks fail mostly through drift: the agent loses track of which subgoals are done and repeats or abandons them (inference). A written plan gives the agent a record of subgoals it can check off, which would reduce drift without changing the model. The strongest version lets the agent revise the plan after each page load, because a fixed plan breaks when pages change; that repair keeps the same bet.

- Baseline success falls from 61% on short tasks to 22% on long tasks in `runs/baseline-v3/summary.md` (evidence).
- Plan-then-act prompting is an established pattern for tool-using agents, with reported gains on multi-step tasks (evidence from the prior-art check; transfer to this agent is unmeasured).

**Attacks, by impact:**

1. The long-task failures may not be drift. If most are grounding errors (acting on the wrong page element) or page-load timeouts, a plan cannot fix them. Nobody has labeled the failure causes, so this is speculation, and it is the attack the decision hinges on. Ruled out if a failure sample shows drift accounts for a large share of long-task failures.
2. A gain could come from extra compute, not from planning. The plan step adds a model call and tokens, so any improvement may come from the added budget (inference). Ruled out if the plan arm beats a control that spends the same extra tokens on unstructured deliberation before acting.
3. Plans go stale. On tasks with pop-ups or multi-page forms, a plan written before the first page load can lock the agent into wrong steps; the revisable steelman reduces this risk without removing it (speculation).

**Closest prior work:** The prior-art check (searched 2026-10-12, `research/2026-10-12-plan-first/prior-art.md`) found plan-then-act agents well established, so the method itself is not new (evidence). The delta is whether the pattern helps this agent on this benchmark at this model size. That is still a valid engineering question, so the delta does not change the decision to test it.

**Deciding measurement:**

- First, label 50 failed long-task trajectories from `runs/baseline-v3/` by cause: drift, grounding, timeout, or other. About two hours of reading and no compute. Contradiction if drift causes under a tenth of failures: with 78% of long tasks failing, fixing every drift failure would then raise success by under eight points. This pass cannot support the claim; drift causing at least a third of failures only shows room for a gain of up to 26 points.
- If the labels leave room, run the plan arm against the equal-token control on the long-task split with three seeds each, about one accelerator-day. Support if the plan arm beats the control by ten points or more and by more than the seed spread; contradiction if the gain is under three points and the seed spread is small enough to rule out a ten-point gain; anything between is inconclusive and calls for more seeds before a decision. The comparison conditions and budget go to `evaluation-design`.

**Status:** unmeasured. No evidence yet at the claim's conditions; `runs/baseline-v3/summary.md` shows that long tasks fail, not why. The effort keeps no critique record, so the critique stays in chat.

The critique proposes no other design. If the label pass contradicts the hunch, deciding what to explore next stays with the user.

## What the example shows

- The vague magnitude got an explicit reading instead of a question, because asking would not change the attacks.
- The steelman absorbed a repair (a revisable plan) that keeps the same bet, and the attacks target that version.
- The prior-art delta is reported on its own line, outside the ranked attacks, because it does not change the decision.
- The cheapest test reuses existing runs and can only contradict; the expensive test is gated on it and can decide either way.
