---
name: fable5-judgment-orchestrator
description: >
  Use when the user wants Fable 5 to lead important judgment, issue review,
  decision synthesis, overlooked-fact checks, strategic recommendations, or
  high-stakes critique while routing token-heavy gathering work to configured
  support lanes. Trigger for "Fable 5로 판단",
  "쟁점 리뷰", "중요한 가치 판단", "놓친 사실 체크", "decision review",
  "strategic synthesis", or when paired with parallel-subagent-orchestrator.
---

# Fable 5 Judgment Orchestrator

## Purpose

Use Fable 5 as the final judgment engine for important decisions, issue
connection, critique, and synthesis. The point is not to make Fable 5 do every
search or file scan. The point is to preserve Fable 5's attention for the
hardest thinking: what matters, what is missing, what conflicts, what changes
the decision, and what recommendation follows.

This skill composes naturally with `parallel-subagent-orchestrator`. Let that
skill handle decomposition, packets, parallel waves, and synthesis mechanics.
Let this skill decide which lanes deserve Fable 5 attention and which lanes
should be delegated for token-efficient evidence collection.

## Quick Start

1. State the user's real decision or review target in one sentence.
2. Identify the judgment core: the trade-off, risk, hypothesis, or review
   question that Fable 5 must personally own.
3. Read `references/lane-routing.md` and route support work before spending
   Fable 5 context on raw collection.
4. Send token-heavy collection lanes to a configured Codex support lane when
   available, especially web search, source lookup, repository/file inventory,
   issue scanning, package checks, and simple re-checks. Use the strongest
   appropriate model available in that lane.
5. Use a configured long-context lane for broad reading or sustained analysis
   that should inform, but not replace, the final decision.
6. Keep Fable 5 on issue framing, cross-lane synthesis, hidden assumption
   checks, missed-fact review, and final recommendation.
7. Before finalizing, use `references/judgment-gate.md`. Do not merely merge
   worker summaries; make the decision yourself from evidence and caveats.

## Fable 5 Owns

- The final recommendation or critique.
- The issue map: which questions are actually decisive and which are noise.
- Cross-source conflict resolution and confidence calibration.
- Detection of missing stakeholders, hidden assumptions, stale facts, and
  unexamined alternatives.
- Whether another evidence wave is worth its cost.
- The final wording to the user, including uncertainty and what would change the
  answer.

## Delegate Aggressively

Delegate support lanes when they are expensive in tokens but bounded in
judgment:

- Web research, source gathering, docs lookup, changelog/version checks.
- Local file discovery, `rg` extraction, repository inventory, issue scanning.
- Re-checking factual claims, dates, names, API surfaces, and links.
- Producing compact evidence tables from a defined source set.
- Running narrow verification commands and reporting results.

Every delegated lane must return compact evidence, not a long essay. Require:
short answer, sources/files inspected, decisive facts, caveats, and confidence.

## Output Behavior

Answer as Fable 5's judgment, not as a committee transcript. Mention delegated
lanes only when they affect trust: what was checked, what was not checked, and
which uncertainty remains.

When the user asks for a recommendation, put the recommendation first. Then give
the evidence that moved the decision, the main caveat, and the condition that
would change your mind.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/lane-routing.md` | Before delegating or choosing a model lane | Fable 5 and support-lane routing rules and packet shapes |
| `references/judgment-gate.md` | Before final answer or follow-up wave | Review checklist for decisive issues, missing facts, conflicts, and recommendation quality |
| `references/source-notes.md` | When maintaining this skill | Why this is separate from the harness-neutral orchestrator |

## Gotchas

- Do not spend Fable 5 on raw search when a support lane can return a compact
  evidence packet.
- Do not outsource the final judgment to Opus, Codex, or a worker summary.
- Do not let token saving erase evidence quality. If the decisive fact is
  current, external, legal, financial, medical, or high-impact, have a worker
  check it and cite the source.
- Do not hide model substitutions. If Fable 5 or a configured support lane is
  unavailable, use the nearest equivalent and say so when it affects confidence
  or cost.
- Do not duplicate `parallel-subagent-orchestrator`. Use this skill for model
  role assignment and judgment discipline; use the parallel skill for
  decomposition and synthesis mechanics.
