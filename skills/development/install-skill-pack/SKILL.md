---
name: install-skill-pack
description: >
  Use when installing or refreshing skills globally from a user-selected Git
  repository with the Skills CLI, optionally from a named branch or exact
  commit, for explicitly selected agents. Reviews the selected packages before
  installation, then verifies revision identity, installed content, and
  discovery. NOT for unpublished local changes, project-local installs,
  unscoped all-agent installs, or silently changing unrelated global skills.
---

# Install Skill Pack

Install reviewed skills from the user's Git repository. The default path passes
the bare source to the CLI and follows the remote's default branch. Branch and
commit pins are optional.

Let the Skills CLI manage global destinations for the agents named by the user.
Third-party security assessments are optional context: read the selected source
directly, make the security decision from that evidence, and do not treat a
missing scanner result as either a pass or a blocker.

## Quick Path

1. Resolve the repository source, selected skill names, and explicit target
   agent IDs from the user's request. Accept GitHub shorthand such as
   `owner/repo`, a full GitHub or GitLab repository URL, or another cloneable
   Git URL. Do not widen the target list to every CLI-supported agent. If no
   skills were named, list the repository's skills first; install every package
   only when the user explicitly requested the complete pack.

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

3. Resolve npm's current `skills@latest` version once and verify that the CLI
   reports the same version:

   ```bash
   skills_cli_version="$(npm view skills@latest version)"
   npx --yes "skills@$skills_cli_version" --version
   ```

   Stop if npm returns an empty or malformed version or the two versions differ.
   Executing the npm CLI is a separate package-manager trust boundary; reviewing
   a skill repository does not establish the CLI publisher's integrity.

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
   explicitly:

   ```bash
   npx --yes "skills@$skills_cli_version" add \
     "$install_source" \
     --global \
     --agent <target-agent-id> \
     --agent <another-target-agent-id> \
     --skill <skill-name> \
     --yes
   ```

   Default mode leaves `install_source` bare, so the CLI follows the remote's
   default branch without assuming `main` or `master`. Commit mode uses the
   reviewed local checkout because remote `#ref` does not reliably accept a raw
   commit ID.

9. Inspect `skills list --global --json`, confirm each requested agent discovers
   every requested name, and take installed directories from the output's
   `path` fields. Recursively compare each installed package with the matching
   reviewed package, for example with `diff -qr`. Ignore installer bookkeeping
   outside the skill directory, but require every installed skill file to
   match. A mismatch means the install is unverified: do not use the skill,
   preserve the review checkout, and report the differing files.

10. Remove the disposable checkout only after content and discovery
    verification pass.

## Selecting Skills

Pass one `--skill` per requested frontmatter name:

```bash
npx --yes "skills@$skills_cli_version" add \
  "$install_source" \
  --global \
  --agent <target-agent-id> \
  --skill <skill-name> \
  --skill <another-skill-name> \
  --yes
```

Use `--skill '*'` only when the user explicitly requests every installable
skill from the repository. That broad scope requires reading every package
first. If a requested name is absent from the reviewed snapshot, stop; do not
silently switch branches, commits, repositories, or local checkouts.

## Revisions And Updates

- Bare sources and named branches follow their latest remote commit. Re-review
  each changed commit.
- Exact commits are fixed. Reinstall through the detached checkout because the
  CLI does not track that temporary local source for remote updates.

If the user explicitly wants every tracked global skill updated, including
skills installed from other sources, run the current npm `latest` CLI:

```bash
npx --yes skills@latest update --global --yes
```

This can fetch sources outside the requested scope and bypass review. State that
limitation and receive explicit acceptance first. For named skills, put their
names before `--global`.

## Gotchas

- `latest` means the npm `latest` dist-tag at operation start. Snapshot it once
  so a CLI release cannot change during the operation.
- Running the Skills CLI trusts its npm publisher and executes remote CLI code.
  The source review covers selected skill packages, not npm provenance or the
  CLI implementation.
- Omit a ref for the normal path. Do not invent `#main`; the remote decides its
  default branch.
- `#<branch>` selects a branch. Do not use `@<branch>`; the CLI interprets `@`
  as a skill filter.
- Do not assume `source#<commit>` can pin an arbitrary commit. Use the reviewed
  detached checkout path.
- Do not use `--all`: it expands to every supported agent. Repeat `--agent` for
  the explicitly selected targets.
- Installation can overwrite selected skills. Back up only those directories
  when the exact old version must be preserved until verification passes.
- Global installation does not authorize deletion of unrelated or stale
  skills. Remove those only when the user explicitly names them.

## Validation

Before publishing this skill, validate the package and confirm repository
discovery. Run the active `skill-builder` validator against
`skills/development/install-skill-pack`, then run:

```bash
npx --yes skills@latest add . --list --full-depth
```

## Output

Report the resolved Skills CLI version, repository source, revision mode,
reviewed commit, selected agents and skills, source-review decision,
installed-content comparison, and discovery result. For an exact commit, also
state that automatic remote updates are unavailable and the pinned workflow
must be rerun. If blocked, identify the observable finding, affected file or
command, and whether the risk is inherent to the requested capability or
unexplained.
