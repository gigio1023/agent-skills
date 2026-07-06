# Official 1Password Docs Crosswalk

Use this file when current official documentation mentions a feature that may not exist in the installed local stable CLI, or when the user asks about adjacent 1Password developer features.

Checked against official docs on 2026-06-27 and local `op` 2.34.1 help on macOS arm64.

## Local Stable vs Official Docs

| Topic | Official docs say | Local stable 2.34.1 check | Agent guidance |
| --- | --- | --- | --- |
| 1Password Environments | `op run --environment <environmentID> -- <command>` is documented for Environments beta and requires a beta CLI build. | `op environment` is unknown and `op run --help` does not show `--environment`. | Do not use Environment commands unless local help confirms support or the user intentionally installed beta. Prefer `op run --env-file` for stable local use. |
| 1Password MCP Server | Docs banner and Environments docs mention MCP Server for Codex to manage Environments without exposing secrets to the agent. | Not a CLI command in local `op --help`. | Treat as a separate MCP/integration task, not a default fallback for CLI work. |
| Secret references | Official docs recommend copying from the desktop app, VS Code extension, or extracting `reference` from `op item get --format json`. | `op item get --format json --fields ...` is available. | Prefer extracting `.reference` from JSON over hand-composing references when names are uncertain. |
| `.env` loading | Official docs define dotenv parsing, variable expansion, comments, quotes, and `op run --env-file`. | `op run --env-file` is available. | Use for local dev secrets. Remember environment variables are visible to same-user processes on many systems. |
| Config files | Official docs show raw secret references in config templates and note resolved files must be deleted when no longer needed. | `op inject` is available and local help also shows `{{ op://... }}` examples. | Use whichever template syntax local `op inject` accepts; keep resolved outputs out of git and delete them. |
| Service accounts | Official docs recommend least privilege and scoped vault access. | `op service-account create` supports `--vault`, `--expires-in`, `--can-create-vaults`; token is returned once. | Good for automation, not default local macOS auth. Save token in 1Password immediately if created. |
| Connect Server | Official config-file docs say `op run`, `op inject`, `op read`, and `op item get` can be used with Connect via `OP_CONNECT_HOST` and `OP_CONNECT_TOKEN`. | Supported as environment-variable auth mode, but not needed for normal desktop use. | Mention only for CI/server/self-hosted workflows. |
| Shell plugins | Official docs list many supported third-party CLIs and require desktop app integration. | `op plugin` commands are present. | Useful for interactive local CLI auth; prefer narrow credential scope during `op plugin init`. |
| SSH Agent | Official SSH docs recommend the SSH Agent for Git/SSH so clients never read private keys. | CLI can also create/read SSH Key items. | Prefer SSH Agent for Git/SSH. Export private keys only when necessary. |

## Official Docs Worth Checking for Freshness

- CLI overview: https://www.1password.dev/cli/
- CLI reference: https://www.1password.dev/cli/reference/
- Get started: https://www.1password.dev/cli/get-started
- App integration: https://www.1password.dev/cli/app-integration
- App integration security: https://www.1password.dev/cli/app-integration-security
- Best practices: https://www.1password.dev/cli/best-practices
- Secret reference syntax: https://www.1password.dev/cli/secret-reference-syntax
- Load secrets into environment variables: https://www.1password.dev/cli/secrets-environment-variables
- Load secrets into config files: https://www.1password.dev/cli/secrets-config-files
- Load secrets into scripts: https://www.1password.dev/cli/secrets-scripts
- Item fields: https://www.1password.dev/cli/item-fields
- Shell plugins: https://www.1password.dev/cli/shell-plugins
- SSH Agent: https://www.1password.dev/ssh/agent
- Service accounts: https://www.1password.dev/service-accounts/
- Connect with CLI: https://www.1password.dev/connect/cli
- Documentation index: https://www.1password.dev/llms.txt

## Decision Rules

- If the user asks for stable local macOS usage, local `op --help` wins over docs examples.
- If the user asks for latest/beta/Environments/MCP, check the official docs and the installed CLI before recommending commands.
- If the user asks for Git or SSH authentication, prefer 1Password SSH Agent rather than `op read` private-key export.
- If the user asks for a third-party CLI login and a shell plugin exists, prefer `op plugin init` / `op plugin run` over storing tokens in dotfiles.
- If the user asks for CI or server runtime, discuss service accounts or Connect explicitly; do not reuse desktop app integration assumptions.
