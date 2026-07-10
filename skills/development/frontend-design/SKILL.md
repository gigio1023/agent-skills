---
name: frontend-design
description: >
  Use when building, reshaping, or reviewing UI whose success depends on visual
  hierarchy, interaction feel, presentation quality, or a deliberate art
  direction. Applies across web frameworks, static HTML reports, dashboards,
  landing pages, prototypes, games, and visual tools. Trigger for "make this UI
  beautiful", "polish the interface", "make it distinctive", and UI-heavy
  implementation. NOT for logic-only frontend changes or pixel-preserving
  maintenance where the existing design must remain unchanged.
---

# Frontend Design

Use this skill when the task's success depends on visual judgment, interaction feel, hierarchy, or presentation quality, not just whether the code compiles.

This is the design judgment layer. Do not split by framework by default. React, Vue, Svelte, Tailwind, CSS Modules, plain HTML, SVG, Canvas, and static reports all need the same upstream decisions: subject, audience, surface, hierarchy, typography, palette, motion, assets, and verification. Let the repo's existing stack determine implementation details.

## Architecture

Use one general skill plus focused references:

| File | Read when |
|---|---|
| `references/surface-patterns.md` | Before creating or substantially redesigning UI. Pick the relevant surface: app, dashboard, landing, report, game, doc, tool. |
| `references/quality-gate.md` | Before finalizing any UI work or review. Use it for screenshots, accessibility, responsive behavior, and anti-slop checks. |
| `references/source-notes.md` | Only when maintaining this skill or explaining why it is structured this way. |

Create framework-specific child skills only after repeated evidence shows a framework-specific failure that cannot be handled by normal codebase conventions, such as a company design system API, a motion library's footguns, or a platform-specific visual QA script.

## Core Loop

1. Classify the request before acting:
   - **Review/report:** inspect and report findings. Do not edit files or broaden
     the review into a redesign unless the user asks.
   - **Build/change:** implement the requested UI change within its stated scope.
2. Identify the surface: landing page, product app, data dashboard, HTML report,
   generated document, game, interactive demo, or component.
3. Name the real subject, audience, and one job of the screen. If the brief is
   vague, choose a concrete subject and state the assumption briefly.
4. Read `references/surface-patterns.md` and select the relevant surface guidance.
5. Record only the decisions needed for the current mode: reading order and
   dominant anchor, existing design-system constraints, required states and
   viewports, and at most one subject-specific signature.
6. In build/change mode, use the existing framework, component library, and local
   conventions. If there is a design system, use its components and tokens first.
7. Inspect the relevant desktop/mobile viewports and interaction states against
   `references/quality-gate.md`. Run available build, lint, and accessibility
   checks when relevant. In review mode these checks produce findings, not edits.
8. In build/change mode, revise if the rendered result is generic, cluttered,
   inaccessible, broken, or inconsistent with the brief. If rendering is not
   possible, say what remains unverified instead of inferring success from code.

## Design Judgment

The goal is not "always flashy." The goal is appropriate and memorable. A sober finance dashboard, a Korean real-estate comparison report, a playful game, and a research memo in static HTML should not share the same visual language.

Spend boldness in one place. A strong interface usually has one signature move, not ten decorations. Examples: a precise data table with editorial typography, a hero that behaves like the product, a report whose section rhythm mirrors the argument, or a game UI whose controls feel native to the play world.

Use assets when the surface needs them. Product, venue, object, travel, portfolio, landing, and game work should have real imagery, generated imagery, video, canvas, SVG, or domain-native visual material. Static HTML reports can use charts, callouts, maps, tables, or diagrams as their visual substance.

## Defaultness Check

Do not turn familiar motifs into a blacklist. A gradient, glass surface, card, or
large metric is valid when the subject and product system call for it. Reject the
result when the choices are interchangeable with an unrelated product:

- Does the composition match this surface's job rather than a generic landing page?
- Does the visual anchor come from the subject, data, product, or user task?
- Do color, type, motion, and copy carry meaning instead of filling space?
- Would removing decorative effects leave a clear hierarchy and usable controls?

## Implementation Rules

For existing apps, match the local stack and design system before inventing new primitives. Use semantic HTML and accessible components. Prefer CSS variables or existing tokens for new palettes. Keep responsive behavior explicit.

For plain HTML reports, treat the page like a designed document: readable measure, print-friendly sections if relevant, strong tables, captions, hierarchy, and restrained color. Avoid turning reports into marketing landing pages.

For games and interactive demos, use domain-appropriate engines or proven libraries for core rules/physics/parsing where available. Verify that the primary canvas or scene actually renders and responds.

## Output Behavior

Keep planning internal unless the user asks for it. For a review, lead with the
most consequential findings and say that no files were changed. For a build or
change, lead with the implemented outcome. Then name only the viewports, states,
and checks actually verified. Mention any remaining visual risk, missing asset,
or unverified viewport; do not substitute a design rationale for render evidence.

## Gotchas

- Stronger art direction does not authorize extra product features, new design
  systems, or decorative UI outside the request.
- A passing build is not visual proof. Inspect the rendered states and viewports
  that could change the user's experience.
- Do not replace an established product language with a portfolio-style redesign
  merely to make the result look more distinctive.
