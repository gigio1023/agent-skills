---
name: install-skill-pack
description: >
  Use when installing or refreshing the published `gigio1023/agent-skills` pack
  globally for explicitly selected agents after changes reach `main`, or when
  updating already tracked global skills on request. Uses the Skills CLI,
  reviews partner security audits before installation, and verifies global
  discovery. NOT for local checkouts, PR or feature branches, commit SHAs,
  project-local installs, pre-merge testing, unscoped all-agent installs, or
  silently changing unrelated global skills.
---

# Install Skill Pack

Install only the published `main` branch of `gigio1023/agent-skills` at global
scope. Let the Skills CLI manage destinations for the agents named by the user.
Never substitute a newer local checkout or PR ref.

## Quick Path

1. Confirm the published `main` contents without installing:

   ```bash
   npx --yes skills add 'gigio1023/agent-skills#main' --list
   ```

   If a requested skill is absent, stop. It has not reached `main`; do not fall
   back to a local path, feature branch, or commit.

2. Resolve an explicit list of target agent IDs from the user's request or the
   current harness. Do not widen that list to every CLI-supported agent.

3. The CLI automatically enables non-interactive mode when it detects an
   agent. For this child process only, remove its detection signals so the audit
   prompt remains available. In Bash or Zsh, define:

   ```bash
   audit_env=(
     -u AI_AGENT -u CURSOR_TRACE_ID -u CURSOR_AGENT
     -u CURSOR_EXTENSION_HOST_ROLE -u GEMINI_CLI
     -u CODEX_SANDBOX -u CODEX_CI -u CODEX_THREAD_ID
     -u ANTIGRAVITY_AGENT -u AUGMENT_AGENT -u OPENCODE_CLIENT
     -u CLAUDECODE -u CLAUDE_CODE -u CLAUDE_CODE_IS_COWORK
     -u REPL_ID -u COPILOT_MODEL -u COPILOT_ALLOW_ALL
     -u COPILOT_GITHUB_TOKEN
   )
   ```

   Then start the complete-pack install in an interactive terminal, replacing
   the target placeholder with the resolved IDs. Keep `npx --yes` only to fetch
   the CLI; do not pass `-y` or `--yes` to the Skills CLI:

   ```bash
   env "${audit_env[@]}" npx --yes skills \
     add 'gigio1023/agent-skills#main' \
     --global \
     --agent <target-agent-ids...> \
     --skill '*'
   ```

   If the CLI still prints `Agent detected — installing non-interactively`,
   terminate it immediately and stop. Do not let an unreviewed install finish.

4. Wait at the CLI's `Proceed with installation?` prompt and review the complete
   security table before answering:

   - Cancel on any Gen high/critical result or any Socket alert.
   - Inspect every Snyk medium/high/critical detail page. Continue only when the
     finding is inherent to the requested capability, the source and trust
     boundary are understood, and the risk is proportionate to the request.
   - Treat a missing security table or `--` results as unverified. Stop unless
     the user explicitly accepts proceeding without that audit evidence.
   - Answer yes only after the gate passes. Otherwise answer no, report the
     affected skill and finding, and do not rerun with a bypass flag.

5. Verify the global result:

   ```bash
   npx --yes skills list --global --json
   ```

   Confirm the expected names are present for the selected agents and report
   any missing entry instead of claiming a complete install.

## Selected Skills

When the user explicitly requests a subset, keep the same source and scope:

```bash
env "${audit_env[@]}" npx --yes skills \
  add 'gigio1023/agent-skills#main' \
  --global \
  --agent <target-agent-ids...> \
  --skill <skill-name>
```

Pass additional names after `--skill` when needed. Keep the same explicit agent
list used for the full-pack path and apply the same interactive security gate.

## Ongoing Updates

If the user explicitly wants every tracked global skill updated, including
skills installed from other sources, run:

```bash
npx --yes skills update --global --yes
```

This update command does not provide the audited pre-install decision gate. Use
it only after telling the user that limitation and receiving explicit
acceptance. For named skills, put their names before `--global`. To refresh only
this pack or pick up new skills, repeat the applicable audited `add` command
with the same agent list. Updates run on demand, not in the background.

## Gotchas

- Keep `#main` explicit and quote the complete source so the repository and ref
  remain visibly atomic as one argument.
- `npx --yes` approves fetching the Skills CLI. It is not permission to add the
  Skills CLI's own `--yes`, which would skip the audit decision point.
- Removing detection variables affects only the child CLI's prompt behavior; it
  does not alter the harness's actual sandbox or permission enforcement.
- Do not use `@main`; this CLI uses `@` for a skill filter, not a Git branch.
- Do not replace the source with `.`, an absolute checkout path, a PR branch, or
  a commit SHA, even when it is newer than remote `main`.
- Use `--global` for user scope. The current CLI discovers this repository's
  category layout without `--full-depth`.
- Do not use `--all`: it expands to every discovered skill and every supported
  agent. Use `--skill '*'` with an explicit `--agent` list instead.
- After the user accepts its audit limitation, use `update` directly. The
  current CLI does not document a separate read-only `check` step.
- `update` refreshes tracked skills but does not add newly published skill names;
  repeat the remote `add` command when the pack grows.
- `add` installs or refreshes skills present on `main`. It does not authorize
  deletion of unrelated or stale global skills; remove those only when the user
  explicitly names them.

## Output

Report that the source was `gigio1023/agent-skills#main`, the selected agents,
whether the full pack or a subset was installed or updated, the verification
result, the audit evidence reviewed, and any missing skill. If installation was
cancelled, report the exact partner finding and whether it is an inherent
capability risk or an unexplained blocker. Do not claim that unmerged work was
installed.
