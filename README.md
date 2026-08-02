# Agent Skills

[![skills.sh](https://skills.sh/b/gigio1023/agent-skills)](https://skills.sh/gigio1023/agent-skills)

A curated pack of 15 reusable Agent Skills for shipping software, operating
agent harnesses, writing clearly, and handling a few everyday workflows.

Each skill follows the [Agent Skills format](https://agentskills.io/) with a
`SKILL.md` file and any supporting references, scripts, or assets kept beside
it. Install only what you need with [`npx skills`](https://github.com/vercel-labs/skills),
then pull later revisions from the same tracked source.

[Migration notice](#development-skills-moved-to-the-gigio-pack) ·
[Browse the catalog](#skill-catalog) · [Install](#install-with-npx-skills) ·
[Update](#keep-skills-up-to-date) · [Related repositories](#related-skill-repositories) ·
[Local development](#local-development)

## Development skills moved to the gigio-pack

Nine work-loop skills that used to live in this repository have moved to
[gigio-pack](https://github.com/gigio1023/gigio-pack) (private repo; local
checkout at `~/git/agent-skills-orch/gigio-pack`). Their directories were
removed from this repository on 2026-07-26; install those nine from the
gigio-pack instead.

Five of the nine were renamed during the move (the last two renames landed
2026-07-26 with the pack's final naming):

| Old name (this repo) | New name (gigio-pack) |
| --- | --- |
| `unknowns-pass` | `find-unknowns` |
| `handoff-prompt` | `session-handoff` |
| `lower-capability-executor-prompt` | `small-model-handoff` |
| `fable5-judgment` | `fable5-model-routing` |
| `parallel-subagents` | `orchestrate-subagents` |

The other four kept their names: `commit-and-push`, `deep-interview`,
`draft-pr`, `git-worktree-setup`.

**2026-07-26 — eleven skills came back.** This notice originally covered 20
migrated skills. Six craft skills (`frontend-design`, `mermaid-diagrams`,
`python-docstrings`, `engineering-docs`, `terminology-review`,
`english-prompt-review`) and five meta skills (`skill-builder`,
`cross-harness-skills`, `fable5-prompting-guide`, `gpt56-sol-prompting-guide`,
`install-skill-pack`) returned to this repository as their canonical home.
Install all eleven from here, the normal way. Seven of the eleven
(`frontend-design`, `mermaid-diagrams`, `terminology-review`, `skill-builder`,
`cross-harness-skills`, `fable5-prompting-guide`, `gpt56-sol-prompting-guide`)
carry `SKILL.md` improvements ported back from the pack copies; the other four
are unchanged.

**2026-07-26 — two writing skills merged into `clear-writing`.**
`engineering-docs` and `terminology-review` were absorbed into the unified
[clear-writing](https://github.com/gigio1023/clear-writing) skill — one
router covering repository-grounded authoring, humanizing revision,
terminology review, and Korean polish. Their directories were removed from
this repository; install `clear-writing` from its own repository instead.

Everything else remains this repository's active catalog — 15 skills listed
in the [Skill catalog](#skill-catalog) below, including the three that never
moved: [1password-cli](skills/development/1password-cli/),
[pdf-page-count](skills/productivity/pdf-page-count/), and
[toss-portfolio-state](skills/development/toss-portfolio-state/).

## Install with `npx skills`

Prerequisite: Node.js 18 or newer.

Browse the published pack before installing anything:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' --list
```

Install selected skills globally for the agents you use:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' \
  --skill mermaid-diagrams skill-builder \
  --agent codex claude-code \
  --global \
  --yes
```

Replace the skill names and agent IDs as needed. Omit `--global` for a
project-local install.

To install all 15 skills for a deliberate set of agents, quote the wildcard so
the shell does not expand it:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' \
  --skill '*' \
  --agent codex claude-code cursor \
  --global \
  --yes
```

Prefer an explicit `--agent` list. The CLI's `--all` option targets every skill
and every supported agent, which is usually broader than intended.

Verify a global install with:

```bash
npx --yes skills list --global
```

The quoted source keeps the repository and `main` ref together as one literal
argument. Installing from the remote source, rather than a local checkout,
also gives the CLI the metadata it needs for later updates.

The CLI manages each agent's install destination. This repository therefore
does not maintain separate `.claude/`, `.codex/`, `.cursor/`, or `.gemini/`
installation adapters.

## Keep skills up to date

Remote installs are tracked by source, branch, skill path, and content version.
Update every tracked global skill with:

```bash
npx --yes skills update --global
```

Or update only named skills:

```bash
npx --yes skills update skill-builder mermaid-diagrams --global
```

Add a trailing `--yes` when the Skills CLI itself must run non-interactively:

```bash
npx --yes skills update --global --yes
```

Updates are pull-based, not automatic background subscriptions. `update`
refreshes skills already recorded in the lock metadata; it does not install new
skills added to this pack later. Rerun the relevant `add` command to pick up new
skills or to refresh only this repository without updating skills from other
sources. If an older install is reported as untracked, reinstall it once from
the quoted remote source above.

Use `update` directly; the current CLI does not document a separate read-only
`check` step.

## Skill catalog

The catalog is organized by the job a person wants to get done, rather than by
the agent that happens to run it. The on-disk source paths remain stable so
existing `npx skills` lock entries can continue to update in place.

- [Software Development and Delivery](#software-development-and-delivery) (1)
- [Agent and Harness Engineering](#agent-and-harness-engineering) (8)
- [Design and Visualization](#design-and-visualization) (2)
- [Writing and Language](#writing-and-language) (1)
- [Personal and Everyday Tools](#personal-and-everyday-tools) (3)

### Software Development and Delivery

| Skill | What it helps with |
| --- | --- |
| [python-docstrings](skills/development/python-docstrings/) | Document Python API contracts, lifecycle behavior, side effects, and invariants |

### Agent and Harness Engineering

| Skill | What it helps with |
| --- | --- |
| [cursor-cli-delegation](skills/productivity/cursor-cli-delegation/) | Delegate a closed execution mission through Cursor Agent CLI while the calling harness retains judgment and acceptance |
| [codex-delegate](skills/development/codex-delegate/) | Delegate packaged, bounded tasks from a non-Codex host to the flagship Codex model in Fast mode, with durable runs, file-only handoff, and packet-defined judgment |
| [cross-harness-skills](skills/development/cross-harness-skills/) | Build and audit one portable skill for Claude Code and Codex while isolating harness adapters |
| [fable5-prompting-guide](skills/development/fable5-prompting-guide/) | Write and migrate prompt stacks specifically for Claude Fable 5 |
| [goal-prompting](skills/development/goal-prompting/) | Explain, draft, review, translate, and activate verifiable goal prompts for Codex and Claude Code |
| [gpt56-sol-prompting-guide](skills/development/gpt56-sol-prompting-guide/) | Write and migrate prompt stacks for GPT-5.6 Sol and the GPT-5.6 family |
| [install-skill-pack](skills/development/install-skill-pack/) | Review and install the published pack globally from its tracked `main` source |
| [skill-builder](skills/development/skill-builder/) | Create, audit, maintain, and modernize reusable agent skills |

### Design and Visualization

| Skill | What it helps with |
| --- | --- |
| [frontend-design](skills/development/frontend-design/) | Apply visual hierarchy, art direction, interaction judgment, and UI quality checks |
| [mermaid-diagrams](skills/development/mermaid-diagrams/) | Design readable, parser-safe Mermaid diagrams and validate their rendering |

### Writing and Language

| Skill | What it helps with |
| --- | --- |
| [english-prompt-review](skills/productivity/english-prompt-review/) | Rewrite English technical prompts naturally and explain important nuance in Korean |

### Personal and Everyday Tools

| Skill | What it helps with |
| --- | --- |
| [1password-cli](skills/development/1password-cli/) | Use the local macOS 1Password CLI for vault, secret, OTP, and environment workflows |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce exact, minimum, or maximum page limits |
| [toss-portfolio-state](skills/development/toss-portfolio-state/) | Export a read-only Toss Invest portfolio and market-context snapshot |

## Related skill repositories

These independently versioned repositories are not included when this pack is
installed. Use each repository's README for its current install command,
supported harnesses, and update workflow.

| Repository | Included skills | What it adds |
| --- | --- | --- |
| [Astro Dev](https://github.com/gigio1023/astro-dev-skill) | `astro-dev` | Version-aware Astro implementation and migration guidance with focused checks for current framework conventions |
| [clear-writing](https://github.com/gigio1023/clear-writing) | `clear-writing` | Repository-grounded authoring, humanizing revision, terminology checks, and surgical Korean polish in one prose skill |
| [draw.io Agent Skill](https://github.com/gigio1023/drawio-agent-skill) | `drawio-diagram` | Native, editable draw.io authoring with structural, layout, export, and visual checks |
| [Game Studio](https://github.com/gigio1023/game-studio) | `game-direction`, `game-production`, `game-review` | Creator-owned direction, proof-based production, and evidence-first review across the game lifecycle |
| [Godot Best Practice](https://github.com/gigio1023/godot-best-practice) | `godot-best-practice` | Godot-native implementation and review grounded in the project's engine version, serialized resources, and engine-level evidence |
| [Unity Game Development](https://github.com/gigio1023/unity-game-dev-skill) | `unity-game-dev` | Version-aware Unity gameplay implementation and review across repository-only and live Editor workflows |

## Useful external skills

These are maintained elsewhere and are not part of this pack.

| Repository or skill | Includes | Useful for |
| --- | --- | --- |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | `obsidian-bases`, `obsidian-cli`, `obsidian-markdown`, and more | Working with Obsidian vaults and file formats |
| [find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) | `find-skills` | Discovering and installing additional skills |

You can also browse [skills.sh](https://skills.sh/) or search from the CLI:

```bash
npx --yes skills find
```

## Local development

This repository is a multi-skill pack. The canonical source for each bundled
skill is `skills/<source-category>/<skill-name>/`.

Inspect a checkout without creating an update-tracked install:

```bash
npx --yes skills add . --list
```

Before publishing a change, verify that each `SKILL.md` name matches its folder,
every referenced path exists, the README entry still points to the correct
skill, and the local listing discovers the expected 15 unique names. See
[Repository Structure](docs/repo-structure.md) for the catalog, storage, and
installation boundaries.

The pack was re-audited for GPT-5.6 Sol and Claude Fable 5 in July 2026.
Portable domain skills keep task-specific knowledge, authority boundaries, and
verification in shared files; exact model prompting stays in the dedicated
model guides.
