# Goal Prompting Source Notes

Last reviewed: 2026-08-03.

## Contents

- Official OpenAI sources
- Official Anthropic sources
- Public skill prior art
- Adopted design decisions
- Rejected assumptions
- Maintenance notes

## Official OpenAI Sources

- [Long-running work](https://learn.chatgpt.com/docs/long-running-work) documents Codex Goal mode, the outcome/constraints/verification contract, steering, parallel chats, and unchanged permission boundaries.
- [Prompting](https://learn.chatgpt.com/docs/prompting) distinguishes goal, context, output, and boundaries, recommends result-first prompts, and routes unsettled multi-step Codex work through plan mode before Goal mode.
- [Codex slash commands](https://learn.chatgpt.com/docs/reference/slash-commands) documents `/goal` lifecycle commands and the 4,000-character objective limit.
- [Codex App Server](https://developers.openai.com/codex/app-server) documents persisted thread goal state, status and budget updates, usage accounting, and the same 4,000-character limit.
- [OpenAI `define-goal` skill](https://github.com/openai/skills/blob/main/skills/.curated/define-goal/SKILL.md) emphasizes measurable objectives, evidence, bounded scope, active-goal inspection, and explicit activation intent.
- [Build skills](https://learn.chatgpt.com/docs/build-skills) documents the shared Agent Skills format, progressive disclosure, discovery descriptions, and instruction-first packaging used by this skill.

## Official Anthropic Sources

- [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal) documents the v2.1.139 minimum, separate evaluator loop, transcript-only evidence, one active goal per session, optional run bounds, the 4,000-character condition limit, resume behavior, and hook or trust prerequisites.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices) recommends checks Claude can run, evidence over assertions, exploration and planning before risky implementation, specific context, and concise interviewing for larger work.
- [Claude Code prompt library](https://code.claude.com/docs/en/prompt-library) favors outcomes over prescribed steps and treats saved skills as reusable versions of successful prompt patterns.
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) supports concise skills, trigger-focused descriptions, progressive disclosure, one-level references, appropriate degrees of freedom, and real-usage iteration.

## Public Skill Prior Art

The review sampled original or materially distinct public packages rather than counting the many repositories that copy OpenAI's `define-goal` unchanged.

| Skill | Useful pattern | Limitation for this package |
| --- | --- | --- |
| [OpenAI `define-goal`](https://github.com/openai/skills/tree/main/skills/.curated/define-goal) | Concise outcome, evidence, scope, and explicit goal creation | Codex goal tools only; does not explain or translate Claude Code semantics |
| [techwolf-ai `goal-prompt`](https://github.com/techwolf-ai/ai-first-toolkit/tree/main/plugins/session-tools/skills/goal-prompt) | Compact Claude condition with transcript-demonstrable proof | Draft-only and Claude-specific |
| [nbbaier `goal-refiner`](https://github.com/nbbaier/agent-skills/tree/main/skills/goal-refiner) | Realistic environment, false-completion checks, cleanup, and 4,000-character guard | Codex-only and can overfill bounded goals with a large fixed template |
| [xopc `define-goal`](https://github.com/xopcai/xopc/tree/main/skills/engineering/define-goal) | Small rewrite of the official pattern with an objective rubric | Harness metadata and persistent-goal-only scope |
| [zdx `define-goal`](https://github.com/tallesborges/zdx/tree/master/crates/zdx-assets/bundled_skills/define-goal) | Read-only shaping and honest quantitative defaults | Requires confirmation and does not support activation or cross-harness translation |
| [dxiiren `define-goal`](https://github.com/dxiiren/python-bootcamp-projects/tree/main/.claude/skills/define-goal) | File-backed work lists, terminal statuses, and resume discipline for very large runs | Claims the evaluator re-reads the goal file, which conflicts with Anthropic's transcript-only evaluator contract; also mandates an exhaustive interview and file system |
| [alirezarezvani `fable-goal`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/fable-goal/skills/fable-goal) | Extracts intent from rough input, verifies named resources, and avoids implementation micromanagement | Assumes broad autonomy, internet, deployment, subagents, and no questions until completion |
| [krzemienski `goal-condition-architect`](https://github.com/krzemienski/shannon/tree/main/skills/goal-condition-architect) | Transcript-provable checks, adversarial false-completion review, and explicit bounds | Makes fixed check counts, generic anti-cheat rules, and a bound mandatory for every task |
| [alfredolopez80 `goal-refiner`](https://github.com/alfredolopez80/codex-ralph-vault-loop/tree/main/.agents/skills/goal-refiner) | Quick, file-backed, and audit modes with evidence and approval gates | Generates several durable artifacts and extensive scaffolding by default for uncertain risk |
| [win4r `goal-prompt-builder`](https://github.com/win4r/goal-prompt-builder/tree/main/goal-prompt-builder) | Project inspection, scenario-aware checks, and copy-paste output | Requires interviews, fixed sections, and token budgets while relying on undocumented internal-version assumptions |
| [agentara `mega-goal-prompt`](https://github.com/agentara/skills/tree/main/skills/productivity/mega-goal-prompt) | Explicitly names Claude Code and Codex and gathers outcome, context, evidence, and boundaries | Treats both harnesses as one runtime and mandates a large interview-driven prompt |

GitHub code search also surfaced many copies of OpenAI's skill and narrower orchestration stacks. Copy count was not treated as independent evidence. The useful consensus was measurable completion, visible proof, bounded scope, and an explicit distinction between prompt authoring and execution.

## Adopted Design Decisions

- One portable skill supports explain, draft, review, translation, and explicit activation. This matches the user's need for advice in either harness and handoff text from either harness to the other.
- `goal-prompting` is broader and more durable than `define-goal`, which implies creation only and collides with OpenAI's narrower skill.
- The shared core uses outcome, context, verification, constraints, scope, and stop or escalation as optional fields rather than a mandatory template.
- Direct goal payloads remain below 4,000 characters for both current targets.
- Long detail may live in a file, but completion evidence must still be surfaced in the conversation. A file is context, not evaluator-visible proof.
- Activation requires explicit user intent and an agent-callable goal capability in the current session. Claude Code `/goal` handoffs return command text for the user to submit. Advice, review, and copy generation remain non-mutating.
- The package is instruction-only. Drafting and translation require contextual judgment; a generator script would not remove the hard work. Character count can use ordinary runtime tools only when a draft approaches the limit.

## Rejected Assumptions

- The two `/goal` commands are not treated as identical. Claude Code documents a separate transcript-only evaluator; Codex documents a persisted objective that is both the initial request and completion criterion.
- An evaluator is never assumed to open a referenced goal file or rerun a check.
- Token, turn, time, and cost bounds are not conflated. Codex token budgets are supplied only on explicit request; Claude turn or time clauses remain optional.
- “Never ask the user” is not used because permissions, missing access, unsafe operations, and product decisions can require escalation.
- Universal anti-cheat clauses, fixed check counts, mandatory clean worktrees, mandatory status ledgers, and exhaustive interviews were rejected. They add friction and can conflict with legitimate tasks or existing user changes.
- Model names, effort levels, subagent topology, hooks, permission modes, and install paths stay outside the portable core unless a target reference must explain a verified runtime fact.

## Maintenance Notes

Recheck the two goal-mode pages, slash-command limits, and native goal-state contracts before changing target behavior. Keep current runtime details in the two harness references. Preserve the shared contract unless a semantic change affects both targets.

Community skills evolve quickly and may copy one another. Re-sample original packages and compare claims against official documentation before adopting new rules. Treat undocumented internal prompt names, version gates, and evaluator behavior as unverified until a public source or current runtime confirms them.
