# Interface Checks

Choose checks for the changed reader task and the actual supported targets. Use the project's existing commands and test infrastructure.

## Package and design system

Build, type check, lint, and run relevant tests in the application package. Confirm lint includes intended UI files and loads the correct theme. When adding policy, exercise an intentional violation and its correction. Review primitive changes, variants, and narrow exceptions with the requested behavior still intact.

## Reading and layout

Inspect the initial view at a relevant laptop and narrow viewport. Confirm the main answer, comparison, or action has a clear reading position. Try long names, dense rows, large and negative values, and sparse data where relevant. Preserve meaningful units, readable labels, and numeric alignment. Use reflow or a deliberate scroll region instead of compressing the entire view.

## Behavior and accessibility

Exercise the changed task with pointer and keyboard input. Check visible focus, meaningful control names, native link/button behavior, overlay focus return, and semantic headings/tables. Use automated accessibility checks when available and inspect interactions manually. Give charts a usable accessible explanation or data view, and pair color-based status with text or shape.

Exercise relevant loading, empty, error, stale, and success states rather than only checking their JSX branches. Verify that a recovery action works and that background updates preserve useful context. Respect reduced-motion preferences for meaningful animations.

## Data and selection

Independently calculate a representative displayed value. Check the same population and definition across rows, cards, chart, title, and export. Change to a selection that alters the finding, then try a missing or zero-denominator case. Reload URL state, navigate back, reset, and test rapid changes with delayed responses. Confirm an older response cannot replace the newest selection.

## Actual delivery

For offline HTML, open the built file with networking disabled and check essential scripts, fonts, images, navigation, and data. For print, inspect the actual PDF: visible selected comparisons, readable labels, complete text, useful citations, and sound page boundaries. For a hosted internal tool, verify the intended access boundary rather than using an unrestricted preview to bypass it.

Report the checks actually exercised and failures that affect use. Build and static lint are useful evidence; they do not establish complete accessibility, analytical validity, or visual clarity.
