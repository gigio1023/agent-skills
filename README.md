# Gigio Skills

[![skills.sh](https://skills.sh/b/gigio1023/gigio-skills)](https://skills.sh/gigio1023/gigio-skills)

A personal collection of 46 specialized, reusable Agent Skills for research and evaluation, project continuity, working with agent harnesses, development and delivery, designing interfaces, writing clearly, and handling a few everyday workflows.

The skills of two earlier personal packs, gigio-pack and research-credo, were absorbed into this pack on 2026-10-12; both repositories are archived and private, and [package migration](docs/migration.md) maps their former names. Packages are grouped into two install sets: `skills/minimal/` is the default install and `skills/additional/` is installed on request. A set decides availability only; each skill's description and invocation settings still decide when it runs. Each skill can be used independently; ordinary tasks need not start a project workflow.

Each skill follows the [Agent Skills format](https://agentskills.io/): a `SKILL.md` plus any colocated references, scripts, and assets. Install only what you need with [`npx skills`](https://github.com/vercel-labs/skills), then update from the tracked source.

[Catalog](#skill-catalog) · [Install](#install-with-npx-skills) · [Update](#keep-skills-up-to-date) · [Related repositories](#related-skill-repositories) · [Local development](#local-development)

## Install with `npx skills`

Prerequisite: Node.js 22.20 or newer, as Skills CLI 1.7 declares.

Browse the pack:

```bash
npx --yes skills add 'gigio1023/gigio-skills#main' --list
```

Install selected skills globally for the agents you use:

```bash
npx --yes skills add 'gigio1023/gigio-skills#main' \
  --skill mermaid-diagrams skill-builder \
  --agent codex claude-code \
  --global \
  --yes
```

Replace the skill names and agent IDs as needed. Omit `--global` for a project-local install.

Install the minimal set, the pack's default install, for a deliberate set of agents. The URL path selects the set, and the quoted wildcard selects every package in it:

```bash
npx --yes skills add 'https://github.com/gigio1023/gigio-skills/tree/main/skills/minimal' \
  --skill '*' \
  --agent codex claude-code cursor \
  --global \
  --yes
```

Use `skills/additional` the same way for the on-request set, or name individual skills as above.

Install all 46 skills for a deliberate set of agents. Quote the wildcard so the shell does not expand it:

```bash
npx --yes skills add 'gigio1023/gigio-skills#main' \
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
- [Agent and Harness Engineering](#agent-and-harness-engineering) (10)
- [Design and Visualization](#design-and-visualization) (3)
- [Writing and Language](#writing-and-language) (3)
- [Personal and Everyday Tools](#personal-and-everyday-tools) (4)
- [Research and Evaluation](#research-and-evaluation) (14)
- [Project Continuity and Discovery](#project-continuity-and-discovery) (5)

### Software Development and Delivery

| Skill | Set | What it helps with |
| --- | --- | --- |
| [pr-review-comment](skills/additional/pr-review-comment/) | additional | Validate review findings against a PR diff and post approved inline comments |
| [git-worktree-setup](skills/minimal/git-worktree-setup/) | minimal | Isolate authorized repository work while preserving existing changes |
| [commit-and-push](skills/minimal/commit-and-push/) | minimal | Commit and push the requested changes with appropriate evidence |
| [draft-pr](skills/minimal/draft-pr/) | minimal | Publish or update an actual pull request |
| [write-issue](skills/minimal/write-issue/) | minimal | Write and consolidate tracker issues around useful outcomes, with enough context to act and sources readers can open |
| [python-coding-standards](skills/minimal/python-coding-standards/) | minimal | Write, structure, and document maintainable Python: project shape, function and module boundaries, Pydantic models, uv, docstrings, and checks |
| [bug-diagnosis](skills/minimal/bug-diagnosis/) | minimal | Find and verify the root cause of a code or system failure, with an evidence-limited path when no reproduction loop exists |

### Agent and Harness Engineering

| Skill | Set | What it helps with |
| --- | --- | --- |
| [cursor-cli-delegation](skills/additional/cursor-cli-delegation/) | additional | Explicitly delegate planning, research, implementation, or review through direct Cursor CLI calls with task-specific options and session follow-ups |
| [codex-delegate](skills/additional/codex-delegate/) | additional | Delegate complete tasks from a non-Codex host to Astra with durable launch, resume, cancellation, and verified handoff |
| [goal-prompting](skills/additional/goal-prompting/) | additional | Explain, draft, review, translate, and hand off verifiable Codex and Claude Code goal prompts |
| [install-skill-pack](skills/minimal/install-skill-pack/) | minimal | Review and globally install skills from a selected Git repository, branch, or commit |
| [skill-builder](skills/minimal/skill-builder/) | minimal | Turn real workflows and preferences into personal, project-local, or shared skills, including skills that must work across Claude Code and Codex |
| [read-agent-sessions](skills/additional/read-agent-sessions/) | additional | Locate and read stored Codex, Claude Code, Zcode, or Hermes sessions on the local machine and summarize them for another agent |
| [orchestrate-subagents](skills/minimal/orchestrate-subagents/) | minimal | Coordinate delegated work, whether the user asked for it or the lead chose it, and synthesize its evidence |
| [model-routing](skills/minimal/model-routing/) | minimal | Choose each subagent's model and effort from the routing policy of its model family, Fable or GPT |
| [prompting-guide](skills/minimal/prompting-guide/) | minimal | Write, review, and migrate prompts, skills, and agent instructions for Claude Fable, Claude Opus, or GPT-6, loading only that family's guide |
| [small-model-handoff](skills/additional/small-model-handoff/) | additional | Package a settled bounded step for a less capable executor |

### Design and Visualization

| Skill | Set | What it helps with |
| --- | --- | --- |
| [frontend-design](skills/additional/frontend-design/) | additional | Route and verify user-visible frontend work from bug fixes and local changes through new UI and redesigns |
| [mermaid-diagrams](skills/additional/mermaid-diagrams/) | additional | Design readable, parser-safe Mermaid diagrams and validate their rendering |
| [insight-dashboard](skills/additional/insight-dashboard/) | additional | Build evidence-led dashboards with aligned comparisons, filters, factual captions, and static output |

### Writing and Language

| Skill | Set | What it helps with |
| --- | --- | --- |
| [english-prompt-review](skills/additional/english-prompt-review/) | additional | Rewrite English technical prompts naturally and explain important nuance in the user's native language, Korean by default |
| [copydesk](skills/minimal/copydesk/) | minimal | Write, revise, and review meaningful explanations with natural Korean and precise English, preserving facts through local corrections and broader rewrites |
| [write-notion](skills/minimal/write-notion/) | minimal | Create and revise team pages in Notion: document shape, people mentions, compact tables, figures, safe edits, and a re-fetch check after publishing |

### Personal and Everyday Tools

| Skill | Set | What it helps with |
| --- | --- | --- |
| [1password-cli](skills/additional/1password-cli/) | additional | Use the local macOS 1Password CLI for vault, secret, OTP, and environment workflows |
| [pdf-page-count](skills/additional/pdf-page-count/) | additional | Count PDF pages and enforce exact, minimum, or maximum page limits |
| [reddit-search](skills/additional/reddit-search/) | additional | Find Reddit threads and read full comment trees through the Arctic Shift archive, since Reddit blocks agent fetches |
| [toss-portfolio-state](skills/additional/toss-portfolio-state/) | additional | Export a read-only Toss Invest portfolio and market-context snapshot |

### Research and Evaluation

| Skill | Set | What it helps with |
| --- | --- | --- |
| [design-exploration](skills/minimal/design-exploration/) | minimal | Open the design space for a model- or agent-based system before designing: a root such as the threat model or research question, mechanism material, hunches, and concepts that differ in their bet |
| [idea-critique](skills/minimal/idea-critique/) | minimal | Steelman and attack one stated idea, then name the measurement that would decide it |
| [design-doc](skills/minimal/design-doc/) | minimal | Write or update a design document with fixed interfaces, a test-or-eval verification split, a decision log, and an experiment queue |
| [literature-research](skills/minimal/literature-research/) | minimal | Read a paper for a purpose, check prior art for a claim, survey open models or datasets at pinned revisions, map the mechanisms that address a problem, and preserve sources |
| [ml-experiment](skills/minimal/ml-experiment/) | minimal | Design, run, or interpret training, adaptation, serving, or reproduction experiments and their training data |
| [evaluation-design](skills/minimal/evaluation-design/) | minimal | Design what an eval measures: failure modes, cases and labels, code checks, judges and their validation, comparison conditions |
| [evaluation-audit](skills/minimal/evaluation-audit/) | minimal | Give a launch, hold, or report verdict on a built eval, judge, harness, scoring change, or result |
| [evaluation-operations](skills/minimal/evaluation-operations/) | minimal | Operate approved evaluation campaigns with durable attempt and result records |
| [internal-source-research](skills/minimal/internal-source-research/) | minimal | Reconstruct work context from authorized internal sources |
| [praxis-direction](skills/minimal/praxis-direction/) | minimal | Sharpen an agenda into one bet, run the failure-mode pass on a new system, or set up and audit the praxis profile |
| [credo-taste](skills/additional/credo-taste/) | additional | Choose a research direction, decide whether to continue, pivot, or stop, or judge whether a work result could become a paper; invoked by name |
| [credo-paper-plan](skills/additional/credo-paper-plan/) | additional | Plan the argument, claim-evidence map, closest prior work, and figures; critique a draft; plan the response to peer reviews |
| [credo-journal](skills/additional/credo-journal/) | additional | Record research ideas, predictions, and hindsight; invoked by name |
| [credo-release](skills/additional/credo-release/) | additional | Check a paper before submission or release |

### Project Continuity and Discovery

| Skill | Set | What it helps with |
| --- | --- | --- |
| [find-unknowns](skills/minimal/find-unknowns/) | minimal | Scan broadly for what neither side has noticed, lead with a view, and ask the consequential questions together, in any domain |
| [interview](skills/minimal/interview/) | minimal | Interview in batched question rounds until the next action is clear |
| [work-plan](skills/minimal/work-plan/) | minimal | Write, execute, or review a plan through the next decision, each mode on request |
| [session-handoff](skills/minimal/session-handoff/) | minimal | Write one file a successor executes: current state, next actions, and questions for the user |
| [terminology](skills/minimal/terminology/) | minimal | Apply a project's recorded terms, and settle contested names from project, paper, and competitor usage |

## Writing, documents, and dashboards

Use `copydesk` as the document-authoring entry point in the requested language and medium. It distinguishes new writing, local corrections, and broader rewrites, preserves evidence and meaning, and chooses prose, tables, or figures for the reader's question. Its English clarity guidance draws useful principles from STE without imposing word counts, a fixed dictionary, or English sentence rules on Korean. It also provides shared writing principles for PRs, issues, and Notion pages; their specialist skills own structure and publication, and `write-notion` covers Notion page layout and editing mechanics. Use `insight-dashboard` for analytical or operational data views and selection-dependent values and explanations. For shadcn/ui implementation, use the [official shadcn skill](https://ui.shadcn.com/docs/skills) directly. PDF and editable documents can use native production tools.

The skills teach decisions through finished examples: what helps this reader understand, compare, or act; what can be deleted; and what the reader needs to interpret a claim. Consult [synthetic examples](skills/minimal/copydesk/references/synthetic-examples.md), [dashboard patterns](skills/additional/insight-dashboard/references/pattern-examples.md), or the [public writing sources](docs/writing-sources.md) for the current task, not as a mandatory reading list.

For internal sharing, the writer's [sharing and delivery](skills/minimal/copydesk/references/sharing-and-delivery.md) reference adds recipient suitability, usable source access, the sharing pass, and authorized delivery; the former Gigio Pack `share-internal-doc` was merged here on 2026-09-24. See [composition guidance](skills/minimal/copydesk/references/composition.md) and [adoption and cross-repository migration](docs/writing-skills.md).

## Related skill repositories

These repositories are independently versioned and not included when this pack is installed. Use each README for its install and update workflow.

| Repository | Included skills | What it adds |
| --- | --- | --- |
| [Astro Dev](https://github.com/gigio1023/astro-dev-skill) | `astro-dev` | Version-aware Astro implementation and migration guidance with focused checks for current framework conventions |
| [Slop-Aware Writing](https://github.com/gigio1023/slop-aware-writing) | `slop-aware-writing`, `korean-clarity` | Merged into `copydesk`; the repository was archived on 2026-09-24 and remains the MIT license source |
| [Gigio Figures](https://github.com/gigio1023/gigio-figures) | `technical-figure`, `eli5-figure`, `drawio-diagram` | Planned figure sets for technical documents (mechanism diagrams, geometry, grids, and charts on one visual grammar, rendered and linted in light and dark), deliberately simple figures on request, and native editable draw.io authoring |
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

Keep Markdown prose in natural paragraphs without fixed-column hard wrapping; use editor soft wrap for display. Follow [skill-builder](skills/minimal/skill-builder/SKILL.md) when authoring or maintaining a skill.

This repository is a multi-skill pack. The canonical source for each bundled skill is `skills/<install-set>/<skill-name>/`, where the install set is `minimal` or `additional`.

Inspect a checkout without creating an update-tracked install:

```bash
npx --yes skills add . --list
```

Before publishing a change, verify that each `SKILL.md` name matches its folder, every referenced path exists, the README entry still points to the correct skill, and the local listing discovers the expected 46 unique names. See [package migration](docs/migration.md) for source moves and coordinated installation. See [Repository Structure](docs/repo-structure.md) for the catalog, storage, and installation boundaries. Vocabulary decisions for the pack's prose live in [terminology.md](terminology.md), and [docs/routing-skills.md](docs/routing-skills.md) describes how `model-routing` divides work with the orchestration skills. The reasons behind `codex-delegate`'s design are kept in [its decision log](docs/codex-delegate-decision-log.md).

## License

MIT, see [LICENSE](LICENSE). Files that carry their own license notice, such as those in `skills/minimal/copydesk/`, keep its terms, and ideas adapted from other projects are credited in each skill's source notes. Prompt clauses quoted from Anthropic's documentation in `skills/minimal/prompting-guide/references/fable/` are marked and linked there; they remain Anthropic's and are not covered by this license.
