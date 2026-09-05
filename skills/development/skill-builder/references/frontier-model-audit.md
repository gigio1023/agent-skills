# Model-Aware Skill Audit

Use when a model change or observed failure suggests old instructions no longer help. Do not rewrite a package merely to mention a newer model.

## Establish The Problem

Read the skill, relevant loaded instructions, and user correction. Distinguish the expected result, actual result, and suspected cause. A hypothetical failure is not a measured regression.

Inspect the relevant stack together: project guidance, co-loaded skills, linked resources, and tool descriptions. Locate where a duplicated or conflicting rule belongs. Do not turn a scoped audit into an edit of every installed instruction.

Consult the matching model guide and current primary source for model claims. [OpenAI's Astra guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) identifies clarification pauses, loaded-file conflicts, presentation, delegation, and excessive verification as areas to investigate. It does not establish that every skill needs every intervention.

## Audit By Function

| Instruction | Treatment |
| --- | --- |
| Domain fact or artifact invariant | Preserve/correct against its source |
| Fragile command, ordering, authority | Keep precise and verify |
| Observed mistake | Keep condition and remedy |
| Repeated policy or generic knowledge | Remove when it adds no task information |
| Host-specific feature | Put in the documented target layer |
| Legacy compensation | Reassess; age alone does not invalidate it |
| Repeated user preference | Preserve when it usefully selects audience, taste, or output |

Classify only enough to make the edit. No audit matrix, fixed edit count, or target byte size is required.

Thariq's [July 2026 context guidance](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) reports reducing Claude Code's system prompt by over 80% without measurable loss on its coding evaluations. That is evidence about those models and that harness, not a reduction target or evidence of gains for this package or another model.

## Fix The Cause

Resolve conflicts at their source. Preserve the user's authorized outcome; do not append an unlimited-autonomy override. Missing decisions block only the dependent work.

Use the [diagnosis options](skill-tips.md) to distinguish missing information, retrieval problems, ambiguous requirements, interface limits, and missing outcome evidence. Improve the affected resource or interface when prose is not the cause. An expressive parameter or useful error can replace several instructions about working around an awkward helper.

Keep required detail when shortening. Use code for reliable repetitive work and leave contextual choices to the agent. Delegation needs actual capability, bounded work, and an integration owner. A domain skill should not silently select a model tier or runtime setting.

Inspect affected references and templates. A clean entry point does not repair a contradictory procedure it subsequently loads.

Keep a workaround's failure condition and supporting evidence in an existing reference or change record when future maintainers need it. Reconsider it when the relevant model, tool, or contract changes. Preserve essential constraints and retain enough provenance to explain a removal.

## Verify And Finish

Run package checks and meaningful tests of changed executable resources. Use actual task feedback and existing traces when available. Model trials, benchmarks, and scorecards require a corresponding request.

For requested comparisons, hold inputs, tools, environment, and relevant settings constant. Compare required outputs and unwanted effects. Report improvement only for behavior exercised.

Deliver the changed contract, preserved constraints, checks, and untested behavior. Editing instructions does not switch runtime models.
