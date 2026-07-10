# Agent Skills

Reusable agent workflow skills for coding, documentation, review, and publishing.

This is a curated pack of installable skills for Codex, Claude Code, Cursor,
Gemini CLI, and similar coding agents. These skills capture practical workflows
agents should run reliably: clean PRs, safe tool use, frontend judgment,
technical writing, subagent orchestration, and skill creation.

The pack was re-audited for GPT-5.6 Sol and Claude Fable 5 in July 2026.
Portable domain skills keep task-specific knowledge, authority boundaries, and
verification while avoiding model-specific micromanagement. Exact model routing
and prompting guidance live only in the dedicated model skills. Claude Code and
Codex installation, invocation, metadata, and permission differences remain in
their adapter documentation rather than the shared skill core.

## Included skills

These skills live directly in this repo under `skills/`.

### Development

| Skill | Description |
| --- | --- |
| [1password-cli](skills/development/1password-cli/) | Use the local 1Password CLI safely for vaults, items, secret references, env injection, and Mac app integration |
| [commit-push-sync](skills/development/commit-push-sync/) | Split local changes into logical commits, push safely, and keep issue or PR sync explicit |
| [cross-harness-skill-authoring](skills/development/cross-harness-skill-authoring/) | Author and audit one portable skill for Claude Code/Fable and Codex/GPT-5.6 while isolating harness adapters |
| [writing-engineering-docs](skills/development/writing-engineering-docs/) | Write, update, restructure, and review evidence-backed engineering documentation |
| [draft-pr](skills/development/draft-pr/) | Publish or update actual draft GitHub PRs with `gh`, preserving reviewer context and rebasing only when needed |
| [fable5-prompting-guide](skills/development/fable5-prompting-guide/) | Write, review, and migrate prompt stacks for Claude Fable 5, including long-run, effort, tool, memory, and refusal behavior |
| [toss-portfolio-state](skills/development/toss-portfolio-state/) | Fetch read-only Toss Invest OpenAPI balances, holdings, order/conditional-order history, trading capacity, fees, FX, calendars, and optional market context into a normalized portfolio snapshot |
| [frontend-design](skills/development/frontend-design/) | Design judgment layer for UI, reports, apps, dashboards, games, and visual QA |
| [mermaid-diagram-design](skills/development/mermaid-diagram-design/) | Design readable Mermaid diagrams with type selection, parser-safe syntax, accessible palettes, renderer compatibility, and render validation |
| [python-docstring-enhancer](skills/development/python-docstring-enhancer/) | Document and audit Python API contracts with lifecycle-aware patterns and a doc-only diff guard |
| [skill-builder](skills/development/skill-builder/) | Create, audit, evaluate, and modernize agent skills with compact `SKILL.md` files and progressive disclosure |
| [gpt56-sol-prompting-guide](skills/development/gpt56-sol-prompting-guide/) | Write, review, and migrate prompt stacks for GPT-5.6 Sol with compact contracts, tool routing, grounding, runtime controls, and evals |

### Productivity

| Skill | Description |
| --- | --- |
| [anti-ai-slop-terminology](skills/productivity/anti-ai-slop-terminology/) | Review unnatural or domain-inaccurate terminology without treating a watch-list hit as proof of AI authorship |
| [conducting-deep-interviews](skills/productivity/conducting-deep-interviews/) | Lead an Ouroboros-centered, context-first Socratic interview one question at a time and close with a user-approved brief |
| [fable5-judgment-orchestrator](skills/productivity/fable5-judgment-orchestrator/) | Let Fable 5 lead difficult judgment and end-to-end work, delegating only when another lane has a concrete advantage |
| [handoff-prompt-writer](skills/productivity/handoff-prompt-writer/) | Compile current intent, decisions, artifacts, evidence, and remaining work into one executable successor prompt file |
| [parallel-subagent-orchestrator](skills/productivity/parallel-subagent-orchestrator/) | Orchestrate independent subagent workstreams when parallelism materially improves speed, coverage, or verification |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce page-limit checks |
| [reviewing-english-prompts](skills/productivity/reviewing-english-prompts/) | Rewrite English technical prompts naturally, explain nuance in Korean, and keep key terms and contrasts in English |

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

Install one skill globally for Codex:

```bash
npx skills add gigio1023/agent-skills \
  --skill reviewing-english-prompts \
  --agent codex \
  --global \
  --yes
```

Install the same skill globally for Codex, Claude Code, and Cursor:

```bash
npx skills add gigio1023/agent-skills \
  --skill reviewing-english-prompts \
  --agent codex claude-code cursor \
  --global \
  --yes
```

CLI options must start with two ASCII hyphens, such as `--skill`. Unicode
dashes such as `—skill` are not valid options.

For local development, replace the GitHub source with the checkout path:

```bash
npx skills add ./agent-skills \
  --skill skill-builder \
  --agent codex
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
    │   ├── writing-engineering-docs/
    │   ├── draft-pr/
    │   ├── fable5-prompting-guide/
    │   ├── toss-portfolio-state/
    │   ├── frontend-design/
    │   ├── mermaid-diagram-design/
    │   ├── python-docstring-enhancer/
    │   ├── skill-builder/
    │   └── gpt56-sol-prompting-guide/
    └── productivity/
        ├── anti-ai-slop-terminology/
        ├── conducting-deep-interviews/
        ├── fable5-judgment-orchestrator/
        ├── handoff-prompt-writer/
        ├── parallel-subagent-orchestrator/
        ├── pdf-page-count/
        └── reviewing-english-prompts/
```
