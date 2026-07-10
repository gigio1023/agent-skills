# 1Password CLI Security Patterns

Read this before any action that may reveal, write, create, edit, or automate secrets.

## Table of Contents

- Default Posture
- Safe Retrieval Patterns
- Creating or Editing Items
- macOS App Integration
- Manual Sign-In Fallback
- Service Account Tokens
- Connect and Environments Boundary
- SSH Key Handling
- Output Review Checklist
- Common Failure Modes

## Default Posture

Treat secret values as toxic output:

- Do not paste secret values into chat, logs, durable notes, commit messages, shell history, or issue text.
- Do not use `--reveal`, `--no-masking`, or `--out-file` unless the user explicitly asked for that exposure or it is required for the task.
- Prefer commands that let a consumer process receive the secret without showing it to the agent.
- Prefer `--format json` for metadata, but remember JSON can contain sensitive fields if `--reveal` is used.
- Assume same-user processes on the computer may be able to inspect environment variables of other same-user processes. `op run` is still safer than committing secrets, but it is not a perfect boundary against local same-user process inspection.

## Safe Retrieval Patterns

Best-to-riskier order:

1. Verify existence/metadata: `op item list`, `op item get` without `--reveal`.
2. Feed a secret directly to a process: `op run --env-file=.env -- <command>`.
3. Read one field into a command pipeline: `op read --no-newline 'op://vault/item/field'`.
4. Write to a file only when the tool needs a file: `op read --out-file ... --file-mode 0600 ...`.
5. Display the value only after explicit user confirmation.

When the user asks "can you use the token?" prefer using it without displaying it. When the user asks "what is the token?", confirm that showing it in the conversation is intentional.

## Creating or Editing Items

Avoid passing sensitive values as command arguments:

```bash
op item edit Example 'password=secret-value'
```

Arguments can appear in shell history and process listings. Prefer:

- A JSON template edited in a secure local flow.
- Piped stdin when practical.
- `--generate-password` for generated passwords.
- `--dry-run` before write operations when structure is uncertain.

After using a temporary template or injected config file:

- Ensure permissions are restrictive, ideally `0600`.
- Keep it out of git.
- Delete it when no longer needed.
- Do not summarize its secret contents.

## macOS App Integration

For local macOS, desktop app integration is usually the best auth mode:

- The 1Password app handles unlock and Touch ID/system auth.
- `op signin` is idempotent and can be run directly.
- In agent harnesses, repeated fresh shell invocations can still trigger repeated app authorization prompts. Treat the authorization cache as terminal-session-sensitive.
- App integration authorization is per account. A new terminal/tab may prompt again, inactivity can require reauthorization, and locking the 1Password app revokes prior authorization.
- On macOS, 1Password CLI uses app-mediated IPC and biometric/system authorization; do not try to bypass this with session-token handling.

Goal for agent work: after the user approves one 1Password authorization prompt, keep work inside the same effective terminal session for the next short work window. Do this by choosing one of two patterns before touching real vault data:

1. One-shot batch: run a single `op` command and pipe the JSON into local analysis.

```bash
op item list --format json | jq '...all grouping, filtering, and reporting...'
```

2. Persistent PTY: start one interactive shell and send every follow-up `op` command through that same session. Use this when the task genuinely needs multiple `op` calls such as list, targeted item detail, then edit or verify.

Avoid the pattern that causes prompt storms: `op whoami` in one shell, `op item list` in another, then another `op item list` for a slightly different `jq` query. Fetch once and reuse the data in the same process or session.

Before starting a multi-step agent-run 1Password task:

- Say that the work will use one authorization window.
- Plan the needed `op` calls up front.
- Prefer `op --format json` once, then local filtering.
- If more data is needed, keep using the same PTY session rather than opening a fresh shell.
- Stop and reassess if the user sees a second unexpected authorization prompt.

Troubleshooting steps:

1. Ask the user to open and unlock the 1Password app.
2. Ask them to enable Developer settings for CLI integration.
3. Retry `op whoami` directly.
4. If multiple accounts exist, use `op account list` and select with `--account`.

Do not add tmux instructions. This skill is for local macOS use, not an OpenClaw persistent gateway session.

## Manual Sign-In Fallback

Manual sign-in is useful only when app integration is unavailable:

```bash
op account add --address my.1password.com --email user@example.com
eval "$(op signin --account my)"
```

The session token expires after inactivity and may not persist between separate agent shell calls. Avoid collecting or storing session tokens. If manual signin cannot be completed cleanly through direct commands, ask the user to run it in their own terminal and then retry direct `op` checks.

## Service Account Tokens

Use service accounts for automation with least-privilege vault access.

Do:

- Scope the service account to only required vaults.
- Prefer short-lived task-specific shell environments.
- Use explicit `--vault` or stable secret references.
- Check rate limits with `op service-account ratelimit` when automation is failing unexpectedly.

Avoid:

- Adding `OP_SERVICE_ACCOUNT_TOKEN` to `.zshrc`, `.env`, repo files, or task notes.
- Sharing one broad service account across unrelated projects.
- Using a service account for general personal desktop access when app integration is available.

## Connect and Environments Boundary

1Password CLI can work with Connect Server by setting `OP_CONNECT_HOST` and `OP_CONNECT_TOKEN`, but that is a server/automation architecture. Do not recommend Connect for ordinary local macOS use unless the user specifically asks for self-hosted infrastructure or CI/CD.

Official docs also describe 1Password Environments and the 1Password MCP Server. Treat those as adjacent capabilities:

- Use `op run --env-file` and secret references for stable local CLI workflows.
- Use Environments only after verifying the installed CLI supports the relevant flags or the user chose the beta/Environments path.
- Use an MCP Server only when the user explicitly asks for MCP-based Environments management. Do not silently switch a CLI task to MCP.

## SSH Key Handling

Prefer the 1Password SSH Agent for Git and SSH workflows. It lets clients authenticate without exposing private keys.

If a private key must be exported with `op read --out-file`:

- Use `--file-mode 0600`.
- Write only to the exact path needed by the consuming tool.
- Do not print the key.
- Delete the file after use when practical.
- Prefer `ssh-format=openssh` only for tools that need OpenSSH private key format.

## Output Review Checklist

Before sending a response after using `op`, check:

- Did any command output include a secret value?
- Did any command use `--reveal` or `--no-masking`?
- Did any command write an injected config, key, or token file?
- Does the final answer avoid echoing secret values?
- If a file was created, did you state its path and sensitivity without printing contents?
- If auth failed, did you explain the next user-visible step without asking for secrets?

## Common Failure Modes

| Symptom | Likely cause | Response |
| --- | --- | --- |
| `op whoami` says no account is authenticated | App locked, integration disabled, or no manual session | Ask user to unlock app and enable CLI integration, then retry. |
| Duplicate item names | Name lookup is ambiguous | Use `--vault`, item ID, or JSON list filters. |
| Service account item lookup fails | Missing explicit vault scope | Add `--vault` or use a fully qualified secret reference. |
| Secret appears masked in output | `op run` masking is working | Do not disable masking unless the user explicitly needs visible output. |
| A command from docs is unknown | Docs are ahead of installed stable CLI | Run `op --help` and use local stable command surface. |
| `op run --environment` fails | Environments support is beta or not in installed stable CLI | Verify `op run --help`; fall back to `--env-file` secret references unless the user wants beta setup. |
