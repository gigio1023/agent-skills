---
name: install-skill-pack
description: >
  Use when installing or refreshing skills globally from a user-selected Git
  repository or revision with the Skills CLI for the standard Claude Code,
  Hermes Agent, OpenCode, Cursor, and Codex targets. Reviews packages and
  verifies revision identity, installed content, symlinks, and discovery. NOT
  for unpublished local changes, project-local installs, unscoped all-agent
  installs, or silently changing unrelated global skills.
---

# Install Skill Pack

Install reviewed skills from the user's Git repository. The default path passes
the bare source to the CLI and follows the remote's default branch. Branch and
commit pins are optional.

Use the five-agent standard set unless the user explicitly excludes a member.
Add named extras without the broad `--all` option. Let the CLI manage the
canonical global package and agent-facing links.

Third-party security assessments are optional context: read the selected source
directly, make the security decision from that evidence, and do not treat a
missing scanner result as either a pass or a blocker.

## Quick Path

1. Resolve the repository source and selected skill names. Accept GitHub
   shorthand, a full repository URL, or another cloneable Git URL. Read
   [`references/skills-cli-usage.md`](references/skills-cli-usage.md) for the
   standard target IDs, current CLI contract, symlink mode, and per-agent
   verification. If no skills were named, list the repository's skills first;
   install every package only when the user explicitly requested the complete
   pack.

2. Select one revision mode:

   - Default: no revision input. Use the remote default branch at its latest
     commit and keep the CLI source bare, for example `owner/repo`.
   - Branch: append `#<branch>` to the CLI source.
   - Commit: require an exact full commit ID and use the detached-checkout path
     below. Do not append a raw commit ID to the CLI source.

   Branch and commit inputs are mutually exclusive. Preserve the user's source
   form for the CLI. Normalize it separately for Git review; for example, clone
   `owner/repo` through
   `https://github.com/owner/repo.git`. Read and apply
   [`references/revision-selection.md`](references/revision-selection.md) to
   prepare `install_source`, `reviewed_sha`, and the review checkout.

3. Resolve npm's current stable `skills@latest` version once per operation and
   verify its version and live interface through the CLI-usage reference. Stop
   if the version is malformed, the reported version differs, or a standard
   target ID is unsupported. Executing the npm CLI is a separate package-manager
   trust boundary; reviewing a skill repository does not establish the CLI
   publisher's integrity.

4. Prepare the disposable checkout through the selected revision path. Record
   the checked-out commit as `reviewed_sha`. Stop if the source cannot be mapped
   to one repository, the branch is absent, the commit is unreachable, or the
   exact requested commit differs from the checkout.

5. Locate every requested skill by its frontmatter name and require exactly one
   matching package per name. Before installing anything, read its complete
   `SKILL.md` and every file in its package, including references, scripts,
   assets, templates, configuration, symlinks, and otherwise non-obvious files.
   For a full-pack install, review every package that will be installed; do not
   sample.

6. Read and apply [`references/source-review.md`](references/source-review.md).
   Record concise observable evidence for each selected skill: files inspected,
   intended capability, commands and external access, material findings, and a
   `pass` or `block` decision.

7. Immediately before a default-branch or named-branch installation, use the
   revision reference to confirm the remote still points to `reviewed_sha`. If
   it changed, discard the checkout and repeat the review against the new
   snapshot. An exact commit is immutable once the checkout and full ID match.

8. Install with the resolved CLI version, passing every target agent and skill
   explicitly. The standard target IDs are deliberately repeated; append named
   extras and omit only explicit user exclusions:

   ```bash
   npx --yes "skills@$skills_cli_version" add \
     "$install_source" \
     --global \
     --agent claude-code \
     --agent hermes-agent \
     --agent opencode \
     --agent cursor \
     --agent codex \
     --skill <skill-name> \
     --yes
   ```

   Default mode leaves `install_source` bare, so the CLI follows the remote's
   default branch without assuming `main` or `master`. Commit mode uses the
   reviewed local checkout because remote `#ref` does not reliably accept a raw
   commit ID. Omit `--copy`: the verified normal path uses the CLI's default
   canonical-copy plus agent-symlink mode.

9. Inspect `skills list --global --agent <id> --json` separately for every
   target. Require each requested name and that agent's display name in the
   result's `agents` field; name presence alone is insufficient. Take the
   canonical installed directories from the `path` fields, compare every file
   with the reviewed package, and apply the CLI-usage reference's symlink checks
   for non-universal agents. A content mismatch, absent discovery record,
   unresolved link, or copy fallback makes the install unverified: do not use
   the skill, preserve the review checkout, and report the evidence.

10. Remove the disposable checkout only after content and discovery
    verification pass.

## Selecting Skills

Add one `--skill <frontmatter-name>` argument per requested package to the
standard command. Use `--skill '*'` only for an explicitly requested complete
pack, after reviewing every package. If a name is absent, stop; do not silently
switch revisions, repositories, or local checkouts.

## Revisions And Updates

- Bare sources and named branches follow their remote and require review again
  after a commit change. Exact commits reinstall through the detached checkout;
  the CLI cannot update that temporary local source from the remote.

Only an explicit request to update every tracked global skill authorizes:

```bash
npx --yes "skills@$skills_cli_version" update --global --yes
```

It can fetch unreviewed sources outside the current repository. State that scope
beforehand. For named skills, put their names before `--global`.

## Gotchas

- Running the Skills CLI trusts its npm publisher and executes remote CLI code.
  The source review covers selected skill packages, not npm provenance or the
  CLI implementation.
- Omit a ref for the normal path. Do not invent `#main`; the remote decides its
  default branch.
- `#<branch>` selects a branch. Do not use `@<branch>`; the CLI interprets `@`
  as a skill filter.
- Do not assume `source#<commit>` can pin an arbitrary commit. Use the reviewed
  detached checkout path.
- Do not use `--all` or add `--copy` on the normal path. The former expands the
  target set; the latter defeats the required agent-link topology.
- Installation can overwrite selected skills. Back up only those directories
  when the exact old version must be preserved until verification passes.
- Global installation does not authorize deletion of unrelated or stale
  skills. Remove those only when the user explicitly names them.

## Validation

Before publishing this skill, validate the package and confirm repository
discovery. Run the active `skill-builder` validator against
`skills/development/install-skill-pack`, then run:

```bash
npx --yes "skills@$skills_cli_version" add . --list --full-depth
```

## Output

Report the resolved Skills CLI version, repository source, revision mode,
reviewed commit, selected agents and skills, source-review decision, canonical
content comparison, agent-link topology, and discovery result. Name any
explicit standard-target exclusion. For an exact commit, also state that
automatic remote updates are unavailable and the pinned workflow must be rerun.
If blocked, identify the observable finding, affected file or command, and
whether the risk is inherent to the requested capability or unexplained.
