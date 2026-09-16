---
name: shadcn-frontend
description: >
  Use when building or reviewing shadcn/ui pages, components, report interfaces,
  or design-system linting. Turns content into task-focused layouts with
  project-aware components, working states, and rendered checks. NOT for
  framework-independent writing or deciding a dashboard's analytical claim.
---

# Shadcn Frontend

Build a coherent, working interface using the project's shadcn components. Make the main content easy to read and the next action easy to perform. Preserve the framework, base library, theme, package manager, and component customizations unless the requested change includes them. A review returns findings; a build request returns working source and the requested artifact.

## Discover the real project

Read project instructions, `components.json`, package metadata, theme CSS, and affected components. Run `shadcn info --json` with the project's runner from the application directory; a monorepo root may not own the UI. Execute context discovery explicitly so the workflow works across harnesses.

Use the official `shadcn` skill when available, or its maintained entry and relevant references through [official guidance](references/official-guidance.md). Before composing an unfamiliar component, run `shadcn docs <component>` and read the returned documentation. Match the installed Radix or Base UI API, including `asChild` versus `render`, to the actual component implementation.

Search installed components and configured registries before adding replacements. Use explicit registry names; select the official `@shadcn` registry when an unconstrained brief needs a default. Preview additions and updates with `--dry-run` and `--diff`, then preserve intentional local changes.

## Turn content into an interface

1. **Choose the reading order before containers.** Identify the main answer, comparison, procedure, or form action. Give it the dominant content area. Place navigation and supporting context where they help that task.
2. **Choose components by behavior.** Use a semantic table for aligned exact values, tabs for genuine alternate views, disclosure for optional detail, and a dialog for a bounded interruption. Use a link for navigation and a button for an action. Choose a card when the content forms a useful unit, not as a wrapper for every paragraph.
3. **Compose through the existing design system.** Use variants for appearance, semantic theme tokens for color, and layout utilities at the call site. Add a shared variant when repeated design intent requires it. Keep labels, numeric alignment, spacing, status treatment, and interactive feedback consistent.
4. **Implement one truthful state transition.** Carry the selected state through the request, derived values, controls, title, and export. Reuse one calculation path for representations of the same result. Handle rapid changes so an older response cannot replace the newer selection.
5. **Preserve meaning at different sizes.** Keep reading text comfortable and exact comparisons legible. Reflow supporting regions; use a labeled horizontal-scroll region for a genuinely wide table. Keep important labels and units visible rather than shrinking the whole page.
6. **Make actions understandable and accessible.** Supply meaningful names, visible focus, keyboard paths, and local feedback. Restore focus after overlays. Pair status color with text or shape, and give charts an accessible explanation or data view.
7. **Finish the states the task exposes.** Design loading, empty, error, stale, success, and dense-data behavior where applicable. Preserve useful last-known data with its time and failure state. A zero-result search should offer a relevant recovery action.

Read [content to components](references/content-to-components.md) when building reports, comparisons, operational views, or explanatory interactions. Its public examples teach composition and testable behavior; the official component documentation remains the API authority.

Use `frontend-design` when available to select design intensity and review the visual result. A local bug fix preserves the visual language; a new page needs deliberate composition. `technical-report-writing` supplies technical explanation, `insight-dashboard` supplies the data comparison, and `share-internal-doc` supplies recipient context when relevant. Use each specialty within this task, without requiring a fixed multi-skill pipeline.

For an otherwise unconstrained new static web application, React + TypeScript + Vite + Tailwind v4 is a practical default. Preserve Next.js when the existing project needs it. A print-first PDF belongs to document-production tooling, not a mandatory React build.

## Make the rules an effective feedback loop

Read [design-system linting](references/design-system-lint.md) when adding or changing `@shadcn/lint`. Register the plugin and, when policy setup is authorized, enable the intended rules. Prove enforcement with a representative violation and a corrected version that uses the intended token or variant. Preserve installation-only scope when policy changes were not requested.

Correct diagnostics at their real source: variants, theme declarations, or deliberate primitive changes. Keep requested behavior intact, inspect new exceptions, and keep checks active on feature components. Preserve dependency release-age safeguards; use an eligible compatible version or report a blocked run.

## Verify the artifact the reader will use

Use [interface checks](references/interface-checks.md) to exercise the changed task. Run build, type check, lint, and relevant tests. Inspect a real render, keyboard interaction, and a relevant narrow viewport. Verify the relationship between the selected data and what the screen says; lint alone cannot establish it.

For offline HTML, open the built artifact with networking disabled and exercise its essential paths. For PDF, inspect the exported pages and replace interaction-only information with visible content. Preserve the intended access boundary of hosted tools; confidential data stays within authorized recipients.

Deliver working source and the requested build or file, plus the checks actually run and any blocker affecting use. Deployment, global installation, and commits follow the user's requested scope.
