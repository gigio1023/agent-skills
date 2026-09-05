# Authoring Patterns

These are adaptations, not a reproduction of an external article. The [source guide](skill-docs.md) records attribution and scope.

## Contents

- Choose the necessary depth
- Diagnose before adding instructions
- Turn evidence into instructions
- Select a mechanism
- Retrieval and execution
- Human-facing artifacts
- Learning from use

## Choose The Necessary Depth

A repeated preference can justify a skill even when the model already knows how to perform the task. Thariq's [ELI5 implementation](https://github.com/anthropics/claude-plugins-community/blob/794af9e63d07fad17087dcab61f21f44cb48effd/eli5/skills/eli5/SKILL.md) specifies a novice audience and a visual HTML result with very little instruction. It demonstrates a small package, not measured superiority or a universal length.

For such a skill, write clear discovery and the intended result, check the package, and finish. No script, reference folder, elaborate workflow, or invented gotcha is necessary. For a fragile task, retain precise ordering, effects, and required checks. Choose depth from the work, not a preferred file size.

Thariq's [later context guidance](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) also emphasizes expressive interfaces and rich references. Use these as design choices, not rules to delete all examples or shorten every skill by a percentage.

## Diagnose Before Adding Instructions

Use the observed task, result, and available context to choose a repair:

| Failure evidence | Authoring response |
| --- | --- |
| Essential fact was unavailable | Supply an authoritative reference or document the prerequisite |
| Relevant fact existed but was not found | Improve the loading condition, search hint, or resource interface |
| Task-specific preference or decision was missing | Supply the known default; ask about consequential ambiguity |
| Tool could not express the needed operation or report its result | Improve parameters, output, or errors; document unsupported cases |
| Loaded instructions conflict or repeat unnecessarily | Resolve the rule at its authoritative source within edit scope |
| Outcome could not be checked | State the task's observable result and available evidence |
| Old workaround constrains a capable model | Review the original reason and current evidence before removing it |

These are diagnostic options, not phases every authoring task must run. A suspected cause remains a hypothesis until supported by a trace, artifact, or actual use. Inspect only the relevant instruction stack: project guidance, this skill's references, co-loaded skills, and tool descriptions. Package lint cannot establish that their meanings agree.

When the reusable behavior is still unclear, choose the cheapest useful source of clarity: inspect existing work, compare a prototype, or ask a question whose answer changes the result. New information during implementation may justify revising the procedure. Keep material deviations in task artifacts when useful; carry only generalizable lessons into the installed skill. Do not force an interview or a new session for already-defined work.

## Turn Evidence Into Instructions

Start with failed artifacts, user corrections, successful commands, preferences, project contracts, or expert runbooks. Extract reusable decisions, not incidental identifiers from one run.

Write conditions and verification: "An accepted job may still be queued; check terminal state before reporting completion" is stronger than "verify everything."

For schemas, link to the authoritative definition rather than copying it into three documents. Source code can preserve behavior more faithfully than a prose summary; identify the semantics to retain. For subjective artifacts, name the properties to preserve and use a reference when it helps convey them. Examples should clarify requirements without making incidental details mandatory.

## Select A Mechanism

| Need | Resource | Contract |
| --- | --- | --- |
| Repeated audience, taste, or presentation preference | Short instruction | Trigger and intended result |
| Repeated parsing or transformation | Script | Inputs, outputs, dependencies, error status |
| Variable artifact with stable structure | Template | Required fields versus examples |
| Domain judgment | Instructions and evidence | Defaults and reasons |
| Rare error/provider variant | Focused reference | Loading condition |
| Deterministic action restriction | Supported hook | Installation, duration, cleanup |
| Historical context | External state | Owner, privacy, retention, update authority |
| Reusable orchestration pattern | Workflow template | Invariants, adaptable choices, completion condition, supported runtime |

Code can be valuable even when the agent makes the final judgment: use it to reduce repetitive work or produce reliable evidence. Avoid wrappers that only forward a small decision back to the model.

Expose meaningful parameters and actionable errors in a helper's own interface. Keep its usage contract there; avoid repeating a full manual across the skill, project instructions, and tool description. A worked example is useful for a non-obvious format or fragile operation, not as the only permitted approach.

For orchestration skills, distinguish executable procedures from templates the agent may adapt. Let task shape determine decomposition and useful parallelism; fixed agent counts or passes need a task-specific reason. Include supported runtime and resource constraints. A generic domain skill need not acquire orchestration.

## Retrieval And Execution

Choose a normal route and specific fallback. Group detail by when it is needed, not arbitrary size quotas. Put essential exceptions before the relevant action.

Prefer direct operational references; explanatory cross-links are valid. Avoid forcing several hops to discover a required step. Verify paths rather than forbidding links between references.

State whether a helper is read, imported, or executed. Give commands a working directory or resolve paths from the package. Installing a skill does not install its dependencies or authorize account operations.

Keep only relevant context on the normal route. Broad retrieval should expose findings and source pointers rather than require every intermediate result to be loaded. Where the harness supports isolation, use it when the task benefits from separating noisy exploration; preserve useful context for continuing work. Avoid universal session-reset or delegation instructions.

Stable package instructions and mutable run state have different lifecycles. Keep timestamps, current progress, and per-run identifiers in task artifacts or supported external storage. For a cache-sensitive harness adapter, consult the [caching source](skill-docs.md) before changing prompt layout or tool definitions. A portable skill cannot guarantee cache behavior.

## Human-Facing Artifacts

When the skill produces something a person must review, specify the decision or action it should support. Select a format for that purpose: prose, code, a test fixture, an annotated diff, a mockup, or an interactive document. HTML can help with visual comparisons and exploration; it is not a universal replacement for Markdown or a requirement for skill authoring.

For interactive output, define how selections carry forward: saved configuration, exported JSON, or a concise decision record the next step can consume. Preserve source links and the properties the implementation must honor. A polished display does not establish that its factual content is correct.

## Learning From Use

Review a normal trigger and an adjacent out-of-scope request when editing discovery. This may be a read-through, not an implicit request for agent runs or an evaluation suite.

When model evaluation is requested, compare the same task and environment against no skill or the previous version. Judge required outputs and side effects, not obedience to incidental stylistic sentences.

For important workarounds, retain the observed condition, evidence, and relevant model/tool dependency in a reference or change record. On a related change, revisit that reason and retire rules that no longer apply. A date alone is not evidence for deletion, and a past failure is not a reason to keep a rule forever. This does not require telemetry, background optimization, or a registry for every sentence. See the [validator contract](validation.md) for what static checks establish.
