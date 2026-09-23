# Host Notes

When Opus 5.5 runs inside an agent harness, the harness already owns some of the layers the official guidance addresses. This reference says which ones, and what an author of CLAUDE.md, skills, subagent definitions, or output styles can still change. Claude Code facts come from its documentation as of 2026-09-23 unless marked observed; observed items come from one Claude Code 2.1.280 session on macOS and can change with any release.

## Claude Code And The Agent SDK

### Already Handled By The Harness

- **Append-only history.** Anthropic's migration guide states that Claude Code, claude.ai, Claude Managed Agents, and the Claude Agent SDK already keep conversations append-only, so thinking blocks stay valid without author action.
- **Pasted-text marking (observed).** The 2.1.280 system prompt carries a note on `<pasted_content>` tags equivalent to the official one.
- **Silence reminders (observed).** During long tool-calling stretches, the harness appended a one-line reminder asking the model to tell the user what it is doing, matching the official turn-scoped reminder.

Do not restate these in CLAUDE.md, skills, or output styles. A second copy adds context without changing behavior, and a paraphrase can conflict with the harness's own wording.

### Settings An Author Controls

- **Model alias.** From v2.1.280, the `opus` alias resolves to Opus 5.5 on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, and Google Cloud's Agent Platform; before that it resolved to Opus 5 from v2.1.219. On Microsoft Foundry, `opus` resolves to Opus 4.6. Opus 5.5 requires v2.1.280 or later. A subagent definition with `model: opus` changed models when the alias moved; pin `claude-opus-5-5` or set `ANTHROPIC_DEFAULT_OPUS_MODEL` when the version matters. See [model configuration](https://code.claude.com/docs/en/model-config).
- **Effort.** Opus 5.5 starts at `medium`. A top-level `effortLevel` in `~/.claude/settings.json` keeps applying to Opus 5, Fable 5.1, and earlier models, but Opus 5.5 and later models ignore it. Set a level per model under [`modelSettings`](https://code.claude.com/docs/en/settings-reference#modelsettings) (v2.1.251 or later), for example `{"modelSettings": {"claude-opus-5-5": {"effortLevel": "high"}}}`, or cap one model with `maxEffortLevel` (v2.1.267 or later). Neither key accepts `max`. The `ultracode` setting sends `xhigh` and adds workflow orchestration.
- **Subagent effort.** A subagent definition's `effort` frontmatter overrides the session level; without it, the subagent inherits the session's. Available levels depend on the model. See [subagents](https://code.claude.com/docs/en/sub-agents).
- **Delegation caps.** `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (20 concurrent by default), and the SDK's `max_budget_usd` option, which need Claude Code 2.1.217 or later. Anthropic's Opus 5 page notes that Claude Code adds its own delegation instruction on Opus 5 only under its `claude_code` system prompt preset; with a custom or omitted system prompt in the SDK, supply delegation criteria yourself.

### Writing Instructions That Run On Opus 5.5

- **CLAUDE.md, skills, and output styles.** Apply the removal list in `SKILL.md`. Leave out instructions to think carefully, to write reasoning into the response, and to add verification passes. Keep scope, completion conditions, and project facts.
- **Interactive sessions** have a person present. Leave out the unattended stop policy, which would suppress the check-ins that person relies on.
- **Headless runs,** such as `claude -p`, scheduled tasks, background agents, and CI, are unattended. The stop policy and an explicit completion condition fit there. Test in the same mode the run will use.
- **Subagent definitions and delegation prompts.** A subagent returns only its summary to the parent when its turn ends. Inference, not yet observed: if an Opus 5.5 subagent ends its turn on a progress note, that note becomes its result and reports a next step it never took. State the completion condition and what the final message must contain (result, evidence, open items, blocker), and have the lead treat a result that announces pending work as incomplete and resume the subagent rather than accept it. Confirm with a trace before hardening this into a rule. A stop policy belongs in the definition body so it is present from the subagent's first request.

## Other Harnesses

Cursor, OpenCode, Hermes, Codex reaching Claude through a proxy, and custom agent loops differ in whether they render progress-update thinking blocks, treat a text-only end of turn as completion, mark pasted text, or keep history append-only. Before adding a clause, check each of those layers in that harness's documentation or in a trace. Do not assume Claude Code's behavior carries over.
