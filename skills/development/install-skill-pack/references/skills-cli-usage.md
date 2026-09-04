# Skills CLI Usage

Read this before each installation. It defines the standard agent set and the
live CLI checks needed to keep installation behavior aligned with the npm
release used for that operation.

## Resolve The Stable CLI

Treat npm's `latest` dist-tag as the highest stable release. Resolve it once and
reuse the exact version for review, installation, listing, and removal commands:

```bash
skills_cli_version="$(npm view skills@latest version)"
case "$skills_cli_version" in
  ''|*[!0-9.]*|.*|*.) exit 1 ;;
esac
test "$(npx --yes "skills@$skills_cli_version" --version)" = "$skills_cli_version"
npx --yes "skills@$skills_cli_version" --help
```

Require live help to expose `add`, `--global`, repeatable `--agent`, repeatable
`--skill`, `--yes`, `--copy`, and JSON listing. Stop rather than adapting an
unknown interface from memory. Do not opt into a snapshot or prerelease unless
the user explicitly requests that separate trust boundary.

## Standard Target Set

Install every skill to these five CLI IDs unless the user explicitly excludes a
member:

| Agent | CLI ID | Global topology in symlink mode |
| --- | --- | --- |
| Claude Code | `claude-code` | Agent-facing link below `CLAUDE_CONFIG_DIR/skills`, defaulting to `~/.claude/skills` |
| Hermes Agent | `hermes-agent` | Agent-facing link below `HERMES_HOME/skills`, defaulting to `~/.hermes/skills` |
| OpenCode | `opencode` | Universal canonical package under `~/.agents/skills` |
| Cursor | `cursor` | Universal canonical package under `~/.agents/skills` |
| Codex | `codex` | Universal canonical package under `~/.agents/skills` |

Append other explicitly requested IDs, but never replace the standard set with
`--all`. Validate IDs through the resolved CLI's registry when exposed; otherwise
the explicit `add` command is the compatibility gate and must fail closed on an
unknown ID. Hermes uses `hermes-agent`, not `hermes`.

## Preserve Symlink Mode

The normal non-interactive command omits `--copy`. With the standard set's
multiple target directories, the CLI keeps its default symlink mode: it copies
the reviewed package once to the canonical `~/.agents/skills/<name>` directory,
lets universal agents read that location directly, and links non-universal
agent directories to it.

Read the installation summary. Require OpenCode, Cursor, and Codex to appear as
universal targets and Claude Code and Hermes Agent as symlink targets. A reported
symlink fallback or an unexpected copy-only summary fails verification.

An agent may link its entire `skills` directory to the canonical directory
instead of linking each skill. Accept either layout only when the agent-facing
skill resolves to the same canonical package and at least the skill entry or its
parent `skills` directory is a symbolic link.

## Verify Every Agent

For each selected ID, run the resolved version independently:

```bash
npx --yes "skills@$skills_cli_version" list \
  --global --agent <agent-id> --json
```

For every requested skill, require all of the following:

- the JSON entry's `name` matches and its `agents` array contains that target's
  display name;
- the canonical package contains exactly the reviewed files with matching
  contents and executable bits;
- Claude Code and Hermes Agent resolve to that canonical package through a
  verified skill-level or parent-directory symlink;
- OpenCode, Cursor, and Codex resolve through the universal canonical directory,
  so no separate per-agent symlink is expected.

Do not infer discovery from a directory that merely exists. Some CLI listings
can show the canonical package while leaving `agents` empty for the requested
filter; that is a failed target installation, not success.
