# Agent Skills

Reusable agent workflow skills for coding, research, review, and publishing.

This is a curated pack of installable skills for Codex, Claude Code, Cursor,
Gemini CLI, and similar coding agents. These skills capture practical workflows
agents should run reliably: clean PRs, safe tool use, frontend judgment,
research audits, subagent orchestration, and skill creation.

## Included skills

These skills live directly in this repo under `skills/`.

| Skill | Description |
| --- | --- |
| [skill-builder](skills/development/skill-builder/) | Design and create high-quality agent skills (`SKILL.md`, references, and structure) |
| [draft-pr](skills/development/draft-pr/) | Create concise draft GitHub PRs with `gh`, body-file updates, no Codex prefixes, and rebase-first conflict handling |
| [frontend-design](skills/development/frontend-design/) | Design judgment layer for UI, reports, apps, dashboards, games, and visual QA |
| [1password-cli](skills/development/1password-cli/) | Use the local 1Password CLI safely for vaults, items, secret references, env injection, and Mac app integration |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce page-limit checks |
| [web-research-audit](skills/productivity/web-research-audit/) | Audit web research quality, source coverage, and evidence freshness |
| [parallel-subagent-orchestrator](skills/productivity/parallel-subagent-orchestrator/) | Orchestrate parallel subagents across coding, research, review, value judgment, and synthesis |
| [fable5-judgment-orchestrator](skills/productivity/fable5-judgment-orchestrator/) | Keep Fable 5 focused on judgment, critique, and synthesis while routing token-heavy evidence gathering to support lanes |

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
└── skills/
    ├── development/
    └── productivity/
```
