# Source Notes

Reviewed 2026-09-23.

## Anthropic Sources

| Source | Owns | Used in |
| --- | --- | --- |
| [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | 5.5 behavior and prompting patterns, indexed by observed symptom | Symptom patterns for 5.5, the removal list |
| [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) | Opus 5 behavior; named by the 5.5 page as the starting point | Carried-from-Opus-5 patterns, the removal list |
| [What's new in Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) | Breaking changes, feature support, behavior differences, pricing, availability | Runtime and migration |
| [Migrating to Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide) | Code changes and checklists by source model; the `claude-api` skill pointer | Runtime and migration |
| [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) | Levels, per-model defaults, per-message effort | Runtime and migration, the effort paragraph in `SKILL.md` |
| [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback) | Refusal categories and fallback | Refusals |
| [Preserved thinking](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking), [Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages), [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) | Thinking-block binding, append-only history, turn-scoped messages, progress-update blocks | Runtime and migration, silent-turn pattern |
| [Models overview](https://platform.claude.com/docs/en/models/overview) | Model recommendation, IDs, cache pricing notes | Runtime and migration |
| [Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) | Advisory token budgets | Agent-team pattern pointer |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config), [settings](https://code.claude.com/docs/en/settings-reference), [subagents](https://code.claude.com/docs/en/sub-agents) | Alias resolution, effort resolution, `modelSettings`, subagent `effort` and caps | Host notes |

## Observations

- 2026-09-23, Claude Code 2.1.280 on macOS, observed from inside one Opus 5.5 session: the system prompt carried a `<pasted_content>` note equivalent to the official one, and the harness appended a one-line silence reminder several times during long tool-calling stretches. These are single-session observations, not documented guarantees.

## Interpretation Limits

- Anthropic's measured claims, including 5.5 at `medium` matching Opus 5 at `high`, roughly halved silent stretches, multi-app completion gains, and faster chat replies, come from Anthropic's testing. They are not measurements of this package or of any particular workload.
- The clauses in `symptom-patterns.md` are original adaptations that keep the function Anthropic describes; they are not Anthropic's text. The package links each official section instead of copying its snippets. When a clause's effect is in doubt, re-read the official wording and test both.
- The 5.5 page calls the Opus 5 patterns a reasonable starting point but does not restate them. Which Opus 5 behaviors persist on 5.5 is untested here, which is why those clauses require an observed symptom first.
- The subagent early-stop concern in `host-notes.md` is an inference from how Claude Code returns a subagent's final message, not an observed failure.

## Shared With The Fable Guide

These runtime facts also appear in `fable5-prompting-guide`; when either package changes one, update the other: thinking cannot be disabled and manual budgets are rejected; forced `tool_choice` returns 400; thinking blocks are bound to model and conversation, so history must be append-only; `thinking.display: "updates"`; turn-scoped system messages; per-message effort; server-side fallback.

Behavior is not shared. Fable 5.1 sends fewer progress updates during tool runs and tends toward one tool call per turn in loops where the next reads are implied; Opus 5.5 sends updates that can end the turn and thinks more per turn at a given effort level. Keep each model's behavioral clauses in its own package.

## Maintenance

Recheck the 5.5 prompting page, the Opus 5 prompting page, the what's-new page, the migration guide, and the effort page together. The prompting pages own behavior; the what's-new, migration, and effort pages own API facts; the Claude Code documentation owns host facts. Beta header names live only in the table in `runtime-and-migration.md`. When a Claude Code release changes alias resolution, effort precedence, or what the harness injects, update `host-notes.md` and mark whether each item is documented or observed.

Record the pages and sections actually re-read. Updating the review date does not refresh every claim. Keep the failure condition and evidence for any workaround so a later model or harness change can justify removing it.
