---
name: zcode-cli
description: >
  Configure API-key access and run authorized tasks through Zcode's official CLI with an available model, supported reasoning options, and resumable sessions; use for "use Zcode CLI", "set up GLM with an API key in Zcode", "delegate this to Zcode", "Zcode GLM API key 설정", or "Zcode로 위임해줘". NOT for automatic model calls from a Zcode mention, reading stored conversations from another agent (read-agent-sessions), or delegation through Codex or Cursor.
---

# Zcode CLI

Set up the requested Zcode connection or run a task with an explicit model selection and permissions that match the request. Return the working connection, answer, or changed artifact with the observed session settings and evidence needed to check it.

## Working path

1. Establish the task, workspace, permitted effects, requested model and reasoning level, and expected result from the user's request. Inspection or discussion of this skill does not authorize a model call. Reuse existing authority for the requested work.
2. Locate the official CLI and inspect its version, `--help`, and `doctor --json`. Read [the CLI contract](references/cli-contract.md) for the verified commands, macOS bundled-runtime fallback, and version-specific limitations. Do not replace an installed official runtime with a community CLI merely because `zcode` is absent from PATH.
3. Inspect the runtime's available model catalog and authentication status through its supported interface. For API-key setup, read [the supplied-key recipe](references/cli-contract.md#supplied-api-keys), establish whether the key belongs to Coding Plan or the standard API, and use the matching template and access type. Ask for the intended service if the request does not establish it; the key's shape does not decide it. Preserve existing accounts and provider configuration, using a separate private profile when requested. A Desktop login, a stored default, and a successful `doctor` check do not establish usable model access.
4. Select the requested provider, model, and supported reasoning option for the intended session. Read back an existing session's selection before running the task. For a new headless session seeded from a private profile, follow [first-call verification](references/cli-contract.md#first-call-verification) and read back the returned session afterward. For another model, inspect its supported options instead of reusing GLM settings. If the user omits a choice, honor an established preference or reuse a valid existing selection; if neither exists, use the default below and ask for the model only when the catalog does not offer it. Do not silently substitute an unavailable requested model or reasoning level.
5. Choose the permission mode explicitly and apply supported tool exclusions where needed. Read-only work uses plan mode with the restrictions described in the reference. Editing uses the mode and approval interaction permitted by the task. Headless prompts default to `yolo` in the inspected version, so never omit `--mode` or broaden permissions to make an unattended run proceed.
6. Give Zcode a self-contained task with the relevant sources, allowed actions, preservation requirements, and expected answer or artifact. Run in the intended workspace and keep the exact session ID, process outcome, and relevant events. Use the host's process tracking for long work; do not confuse a running process with a completed task.
7. Check the result against the task: inspect cited sources for research, the actual diff and relevant checks for code, and the exact target after an authorized external write. A selected model, a success event, and a correct result are separate verification steps.

## Model and session choices

The scope is any model available through the user's Zcode runtime. The default is `GLM-5.3` at `max`, the level recommended for most tasks; use `high` when the user asks for it or the task is short and mechanical, and `low` for connection checks and smoke tests or on request. These defaults hold only while the active catalog offers them, and another model uses its own catalog options. Use the catalog's exact provider and model IDs, and the session's native reasoning field. Do not invent `--model` or `--reasoning-effort` flags from another CLI. Usage is metered in credits, each call carries a large fixed prompt, and bursts of requests hit a rate limit; read [usage limits](references/cli-contract.md#usage-limits) before planning many calls, and keep one Zcode run per account at a time.

Prefer the TUI for interactive selection and normal approvals. Use `app-server` when automation needs structured model discovery, session selection, and approval responses. A plain headless prompt can continue an already configured session, but its prompt text is not the TUI command dispatcher: passing `'/model'` as a prompt is not model selection.

Resume related work by its exact returned session ID after checking the workspace and selection again. Start a new session for independent work. Avoid `--continue` when concurrent work could make the latest session ambiguous, and never run two continuations of one session at once.

## Authority and records

Keep concurrent writers in separate authorized workspaces or assign disjoint files. A worktree isolates Git changes; it does not contain shell commands, MCP tools, network access, or shared Zcode state. Preserve the host's sandbox and approvals. A tool exclusion removes a whole named tool in this CLI; it is not a command-pattern allowlist.

Use the normal masked login flow or a supplied key in an authorized private provider profile. Do not extract Desktop credentials, copy private authentication headers, change entitlement flags, log secrets, or replace a provider to get past a failure. If authentication, model access, or a required permission cannot be established, stop the affected launch and report the observed error without guessing its cause. Retry only after an identified recoverable condition changes.

Prompts, attachments, and tool results may be sent to the selected provider and retained in Zcode's session storage. Keep credential values out of arguments and prompts. Keep task prompts and diagnostic logs outside this replaceable skill package, restrict access, and inspect them before sharing. Configuration changes, installs, login/logout, publication, and destructive actions need the corresponding task authority; a request to inspect models does not grant them.

## Completion

Return the requested answer or artifact first. Include the CLI version, requested and observed model selection, reasoning level when reported, permission mode, session ID, process or turn outcome, relevant validation, and any remaining blocker. Label a local selection readback as configuration evidence; claim a successful model call only after receiving its actual response. Do not infer subscription billing or entitlement from a model label or successful configuration write.

When maintaining this package, validate metadata, resource links, source-backed commands, and discovery. Documentation changes do not require paid model trials. Report package checks, exercised CLI operations, and live model execution separately.
