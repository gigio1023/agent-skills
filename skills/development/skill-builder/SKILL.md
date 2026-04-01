---
name: skill-builder
description: >
  Design and create high-quality agent skills (SKILL.md + directory structure).
  Use when the user wants to create a new skill, improve an existing skill, or
  asks about skill architecture and best practices. Triggers on: "skill 만들어줘",
  "make a skill", "create a skill for X", "agent skill", "SKILL.md 작성",
  or when discussing skill design, progressive disclosure, or skill directory structure.
  Also use when converting a working conversation workflow into a reusable skill.
---

# Skill Builder

Build agent skills following Anthropic's best practices from hundreds of production skills.

## Quick Start

Most skill creation follows this path:

1. Ask the user what the skill should do and when it should trigger
2. Pick a category (read `references/skill-tips.md` → "Types of Skills" for the 9 categories)
3. Create the directory and write SKILL.md with frontmatter + body
4. Run the validation checklist
5. Test with 2-3 real prompts

Jump to **Detailed Workflow** below for the full process.

## Reference Files

| File | When to read | What's in it |
|------|-------------|--------------|
| `references/skill-tips.md` | Choosing skill type, writing tips, gotchas, distribution, hooks | Anthropic internal lessons: 9 categories, progressive disclosure, composing skills |
| `references/skill-docs.md` | Field constraints, 3-level loading, platform differences, security | Official Anthropic docs snapshot — **refresh if >30 days old** (see below) |

### Refreshing the docs

`references/skill-docs.md` has a snapshot date at the top. If older than 30 days:
```
WebFetch https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
```
Use the fetched content as authoritative. Fall back to the local snapshot only if fetch fails.

`references/skill-tips.md` is static and does not need refreshing.

## Detailed Workflow

### 1. Understand Intent

Ask (or extract from conversation context):
- What should this skill enable Claude to do?
- When should it trigger? (what phrases/contexts)
- What's the expected output?
- Which category does it fit? (see `references/skill-tips.md`)
- Where should it live? (`~/.agents/skills/`, `.claude/skills/`, or a plugin)

If converting a conversation workflow into a skill, extract the sequence of steps,
tools used, corrections made, and input/output patterns from history.

### 2. Choose the Right Structure

A skill is a **folder**, not just a markdown file:

```
skill-name/
├── SKILL.md              # Required. Frontmatter + instructions (<500 lines ideal)
├── references/           # Docs loaded into context as needed
├── scripts/              # Executable code — runs without loading into context
├── assets/               # Templates, icons, fonts — copied into output
└── config.json           # Optional. User-specific setup (stored per-skill)
```

**Progressive disclosure** (from the 3-level loading model):
- Level 1 (~100 tokens): `name` + `description` — always in context
- Level 2 (<5K tokens): SKILL.md body — loaded when skill triggers
- Level 3 (unlimited): Subdirectories — loaded only when referenced

If SKILL.md approaches 500 lines, split into reference files with clear pointers.

#### Script vs LLM-native: When to bundle a script

Not every skill needs a `scripts/` directory. The key question:

> "After the script runs, does the LLM still need to make judgment calls to complete the task?"

If yes, and the input is small enough for the LLM to read directly, the script is a premature middle layer — it adds maintenance cost without reducing the LLM's actual work.

| Factor | Script wins | LLM-native wins |
|--------|------------|-----------------|
| Task nature | Purely deterministic (lint, format, count, compile) | Requires contextual judgment (what date? what description?) |
| Input scale | Large (1000+ files, structured data) | Small (<50 files, <50K tokens) |
| Output | Exact, reproducible result | Natural language + edits that adapt to context |
| Rule completeness | Rules are exhaustive and enumerable | Rules are contextual, hard to encode (e.g. "is this task really done?") |
| Markdown parsing | N/A | Regex for markdown tables/frontmatter is fragile — LLM reads natively |
| Maintenance | Stable input format, infrequent changes | Repo structure evolves — LLM adapts, scripts break |

**Real example — task-sync skill (brain repo, 2026-03):**
Initially built a Python scanner (parse frontmatter, compare INDEX tables, report discrepancies).
Deleted it because: (1) only ~20 task files — trivial for LLM to read, (2) the hard part was judgment calls like "extend due date to when?" and "how should the INDEX description change?", (3) the regex immediately hit edge cases (multiple `data:` lines in dashboard.md), (4) vault-health already covered structural checks. The LLM-native version was simpler and more capable.

**Heuristic:** If the skill's workflow has a "detection" phase followed by a "fix" phase, and the fix requires judgment, consider skipping the detection script entirely. The LLM can detect and fix in one pass.

### 3. Write the SKILL.md

#### Frontmatter

```yaml
---
name: lowercase-with-hyphens    # max 64 chars, no "anthropic"/"claude"
description: >                  # max 1024 chars — this is for the MODEL, not humans
  What this skill does AND when to use it. Be specific about trigger contexts.
  Include example phrases. Err on "pushy" — Claude undertriggers more than overtriggers.
---
```

**Description tips:**
- Lead with what it does, then list trigger contexts
- Include Korean + English trigger phrases if bilingual
- Name adjacent skills it should NOT trigger for (if ambiguous)
- Imagine Claude scanning 50 descriptions — yours needs to win

#### Body Structure

Organize around what Claude needs to DO:

```markdown
# Skill Name

## Quick Start
[80% case — most common usage path]

## Detailed Workflow
[Step-by-step for the full process]

## Gotchas
[Common failure points — highest-signal section]

## Reference Files
[Table: file → when-to-read → content]
```

#### Writing Principles

Read `references/skill-tips.md` → "Tips for Making Skills" for the full set. Key points:

- **Don't state the obvious** — focus on what pushes Claude out of its defaults
- **Explain the why** — reasoning > rigid rules. Avoid ALWAYS/NEVER in all caps
- **Gotchas section is mandatory** — highest ROI content. Update as Claude hits edge cases
- **Progressive disclosure** — don't dump everything in SKILL.md. Split and point
- **Bundle repeated scripts** — if Claude would write the same helper every time, pre-bundle it
- **Config pattern for setup** — `config.json` for user-specific values

### 4. Validate

Before considering the skill done:

- [ ] `name`: lowercase, hyphens only, max 64 chars, no reserved words
- [ ] `description`: <1024 chars, includes trigger contexts, "pushy" enough
- [ ] SKILL.md body: <500 lines (split to references/ if over)
- [ ] Referenced files exist at specified paths
- [ ] Scripts are executable and tested
- [ ] Gotchas section exists
- [ ] No secrets or credentials in any file

### 5. Test with Real Prompts

Create 2-3 realistic prompts — what a real user would actually say.
Evaluate:
- Does the skill trigger when it should?
- Does Claude follow instructions correctly?
- Are outputs what the user expects?
- Does Claude read references at the right time (not too early, not too late)?

### 6. Iterate

Best skills start small and grow:
- Add to Gotchas as Claude makes mistakes
- Refine description if triggering is too broad/narrow
- Bundle scripts when Claude keeps generating the same code
- Split SKILL.md if it grows past 500 lines

## Skill Categories (Quick Reference)

9 categories from Anthropic's internal experience (details in `references/skill-tips.md`):

| # | Category | What it does |
|---|----------|-------------|
| 1 | Library & API Reference | How to use a library/CLI/SDK correctly |
| 2 | Product Verification | Test/verify code works (playwright, tmux) |
| 3 | Data Fetching & Analysis | Connect to data/monitoring stacks |
| 4 | Business Process | Automate repetitive workflows |
| 5 | Code Scaffolding | Generate framework boilerplate |
| 6 | Code Quality & Review | Enforce standards, review code |
| 7 | CI/CD & Deployment | Fetch, push, deploy |
| 8 | Runbooks | Symptom → investigation → report |
| 9 | Infrastructure Ops | Maintenance with guardrails |

If a skill straddles categories, it might be trying to do too much — consider splitting.

## On-Demand Hooks

Skills can register hooks activated only when the skill is called:

```yaml
hooks:
  - event: PreToolUse
    matcher: Bash
    script: ./scripts/guard.sh
```

See `references/skill-tips.md` → "On Demand Hooks" for examples.

## Gotchas

- **Undertriggering > overtriggering.** Make descriptions pushy. The description is the
  most important line in the entire skill — a great skill that never triggers is useless.
- **Progressive disclosure is the architecture's superpower.** Don't put everything in
  SKILL.md. Split to references/ and tell Claude when to read each file.
- **Scripts > inline instructions for deterministic tasks.** Scripts don't consume context
  and are more reliable than asking Claude to regenerate the same code.
  However, if the task requires judgment after detection, and the input is small (<50 files),
  an LLM-native approach may be simpler and more capable. See "Script vs LLM-native" in Step 2.
- **`${CLAUDE_PLUGIN_DATA}` for persistent data.** Skill directory may be deleted on
  upgrade. Use the stable data folder for logs, config, and state.
- **Don't duplicate between SKILL.md and references.** SKILL.md should point to references,
  not restate them. If you find yourself copying content from a reference file into SKILL.md,
  you're violating progressive disclosure.
- **Avoid railroading.** The more rigid the instructions, the more edge cases they break on.
  Explain reasoning so Claude can adapt to situations you didn't anticipate.
- **Overlapping skills? Merge unless both have frequent independent triggers.** When two
  skills seem to overlap, ask: "Will skill B realistically be called on its own, or does it
  almost always follow skill A?" If B is 90%+ called via A, merge B into A as expanded scope
  or a reference doc — don't maintain a separate skill. The brain repo's task-sync was created
  as a separate skill, then merged into conversation-sync's Z10 zone within the same session
  because it had no real independent use case. New phase or separate skill = more moving parts
  to maintain. Expand an existing zone or add a reference checklist instead.
