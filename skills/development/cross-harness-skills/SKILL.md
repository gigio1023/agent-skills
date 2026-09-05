---
name: cross-harness-skills
description: >
  Use when creating, reviewing, or modernizing one agent skill that must work in
  both Claude Code and Codex, especially when reconciling GPT-6 Astra,
  GPT-5.6-series, and Claude Fable prompting guidance, separating instructions from
  harness adapters, or testing the same skill across both runtimes. NOT for a
  single-harness extension or ordinary skill creation without a portability
  requirement; use skill-builder alone.
---

# Cross-Harness Skills

Build one portable skill core for Claude Code and Codex without flattening their different model and runtime behavior into vague advice. The common `SKILL.md` defines the task contract. Harness-only invocation, metadata, hooks, permissions, and path features stay in adapters or installation documentation.

## Quick Start

1. Classify the request. A review-only request returns findings and does not edit files; a create, improve, or modernize request authorizes in-scope edits.
2. Identify the intended model in each harness from the request or active configuration; do not substitute a model merely because this guide names it. Record unavailable combinations rather than treating one successful run as proof for both.
3. Read `references/model-prompting-contract.md` for the shared prompt contract and the model-specific behaviors that must not leak into domain skills.
4. Read `references/harness-portability.md` before using a path, invocation syntax, tool name, frontmatter key, hook, subagent feature, or environment variable.
5. Write the portable core first. Add only domain knowledge, fragile procedure, authority boundaries, evidence requirements, output preservation, and real stop or fallback rules.
6. Move a capability into an adapter when the other harness cannot interpret it with the same meaning. The core must still complete correctly without that adapter.
7. Apply `references/review-gate.md` to the package and its directly linked resources. In change mode, patch measured defects; do not rewrite a passing skill to mention model names.
8. Validate packaging and changed executable resources. Run model comparisons only when requested; reuse existing traces when available and distinguish static findings from behavior exercised in either harness.

## Portable Prompt Contract

Keep the normal path compact and include only fields that change behavior:

- **Outcome and intent:** the user-visible result and why it matters when that context changes decisions.
- **Success:** required artifacts, facts, evidence, and observable done state.
- **Authority:** distinguish answer/review/diagnosis from build/change, and name external, destructive, irreversible, or scope-expanding actions separately.
- **Constraints:** domain invariants, preservation requirements, safety limits, and exclusions. Use exact steps only where order or syntax is genuinely fragile.
- **Routing:** describe required capabilities and decision rules, not a built-in tool name. Keep sequential execution valid; parallel work is an optimization.
- **Validation:** the smallest test, render, source inspection, or evidence gate that proves the result.
- **Output:** what the reader needs to decide or continue, including material caveats and next actions.
- **Stop and fallback:** when enough evidence exists, when to retry, and which missing input genuinely blocks completion.

Do not force this list into eight headings. Use the smallest structure that makes the contract unambiguous for the task.

## Shared Frontier-Model Rules

- Start from the smallest prompt that preserves the task and passes applicable checks. Remove repeated rules, generic competence reminders, obsolete examples, and routine process narration.
- Lead with the outcome. Preserve required facts, artifacts, evidence, caveats, and actions; remove repetition and options not pursued before compressing them.
- Use decision rules for contextual work and deterministic scripts or exact commands for fragile work. A bare `MUST` without a mechanism is rarely useful.
- Define request authority once. A review is not authorization to edit; a change request normally includes in-scope local edits and non-destructive validation.
- Ground progress and completion in current tool results or named artifacts. Visible updates belong at real phase changes, not after routine calls.
- Request evidence, assumptions, decisions, and concise rationale. Never request hidden reasoning, chain-of-thought, reflection transcripts, or scratchpads.
- Use direct work when results affect the next decision. Use deterministic reduction for bounded structured data, and optional parallel workers only for independent work, context isolation, specialized capability, or fresh review.
- Tune model effort, long-run memory, programmatic tool calling, and asynchronous agents in the runtime or harness layer after evaluation, not as domain defaults.

## Adapter Boundary

Portable core examples:

- `name` and `description` frontmatter only;
- forward-slash relative resource paths;
- “read the file”, “search the repository”, or “run the bundled validator”;
- a script invocation documented from the skill root;
- optional parallelism with a sequential fallback.

Adapter-only examples:

- `/skill-name`, `$skill-name`, or another invocation syntax;
- `.claude/skills`, `.agents/skills`, or user-install locations;
- Claude Code dynamic command injection, `${CLAUDE_SKILL_DIR}`, hooks, `context: fork`, `allowed-tools`, or invocation-control frontmatter;
- Codex `agents/openai.yaml`, plugin dependencies, config, approval, or UI policy;
- hard-coded built-in tool or subagent names from either harness.

A side-effecting workflow must remain safe when adapter metadata is absent. Put the authority boundary in the portable body; use an adapter only as additional enforcement or user experience.

## Evaluation Contract

Run this evaluation only when the user explicitly requests one — it is not a prerequisite for ordinary skill work (skill-builder's scope rule governs). When requested, use the same representative repository state, artifacts, prompts, and rubric in both primary targets. For an existing skill compare:

1. target model and harness without the skill;
2. target model and harness with the current skill;
3. target model and harness with the candidate.

Include positive triggers, adjacent near-misses, a normal execution, an evidence failure, and an authority-boundary case. Record tool availability and effort settings. Structural validation cannot substitute for behavioral testing, and a Claude Code pass cannot stand in for a Codex pass.

## Output Contract

For a review, lead with findings and state that files were not changed. For a change, report the portable contract, adapter split, accepted changes, validations actually run in each harness/model pair, and untested cells. If only static or script validation was possible, say so plainly.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/model-prompting-contract.md` | Writing or simplifying instructions | GPT-5.6/Fable synthesis, differences, and portable prompt pattern |
| `references/harness-portability.md` | Using paths, metadata, tools, invocation, or parallel features | Claude Code/Codex loading and adapter matrix |
| `references/review-gate.md` | Reviewing a new or existing package | Per-skill audit, evaluation matrix, and acceptance gate |

## Gotchas

- Portable does not mean vague. Preserve precise domain contracts and exact safety or schema rules.
- Do not copy every recommendation from both model guides into the core; keep only their task-specific intersection and isolate divergent runtime controls.
- XML prompt structure can help a complex Claude API template, but it is not a universal filesystem-skill requirement.
- Do not rely on Claude-only metadata to protect a side effect or on Codex-only policy to make a workflow safe.
- Do not add a wrapper script when the hard part remains contextual judgment.
- A smaller candidate wins only after required behavior and evidence still pass.
