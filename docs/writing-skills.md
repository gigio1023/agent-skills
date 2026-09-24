# Writing skill composition

Use these capabilities for the requested task. Installing them does not create a standing writing policy or a mandatory sequence.

| Capability | Responsibility |
| --- | --- |
| `technical-report-writing` | Own authoring and revision, including explicit AI-slop revision and Korean clarity, plus document selection, structure, compact tables, focused visuals, explanation, and production |
| `insight-dashboard` | Design a useful initial comparison and keep data definitions, selections, values, commentary, and exports consistent |
| Official `shadcn` skill | Implement shadcn/ui using upstream project-aware guidance |
| `share-internal-doc` | Merged into `technical-report-writing` on 2026-09-24 as its sharing-and-delivery reference; retired from Gigio Pack |
| `slop-aware-writing`, `korean-clarity` | Merged into `technical-report-writing`; their repository was archived on 2026-09-24 and remains the MIT license source |

Reuse the reader, evidence, and authority already established for the task. One task may need several capabilities, but it need not pass through every skill. Keep the actual explanation under one editorial judgment.

The writer is the main document-authoring entry point. Its core defaults require noun-phrase headings, explicit row and column meanings, short cells, deliberate table selection and splitting, focused visuals, and meaningful list hierarchy. State findings and proposals directly, omit ornamental author framing and research diaries, and introduce internal aliases through accurate domain terms. These preferences do not depend on opening an optional reference. Genre determines the depth: factual records need observations, explanations need mechanisms, and proposals need reasons and alternatives. A current explicit style request or governing template can override a default.

The writer's [finished examples](../skills/productivity/technical-report-writing/references/finished-examples.md) combine prose and displays for an explanation, measured comparison, and proposal. Its [correction cases](../skills/productivity/technical-report-writing/references/correction-cases.md) show the Korean sentence types users repeatedly removed and the replacement that states the subject, and its [exemplar passages](../skills/productivity/technical-report-writing/references/exemplar-passages.md) quote published Korean technical prose for the same operations. The public source library and close readings in [writing sources](writing-sources.md) retain the original techniques and their limits for pack maintenance; examples teach an operation without imposing a universal outline.

The writer's [sharing and delivery](../skills/productivity/technical-report-writing/references/sharing-and-delivery.md) reference carries the recipient, source-access, sharing-pass, and delivery rules. Publication and installation remain separate actions; no new style skill or mandatory multi-skill sequence is introduced.

Failure details, denominators, responsibilities, comparison conditions, and uncertainty matter when their omission changes interpretation. They are not required sections or ritual caveats. Context, an appropriate source document, or code may already make a condition clear. Explain core definitions and consequential differences where the intended reader needs them.

## Adoption

The writer, its sharing reference, and the dashboard live here. The writer absorbs the explicit slop revision and Korean clarity skills; the archived slop-aware-writing repository remains their license source. Use the [official shadcn skill](https://ui.shadcn.com/docs/skills) directly; this repository has no custom replacement.

Publishing these changes does not install skills or edit standing instructions. Refresh only the packages the user requests through `install-skill-pack`. If old project guidance names `slop-aware-writing` or `korean-clarity`, or mandates an automatic second pass through slop, propose pointing it at the writer within a requested setup; do not silently rewrite project configuration.

See [repository migration](migration.md) for package moves and merge order.
