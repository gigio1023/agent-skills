# Agent Skills

[![skills.sh](https://skills.sh/b/gigio1023/agent-skills)](https://skills.sh/gigio1023/agent-skills)

A personal collection of 29 specialized, reusable Agent Skills for working with agent harnesses, development and delivery, designing interfaces, writing clearly, and handling a few everyday workflows.

For continuity across sessions, models, and agent harnesses, use [gigio-pack](https://github.com/gigio1023/gigio-pack): project intent, plans, execution, review, and handoff. This repository supplies focused capabilities for the work itself. Each skill can be used independently; ordinary tasks need not start a project workflow.

Each skill follows the [Agent Skills format](https://agentskills.io/): a `SKILL.md` plus any colocated references, scripts, and assets. Install only what you need with [`npx skills`](https://github.com/vercel-labs/skills), then update from the tracked source.

[Catalog](#skill-catalog) · [Install](#install-with-npx-skills) · [Update](#keep-skills-up-to-date) · [Related repositories](#related-skill-repositories) · [Local development](#local-development)

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

Replace the skill names and agent IDs as needed. Omit `--global` for a project-local install.

Install all 29 skills for a deliberate set of agents. Quote the wildcard so the shell does not expand it:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' \
  --skill '*' \
  --agent codex claude-code cursor \
  --global \
  --yes
```

Prefer an explicit `--agent` list. The CLI's `--all` option targets every skill and every supported agent, which is usually broader than intended.

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

Updates refresh only already tracked skills. Rerun an `add` command to install new skills from this pack. Verify global installs with:

```bash
npx --yes skills list --global
```

## Skill catalog

The catalog is organized by the job to be done, not by the agent that runs it.

- [Software Development and Delivery](#software-development-and-delivery) (7)
- [Agent and Harness Engineering](#agent-and-harness-engineering) (14)
- [Design and Visualization](#design-and-visualization) (3)
- [Writing and Language](#writing-and-language) (2)
- [Personal and Everyday Tools](#personal-and-everyday-tools) (3)

### Software Development and Delivery

| Skill | What it helps with |
| --- | --- |
| [pr-review-comment](skills/development/pr-review-comment/) | Validate review findings against a PR diff and post approved inline comments |
| [python-docstrings](skills/development/python-docstrings/) | Document Python API contracts, lifecycle behavior, side effects, and invariants |
| [git-worktree-setup](skills/development/git-worktree-setup/) | Isolate authorized repository work while preserving existing changes |
| [commit-and-push](skills/development/commit-and-push/) | Commit and push the requested changes with appropriate evidence |
| [draft-pr](skills/development/draft-pr/) | Publish or update an actual pull request |
| [write-issue](skills/development/write-issue/) | Write and consolidate tracker issues around useful outcomes, with enough context to act and sources readers can open |
| [python-coding-standards](skills/development/python-coding-standards/) | Implement maintainable Python models, modules, and checks |

### Agent and Harness Engineering

| Skill | What it helps with |
| --- | --- |
| [cursor-cli-delegation](skills/productivity/cursor-cli-delegation/) | Explicitly delegate planning, research, implementation, or review through direct Cursor CLI calls with task-specific options and session follow-ups |
| [codex-delegate](skills/development/codex-delegate/) | Delegate bounded tasks from a non-Codex host with durable runs and explicit execution boundaries |
| [cross-harness-skills](skills/development/cross-harness-skills/) | Build and audit one portable skill for Claude Code and Codex while isolating harness adapters |
| [fable5-prompting-guide](skills/development/fable5-prompting-guide/) | Write and migrate prompt stacks specifically for Claude Fable 5 and Fable 5.1 |
| [goal-prompting](skills/development/goal-prompting/) | Explain, draft, review, translate, and hand off verifiable Codex and Claude Code goal prompts |
| [gpt6-prompting-guide](skills/development/gpt6-prompting-guide/) | Design GPT-6 Astra and GPT-6 Sol prompts, skills, and repository instructions with focused context and explicit completion boundaries, including moves from GPT-5.6 |
| [opus5-prompting-guide](skills/development/opus5-prompting-guide/) | Write and migrate Claude Opus 5.5 and Opus 5 prompt stacks, putting each fix in prompt text, request settings, the agent loop, or a tool |
| [install-skill-pack](skills/development/install-skill-pack/) | Review and globally install skills from a selected Git repository, branch, or commit |
| [skill-builder](skills/development/skill-builder/) | Turn real workflows and preferences into personal, project-local, or shared skills; audit and improve them without publishing private evidence |
| [read-agent-sessions](skills/development/read-agent-sessions/) | Locate and read stored Codex, Claude Code, Zcode, or Hermes sessions on this machine and summarize them for another agent |
| [orchestrate-subagents](skills/development/orchestrate-subagents/) | Coordinate requested delegated work and synthesize its evidence |
| [small-model-handoff](skills/development/small-model-handoff/) | Package a settled bounded step for a less capable executor |
| [fable5-model-routing](skills/development/fable5-model-routing/) | Choose each subagent's model and effort when a Claude Fable lead delegates, in any harness with subagents, and ship the subagent definitions that make effort selectable |
| [gpt6-astra-model-routing](skills/development/gpt6-astra-model-routing/) | Choose each subagent's model and effort when a GPT-6 Astra lead delegates, run workers on GPT-6 Sol at full effort, and reserve Astra for judgment |

### Design and Visualization

| Skill | What it helps with |
| --- | --- |
| [frontend-design](skills/development/frontend-design/) | Route and verify user-visible frontend work from bug fixes and local changes through new UI and redesigns |
| [mermaid-diagrams](skills/development/mermaid-diagrams/) | Design readable, parser-safe Mermaid diagrams and validate their rendering |
| [insight-dashboard](skills/development/insight-dashboard/) | Build evidence-led dashboards with aligned comparisons, filters, factual captions, and static output |

### Writing and Language

| Skill | What it helps with |
| --- | --- |
| [english-prompt-review](skills/productivity/english-prompt-review/) | Rewrite English technical prompts naturally and explain important nuance in Korean |
| [technical-report-writing](skills/productivity/technical-report-writing/) | Write, revise, and review documents with clear structure, compact tables, focused visuals, and the explanation each genre needs, including explicit AI-slop revision and Korean clarity |

### Personal and Everyday Tools

| Skill | What it helps with |
| --- | --- |
| [1password-cli](skills/development/1password-cli/) | Use the local macOS 1Password CLI for vault, secret, OTP, and environment workflows |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce exact, minimum, or maximum page limits |
| [toss-portfolio-state](skills/development/toss-portfolio-state/) | Export a read-only Toss Invest portfolio and market-context snapshot |

## Writing, documents, and dashboards

Use `technical-report-writing` as the document-authoring entry point in the requested language and medium. Its core covers noun-phrase headings, information selection, short cells, table and figure planning, explanation, and removal of research diaries and blanket disclaimers. Its existing name remains stable; its scope includes nontechnical and external-facing documents. Use `insight-dashboard` for analytical or operational data views and selection-dependent values and explanations. For shadcn/ui implementation, use the [official shadcn skill](https://ui.shadcn.com/docs/skills) directly. PDF and editable documents can use native production tools.

The skills teach decisions through finished examples: what helps this reader understand, compare, or act; what can be deleted; and what the reader needs to interpret a claim. Consult [synthetic examples](skills/productivity/technical-report-writing/references/synthetic-examples.md), [dashboard patterns](skills/development/insight-dashboard/references/pattern-examples.md), or the [public writing sources](docs/writing-sources.md) for the current task, not as a mandatory reading list.

For internal sharing, `share-internal-doc` from Gigio Pack applies the available writer and adds recipient suitability, usable source access, privacy, and authorized delivery. Naming it alone still produces a complete shared document without a second editorial workflow. See [composition guidance](skills/productivity/technical-report-writing/references/composition.md) and [adoption and cross-repository migration](docs/writing-skills.md).

## Related skill repositories

These repositories are independently versioned and not included when this pack is installed. Use each README for its install and update workflow.

| Repository | Included skills | What it adds |
| --- | --- | --- |
| [Gigio Pack](https://github.com/gigio1023/gigio-pack) | Project continuity and delivery workflows | Preserve intent, plans, actual results, and handoff across sessions and harnesses |
| [Research Credo](https://github.com/gigio1023/research-credo) | Research methods, internal source reconstruction, and evaluation operations | Investigate, experiment, train, build and review data or benchmarks, and interpret findings |
| [Astro Dev](https://github.com/gigio1023/astro-dev-skill) | `astro-dev` | Version-aware Astro implementation and migration guidance with focused checks for current framework conventions |
| [Slop-Aware Writing](https://github.com/gigio1023/slop-aware-writing) | `slop-aware-writing`, `korean-clarity` | Merged into `technical-report-writing`; the repository remains the MIT license source and will be archived after the merged skill is installed and verified |
| [Gigio Figures](https://github.com/gigio1023/gigio-figures) | `technical-diagram`, `eli5-figure`, `data-chart`, `drawio-diagram` | Editorial technical diagrams for domain readers, deliberately simple figures on request, measured data charts, and native editable draw.io authoring |
| [Game Studio](https://github.com/gigio1023/game-studio) | `game-direction`, `game-production`, `game-review` | Creator-owned direction, proof-based production, and evidence-first review across the game lifecycle |
| [Godot Best Practice](https://github.com/gigio1023/godot-best-practice) | `godot-best-practice` | Godot-native implementation and review grounded in the project's engine version, serialized resources, and engine-level evidence |
| [Unity Game Development](https://github.com/gigio1023/unity-game-dev-skill) | `unity-game-dev` | Version-aware Unity gameplay implementation and review across repository-only and live Editor workflows |

## Useful external skills

| Repository or skill | Includes | Useful for |
| --- | --- | --- |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | `obsidian-bases`, `obsidian-cli`, `obsidian-markdown`, and more | Working with Obsidian vaults and file formats |
| [find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) | `find-skills` | Discovering and installing additional skills |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui/tree/main/skills) | `shadcn`, `migrate-radix-to-base` | Project-aware shadcn/ui component work and Radix UI to Base UI migration ([docs](https://ui.shadcn.com/docs/skills)) |

You can also browse [skills.sh](https://skills.sh/) or search from the CLI:

```bash
npx --yes skills find
```

## Local development

Keep Markdown prose in natural paragraphs without fixed-column hard wrapping; use editor soft wrap for display. Follow [skill-builder](skills/development/skill-builder/SKILL.md) when authoring or maintaining a skill.

This repository is a multi-skill pack. The canonical source for each bundled skill is `skills/<source-category>/<skill-name>/`.

Inspect a checkout without creating an update-tracked install:

```bash
npx --yes skills add . --list
```

Before publishing a change, verify that each `SKILL.md` name matches its folder, every referenced path exists, the README entry still points to the correct skill, and the local listing discovers the expected 29 unique names. See [package migration](docs/migration.md) for source moves and coordinated installation. See [Repository Structure](docs/repo-structure.md) for the catalog, storage, and installation boundaries. Vocabulary decisions for the pack's prose live in [terminology.md](terminology.md), and [docs/routing-skills.md](docs/routing-skills.md) describes how the two model-routing skills divide work with the orchestration skills.
