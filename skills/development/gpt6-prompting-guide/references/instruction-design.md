# Designing Skills And Repository Instructions

Use this reference for the skill or instruction files in scope. The [OpenAI article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) motivates the design choices below; its observations are not evidence that any particular package has failed.

## Skill Discovery

A skill description should make selection easy before the body is loaded. Put the concrete task and any essential model target first. Remove feature inventories, repeated trigger phrases, and broad claims such as using a specialized skill for every related task. Add exclusions only when they distinguish a real neighboring workflow.

For example, a release skill can say:

```text
Prepare release notes from merged changes. Use when drafting or revising notes for a named release.
```

Expanding that trigger to all commits, reviews, or documentation work would load the skill where it adds little. When discovery is the problem, compare the relevant neighboring descriptions for overlap or contradiction. OpenAI reports that Codex can shorten descriptions when many skills are available; keep the useful selection signal early. The article specifies no universal character limit, skill-count limit, or truncation threshold.

## Progressive Disclosure

For a skill with multiple workflows, keep the entry point a small router. Give each resource a condition explaining when to read it and what it resolves. Put optional procedures, examples, and runtime details behind those links. A single-purpose skill may be complete in its entry point; creating references is not a requirement.

Keep indispensable constraints on the normal path. Moving a permission boundary or fragile command prerequisite into a reference that the agent may never open weakens the package. Selective reading should reduce irrelevant context while preserving the information needed for the chosen task.

Apply this design to the package being edited, including its templates. A short entry point that unconditionally loads all references still creates the same context burden. Remove duplicate policies and repair affected links together.

## Replace Inherited Recipes With Useful Decisions

For each questionable instruction, identify what it contributes: domain knowledge, an output requirement, a real permission boundary, a fragile operation, a user preference, or compensation for an observed failure. Retain the contribution. Remove generic narration and unnecessary prescribed sequences when the model can choose a suitable approach from the goal and constraints.

Keep exact procedures when order or syntax determines correctness, such as a migration prerequisite or a tool's result-correlation contract. Explain the reason when it helps the agent adapt. Do not replace a reliable procedure solely to shorten the file, impose a reduction percentage, or claim that stronger models need no guidance.

Repository instructions may also be used by contributors running Claude models or other harnesses. Keep shared project facts and invariants model-neutral. Scope GPT-6-specific tuning to an explicit target or a documented model-specific route; do not silently impose it on every contributor. Within the GPT-6 family, a clause written for an Astra behavior applies to Sol only after the Sol workload shows the same behavior. If a workaround has evidence worth retaining, keep its failure condition and source in a maintenance reference so it can be reconsidered when the model or tool changes.

## Make Repository Reading Conditional

`AGENTS.md` affects work throughout its applicable repository scope. Replace blanket reading requirements with links tied to the decisions they support:

```text
Use architecture.md when changing service boundaries, database.md for schema changes, and deployment.md when preparing a deployment.
```

Check that the linked material is still accurate. A typo fix need not inherit an architecture tour, and a schema change still needs its database constraints. Keep rules that apply to every task concise and in their authoritative location.

## Define Permission And Completion Together

Revisit an old ask-first rule by naming the action it governs and checking whether the session already authorizes that action. Narrow unnecessary review stops without deleting genuine boundaries. When approval remains necessary, complete the authorized preparation so the user can review a concrete action. Missing task information can still require an early question; continue independent work while awaiting it.

For a known local test workflow, an instruction can state:

```text
The local tests use disposable fixtures and have no production access. Run the affected suite, fix failures introduced by this change, and rerun affected checks without asking for approval at each step. Finish when the acceptance condition and required checks pass; report any pre-existing failure separately.
```

Use such wording only when the environment supports those claims. The article's confidence in Astra's judgment is not a safety guarantee or permission to bypass application or tool boundaries.

Define completion in terms of the requested result. If the task includes running the implementation, inspecting its output, and repairing failures, state that scope. Remove a first-implementation review stop when that decision is unnecessary. For exploratory work, name the question to investigate and the evidence or scope limit that ends the exploration. Avoid open-ended demands to keep improving forever.

## Review The Authored Result

For an explicitly requested multi-skill audit, account for every selected package and its affected normal paths. For a narrow edit, inspect only the relevant paths. Check that descriptions select the intended task, reference conditions preserve necessary constraints, and examples do not reintroduce mandatory itineraries or conflicting approval rules. Identify out-of-scope conflicts with proposed wording rather than changing unrelated packages.

Static checks can establish package structure and valid links. Claim behavior changes as measured only when actual task feedback or runs support them. Report a documented rationale as a rationale, not as a benchmark result.
