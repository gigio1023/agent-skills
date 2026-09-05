---
name: "1password-cli"
description: >
  Use when the user wants to use the local macOS 1Password CLI (`op`) for
  setup or authentication, vault/item/document lookup or CRUD, secret
  references, `op read`, `op run`, `op inject`, service accounts, shell
  plugins, or SSH-key fields. Triggers on 1Password, `op`, vaults, items, OTP,
  CLI login, env-file secrets, 1Password shell plugins, or API tokens and SSH
  keys stored in 1Password. NOT for generic password advice, OpenClaw gateway/tmux auth flows,
  or silently replacing a CLI request with MCP, Connect, or Environments.
---

# 1Password CLI

Complete the requested local `op` operation while exposing as little secret material as possible. Preserve the requested facts, caveats, and next action; omit command-by-command narration that does not help the user verify the result.

The installed CLI is the command-surface authority:

```bash
command -v op
op --version
op <command> --help
```

If documentation and local help disagree, follow local help and report the mismatch only when it changes the task.

## Quick Start

1. Classify the request as metadata lookup, secret consumption, a mutating operation, or setup/troubleshooting.
2. Plan the required `op` calls before accessing real vault data. Use one batched call when possible; otherwise keep every call in one persistent PTY shell so one macOS app authorization window covers the task.
3. Check authentication with `op whoami`. When multiple accounts exist, use `--account <account>` or set `OP_ACCOUNT` for that command.
4. Choose the least-revealing route:
   - Metadata: `op vault list`, `op item list`, `op item get`.
   - Discover a reference: `op item get <item> --format json --fields label=<field> | jq -r .reference`.
   - Read one field: `op read 'op://vault/item/field'`.
   - Give a subprocess environment variables: `op run --env-file=.env -- <command>`.
   - Resolve a config template: `op inject -i config.tpl -o config.local`.
5. Before item/vault/document/service-account/plugin writes, verify that the user requested the mutation and that the account, vault, item, and destination are unambiguous. Read `references/security-patterns.md` and use `--dry-run` where the command supports it. Reuse the account and destination already established in this session; ask only about unresolved identity or exposure, not whether to perform the same authorized operation again.
6. Verify the requested outcome without printing secret values. Report the account or vault scope, what changed or was found, any sensitive file created, and the smallest unblock step if authentication failed.

If a write returns an uncertain result, inspect metadata in the same session before retrying. Do not repeat a create operation merely to obtain clearer output or verify success by revealing the stored secret.

## macOS Authentication

Desktop app integration is the default local path: the user unlocks the 1Password app, enables CLI integration and Touch ID/system authentication, and approves the prompt. Separate agent shell invocations can count as separate terminal sessions and cause repeated prompts.

Use one of these execution shapes before the first real data call:

- One-shot batch: fetch JSON once, then filter or group locally with `jq`.
- Persistent PTY: authenticate once, then run every follow-up `op` command in that same shell.

If a second unexpected prompt appears, stop opening fresh shells and switch to one of those shapes. Do not use tmux to work around macOS app integration.

Manual sign-in is a fallback when app integration is unavailable:

```bash
op account add --address my.1password.com --email user@example.com
eval "$(op signin --account my)"
op whoami
```

Manual session tokens expire and may not survive separate tool calls. Do not collect or persist them. Use service accounts only for scoped automation, not as a substitute for ordinary personal desktop access.

## Operation Routing

Use `references/cli-usage.md` for exact syntax beyond the common paths below.

### Read or Consume a Secret

Prefer references over plaintext and quote references containing spaces:

```text
op://vault/item/field
op://vault/item/section/field
op://vault/item/one-time password?attribute=otp
```

```bash
op read --no-newline 'op://app-prod/api/token'
op run --env-file=.env -- npm test
op inject -i config.yml.tpl -o config.yml
```

If a command can consume the value directly, do that instead of returning it to chat. `op run` masks matching output by default; do not disable masking unless visible plaintext is explicitly required.

### Create or Edit

Sensitive assignment values can leak through shell history or process inspection. Prefer JSON templates or stdin, generate passwords with the CLI, and dry-run uncertain item shapes. Do not template-edit an item containing passkeys unless the user accepts that local CLI templates can overwrite them.

Service-account creation is a special case: the CLI returns the token once on stdout. Never run a bare `op service-account create` through an agent tool whose stdout is captured. Read the stdout-safe capture-and-store recipe in `references/cli-usage.md`, or have the user create and save the token in their own terminal.

For injected configs or exported keys, use restrictive permissions, keep the file out of git, and delete it after use when practical:

```bash
op read --out-file ./key.pem --file-mode 0600 \
  'op://ExampleVault/server ssh/private key?ssh-format=openssh'
```

Prefer the 1Password SSH Agent for normal Git/SSH use so private keys are not exported at all.

## Output and Safety Contract

- Never echo secret values, bearer tokens, session tokens, raw private keys, or injected config contents into chat, logs, durable notes, shell profiles, or repository files.
- `--reveal`, `--no-masking`, secret display, key export, and durable token storage require an explicit need. State the exposure and destination before proceeding.
- Prefer `--format json` for metadata parsing, but remember revealed JSON can still contain secrets.
- If only setup status is needed, report fields as present/missing; do not show their values.
- Do not run `op update` unless the user asked to update the CLI.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| [references/cli-usage.md](references/cli-usage.md) | Exact commands, flags, CRUD, documents, service accounts, plugins, or SSH fields are needed | Installed stable command map and recipes |
| [references/security-patterns.md](references/security-patterns.md) | A task may reveal, write, create, edit, export, or automate secrets | Exposure gates, macOS auth behavior, and cleanup rules |
| [references/official-doc-crosswalk.md](references/official-doc-crosswalk.md) | Local help and official docs disagree, or the task touches Environments, MCP, Connect, SSH Agent, or VS Code | Feature-boundary and freshness checks |

## Gotchas

- Commands or flags documented for a beta may be absent from the installed stable CLI. Verify `op <command> --help`; do not guess.
- Item names are not unique. Use `--vault` or an item ID when lookup is ambiguous or automation needs stable identity.
- `op item get` is for item details; use `op read` for one secret field.
- Shell expansion needed after `op run` belongs inside a subprocess, for example `op run -- sh -c 'command "$VAR"'`.
- Same-user processes may be able to inspect environment variables. `op run` avoids durable plaintext but is not a complete boundary against local process inspection.
- If authentication cannot connect, ask the user to unlock the app and confirm CLI integration, then retry directly in the same PTY session.
