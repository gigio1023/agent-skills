---
name: 1password-cli
description: >
  Use 1Password CLI (`op`) on a user's MacBook for local account setup, 1Password app integration, sign-in checks, vault/item/document lookup, secret references, `op read`, `op run`, `op inject`, item CRUD, service accounts, shell plugins, SSH-key fields, and secrets in .env/config/scripts. Trigger when the user mentions 1Password, 1password, `op`, secret references, vaults, items, OTP, CLI login, env-file secrets, shell plugins, API tokens, SSH keys in 1Password, or reading/using/managing secrets from the terminal. Mac-local skill; batch `op` work into one command or one persistent PTY session to avoid repeated app authorization prompts; do not use OpenClaw gateway or tmux auth flows.
---

# 1Password CLI

Use this skill to work with the local 1Password CLI on a MacBook. It is a Library & API Reference skill, not an OpenClaw gateway runbook.

Verified context when written: macOS arm64, `op` 2.34.1, stable release notes checked 2026-06-27. Before operational work, trust the installed CLI over memory:

```bash
command -v op
op --version
op --help
```

If docs and local help disagree, follow local `op <command> --help` first and note the mismatch.

## Quick Start

1. Verify the binary and version with `command -v op` and `op --version`.
2. Prefer 1Password desktop app integration on MacBook. Ask the user to unlock the 1Password app or approve Touch ID/system auth when prompted. Before any real `op` access, decide whether the task can be completed with one `op` call; if not, open one persistent PTY shell and keep all `op` calls inside that session.
3. Check auth with `op whoami`. If multiple accounts exist, use `--account <account>` or set `OP_ACCOUNT` for the command.
4. Use the least-revealing command that solves the task, and avoid re-running the same metadata query:
   - Metadata: `op item list`, `op item get`, `op vault list`.
   - Secret reference discovery: `op item get <item> --format json --fields label=<field> | jq -r .reference`.
   - One field: `op read 'op://vault/item/field'`.
   - Command needs env vars: `op run --env-file=.env -- <command>`.
   - Config template needs substitution: `op inject -i config.tpl -o config.local`.
5. Prefer `--format json` for scripts or agent parsing. Avoid `--reveal`, `--no-masking`, and printing secret values unless the user explicitly asked for the value to be displayed.
6. For sensitive item create/edit operations, prefer JSON templates or stdin over assignment statements because command arguments can leak through shell history or process inspection.

## Detailed Workflow

### Installation and Update Checks

If `op` is missing on macOS, suggest the official 1Password CLI install flow or Homebrew formula `1password-cli`; do not invent a custom install script. Do not run `op update` automatically unless the user asked to update. It can download an update.

Useful checks:

```bash
op --version
op update --help
brew list --versions 1password-cli
```

### Authentication on a MacBook

The normal MacBook path is desktop app integration:

1. The user installs and unlocks the 1Password desktop app.
2. In 1Password, the user enables Touch ID/system auth and CLI integration.
3. The agent runs direct `op` commands, but should group them into one terminal session. `op signin` is idempotent with app integration and only prompts if needed.

Codex execution detail: each separate shell/tool invocation can look like a new terminal session to 1Password and may trigger another authorization prompt. To let one app authorization cover the next several minutes of work, prefer one of these patterns:

- One-shot batch: call `op` once, then do all filtering, grouping, and reporting with local tools such as `jq`.
- Persistent PTY: start one interactive shell with `tty: true`, perform sign-in/auth once, then send all follow-up `op` commands through that same session.

Do not repeatedly call `op` from fresh shell invocations for exploratory steps. If a task starts generating multiple authorization prompts, stop, explain the session issue, and switch to a one-shot or persistent-PTY plan before continuing.

Do not use tmux for MacBook app integration. If a command cannot connect to the 1Password app, ask the user to confirm the app is running, unlocked, and CLI integration is enabled, then retry direct `op`.

Standalone manual sign-in is a fallback, not the default:

```bash
op account add --address my.1password.com --email user@example.com
eval "$(op signin --account my)"
op whoami
```

Manual sign-in creates session tokens that expire after inactivity and may not persist across separate agent shell invocations. If a persistent manual session is required, ask the user to run the flow in their own terminal or combine the reviewed operation into one command. Do not add tmux instructions.

Service accounts are appropriate for automation and narrow vault-scoped access, not general personal desktop use. If using one, prefer a least-privilege token and avoid writing `OP_SERVICE_ACCOUNT_TOKEN` into shell startup files.

### Secret References

Use secret references instead of plaintext secrets:

```text
op://vault/item/field
op://vault/item/section/field
op://vault/item/one-time password?attribute=otp
op://vault/item/private key?ssh-format=openssh
```

Quote references that contain spaces:

```bash
op read 'op://ExampleVault/GitHub/token'
op read 'op://Work API/Production DB/password'
```

Prefer item IDs and vault names/IDs when names are ambiguous or scripts need stability.

### Reading Secrets

Use `op read` for a single field. Do not echo secret values into chat or logs.

```bash
op read 'op://app-prod/db/password'
op read --no-newline 'op://app-prod/api/token'
op read --out-file ./key.pem --file-mode 0600 'op://ExampleVault/server ssh/private key?ssh-format=openssh'
```

If the user only needs a command to consume the secret, pipe or inject it directly into that command instead of revealing the value.

### Running Commands With Secrets

Use `op run` when a process needs secrets as environment variables for only that subprocess:

```bash
op run --env-file=.env -- npm test
op run --env-file=.env.local -- sh -c 'echo "$DATABASE_URL"'
```

`.env` files can contain secret references:

```dotenv
DATABASE_URL=op://app-prod/db/url
API_TOKEN=op://app-prod/api/token
```

Secrets printed to stdout/stderr are masked by default. Use `--no-masking` only when the user explicitly needs the real value visible.

### Injecting Config Files

Use `op inject` for template files with embedded references:

```yaml
database:
  password: "{{ op://app-prod/db/password }}"
```

```bash
op inject -i config.yml.tpl -o config.yml
```

Treat injected files as sensitive artifacts: use restrictive permissions, do not commit them, and delete them after use when practical.

### Items, Vaults, Documents, and Plugins

Read [references/cli-usage.md](references/cli-usage.md) when you need command-level syntax for `account`, `item`, `vault`, `document`, `service-account`, `plugin`, `completion`, `read`, `run`, or `inject`.

Read [references/security-patterns.md](references/security-patterns.md) before creating/editing items, writing injected files, using service account tokens, or showing secret values.

Read [references/official-doc-crosswalk.md](references/official-doc-crosswalk.md) when official docs mention 1Password Environments, MCP Server, Connect, SSH Agent, app-integration security details, VS Code secret references, or any command/flag missing from local `op --help`.

## Gotchas

- The public docs may mention commands that are not in the installed stable CLI. On local `op` 2.34.1, `op environment` is not available; verify with `op --help` before using doc-only commands.
- Official docs describe 1Password Environments beta with `op run --environment`; local stable 2.34.1 help does not expose that flag. Use it only after verifying the installed CLI supports it or the user intentionally installed a beta build.
- 1Password app authorization is session-sensitive. In Codex, repeated fresh shell calls can produce repeated authorization prompts even within the app's short authorization window. Batch `op` work or use one persistent PTY session.
- `op item get <name>` can be ambiguous. Add `--vault` or use item IDs when there are duplicate names or scripts need stable behavior.
- `op item get` is for item details. Use `op read` for a single field value.
- `op item create` and `op item edit` assignment statements can expose values in shell history or process listings. Use templates/stdin for sensitive values.
- `op item edit --template` can overwrite passkeys in JSON item templates. Avoid template-editing items that contain passkeys unless the user accepts that risk.
- `op run` expands references before the subprocess sees env vars. If the shell must expand an env var, use a subshell: `op run -- sh -c 'command "$VAR"'`.
- `--no-masking`, `--reveal`, `--out-file`, and service account tokens all increase exposure. Use them deliberately and say why.
- Do not place 1Password tokens, session tokens, or injected secrets in repo files, logs, shell startup files, or durable notes.

## Reference Files

| File | When to read | Content |
| --- | --- | --- |
| [references/cli-usage.md](references/cli-usage.md) | Need exact `op` command patterns, flags, examples, or command map | Local 2.34.1 command surface and practical recipes |
| [references/security-patterns.md](references/security-patterns.md) | Any operation may reveal, write, create, edit, or automate secrets | Secret-handling guardrails and MacBook-specific troubleshooting |
| [references/official-doc-crosswalk.md](references/official-doc-crosswalk.md) | Official docs and local CLI help disagree, or the task touches Environments, MCP, Connect, SSH Agent, or VS Code | Current official-doc notes and feature-boundary guidance |

## Source Notes

- Local CLI help: `op --version`, `op --help`, and selected `op <command> --help`, checked on 2026-06-27.
- Official docs: https://www.1password.dev/cli/ and https://www.1password.dev/cli/reference/
- Stable release notes: https://app-updates.agilebits.com/product_history/CLI2
- OpenClaw 1Password skill was used as a structural reference only; this skill intentionally omits OpenClaw metadata, gateway assumptions, and tmux flows.
