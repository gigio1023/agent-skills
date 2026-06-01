---
name: skill-builder
description: >
  Use when the user wants to create a new agent skill, improve an existing skill,
  convert a working conversation workflow into a reusable skill, or asks about
  skill architecture, progressive disclosure, references/scripts/assets layout, or
  cross-harness portability. Also use when manually optimizing a skill from traces,
  failed prompts, user feedback, validation results, or repeated agent mistakes.
  Triggers on "skill 만들어줘", "make a skill", "create a skill for X", "agent skill",
  "SKILL.md 작성", "improve this skill". Produces SKILL.md plus directory structure
  for Claude Code, Codex, Cursor, Gemini, and other agents that load filesystem
  skills. NOT for writing ordinary project docs (use a docs skill) or PR bodies.
---

# Skill Builder

Build portable agent skills following Anthropic's best practices. A skill is a
folder, not just a markdown file, and the same SKILL.md may be loaded by Claude
Code, Codex, Cursor, Gemini, and other agents, so everything here stays
harness-neutral.

## Quick Start

Most skill creation follows this path:

1. Ask the user what the skill should do and when it should trigger.
2. Pick a category (`references/skill-tips.md` -> "Types of Skills", 9 categories).
3. Create the directory and write SKILL.md (frontmatter plus body).
4. Run the Validate checklist below, including the self-test for any bundled script.
5. Test with 2-3 real prompts plus near-miss negative prompts.

For improving an existing skill from observed behavior, use the manual
SkillOpt-style loop in **Manual Skill Optimization** below: read
`references/skillopt-manual.md`, then work from evidence batches, bounded patch
ops, explicit ranking, and a fixed validation gate.

## Reference Files

References are exactly one level deep (SKILL.md points here; these files do not
chain to each other). Read only what you need.

| File | When to read | What's in it |
|------|-------------|--------------|
| `references/skill-tips.md` | Choosing skill type, writing tips, portability, naming, descriptions, gotchas, distribution, hooks | Anthropic lessons plus skill-builder Addenda (A1-A10). Has a TOC up top |
| `references/skill-docs.md` | Field constraints, 3-level loading, platform differences, security | Official Anthropic docs snapshot. Refresh if >30 days old (see below) |
| `references/skillopt-manual.md` | Improving an existing skill from traces, failing prompts, feedback, or validation results | Manual SkillOpt protocol: failure/success analysis, merge, rank, bounded patch ops, validation gate, rejected-edit notes |

### Refreshing the docs

`references/skill-docs.md` has a snapshot date at the top. If older than 30 days,
fetch the current docs from the Anthropic agent-skills overview page and treat the
fetched content as authoritative; fall back to the local snapshot only if the
fetch fails. `references/skill-tips.md` is static and does not need refreshing.

## Detailed Workflow

### 1. Understand Intent

Ask, or extract from conversation context:

- What should this skill enable the agent to do, and when should it trigger?
- What is the expected output, and which of the 9 categories does it fit?
- Where should it live (personal skills dir, project `.claude/skills/`, or a plugin)?
- If improving an existing skill: what concrete evidence shows current success,
  failure, undertriggering, overtriggering, or missing procedure? What fixed
  validation signal will decide whether the edit helped, and what is the baseline
  before editing? Keep model, harness, prompts, tests, and evaluator fixed while
  comparing a candidate patch.

If converting a conversation workflow into a skill, extract the sequence of steps,
tools used, corrections made, and input/output patterns from history.

### 2. Choose the Right Structure

```
skill-name/
├── SKILL.md              # Required. Frontmatter plus instructions
├── references/           # Docs read into context as needed (one level deep)
├── scripts/              # Executable code, runs without loading into context
├── assets/               # Templates, icons, fonts, copied into output
└── config.json           # Optional. User-specific setup, stored per-skill
```

**Progressive disclosure** (the 3-level loading model): Level 1 is `name` plus
`description` (~100 tokens, always in context); Level 2 is the SKILL.md body
(loaded on trigger); Level 3 is subdirectories (loaded only when referenced).

Keep SKILL.md small, target under ~8KB and under ~500 lines, so it loads on any
harness including Codex; split detail into references if it grows past that.
References stay one level deep and never chain, and a reference over ~100 lines
starts with a TOC (A4). On whether to bundle a script at all: not every skill
needs `scripts/`, and a detection script whose output still needs LLM judgment is
usually a premature middle layer. Full decision table in `skill-tips.md` A10.

### 3. Write the SKILL.md

#### Frontmatter (strict, two fields only)

```yaml
---
name: creating-skills         # lowercase-hyphens, max 64 chars, no anthropic/claude
description: >                 # max 1024 chars, written for the MODEL, not humans
  Use when ... (lead with trigger conditions, third person). Include example
  phrases. Name adjacent skills it should NOT trigger for.
---
```

- **Frontmatter is strict** (A9): two fields only by default. Extra keys like
  `version`/`tags` may be rejected by strict runtimes and fail the whole load; gate
  any on a specific target harness that documents it.
- **Name** (A5): verb-first, gerund-leaning (`processing-pdfs`, `creating-skills`).
  Avoid vague names (`helper`, `utils`, `tools`, `data`); they carry no signal.
- **Description** (A6): it carries the entire discovery/trigger burden, since the
  body is not in context when the agent scans the skill listing. Third person,
  lead with "Use when ..." (not a workflow summary), keep "NOT for X; use Y"
  pointers, and test against near-miss NEGATIVE prompts to guard both
  under-triggering and over-triggering.

#### Body Structure

Organize around what the agent needs to DO: a Quick Start for the 80% case, a
Detailed Workflow, a mandatory Gotchas section (highest-signal content), and a
Reference Files table.

#### Writing Principles

Each principle below is a one-line pointer; the full reasoning lives in
`references/skill-tips.md` (read the linked section before applying it). Don't
restate the linked text here.

- **Don't state the obvious.** Focus on what pushes the agent out of its defaults.
- **Gotchas section is mandatory.** Update it as the agent hits edge cases.
- **Progressive disclosure.** Don't dump everything in SKILL.md; split and point.
- **Mechanism over bare MUST/ALWAYS** (A8): pair every rule with HOW and WHY so the
  model generalizes; reserve exact non-negotiable commands for fragile/destructive
  ops like migrations or force-push.
- **Single-source vocabulary** (A7): define a shared section list or status enum
  ONCE as a closed set; every other mention is a thin pointer, never a restatement.
- **Portability** (A1): forward-slash relative paths, no absolute machine paths, no
  time-sensitive instructions in the main flow (use a `<details>` "Old patterns"
  block), no assumed-installed packages (show the install step), fully-qualified
  MCP tool names (`Server:tool`), WHAT-to-do prose (not "use the Read tool").
- **Parallelism is optional, not a dependency** (A2): when work splits into
  independent streams use the harness's parallel capability aggressively, else run
  a single linear session. Probe for a native capability first; if none, run
  sequentially and say so. Claude Code workflows/subagents and Codex threads are
  only examples of such a capability, never the rule. The skill must complete
  correctly run sequentially.
- **Self-test what you ship** (A3): any bundled script or template must pass its
  own documented invocation.
- **Config pattern for setup:** use `config.json` for user-specific values.

### 4. Validate

Before considering the skill done:

- [ ] `name`: lowercase, hyphens only, max 64 chars, no reserved words, verb-first.
- [ ] `description`: <1024 chars, third person, "Use when ..." triggers, NOT-for
      pointers, tested against near-miss negatives.
- [ ] Frontmatter has only `name` and `description`.
- [ ] SKILL.md body under ~8KB and ~500 lines (split to references/ if over).
- [ ] References exist at forward-slash relative paths, one level deep, no chaining;
      any reference over ~100 lines has a TOC.
- [ ] No absolute machine paths, no time-sensitive instructions in the main flow,
      no assumed-installed packages, MCP tools fully qualified as `Server:tool`.
- [ ] Any bundled script/template passes its own documented invocation. A
      generate-then-validate skill ships a smoke test (init then validate, assert
      exit 0); run it and report the exit code. A template that fails its own
      validator is a defect (A3).
- [ ] Gotchas section exists. No secrets or credentials in any file.
- [ ] Optimization pass only: edits were bounded, evidence-backed, and checked
      against the same validation prompts/tests before acceptance (ties rejected).

### 5. Test with Real Prompts

Create 2-3 realistic positive prompts plus 1-2 near-miss negative prompts, and
check:

- Does the skill trigger when it should, and stay quiet on the near-misses (an
  adjacent skill, or no skill, should win there)?
- Does the agent follow instructions correctly and read references at the right
  time (not too early, not too late)?
- Are outputs what the user expects?
- For optimization work, keep a small fixed validation set separate from the
  examples used to invent the edit. Do not judge only on the failure that inspired
  the patch.

### 6. Iterate

Best skills start small and grow: add to Gotchas as the agent makes mistakes,
refine the description if triggering is too broad or narrow, bundle a script when
the agent keeps generating the same code, and split SKILL.md if it grows past the
size budget. For SkillOpt-style improvement, prefer deliberate user-triggered
sessions with evidence and validation over automatic periodic learning.

## Manual Skill Optimization

Use this only when the user explicitly asks to improve/optimize a skill or
provides concrete behavior to learn from. Do not create background jobs,
scheduled learning, or automatic self-editing unless the user asks.

Read `references/skillopt-manual.md` and follow its Manual Session Template. In
short: freeze the target (skill file, model/harness, core loop, baseline,
validation gate); split evidence into failures and successes and analyze them
separately, then merge with failure fixes taking priority; rank edits by
systematic impact, complementarity, generality, and actionability; apply at most
1-4 atomic edits (`append`, `insert_after`, `replace`, `delete`); validate against
the fixed gate and accept only clear improvements without regression, keeping
rejected edits out of SKILL.md.

## Skill Categories and Hooks

The 9 skill categories (Library/API Reference, Product Verification, Data
Fetching, Business Process, Code Scaffolding, Code Quality/Review, CI/CD,
Runbooks, Infrastructure Ops) are detailed with examples in
`references/skill-tips.md` -> "Types of Skills". Pick one; a skill that straddles
categories is usually doing too much. Some harnesses also let a skill register
on-demand hooks that live only for the session (for example a shell-command
guard). Treat hooks as a harness-specific, optional enhancement and keep the skill
working without them (`skill-tips.md` -> "On Demand Hooks").

## Gotchas

The Writing Principles above are the canonical home for the portability, naming,
description, parallelism, self-test, single-source, mechanism, and frontmatter
rules (each links to a `skill-tips.md` section). These gotchas are the
highest-signal reminders that do not appear there:

- **Undertriggering > overtriggering.** The description is the most important line
  in the skill; a great skill that never triggers is useless. Guard the other
  direction with near-miss negative prompts.
- **Don't duplicate between SKILL.md and references.** SKILL.md points to
  references, it does not restate them. Restated content drifts.
- **Persistent data lives outside the skill dir.** The skill directory may be
  deleted on upgrade; use the harness's stable per-plugin data folder for logs,
  config, and state.
- **Improving a skill is evidence-driven and user-triggered.** Use traces, failing
  prompts, and successful counterexamples; bounded edits beat rewrites; validation
  is the safety rail (`references/skillopt-manual.md`). Do not schedule background
  self-editing unless the user asks.
- **Overlapping skills? Merge unless both have frequent independent triggers.** If
  skill B is 90%+ reached via skill A, fold B into A as expanded scope or a
  reference doc rather than maintaining a separate skill.
