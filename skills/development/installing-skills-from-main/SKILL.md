---
name: installing-skills-from-main
description: >
  Use when installing or refreshing the `gigio1023/agent-skills` pack globally
  after changes have landed on `main`. Always uses the quoted
  `gigio1023/agent-skills#main` source with `npx skills`, installs into the
  user-level `~/.agents/skills` location, and verifies discovery. NOT for local
  checkouts, PR or feature branches, commit SHAs, project-local installs,
  pre-merge testing, or silently pruning unrelated global skills.
---

# Installing Skills from Main

Install only the published `main` branch of `gigio1023/agent-skills` into the
global agent skill location. Never substitute a newer local checkout or PR ref.

## Quick Path

1. Confirm the published `main` contents without installing:

   ```bash
   npx --yes skills add 'gigio1023/agent-skills#main' --list --full-depth
   ```

   If a requested skill is absent, stop. It has not reached `main`; do not fall
   back to a local path, feature branch, or commit.

2. Install the complete pack globally for all supported agents:

   ```bash
   npx --yes skills add 'gigio1023/agent-skills#main' \
     --global \
     --all \
     --full-depth
   ```

3. Verify the global result:

   ```bash
   npx --yes skills list --global --json
   ```

   Confirm the expected names resolve under `~/.agents/skills` and report any
   missing entry instead of claiming a complete install.

## Selected Skills

When the user explicitly requests a subset, keep the same source and scope:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' \
  --global \
  --agent '*' \
  --skill <skill-name> \
  --yes \
  --full-depth
```

Repeat `--skill <name>` for additional skills. Quote `'*'` so the shell does not
expand it.

## Gotchas

- Keep `#main` explicit and quote the complete source. An unquoted `#` starts a
  shell comment and silently drops the branch constraint.
- Do not use `@main`; this CLI uses `@` for a skill filter, not a Git branch.
- Do not replace the source with `.`, an absolute checkout path, a PR branch, or
  a commit SHA, even when it is newer than remote `main`.
- Use `--global` for user scope and `--full-depth` because this repository stores
  skills below category directories.
- `add` installs or refreshes skills present on `main`. It does not authorize
  deletion of unrelated or stale global skills; remove those only when the user
  explicitly names them.

## Output

Report that the source was `gigio1023/agent-skills#main`, whether the full pack
or a subset was installed, the verification result, and any missing skill. Do
not claim that unmerged work was installed.
