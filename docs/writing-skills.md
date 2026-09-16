# Writing Skill Adoption

Use one writer for information selection, explanation, and prose. Add another capability only for a different responsibility in the same task. A report does not need to pass through a chain of writing skills before it can be shared.

## Responsibilities

| Capability | Responsibility |
| --- | --- |
| `technical-report-writing` | Compose, revise, or review reader-facing content; preserve meaning and voice; make the important explanation or comparison visible; produce the requested document |
| `insight-dashboard` | Keep analytical definitions, selected data, values, commentary, and exports consistent; make the useful comparison or operational action visible |
| Official `shadcn` skill | Implement shadcn/ui components using upstream project-aware guidance |
| `share-internal-doc` | Contribute recipient suitability, sensitive attribution, source access, review obligations, and authorized sharing |
| `korean-clarity` | Repair Korean semantic omissions and unclear relationships, including in ordinary responses |
| `slop-aware-writing` | Support an explicit focused revision request; do not require an automatic second pass after the writer |

The last three packages are maintained outside this repository. The table defines how to combine them with this writer, not a claim that their existing instructions have already been narrowed. Reuse the reader, evidence, and scope already established for the task.

## Defaults Without Another Skill

A broad description helps discovery, but installing a skill does not make its full instructions permanently active. For a requested default across document tasks, place a short shared rule in the project's or harness's supported standing instructions. Keep detailed language, examples, and production guidance in the writer's conditional references.

The following is an optional starting point for that setup, not an instruction to modify configuration during ordinary writing:

```text
For reader-facing documents, select and order content for the reader's purpose and background. Make the main finding, explanation, or task clear early; give a decisive comparison prominence when needed.
Preserve evidence strength, attribution, adverse facts, failures, denominators, and conditions that affect meaning or use. Place material qualifications beside the affected claim or result.
Remove accurate but irrelevant production receipts, generic caveats, routine definitions, UI tours, and self-assessment. Relocate detail only for an actual reader need or applicable record requirement; deletion needs no replacement or appendix.
Explain supported relationships in coherent paragraphs. Preserve the requested language, terminology, and voice; let the editor wrap Markdown prose visually instead of inserting fixed-width source breaks.
Inspect the delivered artifact for the reader's task. Keep essential explanations and conditions visible and legible in the intended medium; report material delivery problems without adding routine verification narration to the document.
```

Rendered text width, theme, heading language, and house terminology belong to the requested artifact or project's preferences. They are not universal consequences of these rules. In particular, natural Markdown source paragraphs do not prescribe unlimited CSS line width.

## Cross-Repository Migration

The writer and dashboard changes live in this pack. Complete the following in their owning repositories when migrating existing installations:

- Narrow `share-internal-doc` to its sharing responsibilities, update its catalog and project guidance, and reuse the writer's production resources instead of maintaining a second copy. Review existing local changes selectively; preserve unrelated work.
- Keep `slop-aware-writing` useful for explicit revision when installed alone. Remove its broad authoring and automatic second-pass role only with matching description, documentation, and compatibility changes.
- Retain `korean-clarity` as an independent Korean meaning-repair capability. Update composition references to recognize the writer without making it a prerequisite for ordinary responses.
- Use the [official shadcn skill](https://ui.shadcn.com/docs/skills) directly. Update any old custom-skill references; no local wrapper replaces the removed prototype.

Publishing this repository does not refresh installed copies or standing instructions. Installation remains a separately requested action through the existing install workflow.

## Relationship To Gigio Pack

Gigio Pack's useful distinction is continuity: carrying user intent, plans, actual results, and handoff across sessions, models, and harnesses. This repository supplies specialized methods for doing the work. A writing task can use the writer directly; a long project can use that same writer inside a requested Gigio workflow.

Judge a proposed core Gigio skill by the project decision or continuity boundary it preserves. Sharing fits when it completes authorized delivery; language rules and document composition belong to their specialist owner. Being shipped together can be convenient without giving two skills ownership of the same judgment. Existing explicitly chosen companions can remain optional members of the distribution; their presence need not redefine the core workflow or require every task to traverse it.
