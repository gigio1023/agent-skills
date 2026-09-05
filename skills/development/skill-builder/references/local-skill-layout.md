# Local Skill Layout

Use this reference when creating, moving, or improving skills that should live
in this repository.

## Canonical Source

The source of truth should live in the checked-out skill pack:

```text
skills/<category>/<skill-name>/
```

Use existing categories unless a new one is clearly needed:

- `development/`: coding, design, CLI/API, skill-building, verification.
- `productivity/`: research workflows, writing workflows, orchestration, and
  operating procedures.

Each skill folder should contain `SKILL.md` plus any `references/`, `scripts/`,
`assets/`, or config files it needs.

## Install Locations

The shared runtime-visible location is:

```text
~/.agents/skills/<skill-name>
```

Prefer a symlink from `~/.agents/skills/<skill-name>` to the canonical repo
folder when actively developing a skill. That keeps edits git-tracked while
keeping the installed skill discoverable.

Claude Code can share the same installed set through:

```text
~/.claude/skills -> ~/.agents/skills
```

That shared-directory symlink is one development layout. An installer-managed
per-skill link is also valid. Preserve the selected topology; skill editing
does not authorize replacing the user's whole Claude Code skill directory.

## Creation Workflow

1. Create the canonical folder under `skills/`.
2. Write `SKILL.md` and references there.
3. Add or update `README.md` only when the skill should be listed as part of the
   public skill pack.
4. When installation is requested, expose the skill under `~/.agents/skills/`
   with the selected installer or an explicitly chosen development symlink.
5. For that installation, verify the existing shared-directory or per-skill
   link topology without converting unrelated agent configuration.
6. Validate frontmatter, referenced paths, line count, and trigger examples.

## Migrating Existing Local Skills

For a skill that already exists only under `~/.agents/skills/`:

1. Copy the entire skill folder into the canonical repo location.
2. Compare the copy against the original.
3. Replace the installed folder with a symlink only after the copy matches.
4. Preserve user changes; do not delete or overwrite a local-only skill unless
   the canonical copy has been verified.

## Improvement Workflow

- Edit the canonical repo copy.
- If `~/.agents/skills/<skill-name>` is a symlink, no extra sync is needed.
- If it is a plain directory, report that repository edits are not installed.
  Refresh it only when installation is part of the user's requested scope.
- Keep exact model-routing preferences in dedicated routing skills instead of
  burying them inside harness-neutral skills.

## Validation

Before finishing:

- `SKILL.md` frontmatter name matches the folder and intended trigger.
- Description is under 1024 characters and trigger-oriented.
- `SKILL.md` is comfortably under 500 lines or split into references.
- Every referenced path exists relative to the skill folder.
- The installed `~/.agents/skills` entry points at the intended canonical
  source or the divergence is explained.
- No secrets, tokens, local credentials, private hostnames, or personal profile
  details were copied into the repo.
