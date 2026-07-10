# Agent Skills

Reusable agent workflow skills for coding, research, review, and publishing.

This is a curated pack of installable skills for Codex, Claude Code, Cursor,
Gemini CLI, and similar coding agents. These skills capture practical workflows
agents should run reliably: clean PRs, safe tool use, frontend judgment,
research audits, subagent orchestration, and skill creation.

The pack was re-audited for GPT-5.6 Sol and Claude Fable 5 in July 2026.
Portable domain skills keep task-specific knowledge, authority boundaries, and
verification while avoiding model-specific micromanagement. Exact model routing
lives only in the dedicated Fable/orchestration guidance. Claude Code and Codex
installation, invocation, metadata, and permission differences remain in their
adapter documentation rather than the shared skill core.

## Included skills

These skills live directly in this repo under `skills/`.

### Development

| Skill | Description |
| --- | --- |
| [1password-cli](skills/development/1password-cli/) | Use the local 1Password CLI safely for vaults, items, secret references, env injection, and Mac app integration |
| [commit-push-sync](skills/development/commit-push-sync/) | Split local changes into logical commits, push safely, and keep issue or PR sync explicit |
| [cross-harness-skill-authoring](skills/development/cross-harness-skill-authoring/) | Author and audit one portable skill for Claude Code/Fable and Codex/GPT-5.6 while isolating harness adapters |
| [dev-doc-style](skills/development/dev-doc-style/) | Tighten engineering docs by improving hierarchy, zoom level, and markdown readability |
| [dev-tech-spec-docs](skills/development/dev-tech-spec-docs/) | Create concise development, architecture, API, README, and technical specification docs |
| [docs-conflict-deprecation-review](skills/development/docs-conflict-deprecation-review/) | Audit docs against implementation and fix stale, conflicting, deprecated, or broken guidance |
| [draft-pr](skills/development/draft-pr/) | Publish or update actual draft GitHub PRs with `gh`, preserving reviewer context and rebasing only when needed |
| [echarts-dashboard-patterns](skills/development/echarts-dashboard-patterns/) | Build readable ECharts dashboards with guardrails for labels, legends, axes, gaps, and shared config |
| [toss-portfolio-state](skills/development/toss-portfolio-state/) | Fetch read-only Toss Invest OpenAPI balances, holdings, order/conditional-order history, trading capacity, fees, FX, calendars, and optional market context into a normalized portfolio snapshot |
| [frontend-design](skills/development/frontend-design/) | Design judgment layer for UI, reports, apps, dashboards, games, and visual QA |
| [mermaid-diagram-design](skills/development/mermaid-diagram-design/) | Design clear Mermaid diagrams with type selection, layout control, accessibility, and render preflight |
| [python-docstring-enhancer](skills/development/python-docstring-enhancer/) | Add explanatory Python docstrings and intent comments for complex code paths |
| [skill-builder](skills/development/skill-builder/) | Create, audit, evaluate, and modernize agent skills with compact `SKILL.md` files and progressive disclosure |
| [workspace-delivery-orchestrator](skills/development/workspace-delivery-orchestrator/) | Coordinate multi-repo or multi-workstream delivery with planning, progress tracking, and closure artifacts |
| [workspace-handoff-compiler](skills/development/workspace-handoff-compiler/) | Compile successor handoffs and context packs for work that continues across sessions |

### Productivity

| Skill | Description |
| --- | --- |
| [anti-ai-slop-terminology](skills/productivity/anti-ai-slop-terminology/) | Review unnatural or domain-inaccurate terminology without treating a watch-list hit as proof of AI authorship |
| [fable5-judgment-orchestrator](skills/productivity/fable5-judgment-orchestrator/) | Let Fable 5 lead difficult judgment and end-to-end work, delegating only when another lane has a concrete advantage |
| [parallel-subagent-orchestrator](skills/productivity/parallel-subagent-orchestrator/) | Orchestrate independent subagent workstreams when parallelism materially improves speed, coverage, or verification |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce page-limit checks |
| [web-research-audit](skills/productivity/web-research-audit/) | Audit web research quality, source coverage, and evidence freshness |
| [write-issue](skills/productivity/write-issue/) | Draft, create, edit, comment on, or audit actionable Korean GitHub issues without changing assignees implicitly |
| [write-pr](skills/productivity/write-pr/) | Write Korean, Jira-aware PR titles and bodies sized to reviewer context; remote publication remains explicit |

## Related standalone skills

These skills live in separate repos and are not packaged in this skill pack.

| Skill | Source | Description |
| --- | --- | --- |
| [unity-game-dev](https://github.com/gigio1023/unity-game-dev-skill) | `gigio1023/unity-game-dev-skill` | Game-focused Unity development skill with orchestration, MCP scene work, and QA flow |
| [astro-dev](https://github.com/gigio1023/astro-dev-skill) | `gigio1023/astro-dev-skill` | Astro 7 patterns, compatibility gates, and focused verification for coding agents |
| [humanize-doc](https://github.com/gigio1023/humanize-doc) | `gigio1023/humanize-doc` | Rewrite AI-sounding drafts into readable human documents |
| [drawio-diagram](https://github.com/gigio1023/drawio-agent-skill) | `gigio1023/drawio-agent-skill` | Create editable draw.io diagrams instead of one-off XML |

## Useful external skills

| Skill | Source | Description |
| --- | --- | --- |
| obsidian-bases | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Edit Obsidian Bases (`.base`) files |
| obsidian-cli | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Work with an Obsidian vault from the CLI |
| obsidian-markdown | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian-flavored Markdown editing |
| find-skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Search and install more skills |

## Installation

Install one skill from the pack:

```bash
npx skills add gigio1023/agent-skills --skill skill-builder
```

Local checkout:

```bash
npx skills add ./agent-skills --skill skill-builder
```

Install the cross-harness authoring skill for both primary runtimes:

```bash
npx skills add gigio1023/agent-skills \
  --skill cross-harness-skill-authoring \
  --agent codex --agent claude-code -g
```

Agent-specific setup notes live in `docs/` and the `.codex/`, `.claude/`,
`.gemini/`, and `.cursor/` install files.

## Repo layout

```text
agent-skills/
├── .claude/INSTALL.md
├── .codex/INSTALL.md
├── .cursor/INSTALL.md
├── .gemini/INSTALL.md
├── .snyk
├── README.md
├── docs/
│   ├── README.claude.md
│   ├── README.codex.md
│   ├── README.cursor.md
│   └── README.gemini.md
└── skills/
    ├── development/
    │   ├── 1password-cli/
    │   ├── commit-push-sync/
    │   ├── cross-harness-skill-authoring/
    │   ├── dev-doc-style/
    │   ├── dev-tech-spec-docs/
    │   ├── docs-conflict-deprecation-review/
    │   ├── draft-pr/
    │   ├── echarts-dashboard-patterns/
    │   ├── toss-portfolio-state/
    │   ├── frontend-design/
    │   ├── mermaid-diagram-design/
    │   ├── python-docstring-enhancer/
    │   ├── skill-builder/
    │   ├── workspace-delivery-orchestrator/
    │   └── workspace-handoff-compiler/
    └── productivity/
        ├── anti-ai-slop-terminology/
        ├── fable5-judgment-orchestrator/
        ├── parallel-subagent-orchestrator/
        ├── pdf-page-count/
        ├── web-research-audit/
        ├── write-issue/
        └── write-pr/
```
