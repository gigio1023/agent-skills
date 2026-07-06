# Quality Gate

Run this before finishing UI work. Fix issues you can fix within scope.

## Visual Direction

- The design has one sentence of visual thesis tied to the subject.
- The first viewport or primary surface has a real anchor, not generic decoration.
- Palette roles are clear: background, surface, text, border, accent, status.
- The accent is scarce enough to mean something.
- Typography roles are explicit and not all the same default family unless the project requires it.
- The signature element is doing useful work.
- Removing decorative shadows/backgrounds would not collapse the design.

## Context Fit

- Tool/app screens prioritize action, density, and repeat use.
- Reports prioritize reading order, evidence, tables, and print/share durability.
- Landing pages prioritize subject, promise, proof, and conversion.
- Games prioritize the play surface and feedback.
- Existing design systems and repo conventions were respected.

## Accessibility And Semantics

- Interactive elements are real buttons/links/inputs, not clickable divs.
- Icon-only buttons have labels.
- Images have meaningful `alt` or empty `alt` when decorative.
- Focus states are visible.
- Form controls have labels, names, correct types, and inline errors.
- Color is not the only carrier of meaning.
- Motion respects `prefers-reduced-motion`.
- Text contrast and target sizes are reasonable for the surface.

## Layout And Responsiveness

- Check desktop and mobile viewport behavior.
- Text does not overflow buttons, cards, table cells, tabs, or sidebars.
- Flex/grid children that contain text can shrink (`min-width: 0` or equivalent).
- Fixed-format surfaces have stable dimensions or aspect ratios.
- Safe areas, modals, drawers, and full-bleed sections do not create accidental horizontal scroll.
- Empty, loading, error, and long-content states do not break the layout.

## Motion And Interaction

- Animation has one clear purpose: orientation, feedback, delight, or atmosphere.
- Avoid `transition: all`; animate transform and opacity where possible.
- Hover, active, disabled, loading, selected, and focus states are covered for primary controls.
- Destructive actions have confirmation or undo.
- URL reflects meaningful UI state when the surface is navigational or shareable.

## Copy

- UI text names user-recognizable actions, not implementation details.
- Buttons say the action: "Save Changes", "Publish", "Download PDF".
- Empty states point to the next action.
- Errors say what happened and how to fix it.
- No visible text explains the design itself.

## Verification

When tooling is available:
- Use browser screenshots for visually significant work.
- Inspect both desktop and mobile.
- For canvas/3D/game work, verify nonblank pixels and basic interaction.
- Run available lint/build/tests if the project has them.
- Report what was not verified.

