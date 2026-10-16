# Official Zcode CLI contract

Checked on 2026-10-14 against CLI `0.16.9` bundled with ZCode Desktop `3.15.1`, using Node `24.20.0`, and the [official source at `aac4755`](https://github.com/zai-org/ZCode/tree/aac4755666d09fdcd70272fcf063c077a639015f). The installed CLI's help controls which flags to use; a newer public source file is not proof that its flags exist in a packaged binary.

`--help`, `doctor --json`, and the model and effort help commands below were exercised successfully. Headless requests with a private Coding Plan API-key profile returned model responses and exit 0; persisted session selections confirmed GLM-5.3 with `options.reasoningLevel: "max"`. This verifies the runtime selection and successful calls. Interactive login and the standard API template were source-inspected, not exercised with a live key. Server-side reasoning behavior and provider billing were not measured.

## Contents

- [Runtime discovery](#runtime-discovery)
- [Authentication](#authentication)
- [Supplied API keys](#supplied-api-keys)
- [First-call verification](#first-call-verification)
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

For an existing setup, stop if a required file is absent. When API-key setup is requested, create a valid private profile through the recipe below and point the personal-file variable at it; preserve existing configuration. These variables select configuration files. They do not authenticate an account, make a model selectable, or grant a subscription entitlement. `doctor` reports runtime and packaging facts, not those capabilities. Do not publish raw provider files or diagnostic output containing local account data.

## Authentication

Use the existing authentication first. When the task includes login setup, the installed help exposes normal browser authorization:

```bash
"${zcode_cmd[@]}" login zai
# For a BigModel account, use: login bigmodel
# Add --no-browser only when the user will open the printed authorization URL.
```

The TUI also exposes `/login`. Let the user complete normal browser authorization, then refresh the model catalog. A Desktop connection and a standalone CLI's usable provider catalog must be checked separately. Do not log out, change providers, copy credentials from the app, or rewrite a shared default merely to retry an unavailable model.

### Supplied API keys

When the user supplies a key for setup, use the normal path for the intended service. For a Coding Plan key, open TUI `/login`, choose **Z.AI Coding Plan API Key**, and use the [masked input](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/apps/zcode-cli/packages/cli/src/command-center/login-flow.ts#L39-L57). Keep the key out of process arguments, ordinary prompts, and logs. This route saves a credential and default provider/model; it does not set reasoning effort or validate model access. Select and read back the requested effort afterward.

For a personal provider, establish which service the user intends, then choose the matching [built-in template](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/config/provider/zcode-builtin.json#L6-L74). A key's format does not establish the service or its billing:

| Service | Template | Access type |
| --- | --- | --- |
| Z.AI Coding Plan | `zai-api` | `zhipu-coding-plan-api-key` |
| Standard Z.AI API | `zai-standard-api` | `api-key` |

For an authorized Coding Plan API-key setup, create a private profile outside the repository with a directory mode of `0700` and file mode of `0600`, or merge the following fields into an existing profile while preserving unrelated rules. Create new private files under `umask 077`; do not first write a key into a publicly readable file. Replace the synthetic provider ID and key placeholder privately. The template supplies the API endpoint and built-in model membership, so this recipe needs no `personalModelIds` override.

```json
{
  "schemaVersion": 1,
  "config": {
    "providerConfigRules": {
      "providerRules": [
        {
          "providerId": "zai-coding-plan-example",
          "templateId": "zai-api",
          "enabled": true,
          "config": {
            "group": "standard-personal",
            "access": {
              "type": "zhipu-coding-plan-api-key",
              "apiKey": "<SUPPLIED-KEY-PRIVATE-ONLY>"
            }
          }
        }
      ]
    },
    "modelConfigRules": { "providerModelRules": [], "manualProviderModelRules": [] },
    "defaultModelSelection": {
      "providerId": "zai-coding-plan-example",
      "modelId": "GLM-5.3",
      "options": { "reasoningLevel": "max" }
    }
  }
}
```

For the standard Z.AI API, use the same profile structure with `templateId: "zai-standard-api"` and `access.type: "api-key"`. Keep `group: "standard-personal"`, use one matching provider ID in the rule and default selection, and choose the model and effort from that template's active catalog. Do not change only an endpoint or assume that a Coding Plan login configures standard API access. The standard template was source-checked; the live verification above used Coding Plan.

Set `ZCODE_PERSONAL_PROVIDER_CONFIG_FILE` to the private file for each invocation, together with the verified built-in config path. The configured default can seed a new session after the provider is admitted; it does not change a resumed session's saved selection. Do not place the key itself in command arguments.

`config.group: "standard-personal"` is required for this personal provider to become executable. The [partial rule schema](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/packages/provider/src/config/rule-data-schema.ts#L103-L118) permits omission while editing, but the [complete provider schema](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/packages/provider/src/config/provider-data-schema.ts#L90-L94) requires a group and the template does not supply one. Syntax acceptance therefore does not establish registry admission. In the checked run, adding this group changed the same headless request from `Select a model before continuing`, exit 1, to a response, exit 0.

For other providers, follow the [versioned file codec](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/packages/provider-node/src/provider-config-file-codec.ts), retain supported template/access types, and use model IDs and reasoning options from the catalog. The [access schema](https://github.com/zai-org/ZCode/blob/aac4755666d09fdcd70272fcf063c077a639015f/packages/provider/src/config/provider-data-schema.ts#L28-L37) accepts an `apiKey` string and exposes no environment-variable or secret-reference field; do not invent `apiKeyEnv`, `apiKeyRef`, or `${ENV_VAR}` interpolation. The file contains credential material and belongs outside Git. A stored key and default selection still need model/effort readback and an actual response before reporting a working setup.

### First-call verification

A request for a working connection includes a minimal response check. A request only to inspect this skill or prepare configuration does not authorize a model call. For the verified macOS bundle, rebuild the command array with the private profile path; an earlier array containing a different personal-file value would override an environment prefix:

```bash
zcode_profile=/absolute/private/path/provider_config.json
test -f "$zcode_profile"
zcode_cmd=(
  env
  ZCODE_BUILTIN_PROVIDER_CONFIG_FILE=/Applications/ZCode.app/Contents/Resources/config/provider/zcode-builtin.json
  "ZCODE_PERSONAL_PROVIDER_CONFIG_FILE=$zcode_profile"
  node /Applications/ZCode.app/Contents/Resources/glm/zcode.cjs
)
"${zcode_cmd[@]}" \
  --cwd /absolute/path/to/workspace \
  --mode plan \
  --workflow-mode disabled \
  --disallowed-tools 'Bash,Edit,Write,ExitPlanMode' \
  --json \
  --prompt 'Reply with READY only. Do not use tools.'
```

Inspect configured plugin and MCP tools before using this example; its exclusions cover only the four named tools. For a standalone installation, keep the same supported environment variables and run the verified `zcode` executable instead of the macOS Node bundle. Retain the exit status, actual response, and returned `sessionId` in a private run record. No response or a nonzero exit leaves the connection unverified.

Read back that exact session with the same profile, without sending another ordinary prompt:

```bash
"${zcode_cmd[@]}" tui \
  --cwd /absolute/path/to/workspace \
  --resume sess_REPLACE_WITH_RETURNED_ID \
  --mode plan \
  --workflow-mode disabled \
  --disallowed-tools 'Bash,Edit,Write,ExitPlanMode'
```

In the TUI, explicitly load the exact saved session before inspecting it:

```text
/resume sess_REPLACE_WITH_RETURNED_ID
/model list
/effort list
```

In CLI `0.16.9`, startup `--resume` can defer loading persisted state until the next model turn. The TUI `/resume` handler explicitly loads it first; this prevents the readback from reporting a configured default instead of the saved selection. If the observed provider, model, or effort differs from the request, report the mismatch and select the intended values before a new authorized call. A new default in the profile does not prove the earlier call used it. For unattended readback, use the authoritative conversation snapshot through the version-matched app-server protocol described below. Prompt text, reasoning-token counts, and a provider label do not prove the runtime selection.

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

A legacy session response can show `mode: build` while Plan is enabled: the runtime stores the planning flag separately, and the legacy settings view omits it. Inspect the authoritative V4 conversation snapshot's `config.planEnabled` before concluding that `--mode plan` was ignored.

| Observation | Meaning and next action |
| --- | --- |
| Built-in provider file cannot be located | Check the bundle layout and supported path variables. |
| No selectable models | Check configuration parsing and registry admission, including the personal provider group and template. |
| `Select a model before continuing` | Inspect provider/model admission before changing the default selection. This error alone does not test the API key. |
| Requested reasoning level is unavailable | Use a supported value only with the caller's agreement to the changed choice. |
| A required tool is denied or needs approval | Use the authorized approval interface or report the blocked operation. |
| Timeout, nonzero exit, or no final response | Preserve the owned run's evidence and report incomplete execution. |

After a response, verify the requested artifact or answer independently. Record model and reasoning readback separately from response success. Neither one proves subscription billing; provider accounting needs its own evidence.
