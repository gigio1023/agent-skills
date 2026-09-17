---
name: fable5-model-routing
description: >
  Use on every task in Claude Code or Cursor where Claude Fable (5 or 5.1) is
  the main session model: each time the lead delegates, judge the subagent's
  task difficulty and set its model and reasoning effort deliberately, keeping
  the judgment core with Fable. Also use when the user names
  fable5-model-routing or asks to put Fable on the judgment while another model
  leads. NOT for Codex, for sessions where Fable is neither the lead nor
  available, or as a reason to spawn subagents at all — decomposition and
  fan-out belong to orchestrate-subagents, and the bounded prompt for a weaker
  executor belongs to small-model-handoff.
---

# Fable 5 Model Routing

Assign model roles and effort around a Claude Fable lead. Fable here means Claude Fable 5 or Claude Fable 5.1; the guidance is the same for both.

## When It Applies

Two entry points, decided by who leads the session:

- **Fable leads: standing policy.** In Claude Code or Cursor, when the main session model is Fable, this skill is in force for the whole session without being named. It does not decide whether to delegate; it governs how each delegation is configured once the lead decides to spawn one. Every subagent gets a model and an effort level chosen for its task, not inherited by omission.
- **Another model leads: on request.** Apply the skill only when the user names it or asks to put Fable on the judgment. Then inspect the actual problem and confirm it has a consequential, unresolved judgment core — a material trade-off, hidden premise, conflicting evidence, or defensible recommendation — for which Fable has a concrete advantage over direct completion by the current agent. A hard-looking task or a matching phrase is not that confirmation. Switching the lead or opening a Fable lane lands on the bill, so it waits to be asked.

In Codex, do not apply this skill in either mode; continue with Codex's native capabilities. Explicit invocation does not override that exclusion.

To know who leads, read what the harness states about the session model; in Claude Code, `/model` shows it, and the `fable` alias selects Fable 5.1 from v2.1.257 and Fable 5 before that. If the lead's identity cannot be established, treat the session as non-Fable.

## Purpose

Fable can carry difficult end-to-end work; do not delegate merely to keep its context empty. Delegate when concurrency, context isolation, fresh verification, tool specialization, or a measured cost or latency advantage improves the result, and when you do, spend the capability where it pays.

Spend Fable at the **judgment frontier**: framing, adaptive investigation, and the interpretation that makes later work genuinely bounded. Once the decision rule, research questions, coverage bar, and action specification are stable, route follow-on research, implementation, and verification to the least capable lane that still meets the packet's evidence bar, at the lowest effort that holds quality. If new evidence breaks an assumption or reopens an ambiguous choice, return that choice to Fable.

This skill assigns model roles and effort. `orchestrate-subagents` owns decomposition, packets, asynchronous coordination, and synthesis; `small-model-handoff` owns the bounded prompt when the chosen lane is a weaker executor.

## Assign Model and Effort per Lane

Before each spawn, read the packet and answer three questions: can a worker judge success from the packet alone, or would it have to invent a premise or decision rule; does the next move depend on interpreting intermediate results, or is the work mechanical; and how costly is a wrong or shallow result. The answers place the lane in one of four tiers. `references/lane-routing.md` holds the tier table with default models and effort levels, the harness mechanics for setting them, and the packet shapes.

Defaults, not entitlements:

- Mechanical collection and bounded reduction: the fastest configured model, at `low` where that model supports effort.
- Bounded execution with a stable specification: a mid-tier model, or the configured repository-heavy lane, at `medium`, rising to `high` when a multi-file change must be correct the first time.
- Judgment-adjacent support such as fresh-context verification or long-context extraction where contradictions matter: the strongest non-lead model, or Fable itself, at `high`.
- The judgment core: the lead, at the session's effort. It is not delegated.

Effort level names mean different amounts of thinking on different models, so never copy a level from one model to another unmeasured. Start at `high` on Fable-class lanes; use `xhigh` or `max` only where a long autonomous run has shown a gain; use `medium` and `low` freely for routine lanes, remembering that at `low` Fable 5.1 searches less and answers from memory more. Fable at `low` is often competitive on cost per task with Opus- or Sonnet-class models at higher effort, so include it in the comparison wherever the harness can set effort per subagent.

Say what you chose. When dispatching, name each lane's model, effort, and the one-line reason, so the user can correct the assignment before the work runs. When the harness could not honor a choice — no agent definition carries the wanted effort, a subagent-model override pins every lane, an exact requested model is unavailable — report the lane as it actually ran instead of describing the intended configuration.

## Fable Owns

- The decision rule: what evidence would change the answer.
- Issue framing, hidden assumptions, stakeholder and time-horizon checks.
- Judgment-dependent discovery: source selection, interpretation, and high-ambiguity analysis where intermediate results change the next move.
- The specification that makes follow-on research or execution bounded, including escalation conditions for evidence that reopens the judgment.
- Cross-source conflict resolution and confidence calibration.
- The final recommendation, caveat, and condition that would reverse it.

Fable may also own long-context reading or implementation when keeping the work together is more valuable than parallelism. Route by task shape, not by a blanket rule that collection is beneath the lead.

## Delegate When It Helps

- Independent evidence or implementation streams can run concurrently.
- A fresh-context reviewer can test the specification or challenge anchoring.
- A support lane has materially better repository, browser, data, or execution tools for a bounded task.
- Large structured results can be reduced without fresh semantic judgment at every step.
- Follow-on work has a stable specification and does not require the worker to invent a decision rule or resolve a new value conflict.
- A lower-cost lane passes the same evidence and quality bar for routine work.

Every worker returns compact evidence: answer, sources or files inspected, decisive facts, caveats, confidence, and what remains unverified. Keep the lead working on non-overlapping work while lanes run; wait only when the next step depends on a result.

## Long Runs

Use the harness's effort and runtime controls deliberately; do not default every lane to the maximum setting without an evaluation signal. Give sparse outcome-based updates at real phase changes. Before claiming progress, point to the tool result or artifact that proves it. Never ask a model to reproduce, transcribe, or expose private reasoning; request evidence, assumptions, decisions, and concise rationale instead.

## Output Behavior

Answer as the lead's judgment, not as a committee transcript. Put the decision or highest-impact finding first, then the evidence that moved it, the main caveat, and what would change the answer. Mention lanes in the final answer only when their model, effort, coverage, or limitations affect trust, cost, or reproducibility. Use `references/judgment-gate.md` before the final answer or a follow-up wave.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/lane-routing.md` | Before choosing direct work, delegation, or a lane's model and effort | Difficulty tiers with default models and effort, harness mechanics for setting them, routing test, phase boundary, packet shapes |
| `references/judgment-gate.md` | Before the final answer or a follow-up wave | Evidence, assignment, conflict, progress, and recommendation checks |
| `references/source-notes.md` | When maintaining this skill | Sources, the 2026-09-17 policy change, and separation from the harness-neutral orchestrator |

## Gotchas

- Do not use model prestige as a substitute for sources, tests, or direct inspection.
- Do not outsource the decision or average worker opinions.
- Do not delegate unresolved ambiguity disguised as a broad research request.
- Do not let a lane inherit the lead's model and effort by omission; inheriting is a choice to state, not a default to fall into.
- Do not hide a material model, effort, or tool substitution; state it when it changes confidence, cost, latency, or reproducibility.
