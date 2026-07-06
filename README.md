# Agent Skills

Reusable agent workflow skills for coding, research, review, and publishing.

This is a curated pack of installable skills for Codex, Claude Code, Cursor,
Gemini CLI, and similar coding agents. These skills capture practical workflows
agents should run reliably: clean PRs, safe tool use, frontend judgment,
research audits, subagent orchestration, and skill creation.

## Included skills

These skills live directly in this repo under `skills/`.

### Development

| Skill | Description |
| --- | --- |
| [1password-cli](skills/development/1password-cli/) | Use the local 1Password CLI safely for vaults, items, secret references, env injection, and Mac app integration |
| [commit-push-sync](skills/development/commit-push-sync/) | Split local changes into logical commits, push safely, and keep issue or PR sync explicit |
| [dev-doc-style](skills/development/dev-doc-style/) | Tighten engineering docs by improving hierarchy, zoom level, and markdown readability |
| [dev-tech-spec-docs](skills/development/dev-tech-spec-docs/) | Create concise development, architecture, API, README, and technical specification docs |
| [docs-conflict-deprecation-review](skills/development/docs-conflict-deprecation-review/) | Audit docs against implementation and fix stale, conflicting, deprecated, or broken guidance |
| [draft-pr](skills/development/draft-pr/) | Create concise draft GitHub PRs with `gh`, body-file updates, no Codex prefixes, and rebase-first conflict handling |
| [echarts-dashboard-patterns](skills/development/echarts-dashboard-patterns/) | Build readable ECharts dashboards with guardrails for labels, legends, axes, gaps, and shared config |
| [frontend-design](skills/development/frontend-design/) | Design judgment layer for UI, reports, apps, dashboards, games, and visual QA |
| [mermaid-diagram-design](skills/development/mermaid-diagram-design/) | Design clear Mermaid diagrams with type selection, layout control, accessibility, and render preflight |
| [python-docstring-enhancer](skills/development/python-docstring-enhancer/) | Add explanatory Python docstrings and intent comments for complex code paths |
| [skill-builder](skills/development/skill-builder/) | Design and create high-quality agent skills (`SKILL.md`, references, and structure) |
| [workspace-delivery-orchestrator](skills/development/workspace-delivery-orchestrator/) | Coordinate multi-repo or multi-workstream delivery with planning, progress tracking, and closure artifacts |
| [workspace-handoff-compiler](skills/development/workspace-handoff-compiler/) | Compile successor handoffs and context packs for work that continues across sessions |

### Productivity

| Skill | Description |
| --- | --- |
| [anti-ai-slop-terminology](skills/productivity/anti-ai-slop-terminology/) | Detect suspect AI-generated terminology and replace it with domain-grounded language |
| [fable5-judgment-orchestrator](skills/productivity/fable5-judgment-orchestrator/) | Keep Fable 5 focused on judgment, critique, and synthesis while routing token-heavy evidence gathering to support lanes |
| [parallel-subagent-orchestrator](skills/productivity/parallel-subagent-orchestrator/) | Orchestrate parallel subagents across coding, research, review, value judgment, and synthesis |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce page-limit checks |
| [web-research-audit](skills/productivity/web-research-audit/) | Audit web research quality, source coverage, and evidence freshness |
| [write-issue](skills/productivity/write-issue/) | Draft or refine actionable GitHub issues with clean Markdown and focused next steps |
| [write-pr](skills/productivity/write-pr/) | Write concise pull request titles and bodies that emphasize motivation and review impact |

## Related standalone skills

These skills live in separate repos and are not packaged in this skill pack.

| Skill | Source | Description |
| --- | --- | --- |
| [unity-game-dev](https://github.com/gigio1023/unity-game-dev-skill) | `gigio1023/unity-game-dev-skill` | Game-focused Unity development skill with orchestration, MCP scene work, and QA flow |
| [astro-dev](https://github.com/gigio1023/astro-dev-skill) | `gigio1023/astro-dev-skill` | Astro 6 guardrails for coding agents |
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
    │   ├── dev-doc-style/
    │   ├── dev-tech-spec-docs/
    │   ├── docs-conflict-deprecation-review/
    │   ├── draft-pr/
    │   ├── echarts-dashboard-patterns/
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
