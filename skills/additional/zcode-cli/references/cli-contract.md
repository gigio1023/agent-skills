# Official Zcode CLI contract

Checked on 2026-10-14 against CLI `0.16.9` bundled with ZCode Desktop `3.15.1`, using Node `24.20.0`, and the [official source at `aac4755`](https://github.com/zai-org/ZCode/tree/aac4755666d09fdcd70272fcf063c077a639015f). The installed CLI's help controls which flags to use; a newer public source file is not proof that its flags exist in a packaged binary.

`--help`, `doctor --json`, and the model and effort help commands below were exercised successfully. Interactive login, model selection, a live model response, and provider billing were not verified for this package. The recipes describe the inspected interface, with authentication and a selectable model as prerequisites.

## Contents

- [Runtime discovery](#runtime-discovery)
- [Authentication](#authentication)
- [Model selection](#model-selection)
- [Task execution and permissions](#task-execution-and-permissions)
- [Failure interpretation](#failure-interpretation)

## Runtime discovery

Use an installed official `zcode` command when available:

```bash
command -v zcode
zcode_cmd=(zcode)
"${zcode_cmd[@]}" --help
"${zcode_cmd[@]}" doctor --json
```

On macOS, a Desktop installation may contain the official Node bundle without adding a command to PATH. After verifying the files exist, use this Bash or Zsh command array for the current task:

```bash
zcode_cmd=(node /Applications/ZCode.app/Contents/Resources/glm/zcode.cjs)
"${zcode_cmd[@]}" --help
"${zcode_cmd[@]}" doctor --json
```

This app layout can look for the built-in provider file under `Resources/glm/provider/` even though it ships under `Resources/config/provider/`. For that specific missing-file error, verify the following files and pass the supported paths to the process:

```bash
test -f /Applications/ZCode.app/Contents/Resources/config/provider/zcode-builtin.json
test -f "$HOME/.zcode/v2/provider_config.json"
zcode_cmd=(
  env
  ZCODE_BUILTIN_PROVIDER_CONFIG_FILE=/Applications/ZCode.app/Contents/Resources/config/provider/zcode-builtin.json
  "ZCODE_PERSONAL_PROVIDER_CONFIG_FILE=$HOME/.zcode/v2/provider_config.json"
  node /Applications/ZCode.app/Contents/Resources/glm/zcode.cjs
)
```

Stop if a required file is absent; do not fabricate a provider file or overwrite an existing one. These variables select configuration files. They do not authenticate an account, make a model selectable, or grant a subscription entitlement. `doctor` reports runtime and packaging facts, not those capabilities. Do not publish raw provider files or diagnostic output containing local account data.

## Authentication

Use the existing authentication first. When the task includes login setup, the installed help exposes normal browser authorization:

```bash
"${zcode_cmd[@]}" login zai
# For a BigModel account, use: login bigmodel
# Add --no-browser only when the user will open the printed authorization URL.
```

The TUI also exposes `/login`. Let the user complete normal browser authorization, then refresh the model catalog. A Desktop connection and a standalone CLI's usable provider catalog must be checked separately. Do not log out, change providers, copy credentials from the app, or rewrite a shared default merely to retry an unavailable model.

## Model selection

Inspect local help without submitting a model request:

```bash
"${zcode_cmd[@]}" --mode plan --prompt '/help model'
"${zcode_cmd[@]}" --mode plan --prompt '/help effort'
```

The installed dispatcher handles `/help` locally. This does not generalize to `--prompt '/model'`: that invocation did not select a model in the checked version.

Open the TUI in the intended workspace, with an explicit permission mode:

```bash
"${zcode_cmd[@]}" tui --cwd /absolute/path/to/workspace --mode plan
```

Inside the TUI, use the following sequence. Replace placeholders with values returned by this runtime:

```text
/model list
/model <provider-id>/<model-id>
/effort list
/effort <supported-level>
/model list
/effort list
```

Select an enabled catalog entry by its exact provider/model ID. A new model selection takes the catalog's default reasoning level; set the requested level afterward and read it back. `/effort` has the alias `/variant`. The [model handler](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/apps/zcode-cli/packages/cli/src/command-center/handlers/model.ts) rejects unavailable models, disabled entries, and unsupported reasoning levels. Selection can also remember a default for later sessions, so keep one owner for shared configuration and avoid concurrent selection changes.

The native selection has this shape:

```json
{
  "providerId": "<provider-id-from-catalog>",
  "modelId": "GLM-5.3",
  "options": { "reasoningLevel": "max" }
}
```

This is a data shape, not a standalone CLI flag or an instruction to edit a provider file. GLM-5.3's [inspected catalog](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/config/provider/zcode-builtin.json#L1024-L1045) supports `low`, `high`, and `max`; check the active catalog before using them. Other models can expose different options. `--mode` controls permissions and is unrelated to `options.reasoningLevel`. The installed top-level help exposes neither `--model` nor `--reasoning-effort`. A `defaultModelSelection` value in a file alone does not prove that the session resolved a usable model.

For structured automation, `app-server` exposes Zcode's versioned stdio protocol. Inspect the matching [protocol contract](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/docs/zcode-protocol.md) and its linked schemas before implementing a client. In the inspected source, the workspace config catalog and the conversation's current config are separate; V4 uses `switchModelConfig` through `v4/command`, and an accepted command is not final selection readback. Do not paste legacy `session/*` examples into a new client without checking compatibility. This package does not supply or claim to have exercised an app-server client.

## Task execution and permissions

Run the task in the selected TUI session, or resume its exact `sess_...` ID for a headless task. For example, after verifying the session and the configured tools are appropriate for reading a repository:

```bash
"${zcode_cmd[@]}" \
  --cwd /absolute/path/to/workspace \
  --resume sess_REPLACE_WITH_RETURNED_ID \
  --mode plan \
  --workflow-mode disabled \
  --disallowed-tools 'Bash,Edit,Write,ExitPlanMode' \
  --json \
  --prompt 'Read the README and summarize the setup requirements. Do not change files.'
```

The exclusions remove those whole tools for this run and leave saved settings unchanged. Comma-separated and space-separated names are supported. `Bash(git *)` removes all of Bash; it does not filter Bash commands. The example's four names do not cover every plugin or MCP tool, so inspect the configured tools and exclude effects outside the task's authority before launch.

Plan mode is not a security sandbox: the inspected [permission service](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/apps/zcode-cli/packages/core/src/permission/service.ts) also permits some non-destructive MCP and session-control operations. Use the host's enforced boundaries when the task needs containment. For edits that require approvals, use the TUI with `build` or an appropriately authorized mode; plain headless execution cannot supply an interactive approval response. A denied tool is a reason to use the proper approval interface, not to retry with `yolo` or `guarded`.

The installed `--prompt` default is `yolo`, so always specify the mode. Keep dynamic workflows disabled unless the task requires them. The public [headless permission broker](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/apps/zcode-cli/packages/cli/src/headless-workflow.ts) has workflow-specific approval behavior; do not treat an unattended mode as an authorization boundary.

Use `--attach <path>` only for authorized files; it can be repeated. `--continue` resumes the latest session for the directory, while `--resume` names one explicitly. Preserve process tracking and the exact returned session ID for follow-ups. Inspect the JSON result and errors rather than assuming that selecting `--json` establishes successful generation. The CLI and TUI may persist session data even during a task that does not edit project files.

## Failure interpretation

| Observation | Meaning and next action |
| --- | --- |
| Built-in provider file cannot be located | Check the bundle layout and supported path variables. |
| No selectable models | Check normal authentication and the runtime catalog. |
| `Select a model before continuing` | This session has no usable selection. Inspect its catalog and selection; the message alone does not establish the cause. |
| Requested reasoning level is unavailable | Use a supported value only with the caller's agreement to the changed choice. |
| A required tool is denied or needs approval | Use the authorized approval interface or report the blocked operation. |
| Timeout, nonzero exit, or no final response | Preserve the owned run's evidence and report incomplete execution. |

After a response, verify the requested artifact or answer independently. Record model and reasoning readback separately from response success. Neither one proves subscription billing; provider accounting needs its own evidence.
