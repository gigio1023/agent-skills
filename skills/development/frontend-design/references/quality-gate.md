# Quality Gate

Use this for Adapt, Direct, and Review work. Preserve uses the inline fast path in `SKILL.md`. Apply the common gate, then only the risk sections the changed or reviewed surface triggers.

## Contents

- [Common Gate](#common-gate)
- [Accessibility Depth](#accessibility-depth)
- [Forms And Transactions](#forms-and-transactions)
- [Data And Generated Output](#data-and-generated-output)
- [Responsive And International Content](#responsive-and-international-content)
- [Motion And Interaction](#motion-and-interaction)
- [Performance And Platform Support](#performance-and-platform-support)
- [Copy And Trust](#copy-and-trust)

## Common Gate

- The result serves the screen's stated user job and has a readable hierarchy after decorative effects are removed.
- Components, tokens, spacing, density, and interaction behavior fit the current product contract or an authorized new direction.
- An actual render was inspected at the relevant viewport when a runnable path exists. No code-only inference is reported as visual proof.
- The changed interaction works with keyboard input and exposes a visible focus state, meaningful name, role, and current state.
- Text, controls, tables, and media survive realistic content without clipping, accidental horizontal scroll, or hidden actions.
- Modified controls cover the relevant hover, active, selected, disabled, pending, success, and failure states.
- Missing assets, untested states, and unavailable viewports remain visible in the final report.

## Accessibility Depth

Existing legal, contractual, or project accessibility requirements override the defaults below.

- **Preserve:** do not introduce a regression in the changed path.
- **Adapt:** maintain the project's declared bar. Verify semantics, keyboard operation, focus, labels, errors, and state announcements affected by the change.
- **Direct prototype or one-off demo:** provide semantic structure, keyboard operation, visible focus, accessible names, and a contrast check. Report that WCAG conformance was not fully audited when it was not.
- **Production surface or explicit compliance request:** apply the relevant WCAG 2.2 AA criteria to the affected surface, including contrast, target size where applicable, input purpose, errors, focus visibility, and name, role, and value.

Use native HTML before ARIA. When a composite widget needs ARIA, follow its full keyboard and state pattern rather than adding roles alone. A targeted check does not establish site-wide conformance.

## Forms And Transactions

- Labels and help remain associated with their controls. Required format and constraints appear before submission when users can act on them.
- Errors identify the field, explain the correction, preserve entered data, and remain discoverable by assistive technology.
- Submitting, success, failure, retry, and duplicate-submission behavior are explicit. Consequential actions provide confirmation, review, or recovery.
- Multi-step work communicates progress and preserves a viable back, correction, and resume path when the product supports one.

## Data And Generated Output

- Loading, empty, partial, stale, failed, and long-content states keep the layout and primary action usable.
- Numbers include units, timeframe, comparison basis, and uncertainty when the source provides them. Missing data is distinct from zero.
- Tables and charts support long labels, large values, keyboard or textual access where relevant, and meaning that does not depend on color alone.
- Generated output distinguishes user content, system status, sources, and model output. Retry, stop, edit, copy, cite, or discard actions reflect real product capability.

## Responsive And International Content

- Check the project's supported minimum width and at least one wider viewport. Include touch behavior when the surface targets touch devices.
- Zoom, text enlargement, safe areas, overlays, sticky regions, and virtual keyboards do not hide the active control or primary action.
- Long translations, CJK line breaking, right-to-left layout, and localized date, time, number, and plural formats are checked when the product supports them.
- The document language is declared and mixed-language content remains legible with the available font set.

## Motion And Interaction

- Motion communicates orientation, feedback, progression, or atmosphere tied to the product. It does not conceal latency or replace state text.
- Nonessential motion respects reduced-motion preferences. Long, looping, or auto-playing movement can be paused or stopped when required.
- Animations avoid unexpected layout shifts and preserve input continuity.
- Meaningful navigation and shareable state use stable URLs when the product contract calls for them.

## Performance And Platform Support

- Fonts, images, video, and generated media have loading and fallback behavior that avoids invisible content and large unexpected shifts.
- The change does not add unnecessary client work to a static or server-rendered surface. Expensive interactions are measured with an appropriate local tool when performance is material.
- New CSS and browser APIs fit the project's support policy. Check Web Platform Baseline or explicit target browsers when support is uncertain.
- Local screenshots and lab tools do not prove field Core Web Vitals. Report field metrics only from a real field-data source.

## Copy And Trust

- Controls name a recognizable action. Empty states identify a useful next step and errors say what happened and how to recover.
- Visible content does not explain or praise the design itself.
- Metrics, testimonials, citations, confidence, and status claims come from real product data or remain clearly marked as placeholders.
- Destructive and irreversible outcomes are stated before commitment and provide confirmation or recovery appropriate to their risk.
