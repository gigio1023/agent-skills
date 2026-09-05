---
name: fable5-prompting-guide
description: >
  Use when writing, reviewing, simplifying, debugging, or migrating system
  prompts, agent instructions, tool descriptions, long-run scaffolding, or
  prompt stacks specifically for Claude Fable 5. Applies current guidance for
  effort, strong instruction following, boundaries, progress evidence,
  subagents, memory, context, and refusals. NOT for general Anthropic API setup,
  model selection, or deciding whether Fable 5 should lead a task.
---

# Fable 5 Prompting Guide

Build prompts that give Claude Fable 5 a clear reason, outcome, boundary, and evidence bar while leaving room for strong long-horizon judgment. Remove legacy micromanagement before adding model-specific scaffolding.

## Quick Start

1. Identify the target artifact and workload: new prompt, review, migration, tool contract, long-running agent, or failure diagnosis.
2. Define the observable outcome, why it matters, relevant context, authority boundary, evidence, output, and completion criteria.
3. For an existing prompt, inspect available traces or checks. Separate an observed failure from a suspected prompt cause; runtime availability alone does not authorize comparison runs.
4. Remove repeated rules, exhaustive behavior lists, stale thinking-budget instructions, aggressive tool triggers, and scaffolding for behavior Fable 5 already performs reliably.
5. Add brief, direct clauses only for real gaps. Use `references/prompt-patterns.md` for long-run, tool, memory, and communication patterns. Use `assets/prompt.template.md` for a new complex prompt.
6. Put effort, thinking display, timeout, fallback, compaction, and tool setup in the API or harness rather than pretending they are prompt instructions.
7. Validate the requested artifact. When model evaluation is requested, test the same cases at the intended effort and compare outcome correctness, evidence, scope control, latency, tokens, and cost.
8. Deliver the prompt, required runtime settings, and concise rationale. Request evidence and decisions, never a transcript of private reasoning.

Read `references/source-notes.md` when maintaining model-specific claims or API behavior.

## Core Prompt Shape

For complex work, keep these sections short and omit empty ones:

1. Role and larger purpose.
2. Goal and definition of done.
3. Context, inputs, and accepted evidence.
4. Scope, authority, and pause conditions.
5. Tools, delegation, memory, and progress behavior.
6. Output and user communication.
7. Validation, fallback, and stop rules.

Give the reason behind important instructions. Fable 5 uses intent to resolve ambiguity and connect work across long-running streams.

## Model-Specific Rules

### Use Strong Instruction Following

Prefer one clear instruction over a taxonomy of prohibited variants. If a prompt lists every way to be verbose, pause, or overbuild, replace it with the desired behavior and completion bar. Remove contradictions before adding emphasis.

When enough information exists, instruct the model to act. Ask for a recommendation when judgment is needed, not an exhaustive survey of options that will not be pursued.

Contract steps, not cognition steps. Use numbered steps only when order or completeness is part of the task's correctness: prerequisite retrieval, approval boundaries, required artifact stages, validation, or an externally auditable pipeline. Otherwise state the outcome, invariants, and stopping condition and let the model choose the path. Fable 5 follows short instructions strongly — a misdesigned procedure is followed just as faithfully, so every step must earn its place.

### Bound Scope at High Effort

Fable 5 can explore and improve beyond the request, especially at higher effort. State what the task authorizes and what it does not. Distinguish assessment from implementation and reversible in-scope work from destructive, irreversible, or scope-expanding action.

Do not require permission for every routine step. Pause only for real user input, material scope changes, or consequential actions that need confirmation.

### Ground Progress and Completion

For long autonomous work, require every progress claim to point to a current tool result or named artifact. Failed, skipped, and unverified checks must remain visible. A plan, a changed file, or the model's confidence is not completion evidence.

### Design Long Runs as a Harness Problem

Hard tasks may take minutes or hours. Configure timeouts, streaming, asynchronous status, and resumability in the harness. Give the prompt sparse checkpoint rules instead of forcing narration after every tool call.

When the user must receive exact content mid-run, provide a dedicated send-to-user tool and tell the model when to call it. Do not route narration or reasoning through that tool.

### Delegate Independent Work

Fable 5 can manage sustained subagent collaboration. Delegate when work is independent, context isolation helps, a specialist tool matters, or a fresh verifier reduces anchoring. Prefer asynchronous coordination and continue useful lead work while subagents run.

Do not turn every task into a committee. Keep dependent judgment with the lead and synthesize results before acting.

### Use Durable Memory Selectively

Give long-running agents a place to store corrections, confirmed approaches, decisions, and state that must survive sessions. Keep one lesson per record with a short summary. Do not duplicate the repository or chat history, and update or delete stale memory.

Use compaction for in-session continuity and memory or state artifacts for facts that must survive summarization or a fresh session.

### Keep Final Communication Reader-Facing

After a long run, write the final response as a re-grounding for someone who did not see the tool loop. Lead with the outcome, reintroduce necessary vocabulary, use complete sentences, and explain the one or two user actions that remain.

### Keep Thinking Controls in the Runtime

Fable 5 always uses adaptive thinking. Do not set manual extended-thinking budgets or ask the prompt to reveal its reasoning. Use the effort parameter for depth and the supported thinking display setting for product-visible summaries.

Request concise rationale, assumptions, evidence, and decisions. Instructions to echo or transcribe reasoning can trigger reasoning-extraction safeguards.

### Handle Refusals as API State

The application must handle `stop_reason: "refusal"`, including any configured fallback and user-facing behavior. Do not attempt to prompt around safeguards. Keep fallback routing, billing, and retry behavior in the integration.

## Effort and Evaluation

Create evaluation fixtures or run additional model sessions only on request. A static review may deliver revised wording with an untested-behavior caveat; it does not need a new benchmark to finish.

Use `high` as the initial default for most substantial tasks, `xhigh` for the most capability-sensitive workloads, and `medium` or `low` for routine or interactive work. Lower effort when the model succeeds but spends too long or gathers unnecessary context. Raise it only when representative evals show a useful gain.

Use two to five positive cases and one or two near misses. Include at least one long-run case when the prompt governs tools, state, or subagents. Grade the final environment or artifact, not only the transcript.

## Output Contract

For a new prompt, return the final prompt plus the runtime settings and tools it assumes. For a review, lead with the most consequential issue and provide a minimal revision. For a migration, separate removed legacy scaffolding, added Fable 5-specific clauses, and API or harness changes. State when live Fable 5 evals were unavailable.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/prompt-patterns.md` | Writing or revising a non-trivial Fable 5 prompt | Prompt clauses, long-run scaffolding, runtime controls, migration, and failure patterns |
| `references/source-notes.md` | Maintaining model-specific claims | Official Anthropic sources and durable translations |
| `assets/prompt.template.md` | Starting a new complex prompt | Compact fill-in prompt skeleton |

## Gotchas

- Do not preserve old scaffolding merely because it once improved a weaker model.
- Do not expose token countdowns unless the harness requires them; they can encourage premature wrap-up in very long sessions.
- Do not ask Fable 5 to reproduce hidden reasoning or summarized thinking.
- Do not use manual `budget_tokens`; current Fable 5 thinking is adaptive.
- Do not treat a text-only promise to act as completed work.
- Do not overdelegate tightly coupled work or block on each subagent immediately.
- Do not use memory as a second copy of the repository or conversation.
- Do not hide a refusal or fallback that changes confidence or reproducibility.
