# Agent Skills — Official Anthropic Documentation Snapshot

> **Sources**:
> https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
> and
> https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
> **Snapshot date**: 2026-07-10
> **Freshness policy**: Refresh the official pages before relying on field,
> runtime, API, or availability details when this snapshot is older than 30 days.

## Table of Contents

- Why Skills
- Loading model
- Authoring principles
- Skill structure and frontmatter
- Progressive disclosure
- Evaluation and iteration
- Where Skills work
- Runtime constraints
- Security and retention
- Checklist

## Why Skills

Skills are reusable filesystem packages containing instructions, metadata, and
optional resources. They load on demand, so they are best for domain knowledge,
workflows, and repeatable procedures that should not occupy every conversation.

## Loading Model

Skills use three levels of disclosure:

| Level | Loaded when | Content |
|-------|-------------|---------|
| Metadata | Startup | `name` and `description` |
| Instructions | Skill trigger | `SKILL.md` body |
| Resources | As needed | References, scripts, templates, and data |

Only metadata for every installed skill is loaded at startup. The description
therefore carries discovery; the body and resources should focus on execution.

## Authoring Principles

- Assume the model is already capable. Include only information that earns its
  context cost.
- Match degrees of freedom to risk. Use text heuristics for open-ended work,
  parameterized patterns for preferred approaches, and exact scripts for fragile
  operations.
- Test with every model family the skill is intended to support. A powerful
  model may be harmed by over-explanation while a smaller model may need more.
- Build evaluations before extensive documentation. Establish a no-skill
  baseline, add the minimum instructions, and iterate from real usage.
- Use feedback loops for quality-critical work: run or inspect, fix, and verify
  again.
- Avoid time-sensitive instructions in the main path and keep terminology
  consistent.

## Skill Structure And Frontmatter

Every package requires `SKILL.md`:

```yaml
---
name: processing-pdfs
description: >
  Extracts text and tables, fills forms, and merges PDFs. Use when the user asks
  to work with PDF files or document forms.
---
```

Required fields:

- `name`: at most 64 characters; lowercase letters, numbers, and hyphens; no XML
  tags; no reserved `anthropic` or `claude` terms.
- `description`: non-empty, at most 1024 characters, no XML tags, and specific
  about both what the skill does and when to use it. Write in third person.

The portable default is these two fields only.
Keep `name` on one line. Write `description` as one quoted scalar or an indented
`>`/`|` block; quote a single-line value that contains `: ` so strict YAML
runtimes do not reinterpret it as a mapping. For maximum portability, avoid
inline comments and inner quote/escape syntax in metadata; use a block scalar
when the text needs either.

## Progressive Disclosure

- Keep the `SKILL.md` body under 500 lines; split before it becomes a context
  burden.
- Link references directly from `SKILL.md`. Avoid nested reference chains because
  the model may preview only part of a referenced file.
- Give references over 100 lines a contents map near the top.
- Use descriptive filenames and forward-slash relative paths.
- State whether a bundled script should be executed or read as reference.
- Prefer deterministic scripts for repeatable validation or transformation, and
  give errors enough detail to support repair.
- Make complex or high-stakes changes verifiable through a plan-validate-execute-
  verify loop.

## Evaluation And Iteration

The official process is evaluation-driven:

1. Run representative tasks without the skill and record specific gaps.
2. Create at least three scenarios that test those gaps.
3. Write the minimum instructions needed to address them.
4. Test with a fresh agent using the skill on real work.
5. Observe trigger choice, file navigation, ignored or overused content, and
   output quality.
6. Refine from observations and repeat.

There is no built-in universal evaluation runner. Use project-specific scripts,
rubrics, artifact checks, and representative prompts.

## Where Skills Work

- Claude Code: filesystem Custom Skills, personal or project-scoped, and plugin
  distribution.
- Claude API: pre-built and uploaded Custom Skills through the code-execution
  container and Skills API. Current use requires the documented Skills and Files
  beta headers.
- claude.ai: pre-built and individually uploaded Custom Skills for eligible
  plans with code execution.
- Claude Platform on AWS and Microsoft Foundry: documented Skills API support;
  product-specific deployment requirements apply.

Custom Skills do not automatically sync across these surfaces. API uploads are
workspace-wide, claude.ai uploads are individual, and Claude Code skills are
filesystem installations.

## Runtime Constraints

- Claude API skill containers have no network access or runtime package
  installation; use pre-installed dependencies only.
- Claude Code has the user's local network and execution environment; avoid
  global package installation and respect project policy.
- claude.ai network and installation behavior can vary with product and admin
  settings.
- Fully qualify MCP tools as `ServerName:tool_name` and do not assume a package
  or tool exists without a check or documented prerequisite.

## Security And Retention

Treat a skill like software. Audit every bundled instruction, script, image, and
external fetch for unexpected network access, file access, tool misuse, or data
exposure. External content can change and may contain malicious instructions.

Agent Skills is not eligible for Zero Data Retention under the current official
documentation. Check the live retention page for deployment decisions.

## Checklist

- Description is specific about what and when.
- Body is under 500 lines and contains only behavior-changing guidance.
- References are one level deep; long references have a contents map.
- Terminology and paths are consistent and portable.
- Scripts solve deterministic work, handle errors, and are documented.
- Critical operations have validation and feedback loops.
- At least three evaluations cover real usage and trigger behavior.
- Every intended model family has been tested or the gap is disclosed.
