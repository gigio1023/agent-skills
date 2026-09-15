# Composition with Document and Interface Skills

Use when an existing workflow also needs technical prose, internal sharing, a dashboard, or a shadcn implementation. Compose only the specialties needed for the requested artifact; do not restart intake or recursively invoke a full document workflow at every link.

## Responsibilities

| Skill | Contribution |
| --- | --- |
| `technical-report-writing` | Dry technical voice, factual statements, mechanisms, measurements, decisions, document form, and authoring/export choices |
| `share-internal-doc` | Standalone reader context, internal-recipient suitability, source access, and the authorized sharing workflow |
| `insight-dashboard` | Quantitative comparison, informative initial view, data/filter/claim alignment, and static presentation of selected results |
| `shadcn-frontend` | Project-specific shadcn components, theme/variant rules, design-system lint, and actual interface behavior |
| `frontend-design` | Design intensity, composition, and visual/interaction review for a user-visible change |
| `slop-aware-writing` / `korean-clarity` | Focused prose revision and Korean semantic completeness when their concerns apply |

`share-internal-doc` is maintained separately in [Gigio Pack](https://github.com/gigio1023/gigio-pack/tree/main/skills/share-internal-doc). Keep its package name and source ownership there. This pack supplies the technical-writing craft it can use; it does not ship a second copy or depend on unpublished edits in that repository. Read the available companion at runtime when the task calls for it. Missing optional companions do not remove the core source, accuracy, and recipient checks.

## Useful combinations

- **Internal technical report:** keep `share-internal-doc` as the end-to-end sharing workflow when it is already active; apply the voice/facts, appropriate form, and examples from this skill to the document being written. Return to that workflow's recipient and delivery checks.
- **Standalone technical report or project document:** use this skill directly. Add specialized document or figure tooling only as the medium requires.
- **Data dashboard:** use this skill's measurement and prose guidance with `insight-dashboard`. Use `shadcn-frontend` only for an actual shadcn implementation. A result statement should describe the active data, not advertise the interface.
- **Print-first PDF:** choose a native production route here. Do not load frontend skills or build a web application solely because the document contains tables or charts.
- **Generic shadcn form or product UI:** use `shadcn-frontend` and the relevant frontend design guidance. A technical-report workflow is unnecessary unless the page is itself a report.

Follow the current user's tone and medium requirements over a source's brand voice. For a dry technical report, a company's enthusiastic announcement is not a voice sample. Required project templates and material interpretation conditions remain meaningful; optional boilerplate does not become required through skill composition.

If maintaining an external document-workflow skill, link to this capability for technical writing and document production rather than copying the reference catalog. Changing that other repository or its installed package requires the scope for that change; consuming this package does not itself migrate or install anything.
