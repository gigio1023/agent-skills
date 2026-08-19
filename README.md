# Agent Skills

[![skills.sh](https://skills.sh/b/gigio1023/agent-skills)](https://skills.sh/gigio1023/agent-skills)

A personal collection of 16 specialized, reusable Agent Skills for working
with agent harnesses, designing interfaces, writing clearly, and handling a
few everyday workflows.

For a structured software-development work loop, start with
[gigio-pack](https://github.com/gigio1023/gigio-pack). It is the primary
reference for orienting, planning, executing, reviewing, and handing off work.
This repository complements it with focused skills that fit alongside that
loop.

Each skill follows the [Agent Skills format](https://agentskills.io/): a
`SKILL.md` plus any colocated references, scripts, and assets. Install only
what you need with [`npx skills`](https://github.com/vercel-labs/skills), then
update from the tracked source.

[Catalog](#skill-catalog) · [Install](#install-with-npx-skills) ·
[Update](#keep-skills-up-to-date) · [Related repositories](#related-skill-repositories) ·
[Local development](#local-development)

## Install with `npx skills`

Prerequisite: Node.js 18 or newer.

Browse the pack:

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

Install all 16 skills for a deliberate set of agents. Quote the wildcard so
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

## Keep skills up to date

Update every tracked global skill:

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

Updates refresh only already tracked skills. Rerun an `add` command to install
new skills from this pack. Verify global installs with:

```bash
npx --yes skills list --global
```

## Skill catalog

The catalog is organized by the job to be done, not by the agent that runs it.

- [Software Development and Delivery](#software-development-and-delivery) (2)
- [Agent and Harness Engineering](#agent-and-harness-engineering) (8)
- [Design and Visualization](#design-and-visualization) (2)
- [Writing and Language](#writing-and-language) (1)
- [Personal and Everyday Tools](#personal-and-everyday-tools) (3)

### Software Development and Delivery

| Skill | What it helps with |
| --- | --- |
| [pr-review-comment](skills/development/pr-review-comment/) | Validate review findings against a PR diff and post approved inline comments |
| [python-docstrings](skills/development/python-docstrings/) | Document Python API contracts, lifecycle behavior, side effects, and invariants |

### Agent and Harness Engineering

| Skill | What it helps with |
| --- | --- |
| [cursor-cli-delegation](skills/productivity/cursor-cli-delegation/) | Delegate a closed execution mission through Cursor Agent CLI while the calling harness retains judgment and acceptance |
| [codex-delegate](skills/development/codex-delegate/) | Delegate bounded tasks from a non-Codex host with durable runs and explicit execution boundaries |
| [cross-harness-skills](skills/development/cross-harness-skills/) | Build and audit one portable skill for Claude Code and Codex while isolating harness adapters |
| [fable5-prompting-guide](skills/development/fable5-prompting-guide/) | Write and migrate prompt stacks specifically for Claude Fable 5 |
| [goal-prompting](skills/development/goal-prompting/) | Explain, draft, review, translate, and hand off verifiable Codex and Claude Code goal prompts |
| [gpt56-sol-prompting-guide](skills/development/gpt56-sol-prompting-guide/) | Write and migrate prompt stacks for GPT-5.6 Sol and the GPT-5.6 family |
| [install-skill-pack](skills/development/install-skill-pack/) | Review and globally install skills from a selected Git repository, branch, or commit |
| [skill-builder](skills/development/skill-builder/) | Create, audit, maintain, and modernize reusable agent skills |

### Design and Visualization

| Skill | What it helps with |
| --- | --- |
| [frontend-design](skills/development/frontend-design/) | Route and verify user-visible frontend work from bug fixes and local changes through new UI and redesigns |
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

These repositories are independently versioned and not included when this pack
is installed. Use each README for its install and update workflow.

| Repository | Included skills | What it adds |
| --- | --- | --- |
| [Gigio Pack](https://github.com/gigio1023/gigio-pack) | Software-development work loop | The primary reference for orienting, planning, executing, reviewing, and handing off software work |
| [Astro Dev](https://github.com/gigio1023/astro-dev-skill) | `astro-dev` | Version-aware Astro implementation and migration guidance with focused checks for current framework conventions |
| [Slop-Aware Writing](https://github.com/gigio1023/slop-aware-writing) | `slop-aware-writing` | Evidence-bounded authoring and revision that prevents or removes AI slop while preserving reader context, meaning, and voice across English, Korean, Italian, and Chinese |
| [draw.io Agent Skill](https://github.com/gigio1023/drawio-agent-skill) | `drawio-diagram` | Native, editable draw.io authoring with structural, layout, export, and visual checks |
| [Game Studio](https://github.com/gigio1023/game-studio) | `game-direction`, `game-production`, `game-review` | Creator-owned direction, proof-based production, and evidence-first review across the game lifecycle |
| [Godot Best Practice](https://github.com/gigio1023/godot-best-practice) | `godot-best-practice` | Godot-native implementation and review grounded in the project's engine version, serialized resources, and engine-level evidence |
| [Unity Game Development](https://github.com/gigio1023/unity-game-dev-skill) | `unity-game-dev` | Version-aware Unity gameplay implementation and review across repository-only and live Editor workflows |

## Useful external skills

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
skill, and the local listing discovers the expected 16 unique names. See
[Repository Structure](docs/repo-structure.md) for the catalog, storage, and
installation boundaries.
