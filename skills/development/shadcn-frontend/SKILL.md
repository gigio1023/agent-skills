---
name: shadcn-frontend
description: >
  Use when building or reviewing shadcn/ui pages, components, or design-system
  linting. Combines official shadcn guidance with project-aware implementation
  and rendered checks. NOT for framework-independent document writing or
  choosing a dashboard's argument; use technical-report-writing or insight-dashboard.
---

# Shadcn Frontend

Build the requested interface using the project's shadcn components, with a coherent design system and working interactions. Preserve the existing framework, base library, component customizations, and package manager unless changing them is requested. A review returns findings rather than editing the project.

## Establish the implementation context

Read project instructions, `components.json`, package metadata, theme CSS, and the affected component source. Run `shadcn info --json` with the project's package runner from the actual application directory. In a monorepo, the repository root may not be the application. Do not assume Claude-style dynamic command injection ran in another harness.

Use the official `shadcn` skill when available. Otherwise read the maintained upstream entry and the references needed for the affected components through [official guidance](references/official-guidance.md). Before composing unfamiliar components, use `shadcn docs <component>` and read the returned documentation and examples. Preserve the detected Radix or Base UI APIs; do not guess `asChild` versus `render`.

Use `frontend-design`, when available, for design intensity and interface review. A requested bug fix preserves the visual language; a new page needs a deliberate reading order and dominant content. For a technical report page, `technical-report-writing` supplies the factual voice, argument, and measurement detail; `share-internal-doc` supports internal reader context and recipient suitability when available. For a quantitative dashboard, `insight-dashboard` owns the comparison and data behavior. These specialties do not change the underlying component APIs.

## Compose with the design system

Search installed components and configured registries before creating replacements. Use explicit registry names; propose the official `@shadcn` registry when the brief leaves the source open, and record that choice in project context rather than repeatedly asking. Preview updates with `--dry-run` and `--diff`; preserve local changes instead of overwriting them to match an example.

Use component variants for appearance, semantic theme tokens for colors, and layout utilities at the call site. Add a shared variant only when the actual design calls for it. Keep spacing, density, icons, and state treatment consistent. A component inventory is not a page composition: cards, sidebars, charts, and tabs belong only when the user's task needs them.

For a new, otherwise unconstrained static site, React + TypeScript + Vite + Tailwind v4 is a practical starting point. Reuse Next.js when the project already needs its server or routing behavior. Do not build an application merely to create a PDF; use `technical-report-writing` for document production instead.

## Enforce the chosen rules

Read [design-system linting](references/design-system-lint.md) when adding or changing `@shadcn/lint`. Plugin registration and rule activation are separate tasks. An installation-only request preserves existing policy; an authorized design-system setup defines useful rules and verifies that they detect a representative violation.

Fix reported violations through existing variants, theme tokens, or an intentional component change. Do not make the check green by removing requested behavior, globally exempting the UI directory, disabling rules, or inventing a token for every arbitrary value. Review new exceptions and variants in the diff.

## Verify the delivered interface

Use [interface checks](references/interface-checks.md) for the affected states. Run the project's build, type check, lint, and relevant tests. Inspect an actual render and exercise changed interactions, including keyboard operation and a relevant narrow viewport. Static lint does not inspect visual hierarchy, chart truthfulness, contrast, clipping, or runtime behavior.

For an offline HTML deliverable, build the application and verify the delivered file with network access disabled. For a hosted internal tool, preserve the intended access boundary; do not publish confidential data to obtain a convenient preview URL.

Return the working source and requested build or file, plus the checks actually run. Name a blocker only when it affects use. Deployment, global tool installation, and commits follow the user's requested scope.
