# 1Password CLI Usage Reference

This reference is based on local `op` 2.34.1 help on macOS arm64, checked 2026-06-27. When in doubt, run `op <command> --help` because the installed CLI is the source of truth.

## Table of Contents

- Command Surface
- Global Flags and Environment Variables
- Account and Sign-In Recipes
- Vault and Item Discovery
- Secret References and `op read`
- `op run`
- `op inject`
- Creating and Editing Items
- Documents
- Service Accounts
- Shell Plugins
- SSH Keys and SSH Agent Boundary
- Completions
- Source Links

## Command Surface

Top-level commands in local stable 2.34.1:

| Area | Commands |
| --- | --- |
| Accounts | `op account add`, `op account get`, `op account list`, `op account forget` |
| Vaults | `op vault create`, `op vault get`, `op vault edit`, `op vault delete`, `op vault list`, plus vault `group` and `user` access subcommands |
| Items | `op item create`, `op item get`, `op item edit`, `op item delete`, `op item list`, `op item move`, `op item share`, `op item template ...` |
| Documents | `op document create`, `op document get`, `op document edit`, `op document delete`, `op document list` |
| Secrets | `op read`, `op run`, `op inject` |
| Auth/session | `op signin`, `op signout`, `op whoami` |
| Automation/admin | `op service-account create`, `op service-account ratelimit`, `op connect ...`, `op events-api ...`, `op group ...`, `op user ...` |
| Shell integration | `op completion <shell>`, `op plugin list`, `op plugin init`, `op plugin inspect`, `op plugin run`, `op plugin clear`, `op plugin credential ...` |
| Updates | `op update` |

Local stable 2.34.1 does not expose `op environment`, and local `op run --help` does not expose `--environment`. Official docs describe 1Password Environments as a beta path that requires a beta CLI build; verify local help before using any Environment-specific command.

## Global Flags and Environment Variables

Common global flags:

| Flag | Use |
| --- | --- |
| `--account <account>` | Select account by shorthand, sign-in address, account ID, or user ID. Can also use `OP_ACCOUNT`. |
| `--format json` | Machine-readable output. Prefer this for scripts and agent parsing. Can also use `OP_FORMAT`. |
| `--cache=true|false` | Cache is enabled by default on Unix-like systems. Use `--cache=false` when stale metadata would matter. |
| `--config <directory>` | Use an alternate CLI config directory. |
| `--debug` | Debug mode. Treat output as sensitive. Can also use `OP_DEBUG=true`. |
| `--iso-timestamps` | RFC 3339 timestamps. Can also use `OP_ISO_TIMESTAMPS`. |
| `--no-color` | Useful for machine parsing or logs. |
| `--session <token>` | Authenticate with a session token. Avoid handling this unless the user explicitly chose manual signin. |

## Account and Sign-In Recipes

Check configured accounts:

```bash
op account list
op whoami
op whoami --account <account>
```

Add an account manually only when app integration is not available:

```bash
op account add --address my.1password.com --email user@example.com
eval "$(op signin --account my)"
```

Account selection precedence:

1. `--account` flag.
2. `OP_ACCOUNT` environment variable.
3. Most recently signed-in account for app integration, or current terminal session for manual signin.

## Vault and Item Discovery

List vaults:

```bash
op vault list
op vault list --format json
op vault list --user user@example.com --format json
op vault list --group Security --format json
```

List items:

```bash
op item list --vault ExampleVault
op item list --vault ExampleVault --categories Login --format json
op item list --vault ExampleVault --tags project/foo --format json
op item list --vault ExampleVault --long
```

Get item details without revealing sensitive fields:

```bash
op item get GitHub --vault ExampleVault --format json
op item get <item-id> --vault ExampleVault --format json
op item get GitHub --vault ExampleVault --fields label=username --format json
```

Use piped JSON to inspect multiple items:

```bash
op item list --vault Staging --categories Login --format json | op item get - --fields label=username,label=password --format json
```

Prefer `op read` for a single secret field.

Get a secret reference from an item field without manually composing it:

```bash
op item get GitHub --vault development --format json --fields label=username | jq -r .reference
op item get GitHub --vault development --format json | jq -r '.fields[] | select(.label == "api_token") | .reference'
```

When the item contains duplicate field labels, include section labels or inspect the full JSON field list before selecting.

## Secret References and `op read`

Reference shape:

```text
op://vault/item/field
op://vault/item/section/field
op://vault/item/field?attribute=otp
op://vault/item/private key?ssh-format=openssh
```

Syntax notes from the official docs:

- Secret references are case-insensitive.
- Names may contain letters, digits, `-`, `_`, `.`, and whitespace.
- Quote references that contain whitespace.
- If a vault, item, section, field, or file name contains unsupported characters such as `/`, use that object's unique ID from JSON output.
- A file attachment is referenced by using the file name in the field position: `op://vault/item/[section/]file-name`.
- Field/file attributes can be read with `?attribute=<name>` or `?attr=<name>`.

Examples:

```bash
op read 'op://app-prod/db/password'
op read --no-newline 'op://app-prod/api/token'
op read 'op://app-prod/db/one-time password?attribute=otp'
op read 'op://ExampleVault/aws/access credentials/username?attribute=type'
op read 'op://app-infra/ssh/key.pem?attribute=name'
op read --out-file ./key.pem --file-mode 0600 'op://ExampleVault/server ssh/private key?ssh-format=openssh'
```

Important flags:

| Flag | Use |
| --- | --- |
| `--no-newline` | Useful when piping a token exactly. |
| `--out-file <path>` | Write to a file instead of stdout. Treat the file as sensitive. |
| `--file-mode <mode>` | Defaults to `0600` with `--out-file`. |
| `--force` | Avoid prompts. Use only when the action and destination are clear. |

Useful attribute values:

| Target | Attribute values |
| --- | --- |
| Field | `type`, `value`, `id`, `purpose`, `otp` |
| File attachment | `type`, `content`, `size`, `id`, `name` |

## `op run`

Use `op run` to provide secrets to a subprocess as environment variables.

Example `.env`:

```dotenv
DATABASE_URL=op://app-prod/db/url
API_TOKEN=op://app-prod/api/token
```

Official `.env` parsing notes that matter in practice:

- `KEY=VALUE` statements are separated by newlines; empty lines are skipped.
- Lines beginning with `#` are comments; inline comments after `KEY=VALUE` are supported.
- Empty values become empty strings.
- Surrounding single or double quotes are removed from evaluated values.
- Double-quoted values can expand `$VAR` and `${VAR}` from the environment; single-quoted values do not.
- Variables defined earlier in the same file can be referenced later.
- Backslash can escape special characters such as `$`.
- Inner quotes in values like `JSON={"foo":"bar"}` are preserved.
- Leading/trailing whitespace around unquoted keys and values is ignored.
- Use UTF-8.

Run:

```bash
op run --env-file=.env -- npm test
op run --env-file=.env -- ./scripts/deploy-preview
APP_ENV=dev op run --env-file=./app.env -- myapp deploy
```

If a shell must expand variables, put that expansion inside the subprocess shell:

```bash
MY_VAR=op://ExampleVault/example/password op run -- sh -c 'printf "%s\n" "$MY_VAR"'
```

Precedence:

1. `--env-file` values override shell environment variables with the same name.
2. If multiple env files define the same name, the last env file wins.

Masking is on by default. Use `--no-masking` only when the user explicitly needs the real secret visible in output.

Official docs also describe `op run --environment <environmentID> -- <command>` for 1Password Environments beta. Do not use it on stable 2.34.1 unless `op run --help` shows the flag or the user intentionally installed a supported beta build.

## `op inject`

Use `op inject` when a config file is templated with secret references.

Template:

```yaml
db_password: "{{ op://app-prod/db/password }}"
api_token: "{{ op://app-prod/api/token }}"
```

Inject:

```bash
op inject -i config.yml.tpl -o config.yml
APP_ENV=prod op inject -i config.yml.tpl -o config.yml
```

Important flags:

| Flag | Use |
| --- | --- |
| `-i`, `--in-file` | Read template from a file. |
| `-o`, `--out-file` | Write resolved config to a file. |
| `--file-mode <mode>` | Defaults to `0600` with `--out-file`. |
| `--force` | Avoid prompts. Use only after checking paths. |

Delete or protect resolved files after use.

Official docs show templates that contain raw secret references such as `password: op://prod/mysql/password`, while local CLI help also shows `{{ op://... }}` examples. If a template does not resolve, check `op inject --help` and the official template syntax docs, then choose the form accepted by the installed CLI.

## Creating and Editing Items

Assignment syntax:

```text
[section.]field[[fieldType]]=value
```

Built-in fields are identified by the `id` in `op item template get <category>` output. Do not include a `fieldType` for built-in fields. For a Login item, common built-ins are `username`, `password`, and `notesPlain`.

Custom field types:

| Assignment `fieldType` | JSON `type` | Notes |
| --- | --- | --- |
| `password` | `CONCEALED` | Concealed password. |
| `text` | `STRING` | Text string. |
| `email` | `EMAIL` | Email address. |
| `url` | `URL` | Web address; use `--url` for Login/Password/API Credential autofill website. |
| `date` | `DATE` | `YYYY-MM-DD`. |
| `monthYear` | `MONTH_YEAR` | `YYYYMM` or `YYYY/MM`. |
| `phone` | `PHONE` | Phone number. |
| `otp` | `OTP` | `otpauth://` URI. |
| `file` | N/A | File attachment; assignment statements only. |

Examples:

```bash
op item create --category login --title 'Example Login' --vault ExampleVault --url https://example.com username=user@example.com --generate-password='letters,digits,symbols,32'
op item edit 'Example Login' --vault ExampleVault 'username=new-user@example.com'
op item edit 'Example Login' --vault ExampleVault 'section2.field5[delete]'
op item edit 'Example Login' --vault ExampleVault --generate-password='letters,digits,symbols,32'
op item create --category 'SSH Key' --title 'SSH Host' --vault ExampleVault --ssh-generate-key=ed25519
```

Use `--dry-run` before creating or editing when the shape is uncertain:

```bash
op item create --dry-run --category login --title 'Example Login' --vault ExampleVault username=user@example.com
op item edit 'Example Login' --dry-run --vault ExampleVault 'username=new-user@example.com'
```

For sensitive values, prefer templates:

```bash
op item template get Login --out-file login.json
op item create --template login.json --vault ExampleVault
```

You can also pipe templates:

```bash
op item template get Login | op item create --vault ExampleVault -
```

Do not combine piped input and `--template`.

Passkey warning: JSON item templates do not support passkeys in local 2.34.1 help. Template-editing an item that contains a passkey can overwrite it.

## Documents

Document commands operate on Document items:

```bash
op document list --vault ExampleVault
op document get <document> --vault ExampleVault --out-file ./document.bin
op document create ./local-file.pdf --vault ExampleVault --title 'Local File'
```

Run `op document <subcommand> --help` for exact flags before writing or downloading files.

## Service Accounts

Service accounts are useful for automation with scoped vault access:

`op service-account create` returns its token once. A bare invocation prints
that token to stdout, which exposes it to agent tool output and logs. Do not run
the command as a standalone agent action.

For an agent-run creation, first verify the service-account name, source-vault
permissions, and destination vault for the saved token. Then use one persistent
shell and capture the token directly into a mode-`0600` temporary file before
creating a concealed Password item. This example never prints the token:

```bash
set -euo pipefail
umask 077

service_account_name='my-service-account'
source_vault='Dev'
token_vault='Private'
template_file="$(mktemp -t op-service-account-template.XXXXXX)"
token_file="$(mktemp -t op-service-account-token.XXXXXX)"
cleanup() { rm -f "$template_file" "$token_file"; }
trap cleanup EXIT

# Prepare and validate the destination before creating the one-time token.
op item template get Password --out-file "$template_file" --force
jq -e 'any(.fields[]; .id == "password")' "$template_file" >/dev/null

op service-account create "$service_account_name" \
  --vault "$source_vault:read_items" \
  --expires-in=24h \
  --raw > "$token_file"

jq --rawfile token "$token_file" --arg title "$service_account_name token" '
  .title = $title |
  (.fields[] | select(.id == "password").value) =
    ($token | sub("[\\r\\n]+$"; ""))
' "$template_file" | op item create --vault "$token_vault" - >/dev/null

op item get "$service_account_name token" --vault "$token_vault" \
  --fields label=password --format json | \
  jq -e '.reference | strings | startswith("op://")' >/dev/null
```

The trap deletes both temporary files even when storage or verification fails.
In that case, treat the one-time token as lost, disable the unusable service
account through 1Password administration, fix the destination flow, and create
a replacement. Never disable cleanup merely to reveal the token. If a safe
capture-and-store flow is not available, ask the user to run creation in their
own terminal and save the token immediately.

Use `op service-account ratelimit` for a read-only rate-limit check.

Vault permission syntax:

```text
--vault <vault-name>:<permission>,<permission>
```

Supported permissions in local help:

- `read_items`
- `write_items` (requires `read_items`)
- `share_items` (requires `read_items`)

If permissions are omitted for a vault, the CLI defaults to `read_items`. Service accounts cannot be granted access to Personal or Private vaults.

When using service accounts, many item operations require explicit vault scoping:

```bash
op item get <item-id> --vault <vault-id> --format json
op read 'op://vault/item/field'
```

Keep `OP_SERVICE_ACCOUNT_TOKEN` out of durable shell profiles, repo files, and logs unless the user explicitly decides otherwise.

## Shell Plugins

Shell plugins let third-party CLIs authenticate with credentials stored in 1Password rather than plaintext local files.

Useful commands:

```bash
op plugin list
op plugin init <plugin>
op plugin inspect
op plugin run -- <command>
op plugin clear
```

Use shell plugins for tools such as CLIs that already have a supported 1Password plugin. Prefer plugin-managed credentials over copying tokens into dotfiles.

For scripts that use a supported third-party CLI interactively:

```bash
op plugin run -- aws sts get-caller-identity
```

Shell plugins require desktop app integration and support Bash, Zsh, and fish. `op plugin init` can configure credentials for the current terminal session, a directory tree, or globally; prefer the narrowest scope that works.

## SSH Keys and SSH Agent Boundary

The CLI can create SSH Key items or read an SSH private key field:

```bash
op item create --category 'SSH Key' --title 'Example SSH Key' --ssh-generate-key=ed25519 --vault ExampleVault
op read 'op://ExampleVault/example ssh/private key?ssh-format=openssh'
```

For normal Git and SSH workflows on macOS, prefer the 1Password SSH Agent over exporting private keys. The SSH Agent lets Git/SSH clients use keys without reading private key material. Use CLI private-key export only when a tool cannot use an SSH agent and the user accepts the file-handling risk.

## Completions

For zsh on macOS:

```bash
eval "$(op completion zsh)"; compdef _op op
```

Add this to the user's shell config only if they ask for persistent completion setup.

## Source Links

- CLI docs: https://www.1password.dev/cli/
- CLI command reference: https://www.1password.dev/cli/reference/
- App integration: https://www.1password.dev/cli/app-integration/
- Secret reference syntax: https://www.1password.dev/cli/secret-reference-syntax/
- Loading secrets into environment variables: https://www.1password.dev/cli/secrets-environment-variables
- Loading secrets into config files: https://www.1password.dev/cli/secrets-config-files
- Loading secrets into scripts: https://www.1password.dev/cli/secrets-scripts
- Item fields: https://www.1password.dev/cli/item-fields
- Shell plugins: https://www.1password.dev/cli/shell-plugins
- SSH Agent: https://www.1password.dev/ssh/agent
- Stable release notes: https://app-updates.agilebits.com/product_history/CLI2
