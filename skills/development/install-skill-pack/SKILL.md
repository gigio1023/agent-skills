---
name: install-skill-pack
description: >
  Use when installing or refreshing the published `gigio1023/agent-skills` pack
  globally for explicitly selected agents after changes reach `main`, or when
  updating already tracked global skills on request. Uses the quoted remote
  source with `npx skills` and verifies global discovery. NOT for local
  checkouts, PR or feature branches, commit SHAs, project-local installs,
  pre-merge testing, unscoped all-agent installs, or silently changing
  unrelated global skills.
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

3. Install the complete pack globally for those agents, replacing the target
   placeholder with the resolved IDs:

   ```bash
   npx --yes skills add 'gigio1023/agent-skills#main' \
     --global \
     --agent <target-agent-ids...> \
     --skill '*' \
     --yes
   ```

4. Verify the global result:

   ```bash
   npx --yes skills list --global --json
   ```

   Confirm the expected names are present for the selected agents and report
   any missing entry instead of claiming a complete install.

## Selected Skills

When the user explicitly requests a subset, keep the same source and scope:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' \
  --global \
  --agent <target-agent-ids...> \
  --skill <skill-name> \
  --yes
```

Pass additional names after `--skill` when needed. Keep the same explicit agent
list used for the full-pack path.

## Ongoing Updates

If the user explicitly wants every tracked global skill updated, including
skills installed from other sources, run:

```bash
npx --yes skills update --global --yes
```

For named skills, put their names before `--global`. To refresh only this pack,
or to pick up skills added after the original install, repeat the applicable
remote `add` command from above with the same explicit agent list. Updates are
on demand; they do not run in the background.

## Gotchas

- Keep `#main` explicit and quote the complete source so the repository and ref
  remain visibly atomic as one argument.
- Do not use `@main`; this CLI uses `@` for a skill filter, not a Git branch.
- Do not replace the source with `.`, an absolute checkout path, a PR branch, or
  a commit SHA, even when it is newer than remote `main`.
- Use `--global` for user scope. The current CLI discovers this repository's
  category layout without `--full-depth`.
- Do not use `--all`: it expands to every discovered skill and every supported
  agent. Use `--skill '*'` with an explicit `--agent` list instead.
- Use `update` directly. The current CLI does not document a separate read-only
  `check` step.
- `update` refreshes tracked skills but does not add newly published skill names;
  repeat the remote `add` command when the pack grows.
- `add` installs or refreshes skills present on `main`. It does not authorize
  deletion of unrelated or stale global skills; remove those only when the user
  explicitly names them.

## Output

Report that the source was `gigio1023/agent-skills#main`, the selected agents,
whether the full pack or a subset was installed or updated, the verification
result, and any missing skill. Do not claim that unmerged work was installed.
