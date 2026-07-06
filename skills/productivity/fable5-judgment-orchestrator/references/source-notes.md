# Source Notes

Last updated: 2026-07-04.

This skill records a model-routing pattern where Fable 5 spends its context on
hard judgment rather than raw collection. It is intentionally separate from
`parallel-subagent-orchestrator`:

- `parallel-subagent-orchestrator` stays harness-neutral. It defines how to
  split work, write packets, synthesize evidence, and manage follow-up waves.
- `fable5-judgment-orchestrator` is model-routing policy. It defines which work
  Fable 5 should own and which work should be routed to configured support lanes
  for token efficiency.

When this skill is revised, preserve the core separation:

- Fable 5 owns final judgment, issue connection, critique, and missed-fact
  review.
- Workers gather compact evidence and run bounded checks.
- The final answer is Fable 5's synthesis, not a transcript of delegated lanes.
