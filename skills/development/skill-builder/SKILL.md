---
name: skill-builder
description: >
  Use when creating, improving, or auditing reusable agent skills: trigger
  descriptions, SKILL.md instructions, references, scripts, templates, packaging,
  or adaptation to a different model or harness. Turns real workflows and
  observed failures into scoped, verifiable packages. NOT for ordinary project
  documentation or one-off task prompts.
---

# Skill Builder

Build reusable capability from working procedures, domain knowledge, and recurring preferences. Choose instructions, evidence, and tools that make the task succeed.

## Quick Path

1. Infer the outcome, trigger, target harness, edit scope, and authority from the request and package. Ask only for consequential missing information.
2. Identify evidence: a real task, artifact, documented contract, preference, or correction. Diagnose failures before choosing what to change.
3. Choose coherent scope. Keep coupled steps together; split unrelated tasks with different triggers, tools, or permissions.
4. Edit the source and affected references together. Put routine instructions in SKILL.md, optional detail in references, repeatable operations in scripts, and output structures in assets.
5. Validate changed surfaces. Report format, execution, discovery, and behavioral evidence separately.
6. Deliver the usable patch, material decisions, and remaining limitations. Publication and installation follow the requested scope.

Read [local layout](references/local-skill-layout.md) for repository and installed copies. Read [source guide](references/skill-docs.md) for rule provenance and target-specific differences.

## Choose What Belongs

Add what the agent cannot reliably infer: a preferred explanation style, private schema, subtle API contract, required artifact, fragile operation, or recurring mistake. Start from real work and user preferences.

A simple skill can consist of its trigger, purpose, audience, and result format. Finish at that level when it fully expresses the reusable behavior. Add procedures, resources, or helpers only when the task needs them; the contract below is a set of considerations, not a required template.

Use project instructions for rules applying to every task, skills for reusable tasks, tools or MCP for access, and supported hooks for deterministic enforcement. Prose cannot grant a tool, implement a hook, or create a permission boundary.

Compare nearby skills before adding another. Overlap alone does not justify merging, and length alone does not justify splitting. Choose the boundary that makes selection and execution clearer.

For a failed workflow, identify whether information was missing, hard to retrieve, ambiguous, poorly exposed by tools, or impossible to check. Fix that cause before adding an instruction. Read [authoring patterns](references/skill-tips.md) for diagnosis and resource choices.

Inspect relevant project instructions, co-loaded skills, and tool descriptions for conflicts and duplication. Give each shared rule an authoritative home and link to it where needed. Edit only within the requested scope; report conflicts in instructions you cannot change.

## Write The Working Contract

Include what changes behavior:

- Result and observable completion condition.
- Inputs, authoritative sources, and defaults for routine omissions.
- Non-obvious invariants and preservation requirements.
- Exact steps where order, syntax, or side effects are fragile.
- Preferred route and a fallback for a specific failure.
- Required verification and what warrants retry or broader checks.

Use decision rules where approaches may vary. Explain why when the reason helps adaptation. Avoid mandatory planning files, fixed edit counts, universal headings, or exhaustive menus.

Descriptions drive discovery: lead with concrete tasks and natural user phrases. Add exclusions for real neighboring skills. Do not grow keywords until the skill captures unrelated work. Read [naming](references/skill-naming.md) when needed.

Capture observed gotchas as the condition, tempting mistake, and correction. Put critical exceptions on the normal path if the agent would not know to look for them. Do not invent failures to fill a Gotchas heading.

Use [frontier audit](references/frontier-model-audit.md) for model migration. Loading this skill does not select a model.

## Keep Detail Retrievable

Write Markdown prose as natural paragraphs without inserting line breaks to meet a character or column limit. Let the editor wrap lines visually. Preserve paragraph boundaries, list structure, tables, code blocks, and intentional Markdown hard breaks. Apply the same approach to references and prose in Markdown templates.

There is no universal 8KB limit. Bytes, tokens, and lines measure different things. Published guidance around 500 lines and 5,000 tokens is a reason to review structure, not a runtime rejection threshold.

Keep essential instructions together even above a size target. Move optional details according to when they are needed, with that condition beside the link. Prefer shallow navigation; intentional cross-links are valid. A contents map or search hints help long files, but a specific heading does not prove usability.

Keep schemas and enum values in one authoritative location. Prefer attributed synthesis and links over copied articles. Separate external advice from local choices.

Prefer references that preserve the needed detail: source code, schemas, tests, mockups, or expert criteria. State what the agent should extract or preserve. For human-facing artifacts, choose a form that helps the reader decide or act; interactive choices need a way to carry into the next step.

## Metadata And Harness Features

Start with name and description. Optional standard fields are valid; native fields need the target's documentation and verification. The [source guide](references/skill-docs.md) distinguishes those layers.

Use package-relative resource paths resolved from the skill location, not an assumed current directory. Document relevant interpreter, tool, network, and service prerequisites. Detect missing requirements and provide bounded setup; mentioning a dependency does not authorize installing it.

Design helper inputs, outputs, and errors to expose useful choices. Keep exact syntax and invariants where required; avoid examples that arbitrarily constrain otherwise valid approaches.

For shared packages, apply cross-harness-skills to adapter decisions. Its two-field example is a conservative default, not a format restriction. Keep authority boundaries in the body even when the host offers invocation controls.

State non-obvious network, write, credential, persistence, or cleanup effects. Reuse session grants. Store mutable user data outside replaceable package files. Use hooks and delegation only when supported and useful for the requested task.

## Verify The Authored Package

Distinguish three levels:

1. **Package:** metadata, resource links, dependencies, and warning review. Static checks do not establish security or model quality.
2. **Artifact:** meaningful local fixtures for changed scripts/templates, including outputs and failure paths. Reuse unchanged evidence only when source and relevant environment still match.
3. **Behavior:** actual task feedback or existing traces. Model trials, trigger benchmarks, comparisons, and persistent evaluation suites run only on request.

Model evaluations are opt-in by this package's workflow policy. Ordinary regression tests for a changed parser, validator, or generator remain expected. Documentation-only edits do not require synthetic model runs.

The validator requires Python 3.10+ and PyYAML (verified with 6.0.3). From the package root, with those dependencies available:

```bash
bash scripts/validate_skill.sh .
bash scripts/smoke_test.sh
```

Missing dependencies produce setup instructions, not automatic installation. When dependency fetching is authorized, an isolated alternative is:

```bash
uv run --with PyYAML==6.0.3 bash scripts/validate_skill.sh .
uv run --with PyYAML==6.0.3 bash scripts/smoke_test.sh
```

The Python entry point also supports --target claude-code for the documented Anthropic metadata restrictions. See [validation contract](references/validation.md) for exact coverage and limitations.

Finish when required checks and affected behavior have adequate evidence. Expand only for a new change, failure, requirement, or unresolved risk. For a pack audit, account for every package and fix conflicts at their source.

## Maintenance

Keep dated claims and provenance in references. Recheck relevant sources when changing version-sensitive rules, investigating reported drift, or reconciling runtime disagreement. A calendar interval alone does not require browsing for every edit. Preserve useful domain rules while removing obsolete compensation.

For important workaround rules, retain their failure condition and evidence in the relevant reference or change record. Revisit them when that model, tool, or contract changes; remove them when the reason no longer applies. Keep reusable instructions stable and per-run state in task artifacts or supported external storage. Cache behavior belongs in harness-specific guidance when relevant.

Report what changed, why, what ran, and what remains untested. Do not treat lint advisories as reasons to stop authorized work.
