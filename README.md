# Agent Skills

[![skills.sh](https://skills.sh/b/gigio1023/agent-skills)](https://skills.sh/gigio1023/agent-skills)

A curated pack of 21 reusable Agent Skills for shipping software, operating
agent harnesses, writing clearly, making difficult decisions, and handling a
few everyday workflows.

Each skill follows the [Agent Skills format](https://agentskills.io/) with a
`SKILL.md` file and any supporting references, scripts, or assets kept beside
it. Install only what you need with [`npx skills`](https://github.com/vercel-labs/skills),
then pull later revisions from the same tracked source.

[Browse the catalog](#skill-catalog) · [Install](#install-with-npx-skills) ·
[Update](#keep-skills-up-to-date) · [Standalone skills](#related-standalone-skills) ·
[Local development](#local-development)

## Install with `npx skills`

Prerequisite: Node.js 18 or newer.

Browse the published pack before installing anything:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' --list
```

Install selected skills globally for the agents you use:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' \
  --skill engineering-docs draft-pr \
  --agent codex claude-code \
  --global \
  --yes
```

Replace the skill names and agent IDs as needed. Omit `--global` for a
project-local install.

To install all 21 skills for a deliberate set of agents, quote the wildcard so
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
npx --yes skills update skill-builder handoff-prompt --global
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

- [Software Development and Delivery](#software-development-and-delivery) (5)
- [Agent and Harness Engineering](#agent-and-harness-engineering) (7)
- [Design and Visualization](#design-and-visualization) (2)
- [Judgment and Collaboration](#judgment-and-collaboration) (4)
- [Writing and Language](#writing-and-language) (2)
- [Personal and Everyday Tools](#personal-and-everyday-tools) (3)

### Software Development and Delivery

| Skill | What it helps with |
| --- | --- |
| [commit-and-push](skills/development/commit-and-push/) | Build logical commits and push safely without absorbing unrelated worktree changes |
| [draft-pr](skills/development/draft-pr/) | Publish or update draft GitHub PRs with `gh` while preserving reviewer context |
| [engineering-docs](skills/development/engineering-docs/) | Create and reshape evidence-backed engineering documentation |
| [python-docstrings](skills/development/python-docstrings/) | Document Python API contracts, lifecycle behavior, side effects, and invariants |
| [git-worktree-setup](skills/development/git-worktree-setup/) | Start implementation in an isolated workspace without taking over harness-managed worktrees |

### Agent and Harness Engineering

| Skill | What it helps with |
| --- | --- |
| [cross-harness-skills](skills/development/cross-harness-skills/) | Build and audit one portable skill for Claude Code and Codex while isolating harness adapters |
| [fable5-prompting-guide](skills/development/fable5-prompting-guide/) | Write and migrate prompt stacks specifically for Claude Fable 5 |
| [gpt56-sol-prompting-guide](skills/development/gpt56-sol-prompting-guide/) | Write and migrate prompt stacks for GPT-5.6 Sol and the GPT-5.6 family |
| [lower-capability-executor-prompt](skills/development/lower-capability-executor-prompt/) | Hand off finished plans as bounded change, command, or inspection prompts for lower-capability executors |
| [handoff-prompt](skills/productivity/handoff-prompt/) | Package live work into one successor-ready continuation prompt |
| [install-skill-pack](skills/development/install-skill-pack/) | Install or refresh the published pack globally from its tracked `main` source |
| [skill-builder](skills/development/skill-builder/) | Create, audit, maintain, and modernize reusable agent skills |

### Design and Visualization

| Skill | What it helps with |
| --- | --- |
| [frontend-design](skills/development/frontend-design/) | Apply visual hierarchy, art direction, interaction judgment, and UI quality checks |
| [mermaid-diagrams](skills/development/mermaid-diagrams/) | Design readable, parser-safe Mermaid diagrams and validate their rendering |

### Judgment and Collaboration

| Skill | What it helps with |
| --- | --- |
| [deep-interview](skills/productivity/deep-interview/) | Turn a vague idea into a user-approved brief through a focused Socratic interview |
| [fable5-judgment](skills/productivity/fable5-judgment/) | Put Fable 5 in charge of difficult judgment, strategy, and long-horizon synthesis |
| [parallel-subagents](skills/productivity/parallel-subagents/) | Orchestrate independent agent workstreams when parallelism materially improves the result |
| [unknowns-pass](skills/productivity/unknowns-pass/) | Surface the unknowns in unfamiliar work with the cheapest technique, then compress them into a launch brief |

### Writing and Language

| Skill | What it helps with |
| --- | --- |
| [english-prompt-review](skills/productivity/english-prompt-review/) | Rewrite English technical prompts naturally and explain important nuance in Korean |
| [terminology-review](skills/productivity/terminology-review/) | Replace unnatural or domain-inaccurate terminology without flattening the author's meaning |

### Personal and Everyday Tools

| Skill | What it helps with |
| --- | --- |
| [1password-cli](skills/development/1password-cli/) | Use the local macOS 1Password CLI for vault, secret, OTP, and environment workflows |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce exact, minimum, or maximum page limits |
| [toss-portfolio-state](skills/development/toss-portfolio-state/) | Export a read-only Toss Invest portfolio and market-context snapshot |

## Related standalone skills

These skills live in separate repositories and are not included when this pack
is installed.

| Skill | Source | Description |
| --- | --- | --- |
| [astro-dev](https://github.com/gigio1023/astro-dev-skill) | `gigio1023/astro-dev-skill` | Current Astro patterns, compatibility gates, and focused verification |
| [drawio-diagram](https://github.com/gigio1023/drawio-agent-skill) | `gigio1023/drawio-agent-skill` | Create editable draw.io diagrams with structural and rendered checks |
| [humanize-doc](https://github.com/gigio1023/humanize-doc) | `gigio1023/humanize-doc` | Rewrite AI-sounding drafts into readable human documents |
| [unity-game-dev](https://github.com/gigio1023/unity-game-dev-skill) | `gigio1023/unity-game-dev-skill` | Cross-harness Unity game development with Editor adapters and QA flows |

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
skill, and the local listing discovers the expected 21 unique names. See
[Repository Structure](docs/repo-structure.md) for the catalog, storage, and
installation boundaries.

The pack was re-audited for GPT-5.6 Sol and Claude Fable 5 in July 2026.
Portable domain skills keep task-specific knowledge, authority boundaries, and
verification in shared files; exact model prompting stays in the dedicated
model guides.
