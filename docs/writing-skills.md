# Writing skill composition

Use these capabilities for the requested task. Installing them does not create a standing writing policy or a mandatory sequence.

| Capability | Responsibility |
| --- | --- |
| `technical-report-writing` | Own document selection, structure, compact tables, focused visuals, explanation, and production |
| `insight-dashboard` | Design a useful initial comparison and keep data definitions, selections, values, commentary, and exports consistent |
| Official `shadcn` skill | Implement shadcn/ui using upstream project-aware guidance |
| `share-internal-doc` in Gigio Pack | Apply the writer, then check recipients, sensitive attribution, source access, and authorized delivery |
| `slop-aware-writing` | Explicit focused revision of existing prose; useful on its own |
| `korean-clarity` | Repair Korean semantic omissions and unclear relationships, including in ordinary responses |

Reuse the reader, evidence, and authority already established for the task. One task may need several capabilities, but it need not pass through every skill. Keep the actual explanation under one editorial judgment.

The writer is the main document-authoring entry point. Its core defaults require noun-phrase headings, explicit row and column meanings, short cells, deliberate table selection and splitting, focused visuals, and meaningful list hierarchy. State findings and proposals directly, omit ornamental author framing and research diaries, and introduce internal aliases through accurate domain terms. These preferences do not depend on opening an optional reference. Genre determines the depth: factual records need observations, explanations need mechanisms, and proposals need reasons and alternatives. A current explicit style request or governing template can override a default.

The writer's [finished examples](../skills/productivity/technical-report-writing/references/finished-examples.md) combine prose and displays for an explanation, measured comparison, and proposal. Its [correction cases](../skills/productivity/technical-report-writing/references/correction-cases.md) show the Korean sentence types users repeatedly removed and the replacement that states the subject, and its [exemplar passages](../skills/productivity/technical-report-writing/references/exemplar-passages.md) quote published Korean technical prose for the same operations. The public source library and close readings retain the original techniques and their limits; examples teach an operation without imposing a universal outline.

share-internal-doc adds the sharing context without duplicating those methods. Calling it alone remains enough to obtain a complete shared document. Publication and installation remain separate actions; no new style skill or mandatory multi-skill sequence is introduced.

Failure details, denominators, responsibilities, comparison conditions, and uncertainty matter when their omission changes interpretation. They are not required sections or ritual caveats. Context, an appropriate source document, or code may already make a condition clear. Explain core definitions and consequential differences where the intended reader needs them.

## Adoption

The writer and dashboard live here; sharing stays in Gigio Pack. The separate slop package keeps its explicit revision role and the independent Korean clarity skill. Use the [official shadcn skill](https://ui.shadcn.com/docs/skills) directly; this repository has no custom replacement.

Publishing these changes does not install skills or edit standing instructions. Refresh only the packages the user requests through `install-skill-pack`. If old project guidance mandates an authoring or automatic second pass through slop, propose changing that guidance within a requested setup; do not silently rewrite project configuration.

See [repository migration](migration.md) for package moves and merge order.
