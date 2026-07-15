---
name: fable5-judgment
description: >
  Claude Code and Cursor only. Consider when the user wants Fable 5 to lead
  difficult judgment, long-horizon work, issue review, decision synthesis,
  overlooked-fact checks, strategic recommendations, or critique. First inspect
  the actual problem and independently confirm that it has a consequential,
  unresolved judgment core for which Fable 5 has a concrete advantage. Trigger
  phrases are signals, not sufficient evidence. Do not use in Codex, when Fable
  5 is unavailable, or for routine bounded work the current agent can finish.
---

# Fable 5 Judgment

## Entry Gate

Before applying this skill:

1. Identify the executing harness. In Codex, do not apply this skill or use it
   as routing policy; continue with Codex's native capabilities. Explicit
   invocation does not override this exclusion.
2. In Claude Code or Cursor, inspect the user's actual goal, available context,
   relevant artifacts, stakes, ambiguity, and missing evidence before deciding
   whether the skill fits. Resolve discoverable facts rather than inferring a
   judgment problem from trigger words alone.
3. Apply the skill only when Fable 5 is available and the remaining problem has
   a consequential judgment core—such as a material trade-off, hidden premise,
   conflicting evidence, or defensible recommendation—for which Fable 5 has a
   concrete advantage over direct completion by the current agent.
4. A long task, a matching phrase, or an opportunity to use multiple agents is
   not enough by itself. If the remaining work is routine, already bounded, or
   the advantage is unclear, proceed without this skill.

This gate controls the harness that leads the workflow. It does not prevent an
eligible Claude Code or Cursor run from assigning bounded support work to a
configured Codex or GPT-5.6 Sol lane after the judgment boundary is stable.

## Purpose

After the entry gate passes, use Fable 5 as the lead for work whose value comes
from judgment, ambiguity resolution, sustained context, or a defensible
recommendation. Fable 5 can also perform difficult end-to-end work; do not
delegate merely to keep its context empty. Delegate when concurrency, context
isolation, fresh verification, tool specialization, or a measured cost/latency
advantage improves the result.

Spend scarce Fable 5 capacity at the **judgment frontier**: the early framing,
adaptive investigation, and interpretation needed to make later work genuinely
bounded. Once the decision rule, research questions, coverage bar, and action
specification are stable, route large follow-on research, implementation, and
verification to the strongest suitable execution lane. If new evidence breaks
an assumption or reopens an ambiguous choice, return that choice to Fable 5.

This skill assigns model roles. `parallel-subagents` owns work
decomposition, packets, asynchronous coordination, and synthesis mechanics.

## Quick Start

1. Pass the entry gate, then state the user-visible decision or outcome and its
   completion bar.
2. Identify the judgment core Fable 5 must own: the trade-off, risk, hypothesis,
   conflict, ambiguous implementation choice, and any investigation whose next
   move depends on interpreting what was just found.
3. Have Fable 5 investigate until it can write a stable decision or execution
   specification. Read `references/lane-routing.md`; delegate only work whose
   success can be judged from that packet without inventing a missing premise.
4. Give each lane a bounded question or action, evidence contract, stop
   condition, and escalation trigger. Large straightforward collection or web
   search may start earlier when Fable 5 has defined the coverage and source bar.
5. Use fresh-context verification for consequential long runs or when the lead
   may be anchored to its own approach. Routine work does not need a committee.
6. Ground every progress and completion claim in tool output, inspected sources,
   or a named artifact from the current run.
7. Before answering, use `references/judgment-gate.md`. Resolve conflicts and
   make the recommendation; do not concatenate worker summaries.

## Fable 5 Owns

- The decision rule: what evidence would change the answer.
- Issue framing, hidden assumptions, stakeholder and time-horizon checks.
- Judgment-dependent discovery: source selection, interpretation, and
  high-ambiguity analysis where intermediate results change the next move.
- The specification that makes follow-on research or execution bounded,
  including escalation conditions for evidence that reopens the judgment.
- Cross-source conflict resolution and confidence calibration.
- The final recommendation, caveat, and condition that would reverse it.

Fable 5 may also own long-context reading or implementation when keeping the
work together is more valuable than parallelism. Route by task shape, not by a
blanket rule that collection is beneath the lead model.

## Delegate When It Helps

- Independent evidence or implementation streams can run concurrently.
- A fresh-context reviewer can test the specification or challenge anchoring.
- A support lane has materially better repository, browser, data, or execution
  tools for a bounded task.
- Large structured results can be reduced without fresh semantic judgment at
  every step.
- Follow-on research, implementation, or action has a stable specification and
  does not require the worker to invent a decision rule or resolve a new value
  conflict.
- A lower-cost lane passes the same evidence and quality bar for routine work.

Every worker returns compact evidence: answer, sources or files inspected,
decisive facts, caveats, confidence, and what remains unverified.

## Long Runs

Use the harness's effort and runtime controls deliberately. Important work may
benefit from higher effort; routine work may be better at medium or low effort.
Do not default every lane to the maximum setting without an evaluation signal.

During long runs, give sparse outcome-based updates at real phase changes.
Before claiming progress, point to the tool result or artifact that proves it.
Never ask a model to reproduce, transcribe, or expose private reasoning; request
evidence, assumptions, decisions, and concise rationale instead.

## Output Behavior

Answer as the lead's judgment, not as a committee transcript. Put the decision
or highest-impact finding first, then the evidence that moved it, the main
caveat, and what would change the answer. Mention lanes only when their coverage
or limitations affect trust.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/lane-routing.md` | Before choosing direct work, delegation, or a model lane | Current Fable 5 and support-lane decision rules and packet shapes |
| `references/judgment-gate.md` | Before the final answer or a follow-up wave | Evidence, conflict, progress, and recommendation checks |
| `references/source-notes.md` | When maintaining this skill | Model-generation sources and separation from the harness-neutral orchestrator |

## Gotchas

- Do not overdelegate work Fable 5 can complete coherently in one run.
- Do not use model prestige as a substitute for sources, tests, or direct
  inspection.
- Do not outsource the decision or average worker opinions.
- Do not delegate unresolved ambiguity disguised as a broad research request.
- Do not request hidden reasoning or a chain-of-thought transcript.
- Do not hide a material model or tool substitution; state it when it changes
  confidence, cost, latency, or reproducibility.
- Do not duplicate `parallel-subagents`; this skill owns model-role
  judgment, while the parallel skill owns orchestration mechanics.
