# Composition with Document and Interface Skills

Use when document work also involves internal sharing, a dashboard, focused language repair, or an interface implementation. Compose only the specialties needed for the requested artifact; do not restart intake or route every document through the entire pack.

## Responsibilities

| Skill | Contribution |
| --- | --- |
| `technical-report-writing` | Document craft: selection, structure, headings, tables, visuals, explanation, and production |
| `share-internal-doc` | Merged into this skill on 2026-09-24: recipients, source access, the latest shared copy, the sharing pass, and delivery are in [sharing and delivery](sharing-and-delivery.md); the Gigio Pack skill is retired |
| `insight-dashboard` | Quantitative comparison, informative initial view, data/filter/claim alignment, and static presentation of selected results |
| [Official shadcn skill](https://ui.shadcn.com/docs/skills) | Maintainer-provided shadcn project and component guidance for an actual implementation |
| `frontend-design` | Design intensity, composition, and visual/interaction review for a user-visible change |
| `slop-aware-writing` | Merged into this skill: explicit AI-slop revision is in [authoring and revision](authoring-and-revision.md), adapted under the [MIT notice](../LICENSE.slop-aware-writing) |
| `korean-clarity` | Merged into this skill: Korean semantic repair, including in chat, is in [Korean writing](korean-writing.md) |

Use this writer as the authoring entry point for a document and for its sharing; a request that names `share-internal-doc` is served here. Carry the reader brief and explicit editorial preferences through once, then run the recipient and delivery checks. Do not draft the document twice. No separate style skill is created; the author's standing preferences live in one file, [writing profile](writing-profile.md), which SKILL.md always applies and which the author's instruction files carry by import or synchronized copy. Check installed companion versions during adoption; a draft PR does not update them. Missing companions do not remove accuracy, privacy, or established user preferences.

## Useful combinations

- **Internal document:** use this writer for the document's content and expression, then [sharing and delivery](sharing-and-delivery.md) before the copy leaves the machine.
- **Standalone report, guide, memo, or post:** use this skill directly. Add specialized document or figure tooling only as the medium requires.
- **Data dashboard:** combine the writer's information selection and prose with `insight-dashboard` for comparison and state correctness. Use the official shadcn skill only for an actual shadcn implementation. A result statement should describe the active data, not advertise the interface.
- **Print-first PDF:** choose a native production route here. Do not load frontend skills or build a web application solely because the document contains tables or charts.
- **Generic shadcn form or product UI:** use the official shadcn skill and relevant frontend design guidance. Do not create or require a local wrapper for the official skill. A document-writing workflow is unnecessary unless the requested work includes substantive reader-facing prose.

Follow the current user's tone and medium requirements over a source's brand voice. For a dry technical report, a company's enthusiastic announcement is not a voice sample. Required project templates and material interpretation conditions remain meaningful; optional boilerplate does not become required through skill composition.

A user should not have to learn a prescribed skill order to obtain one document. Changing another repository or its installed package requires the scope for that change; composing available skills does not itself migrate or install them.
