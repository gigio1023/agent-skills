---
name: frontend-design
description: Use when building, reshaping, or reviewing UI across React/Vue/Svelte, static HTML reports, dashboards, landing pages, prototypes, games, or visual tools. Helps choose context-aware art direction, typography, layout, motion, copy, assets, accessibility, and visual QA. Trigger for "make this UI beautiful", "frontend design", "design skill", "HTML report design", "polish the interface", "avoid AI slop", "make it distinctive", and UI-heavy implementation tasks.
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

1. Identify the surface: landing page, product app, data dashboard, HTML report, generated document, game, interactive demo, or component.
2. Name the real subject, audience, and one job of the screen. If the brief is vague, choose a concrete subject and state the assumption briefly.
3. Read `references/surface-patterns.md` and select the relevant surface guidance.
4. Form a compact design plan before coding:
   - Visual thesis: mood, material, energy.
   - Palette: 4-6 named colors with roles, not decorative color soup.
   - Type: display/body/utility roles; use existing fonts if the project already commits to them.
   - Layout: one dominant visual anchor and the information order.
   - Signature: one memorable element that belongs to this subject.
   - Restraint: what you will deliberately avoid.
5. Build using the existing framework, component library, and local conventions. If there is a design system, use its components and tokens first.
6. Critique the result against the brief and `references/quality-gate.md`. Use screenshots or browser verification when available.
7. Revise before final response if the design reads as generic, cluttered, inaccessible, or visually broken.

## Design Judgment

The goal is not "always flashy." The goal is appropriate and memorable. A sober finance dashboard, a Korean real-estate comparison report, a playful game, and a research memo in static HTML should not share the same visual language.

Spend boldness in one place. A strong interface usually has one signature move, not ten decorations. Examples: a precise data table with editorial typography, a hero that behaves like the product, a report whose section rhythm mirrors the argument, or a game UI whose controls feel native to the play world.

Use assets when the surface needs them. Product, venue, object, travel, portfolio, landing, and game work should have real imagery, generated imagery, video, canvas, SVG, or domain-native visual material. Static HTML reports can use charts, callouts, maps, tables, or diagrams as their visual substance.

## Anti-Slop Filters

Reject default AI design moves unless the brief specifically calls for them:

- Purple-blue gradient hero, floating glass cards, generic SaaS dashboard cards, soft orb backgrounds, and meaningless "01 / 02 / 03" markers.
- One-note palettes where every color is a tint of the same hue.
- Big-number hero plus small label plus random stat grid when the subject has richer material.
- Decorative motion scattered everywhere.
- Copy that describes the feature instead of helping the user act.
- Landing-page composition applied to tools, dashboards, reports, or internal ops screens.

## Implementation Rules

For existing apps, match the local stack and design system before inventing new primitives. Use semantic HTML and accessible components. Prefer CSS variables or existing tokens for new palettes. Keep responsive behavior explicit.

For plain HTML reports, treat the page like a designed document: readable measure, print-friendly sections if relevant, strong tables, captions, hierarchy, and restrained color. Avoid turning reports into marketing landing pages.

For games and interactive demos, use domain-appropriate engines or proven libraries for core rules/physics/parsing where available. Verify that the primary canvas or scene actually renders and responds.

## Output Behavior

Keep planning mostly internal unless the user asks to see it. In the final response, summarize the design direction and verification briefly. Mention any remaining visual risk, missing asset, or unverified viewport.
