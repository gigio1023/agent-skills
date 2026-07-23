---
name: install-skill-pack
description: >
  Use when installing or refreshing the published `gigio1023/agent-skills` pack
  globally for explicitly selected agents after changes reach `main`, or when
  updating already tracked global skills on request. Reviews the exact published
  skill source before direct Skills CLI installation, then verifies source
  identity, installed content, and discovery. NOT for PR branches, unpublished
  local changes, project-local installs, pre-merge testing, unscoped all-agent
  installs, or silently changing unrelated global skills.
---

# Install Skill Pack

Install only a reviewed snapshot of the published `main` branch of
`gigio1023/agent-skills`. Let the Skills CLI manage destinations for the agents
named by the user. Third-party security assessments are optional context: read
the selected source directly, make the security decision from that evidence,
and do not treat a missing scanner result as either a pass or a blocker.

## Quick Path

1. Resolve an explicit list of target agent IDs from the user's request or the
   current harness. Do not widen it to every CLI-supported agent.

2. Resolve npm's current `skills@latest` version once and verify that the CLI
   reports the same version:

   ```bash
   cli_version="$(npm view skills@latest version)"
   npx --yes "skills@$cli_version" --version
   ```

   Stop if npm returns an empty or malformed version or the two versions differ.
   Executing the npm CLI is a separate package-manager trust boundary; reviewing
   this skill pack does not establish the CLI publisher's integrity.

3. Clone the published `main` branch into a disposable directory and record the
   reviewed commit:

   ```bash
   review_root="$(mktemp -d "${TMPDIR:-/tmp}/skill-pack-review.XXXXXX")"
   git clone --depth 1 --branch main \
     https://github.com/gigio1023/agent-skills.git "$review_root/repo"
   reviewed_sha="$(git -C "$review_root/repo" rev-parse HEAD)"
   ```

4. Locate every requested skill by its frontmatter name and require exactly one
   matching package per name. Before installing anything, read its complete
   `SKILL.md` and every file in its package, including references, scripts,
   assets, templates, configuration, symlinks, and otherwise non-obvious files.
   For a full-pack install, review every skill that will be installed; do not
   sample.

5. Read and apply [`references/source-review.md`](references/source-review.md).
   Record concise observable evidence for each selected skill: files inspected,
   intended capability, commands and external access, material findings, and a
   `pass` or `block` decision.

6. Immediately before installation, confirm that published `main` still points
   to the reviewed commit:

   ```bash
   current_sha="$(
     git ls-remote https://github.com/gigio1023/agent-skills.git \
       refs/heads/main | awk '{print $1}'
   )"
   test -n "$current_sha" && test "$current_sha" = "$reviewed_sha"
   ```

   If it changed, discard the review checkout, clone the new snapshot, and
   repeat the review. Never install source that changed after inspection.

7. Install directly from the published source with the already resolved CLI
   version, passing every agent and selected skill explicitly:

   ```bash
   npx --yes "skills@$cli_version" add \
     'gigio1023/agent-skills#main' \
     --global \
     --agent <target-agent-id> \
     --agent <another-target-agent-id> \
     --skill <skill-name> \
     --yes
   ```

8. Inspect `skills list --global --json`, confirm each requested agent discovers
   every requested name, and take the installed directory from that output's
   `path` field. Recursively compare it with the corresponding reviewed package,
   for example with `diff -qr`. Ignore installer bookkeeping outside the skill
   directory, but require every installed skill file to match. A mismatch means
   the install is unverified: do not use the skill, preserve the review
   checkout, and report the differing files.

9. Remove the disposable checkout only after content and discovery verification
   pass.

## Selected Skills

Pass one `--skill` per requested name:

```bash
npx --yes "skills@$cli_version" add \
  'gigio1023/agent-skills#main' \
  --global \
  --agent <target-agent-id> \
  --skill <skill-name> \
  --skill <another-skill-name> \
  --yes
```

Use `--skill '*'` only when the user explicitly requests the complete published
pack. That broad scope requires reading every installable package first. Prefer
named skills when the user requested named skills. If a requested name is absent
from the reviewed snapshot, stop; do not fall back to a PR branch or unpublished
checkout.

## Ongoing Updates

To refresh this pack or pick up newly published skills, repeat the snapshot,
source review, identity check, direct install, content comparison, and discovery
verification. A prior review does not cover a changed commit.

If the user explicitly wants every tracked global skill updated, including
skills installed from other sources, run the current npm `latest` CLI:

```bash
npx --yes skills@latest update --global --yes
```

That command can fetch sources outside this pack and therefore bypasses this
skill's source review. Use it only after stating the limitation and receiving
explicit acceptance. For named skills, put their names before `--global`.
Updates run on demand, not in the background.

## Gotchas

- `latest` means the npm `latest` dist-tag at operation start. Snapshot it once
  so a CLI release cannot change during the operation.
- Running the Skills CLI trusts its npm publisher and executes remote CLI code.
  The source review covers the selected skill packages, not npm provenance or
  the CLI implementation.
- Stop if the resolved version is empty, malformed, or differs from the CLI's
  own `--version` output.
- Keep `#main` explicit and quote the complete source. Do not use `@main`; the
  CLI interprets `@` as a skill filter rather than a Git branch.
- Do not use `--all`: it expands to every supported agent. Repeat `--agent` for
  the explicitly selected targets.
- Global installation does not authorize deletion of unrelated or stale skills.
  Remove those only when the user explicitly names them.
- Installation can overwrite a previous copy. If preserving the exact old
  version matters, back up the selected installed directories before the direct
  install and keep that backup until verification passes.

## Validation

Before publishing this skill, validate the package and confirm repository
discovery. Run the active `skill-builder` validator against
`skills/development/install-skill-pack`, then run:

```bash
npx --yes skills@latest add . --list --full-depth
```

## Output

Report the resolved Skills CLI version, source, reviewed commit, selected agents
and skills, source-review decision, installed-content comparison, and discovery
result. Do not claim that unmerged work was installed. If blocked, identify the
observable finding, affected file or command, and whether the risk is inherent
to the requested capability or unexplained.
