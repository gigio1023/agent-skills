# Agent Skills — Official Anthropic Documentation

> **Source**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
> **Snapshot date**: 2026-03-23
> **Freshness policy**: This is a local snapshot. Before relying on specific API details,
> field constraints, or feature availability, fetch the latest version from the URL above
> using WebFetch. The SKILL.md instructs when to refresh.

---

## Why use Skills

Skills are reusable, filesystem-based resources that provide Claude with domain-specific expertise: workflows, context, and best practices that transform general-purpose agents into specialists. Unlike prompts (conversation-level instructions for one-off tasks), Skills load on-demand and eliminate the need to repeatedly provide the same guidance across multiple conversations.

**Key benefits**:
- **Specialize Claude**: Tailor capabilities for domain-specific tasks
- **Reduce repetition**: Create once, use automatically
- **Compose capabilities**: Combine Skills to build complex workflows

## How Skills work

Skills leverage Claude's VM environment to provide capabilities beyond what's possible with prompts alone. Claude operates in a virtual machine with filesystem access, allowing Skills to exist as directories containing instructions, executable code, and reference materials, organized like an onboarding guide you'd create for a new team member.

This filesystem-based architecture enables **progressive disclosure**: Claude loads information in stages as needed, rather than consuming context upfront.

### Three levels of loading

#### Level 1: Metadata (always loaded)
The Skill's YAML frontmatter provides discovery information (~100 tokens per Skill):

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

#### Level 2: Instructions (loaded when triggered)
The main body of SKILL.md contains procedural knowledge — under 5k tokens.

#### Level 3: Resources (loaded as needed)
Additional files: scripts, references, templates. Effectively unlimited since scripts execute without loading into context.

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| **Level 1: Metadata** | Always (at startup) | ~100 tokens per Skill | `name` and `description` from YAML frontmatter |
| **Level 2: Instructions** | When Skill is triggered | Under 5k tokens | SKILL.md body with instructions and guidance |
| **Level 3+: Resources** | As needed | Effectively unlimited | Bundled files executed via bash without loading contents into context |

## Skill structure

Every Skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
```

**Required fields**: `name` and `description`

**Field requirements**:

`name`:
- Maximum 64 characters
- Must contain only lowercase letters, numbers, and hyphens
- Cannot contain XML tags
- Cannot contain reserved words: "anthropic", "claude"

`description`:
- Must be non-empty
- Maximum 1024 characters
- Cannot contain XML tags

The `description` should include both what the Skill does and when Claude should use it.

## Where Skills work

### Claude Code
Custom Skills only. Create Skills as directories with SKILL.md files. Claude discovers and uses them automatically. Filesystem-based, no API uploads required.

Locations:
- Personal: `~/.claude/skills/`
- Project: `.claude/skills/`
- Plugins: shared via Claude Code Plugins

### Claude API
Both pre-built and custom Skills. Specify `skill_id` in the `container` parameter.

### Claude.ai
Both pre-built and custom Skills. Upload as zip files through Settings > Features.

### Claude Agent SDK
Custom Skills through `.claude/skills/` directories. Enable with `"Skill"` in `allowed_tools`.

## Security considerations

Only use Skills from trusted sources. Skills provide Claude with new capabilities through instructions and code — malicious Skills could direct Claude to invoke tools or execute code in harmful ways.

Key considerations:
- **Audit thoroughly**: Review all files (SKILL.md, scripts, images, resources)
- **External sources are risky**: Skills that fetch from external URLs pose particular risk
- **Tool misuse**: Malicious Skills can invoke tools in harmful ways
- **Data exposure**: Skills with access to sensitive data could leak information
- **Treat like installing software**: Only use from trusted sources

## Limitations and constraints

- Custom Skills do not sync across surfaces (Claude.ai, API, Claude Code are separate)
- Claude.ai: Individual user only; each team member uploads separately
- Claude API: Workspace-wide sharing
- Claude Code: Personal (`~/.claude/skills/`) or project (`.claude/skills/`)
- API: No network access, no runtime package installation
- Claude Code: Full network access, avoid global package installation
