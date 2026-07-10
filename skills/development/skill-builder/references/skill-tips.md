# Lessons from Building Claude Code: How We Use Skills

> Author: Thariq (@trq212), Anthropic
> Source: https://x.com/trq212

The original sections through Conclusion describe Claude Code practices and may
name Claude-only tools or metadata. For a skill shared with Codex, treat those
as source examples rather than portable commands; the Addenda and the
`cross-harness-skill-authoring` skill own the common contract.

## Table of Contents

This file is long. Agents preview it with `head -100`, so this map lists every
section and the gap it covers. Read only the section you need.

- What are Skills
- Types of Skills (the 9 categories)
- Tips for Making Skills (don't state the obvious, Gotchas, progressive disclosure, avoid railroading, setup, description-is-for-the-model, memory, scripts, hooks)
- Distributing Skills (check-in vs marketplace, composing, measuring)
- Conclusion
- Addenda for Skill Builder (long-form detail pulled out of SKILL.md):
    - A1. Portability for cross-harness packs
    - A2. Parallelism and subagents are an optimization, not a dependency
    - A3. Self-test discipline for bundled scripts and templates
    - A4. Progressive disclosure depth and reference-file TOCs
    - A5. Naming skills
    - A6. The description carries the discovery burden
    - A7. Single-source vocabulary across contract, template, validator, SKILL.md
    - A8. Mechanism over bare MUST/ALWAYS
    - A9. Frontmatter strictness across harnesses
    - A10. Script vs LLM-native decision (full table and worked example)


Skills have become one of the most used extension points in Claude Code. They're flexible, easy to make, and simple to distribute. But this flexibility also makes it hard to know what works best. What type of skills are worth making? What's the secret to writing a good skill? When do you share them with others?

We've been using skills in Claude Code extensively at Anthropic with hundreds of them in active use. These are the lessons we've learned about using skills to accelerate our development.

## What are Skills?

If you're new to skills, I'd recommend reading our docs or watching our newest course on new Skilljar on Agent Skills, this post will assume you already have some familiarity with skills.

A common misconception we hear about skills is that they are "just markdown files", but the most interesting part of skills is that they're not just text files. They're folders that can include scripts, assets, data, etc. that the agent can discover, explore and manipulate.

In Claude Code, skills also have a wide variety of configuration options including registering dynamic hooks.

We've found that some of the most interesting skills in Claude Code use these configuration options and folder structure creatively.

## Types of Skills

After cataloging all of our skills, we noticed they cluster into a few recurring categories. The best skills fit cleanly into one; the more confusing ones straddle several. This isn't a definitive list, but it is a good way to think about if you're missing any inside of your org.

### 1. Library & API Reference

Skills that explain how to correctly use a library, CLI, or SDKs. These could be both for internal libraries or common libraries that Claude Code sometimes has trouble with. These skills often included a folder of reference code snippets and a list of gotchas for Claude to avoid when writing a script.

Examples:
- billing-lib — your internal billing library: edge cases, footguns, etc.
- internal-platform-cli — every subcommand of your internal CLI wrapper with examples on when to use them
- frontend-design — make Claude better at your design system

### 2. Product Verification

Skills that describe how to test or verify that your code is working. These are often paired with an external tool like playwright, tmux, etc. for doing the verification.

Verification skills are extremely useful for ensuring Claude's output is correct. It can be worth having an engineer spend a week just making your verification skills excellent.

Consider techniques like having Claude record a video of its output so you can see exactly what it tested, or enforcing programmatic assertions on state at each step. These are often done by including a variety of scripts in the skill.

Examples:
- signup-flow-driver — runs through signup → email verify → onboarding in a headless browser, with hooks for asserting state at each step
- checkout-verifier — drives the checkout UI with Stripe test cards, verifies the invoice actually lands in the right state
- tmux-cli-driver — for interactive CLI testing where the thing you're verifying needs a TTY

### 3. Data Fetching & Analysis

Skills that connect to your data and monitoring stacks. These skills might include libraries to fetch your data with credentials, specific dashboard ids, etc. as well as instructions on common workflows or ways to get data.

Examples:
- funnel-query — "which events do I join to see signup → activation → paid" plus the table that actually has the canonical user_id
- cohort-compare — compare two cohorts' retention or conversion, flag statistically significant deltas, link to the segment definitions
- grafana — datasource UIDs, cluster names, problem → dashboard lookup table

### 4. Business Process & Team Automation

Skills that automate repetitive workflows into one command. These skills are usually fairly simple instructions but might have more complicated dependencies on other skills or MCPs. For these skills, saving previous results in log files can help the model stay consistent and reflect on previous executions of the workflow.

Examples:
- standup-post — aggregates your ticket tracker, GitHub activity, and prior Slack → formatted standup, delta-only
- create-\<ticket-system\>-ticket — enforces schema (valid enum values, required fields) plus post-creation workflow (ping reviewer, link in Slack)
- weekly-recap — merged PRs + closed tickets + deploys → formatted recap post

### 5. Code Scaffolding & Templates

Skills that generate framework boilerplate for a specific function in codebase. You might combine these skills with scripts that can be composed. They are especially useful when your scaffolding has natural language requirements that can't be purely covered by code.

Examples:
- new-\<framework\>-workflow — scaffolds a new service/workflow/handler with your annotations
- new-migration — your migration file template plus common gotchas
- create-app — new internal app with your auth, logging, and deploy config pre-wired

### 6. Code Quality & Review

Skills that enforce code quality inside of your org and help review code. These can include deterministic scripts or tools for maximum robustness. You may want to run these skills automatically as part of hooks or inside of a GitHub Action.

Examples:
- adversarial-review — spawns a fresh-eyes subagent to critique, implements fixes, iterates until findings degrade to nitpicks
- code-style — enforces code style, especially styles that Claude does not do well by default.
- testing-practices — instructions on how to write tests and what to test.

### 7. CI/CD & Deployment

Skills that help you fetch, push, and deploy code inside of your codebase. These skills may reference other skills to collect data.

Examples:
- babysit-pr — monitors a PR → retries flaky CI → resolves merge conflicts → enables auto-merge
- deploy-\<service\> — build → smoke test → gradual traffic rollout with error-rate comparison → auto-rollback on regression
- cherry-pick-prod — isolated worktree → cherry-pick → conflict resolution → PR with template

### 8. Runbooks

Skills that take a symptom (such as a Slack thread, alert, or error signature), walk through a multi-tool investigation, and produce a structured report.

Examples:
- \<service\>-debugging — maps symptoms → tools → query patterns for your highest-traffic services
- oncall-runner — fetches the alert → checks the usual suspects → formats a finding
- log-correlator — given a request ID, pulls matching logs from every system that might have touched it

### 9. Infrastructure Operations

Skills that perform routine maintenance and operational procedures — some of which involve destructive actions that benefit from guardrails. These make it easier for engineers to follow best practices in critical operations.

Examples:
- \<resource\>-orphans — finds orphaned pods/volumes → posts to Slack → soak period → user confirms → cascading cleanup
- dependency-management — your org's dependency approval workflow
- cost-investigation — "why did our storage/egress bill spike" with the specific buckets and query patterns

## Tips for Making Skills

Once you've decided on the skill to make, how do you write it? These are some of the best practices, tips, and tricks we've found.

We also recently released Skill Creator to make it easier to create skills in Claude Code.

### Don't State the Obvious

Claude Code knows a lot about your codebase, and Claude knows a lot about coding, including many default opinions. If you're publishing a skill that is primarily about knowledge, try to focus on information that pushes Claude out of its normal way of thinking.

The frontend design skill is a great example — it was built by one of the engineers at Anthropic by iterating with customers on improving Claude's design taste, avoiding classic patterns like the Inter font and purple gradients.

### Build a Gotchas Section

The highest-signal content in any skill is the Gotchas section. These sections should be built up from common failure points that Claude runs into when using your skill. Ideally, you will update your skill over time to capture these gotchas.

### Use the File System & Progressive Disclosure

Like we said earlier, a skill is a folder, not just a markdown file. You should think of the entire file system as a form of context engineering and progressive disclosure. Tell Claude what files are in your skill, and it will read them at appropriate times.

The simplest form of progressive disclosure is to point to other markdown files for Claude to use. For example, you may split detailed function signatures and usage examples into references/api.md.

Another example: if your end output is a markdown file, you might include a template file for it in assets/ to copy and use.

You can have folders of references, scripts, examples, etc., which help Claude work more effectively.

### Avoid Railroading Claude

Claude will generally try to stick to your instructions, and because Skills are so reusable you'll want to be careful of being too specific in your instructions. Give Claude the information it needs, but give it the flexibility to adapt to the situation.

### Think through the Setup

Some skills may need to be set up with context from the user. For example, if you are making a skill that posts your standup to Slack, you may want Claude to ask which Slack channel to post it in.

A good pattern to do this is to store this setup information in a config.json file in the skill directory. If the config is not set up, the agent can then ask the user for information.

Claude Code can present structured choices with its question tool. A portable
skill should request the interaction outcome rather than naming that built-in
tool, because other harnesses expose different interfaces.

### The Description Field Is For the Model

When Claude Code starts a session, it builds a listing of every available skill with its description. This listing is what Claude scans to decide "is there a skill for this request?" Which means the description field is not a summary — it's a description of when to trigger.

### Memory & Storing Data

Some skills can include a form of memory by storing data within them. You could store data in anything as simple as an append only text log file or JSON files, or as complicated as a SQLite database.

For example, a standup-post skill might keep a standups.log with every post it's written, which means the next time you run it, Claude reads its own history and can tell what's changed since yesterday.

Data stored in the skill directory may be deleted when you upgrade the skill, so you should store this in a stable folder, as of today we provide `${CLAUDE_PLUGIN_DATA}` as a stable folder per plugin to store data in.

### Store Scripts & Generate Code

One of the most powerful tools you can give Claude is code. Giving Claude scripts and libraries lets Claude spend its turns on composition, deciding what to do next rather than reconstructing boilerplate.

For example, in your data science skill you might have a library of functions to fetch data from your event source. Claude can then generate scripts on the fly to compose this functionality to do more advanced analysis.

### On Demand Hooks

Skills can include hooks that are only activated when the skill is called, and last for the duration of the session. Use this for more opinionated hooks that you don't want to run all the time, but are extremely useful sometimes.

For example:
- `/careful` — blocks rm -rf, DROP TABLE, force-push, kubectl delete via PreToolUse matcher on Bash. You only want this when you know you're touching prod — having it always on would drive you insane.
- `/freeze` — blocks any Edit/Write that's not in a specific directory. Useful when debugging: "I want to add logs but I keep accidentally 'fixing' unrelated code."

## Distributing Skills

One of the biggest benefits of Skills is that you can share them with the rest of your team.

There are two ways you might share skills with others:
1. Check your skills into your repo (under `./.claude/skills`)
2. Make a plugin and use the Claude Code Plugin marketplace

For smaller teams working across relatively few repos, checking your skills into repos works well. But every skill that is checked in also adds a little bit to the context of the model. As you scale, an internal plugin marketplace allows you to distribute skills and let your team decide which ones to install.

### Managing a Marketplace

How do you decide which skills go in a marketplace? How do people submit them?

We don't have a centralized team that decides; instead we try and find the most useful skills organically. If you have a skill that you want people to try out, you can upload it to a sandbox folder in GitHub and point people to it in Slack or other forums.

Once a skill has gotten traction (which is up to the skill owner to decide), they can put in a PR to move it into the marketplace.

A note of warning, it can be quite easy to create bad or redundant skills, so making sure you have some method of curation before release is important.

### Composing Skills

You may want to have skills that depend on each other. For example, you may have a file upload skill that uploads a file, and a CSV generation skill that makes a CSV and uploads it. This sort of dependency management is not natively built into marketplaces or skills yet, but you can just reference other skills by name, and the model will invoke them if they are installed.

### Measuring Skills

To understand how a skill is doing, we use a PreToolUse hook that lets us log skill usage within the company. This means we can find skills that are popular or are undertriggering compared to our expectations.

## Conclusion

Skills are incredibly powerful, flexible tools for agents, but it's still early and we're all figuring out how to use them best.

Think of this more as a grab bag of useful tips that we've seen work than a definitive guide. The best way to understand skills is to get started, experiment, and see what works for you. Most of ours began as a few lines and a single gotcha, and got better because people kept adding to them as Claude hit new edge cases.

---

# Addenda for Skill Builder

The sections above are Anthropic's original write-up. The sections below are the
long-form detail that SKILL.md points to. SKILL.md keeps a one-line summary of
each point and links here so the body stays small enough to load on any harness.

A skill is rarely used on one agent only. The same SKILL.md may be loaded by
Claude Code, Codex, Cursor, Gemini CLI, and other agents that read filesystem
skills. Everything below keeps a skill portable across those harnesses.

## A1. Portability for cross-harness packs

A portable skill makes no assumption about which agent, OS, shell, or installed
tooling is present. Concrete rules:

- **Forward-slash relative paths only.** Write `references/skill-tips.md`, never
  a backslash path and never an absolute machine path like `/Users/you/...` or
  `C:\...`. Absolute paths break the moment the skill is installed somewhere else.
- **No time-sensitive instructions in the main flow.** Do not write "as of this
  month" or "the new API" in the steps an agent follows. If an old approach must
  be recorded, put it in an `<details>` block so it does not read as current:

  ```markdown
  <details>
  <summary>Old patterns (pre-2025 layout, kept for reference)</summary>

  Earlier skills put everything in one file. Prefer progressive disclosure now.
  </details>
  ```

- **Never assume a package is installed.** If a step needs a tool, show the
  install step first (for example `pip install pypdf` or `npm i -g something`),
  or detect-and-fall-back the way `pdf-page-count`'s script tries `pypdf`, then
  `PyPDF2`, then the `pdfinfo` CLI. The Claude API surface has no runtime package
  installation at all, so a skill that silently assumes a package fails there.
- **Fully-qualified MCP tool names.** When a step uses an MCP tool, write it as
  `Server:tool` (for example `mcp-atlassian:confluence_get_page`), not a bare
  `confluence_get_page`. Different harnesses namespace MCP tools differently, and
  the bare name is ambiguous.
- **Tool-agnostic prose.** Describe WHAT to do, not which built-in tool to call.
  Write "read the file" or "search the codebase for X", not "use the Read tool"
  or "use Grep". Tool names differ per harness (Codex, Cursor, and Gemini do not
  all expose a `Read` tool), so naming a specific tool either fails or is ignored.
- **Keep SKILL.md small.** Target under ~8KB and under ~500 lines. Codex and some
  other harnesses inline the whole body into context, and a large body crowds out
  the user's actual task. Push detail into `references/` and link to it.

## A2. Parallelism and subagents are an optimization, not a dependency

Some harnesses can split work across parallel agents (Claude Code workflows and
subagents, Codex threads, and similar). This is powerful but it must never be a
hard dependency, because a skill that requires it simply fails on a harness that
lacks it.

Frame parallelism as a universal judgment rule, not a harness-specific MUST:

> When work splits into independent streams that benefit from parallelism, use
> the harness's parallel-execution capability aggressively. When a single linear
> session is more effective, do that. Probe for a native capability first; if none
> exists, run sequentially and say so.

Claude Code workflows/subagents and Codex threads are only illustrative examples
of a parallel capability, not the rule itself. So in a skill:

- Write the workflow so it completes correctly run sequentially by one agent.
- Offer parallel/subagent dispatch as an "if your harness supports it" speedup.
- Have the agent probe for the native capability, and if absent, state that it is
  falling back to sequential and continue.

## A3. Self-test discipline for bundled scripts and templates

Anything a skill ships that has a documented way to be run must pass that exact
invocation. A template that fails its own validator is a defect, not a starting
point the user is expected to fix.

- If a skill bundles a generator plus a validator (for example "init creates a
  project, validate checks it"), ship a smoke test that runs init and then
  validate and asserts exit code 0. If init-then-validate does not pass clean, the
  bundled template is broken.
- A bundled lint/format/check script must run cleanly on the skill's own example
  inputs before the skill ships.
- The smoke test is part of the Validate step, not an optional extra. Run it with
  the project's own runner and report the exit code; do not claim success without
  running it.

Example shape of a smoke test (keep comments in Korean per repo convention):

```bash
#!/usr/bin/env bash
# 번들된 템플릿이 자기 자신의 validator 를 통과하는지 확인하는 smoke test.
# init 으로 생성한 산출물을 곧바로 validate 에 넣어 exit 0 인지 본다.
set -euo pipefail

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# 1) 템플릿으로 산출물 생성 (init 단계)
./scripts/init.sh "$tmp/sample"

# 2) 생성한 산출물을 바로 검증 (validate 단계)
./scripts/validate.sh "$tmp/sample"

echo "smoke test passed: init -> validate exit 0"
```

## A4. Progressive disclosure depth and reference-file TOCs

- **References stay exactly one level deep, never chained.** SKILL.md may point to
  `references/foo.md`. That reference file must not, in turn, send the agent to a
  second reference file to understand foo. Chained references force the agent to
  walk a tree and burn context. If foo genuinely needs bar, fold bar into foo or
  point to both from SKILL.md.
- **Reference files over ~100 lines start with a table of contents.** Agents
  preview a file with `head -100`. If the file is long and the first 100 lines are
  prose, the agent cannot tell what is inside or where to jump. A TOC at the top
  (like the one in this file) lets the agent navigate without reading all of it.

## A5. Naming skills

- **Verb-first, gerund-leaning names.** `processing-pdfs`, `creating-skills`,
  `reviewing-prs`. A name that describes the action the skill performs reads well
  in a skill listing and disambiguates from siblings.
- **Avoid vague names.** `helper`, `utils`, `tools`, `data`, `common`. They tell
  the agent nothing about when to trigger, and two such skills in one pack are
  indistinguishable. The name plus the description carry discovery, so a vague
  name wastes half the signal.
- Lowercase with hyphens, max 64 characters, no reserved words (`anthropic`,
  `claude`), no XML tags.

## A6. The description carries the discovery burden

When an agent starts, it builds a listing of every skill's `name` + `description`
and scans that listing to decide which skill fits the request. The body is not in
context yet. So the description does the entire job of getting the skill found and
triggered at the right time, and nothing else can compensate for a weak one.

- **Third person, present tense.** "Creates ...", "Reviews ...", "Use when ...".
  Not "I will ..." or "You should ...".
- **Lead with trigger conditions, not a workflow summary.** Prefer "Use when the
  user wants to create or improve a skill ..." over "This skill walks through six
  steps ...". The agent is matching intent, not reading a manual.
- **Test with near-miss NEGATIVE cases.** Write two or three prompts that look
  close to your skill but should NOT trigger it, and confirm the description does
  not catch them. This guards both failure directions at once:
    - under-trigger: a real request fails to match (description too narrow or
      missing trigger phrases),
    - over-trigger: an adjacent request wrongly matches (description too broad).
  Name the adjacent skill the request should go to instead, inside the description
  ("NOT for X; use the Y skill"), so the listing itself routes the near-miss away.

## A7. Single-source vocabulary across documents

When one value must agree across several places (the list of allowed sections in
a contract doc, the same list baked into a template, the same list checked by a
validator, and the same list mentioned in SKILL.md), define it ONCE as a closed
set in one home location. Every other mention is a thin pointer back to that home,
not a restatement.

- Restating the set in four files means four copies drift the moment one changes,
  and the validator starts disagreeing with the template it is supposed to check.
- The home can be a small section in a reference file, a constant in a script, or
  a single fenced list. Pick one, name it, and link the rest to it.
- This applies to enums and fixed lists especially: section names, status values,
  allowed file types, required frontmatter keys.

## A8. Mechanism over bare MUST/ALWAYS

The original "Avoid Railroading" tip says rigid instructions break on edge cases.
The stronger rule: never write a bare `MUST` or `ALWAYS` without a mechanism and a
reason.

- A bare imperative ("ALWAYS validate the output") gives the agent no way to act
  and no way to generalize to a case you did not foresee. Pair the rule with HOW
  (the mechanism) and WHY (the reasoning), so the agent can apply the intent to a
  new situation.
- Reserve exact, non-negotiable "run this precise command, do not modify it"
  instructions for genuinely fragile or destructive operations, for example
  database migrations, force-push, or destructive cleanup. There, deviation is the
  hazard, so removing the agent's freedom is correct. Everywhere else, explaining
  the reasoning lets the model adapt and produces better behavior than a wall of
  capitalized absolutes.

## A9. Frontmatter strictness across harnesses

- **The portable default is two required fields only: `name` and `description`.**
  Every harness that loads filesystem skills accepts these.
- **Extra keys are not universally safe.** `version`, `tags`, `author`, custom
  metadata: some strict runtimes reject frontmatter they do not recognize, which
  makes the whole skill fail to load. So do not add extra keys by default.
- If a specific target harness documents support for an extra key and the skill is
  only ever used there, gate it on that harness. For a cross-harness pack, keep
  frontmatter to the two required fields. (This skill itself ships with only the
  two fields; keep it that way.)

## A10. Script vs LLM-native decision

Not every skill needs a `scripts/` directory. The key question:

> "After the script runs, does the LLM still need to make judgment calls to
> complete the task?"

If yes, and the input is small enough for the LLM to read directly, the script is
a premature middle layer: it adds maintenance cost without reducing the LLM's
actual work.

| Factor | Script wins | LLM-native wins |
|--------|------------|-----------------|
| Task nature | Purely deterministic (lint, format, count, compile) | Requires contextual judgment (what date? what description?) |
| Input scale | Large (1000+ files, structured data) | Small (<50 files, <50K tokens) |
| Output | Exact, reproducible result | Natural language plus edits that adapt to context |
| Rule completeness | Rules are exhaustive and enumerable | Rules are contextual, hard to encode ("is this task really done?") |
| Markdown parsing | N/A | Regex for markdown tables/frontmatter is fragile; the LLM reads natively |
| Maintenance | Stable input format, infrequent changes | Repo structure evolves; LLM adapts, scripts break |

**Worked example, a detect-then-fix sync skill:**
A skill once shipped a scanner that parsed frontmatter, compared index tables, and
reported discrepancies. It was deleted because: (1) only ~20 files, trivial for the
LLM to read; (2) the hard part was judgment ("extend the due date to when?", "how
should the index description change?"); (3) the regex hit edge cases immediately
(multiple `data:` lines in one file); (4) a sibling skill already covered the
structural checks. The LLM-native version was simpler and more capable.

**Heuristic:** if the workflow is a "detection" phase followed by a "fix" phase and
the fix needs judgment, consider skipping the detection script. The LLM can detect
and fix in one pass.
