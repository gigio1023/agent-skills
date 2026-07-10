---
name: fable5-judgment-orchestrator
description: >
  Use when the user wants Fable 5 to lead difficult judgment, long-horizon work,
  issue review, decision synthesis, overlooked-fact checks, strategic
  recommendations, or multi-agent critique, optionally with GPT-5.6 Sol or
  other support lanes. Trigger for "Fable 5로 판단", "쟁점 리뷰", "중요한 가치
  판단", "놓친 사실 체크", "decision review", or "strategic synthesis". NOT
  for a routine bounded task that one agent can finish directly.
---

# Fable 5 Judgment Orchestrator

## Purpose

Use Fable 5 as the lead for work whose value comes from judgment, ambiguity
resolution, sustained context, or a defensible recommendation. Fable 5 can also
perform difficult end-to-end work; do not delegate merely to keep its context
empty. Delegate when concurrency, context isolation, fresh verification, tool
specialization, or a measured cost/latency advantage improves the result.

This skill assigns model roles. `parallel-subagent-orchestrator` owns work
decomposition, packets, asynchronous coordination, and synthesis mechanics.

## Quick Start

1. State the user-visible decision or outcome and its completion bar.
2. Identify the judgment core Fable 5 must own: the trade-off, risk, hypothesis,
   conflict, or ambiguous implementation choice.
3. Read `references/lane-routing.md`. Choose direct Fable 5 execution unless a
   separate lane has a concrete advantage.
4. When delegating, give each lane a bounded question, evidence contract, and
   stop condition. Let independent lanes run asynchronously while the lead does
   non-overlapping work.
5. Use fresh-context verification for consequential long runs or when the lead
   may be anchored to its own approach. Routine work does not need a committee.
6. Ground every progress and completion claim in tool output, inspected sources,
   or a named artifact from the current run.
7. Before answering, use `references/judgment-gate.md`. Resolve conflicts and
   make the recommendation; do not concatenate worker summaries.

## Fable 5 Owns

- The decision rule: what evidence would change the answer.
- Issue framing, hidden assumptions, stakeholder and time-horizon checks.
- High-ambiguity analysis where intermediate results change the next move.
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
- Do not request hidden reasoning or a chain-of-thought transcript.
- Do not hide a material model or tool substitution; state it when it changes
  confidence, cost, latency, or reproducibility.
- Do not duplicate `parallel-subagent-orchestrator`; this skill owns model-role
  judgment, while the parallel skill owns orchestration mechanics.
