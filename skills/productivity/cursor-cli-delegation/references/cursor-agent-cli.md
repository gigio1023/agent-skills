# Cursor Agent CLI Reference

## Contents

- Preflight and model selection
- Direct invocation
- Evidence and follow-ups
- Long runs and cancellation
- Maintenance evidence

## Preflight And Model Selection

From the intended workspace, inspect the installed CLI without changing configuration. Cursor's documentation names the executable `agent`, but another tool can own that name on PATH: on one macOS machine on 2026-09-16, Grok Build's installer relinked `~/.local/bin/agent` to its own binary, and Cursor answered only as `cursor-agent`. Resolve the executable first and use it in every later command:

```bash
cursor_cli=''
for candidate in agent cursor-agent; do
  command -v "$candidate" >/dev/null 2>&1 || continue
  case "$("$candidate" --version 2>/dev/null)" in
    grok*|'') continue ;;
  esac
  cursor_cli=$candidate
  break
done
"$cursor_cli" --version
"$cursor_cli" status
"$cursor_cli" --help
"$cursor_cli" models
```

Cursor's version string is a dated build such as `2026.09.08-6caf4ff`. If neither name reports one, stop and say which executable answered instead; do not launch a different vendor's CLI with Cursor flags.

Stop if the executable, authentication, requested model, or necessary capability is unavailable. Installation, login, configuration changes, and model substitutions need authorization. Preserve relevant version/model evidence privately; status output may include account details.

Default parent ID: `cursor-grok-4.6-xhigh-fast`. The locally observed listing and initialization label was `Cursor Grok 4.6 Extra High Fast`. An exact user-requested ID overrides this default. Verify the ID with the live account listing; do not repair malformed identifiers or silently route planning/judgment to another model. The listed xhigh profile selects the default effort; do not invent a separate thinking flag. Request-specific profiles or native overrides must be supported by current CLI evidence.

This default governs the external Cursor parent, not the calling harness or every internal child. Leave child selection to Cursor unless the user imposes a policy; then verify the exposed controls and returned evidence, and name unsupported requirements.

## Direct Invocation

Use native CLI commands, not a bundled launcher. A command-execution API that accepts an argument array avoids shell interpolation. When using a shell, quote each dynamic argument and never evaluate prompt content as code.

The following is a POSIX-shell headless example. Set `workspace` to the existing authorized workspace and `packet_path` to a secret-free UTF-8 task file outside the skill package. Short tasks may use a directly quoted prompt instead; a file is not mandatory.

```bash
model='cursor-grok-4.6-xhigh-fast'
workspace='/absolute/path/to/existing-workspace'
packet_path='/absolute/private/path/task.txt'
packet="$(<"$packet_path")"
"$cursor_cli" --print \
  --model "$model" \
  --workspace "$workspace" \
  --output-format stream-json \
  --yolo \
  -- "$packet"
```

This packet-loading syntax works in Bash and Zsh; use the host shell's equivalent elsewhere. The end-of-options delimiter protects a prompt beginning with an option. Embedded quotes, substitutions, and newlines in the quoted variable stay data; shell command substitution removes trailing newlines. If those newlines matter, use the host's argument-array capability and file-reading facility that preserves them. The CLI accepts the prompt positionally; never put secrets in it, even when loaded from a file.

Adapt the invocation using current CLI help and task authority:

| Need | Native choice |
| --- | --- |
| Different parent model | Replace `--model` with the verified exact requested ID |
| Narrower approvals | Omit `--yolo`; an approval block is not permission to bypass it |
| Explicit read-only or planning mode | Use the supported `--mode ask` or `--mode plan` |
| Related continuation | Add `--resume "$session_id"` with the actual returned ID |
| Another output or interaction style | Select a supported format or interactive mode when the host can drive it; adjust completion evidence accordingly |
| Additional native capability | Check current help, prerequisites, and effects; use it directly when authorized |

These are examples, not an exhaustive list or a new CLI abstraction. Keep general mode when no special mode was requested. Preserve sandbox configuration; do not add `--sandbox disabled`, extra workspace roots, blanket MCP approval, or workspace creation as incidental launch fixes.

The observed help describes `--yolo` as an alias of `--force` (“Run Everything”). Treat it as broad unattended command/tool approval. The task's actual authority and the host's stricter policies still apply.

## Evidence And Follow-ups

For headless structured runs, retain process exit status, initialization/model evidence when emitted, terminal result, and exact session identity. A valid session ID must be a nonempty string, and supplied IDs must agree across initialization, result, and an explicit resume request. Reject missing required evidence or conflicting identity rather than choosing whichever ID appears last. Check the current stream contract if its schema changes.

Preserve stdout and stderr using the host's capture facility. When persistent files are needed, create a private per-run directory outside the skill package and avoid overwriting earlier evidence. Save the process status before another shell command replaces it; avoid pipelines that conceal the CLI exit status. For large logs, inspect incrementally instead of loading the entire transcript. There is no required receipt schema or dependency on a custom parser. Logs may contain prompts, tool data, and thinking; share only reviewed evidence, not raw private traces.

For other supported interaction/output styles, use their documented completion and session surfaces. Do not infer success merely because a terminal marker from a different format is absent or because the CLI printed a plausible answer. Separate transport completion from the requested artifact's acceptance.

For a related follow-up, set `session_id` from the actual prior run, prepare the new instruction, and reuse the model/workspace choices as appropriate:

```bash
"$cursor_cli" --print \
  --model "$model" \
  --workspace "$workspace" \
  --output-format stream-json \
  --yolo \
  --resume "$session_id" \
  -- "$followup"
```

Retain any narrower approval or mode choice from the task. Recheck workspace state and carry forward relevant authority/constraints. Do not use bare `--resume`, `--continue`, or a latest-session shortcut when identity is ambiguous. A normal refinement is a valid continuation; resume is not limited to failed-check repair.

## Long Runs And Cancellation

Use the host's native background-process/session facility when available; retain its live handle and captured evidence. If it is unavailable, foreground execution is valid. A host call returning while work continues is not a task failure: inspect the same tracked invocation instead of launching another one. Set a deadline only when the task or host requires it, not as an arbitrary default for long work.

Cancel through a verified live process handle scoped to this invocation. Do not kill by executable name or signal a historical PID from a log. Use process-group cancellation only when the host established and still owns that group; a reaped/reused leader ID is not proof of ownership. If safe cancellation cannot be established, report that limitation rather than targeting unrelated work. Detached children and remote/MCP actions may continue after local exit; inspect relevant effects before resuming.

## Maintenance Evidence

Local syntax and model listing were checked on 2026-09-09. Initial preflight reported `2026.09.02-c22c1a3`; a later probe reported `2026.09.08-6caf4ff`. No install/update command was invoked, and the cause/timing of that transition was not established. Treat these as dated observations, not a guarantee of current CLI availability.

An earlier Python-assisted transport smoke used the exact default, YOLO, an empty temporary workspace, and a no-tools/no-writes task. Fresh and same-session runs succeeded without workspace changes. That helper has been removed; this evidence does not establish execution of the current direct-shell examples or behavior across calling harnesses. Sandbox configuration was already disabled during the earlier smoke, so it establishes no sandbox-enforcement claim.

Recheck installed help and the relevant official surface when changing syntax, permission rules, or stream handling:

- [CLI overview](https://cursor.com/docs/cli/overview)
- [Headless CLI](https://cursor.com/docs/cli/headless)
- [CLI parameters](https://cursor.com/docs/cli/reference/parameters)
- [Output format](https://cursor.com/docs/cli/reference/output-format)
- [Rules and MCP](https://cursor.com/docs/cli/using)
- [CLI subagents and skills](https://cursor.com/changelog/2-4)
- [Asynchronous and nested subagents](https://cursor.com/changelog/2-5)

Do not claim all sources were refreshed after checking one flag. Model/harness comparison runs and paid smoke tests require a separate request; static package validation is sufficient for this documentation-only maintenance unless a specific unresolved issue requires more.
