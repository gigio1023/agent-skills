# Skills CLI Usage

Read this before each installation. It defines the standard agent set and the live CLI checks needed to keep installation behavior aligned with the npm release used for that operation.

## Resolve The Stable CLI

Treat npm's `latest` dist-tag as the highest stable release. Resolve it once and reuse the exact version for review, installation, listing, and removal commands:

```bash
skills_cli_version="$(npm view skills@latest version)"
case "$skills_cli_version" in
  ''|*[!0-9.]*|.*|*.) exit 1 ;;
esac
test "$(npx --yes "skills@$skills_cli_version" --version)" = "$skills_cli_version"
npx --yes "skills@$skills_cli_version" --help
```

Require live help to expose `add`, `--global`, repeatable `--agent`, repeatable `--skill`, `--yes`, `--copy`, and JSON listing. Stop rather than adapting an unknown interface from memory. Do not opt into a snapshot or prerelease unless the user explicitly requests that separate trust boundary.

An npm policy can refuse the newest release before this resolve step even runs. `min-release-age` in `~/.npmrc` rejects versions published within its window, and npm reports the refusal as `ETARGET / No matching version found ... with a date before <cutoff>`, which reads like the version does not exist. Read it as a policy block: resolve `latest`, then step down to the newest release older than the cutoff. Do not bypass the policy by pinning a snapshot, a tag, or a mirror.

## Standard Target Set

Install every skill to these nine CLI IDs unless the user explicitly excludes a member:

| Agent | CLI ID | Global topology in symlink mode |
| --- | --- | --- |
| Claude Code | `claude-code` | Agent-facing link below `CLAUDE_CONFIG_DIR/skills`, defaulting to `~/.claude/skills` |
| Hermes Agent | `hermes-agent` | Agent-facing link below `HERMES_HOME/skills`, defaulting to `~/.hermes/skills` |
| OpenCode | `opencode` | Universal canonical package under `~/.agents/skills` |
| Cursor | `cursor` | Universal canonical package under `~/.agents/skills` |
| Codex | `codex` | Universal canonical package under `~/.agents/skills` |
| GitHub Copilot | `github-copilot` | Universal canonical package under `~/.agents/skills`; its own CLI reads that directory as a personal source |
| ZCode | `zcode` | Agent-facing link below `~/.zcode/skills` |
| OpenClaw | `openclaw` | Agent-facing link below `~/.openclaw/skills`, falling back to `~/.clawdbot` or `~/.moltbot` homes |
| Grok | `grok` | Agent-facing link below `$GROK_HOME/skills`, defaulting to `~/.grok/skills` |

Append other explicitly requested IDs, but never replace the standard set with `--all`. Validate IDs through the resolved CLI's registry when exposed; otherwise the explicit `add` command is the compatibility gate and must fail closed on an unknown ID. Hermes uses `hermes-agent`, not `hermes`. The CLI decides an agent is universal when its registry `skillsDir` is the canonical `.agents/skills`; when a target's topology matters for verification, read the registry from `dist/cli.mjs` in the npx cache instead of assuming this table.

## Preserve Symlink Mode

The normal non-interactive command omits `--copy`. With the standard set's multiple target directories, the CLI keeps its default symlink mode: it copies the reviewed package once to the canonical `~/.agents/skills/<name>` directory, lets universal agents read that location directly, and links non-universal agent directories to it.

Read the installation summary. Require OpenCode, Cursor, Codex, and GitHub Copilot to appear as universal targets and Claude Code, Hermes Agent, ZCode, OpenClaw, and Grok as symlink targets. A reported symlink fallback or an unexpected copy-only summary fails verification.

An agent may link its entire `skills` directory to the canonical directory instead of linking each skill. Accept either layout only when the agent-facing skill resolves to the same canonical package and at least the skill entry or its parent `skills` directory is a symbolic link.

## Verify Every Agent

For each selected ID, run the resolved version independently:

```bash
npx --yes "skills@$skills_cli_version" list \
  --global --agent <agent-id> --json
```

For every requested skill, require all of the following:

- the JSON entry's `name` matches and resolves to the canonical package;
- when the target harness is detected on the host, its display name appears in the entry's `agents` array;
- the canonical package contains exactly the reviewed files with matching contents and executable bits;
- symlink targets (Claude Code, Hermes Agent, ZCode, OpenClaw, Grok) resolve to that canonical package through a verified skill-level or parent-directory symlink;
- universal targets (OpenCode, Cursor, Codex, GitHub Copilot) resolve through the universal canonical directory, so no separate per-agent symlink is expected.

Universal targets share one canonical directory. When such a harness is not installed or its configured home is absent, the CLI may accept the target and prepare the canonical package while omitting its display name from `agents`. Require that target in the successful installation summary, leave its config directory untouched, and report `canonical-ready; runtime discovery unavailable`. If the harness is present but omitted, treat that as failed discovery.

Do not infer runtime discovery from a directory that merely exists. The JSON `name` and canonical path prove package readiness; the `agents` member proves discovery only for a harness the CLI can detect.

## Check Lock Freshness

The lock file's `skillFolderHash` is the git tree hash of the skill folder, not a content digest of a tarball. `git rev-parse <rev>:<skill-path>` in the source repository therefore says whether an installed skill is current without diffing files: equal hashes mean the canonical package matches that revision exactly. Use it to decide whether a reinstall is needed and to confirm one afterwards; a mismatch with matching content means only the lock's source metadata is stale.
