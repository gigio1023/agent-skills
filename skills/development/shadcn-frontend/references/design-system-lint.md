# Design-System Linting

Use when setting up or changing `@shadcn/lint`. This is a source-code linter for Tailwind v4 design systems; shadcn/ui is not required. The inspected package is 0.1.0 at [53de86f0e7dcc341a9cb45c383a9f2c454d1e958](https://github.com/shadcn-ui/lint/tree/53de86f0e7dcc341a9cb45c383a9f2c454d1e958), checked 2026-09-15. Consult the current [README](https://github.com/shadcn-ui/lint) and [setup instructions](https://github.com/shadcn-ui/lint/blob/main/SETUP.md) before changing a project's dependencies.

## Register, then select policy

The inspected prerequisites are Node.js >=20.19, ESLint >=9.30 or Oxlint >=1.80, and Tailwind v4. The Oxlint JS plugin API is described as alpha. Keep the existing linter and framework parser. If neither linter exists, the official setup selects Oxlint. Resolve monorepo component aliases and each app's theme rather than overwriting them with one workspace-wide guess.

`SETUP.md` deliberately registers the plugin without enabling new rules. A successful setup check proves registration, not enforcement. For an authorized new design-system setup, choose the rule policy below and make the project's lint command run it. For an existing codebase, follow [adoption guidance](https://github.com/shadcn-ui/lint/blob/53de86f0e7dcc341a9cb45c383a9f2c454d1e958/docs/adoption.md): establish current findings, fix recurring problems, and increase strictness without making unrelated legacy work part of the requested change.

## Rules and intended use

| Rule | Purpose | Initial choice for a new controlled UI |
| --- | --- | --- |
| `shadcn/no-restyle` | Component call sites cannot bypass allowed appearance | Error; allow layout, use component-specific contracts for intentional flexibility |
| `shadcn/no-raw-colors` | Palette colors, undeclared theme tokens, literal SVG colors | Error; define semantic and chart tokens in the actual theme |
| `shadcn/no-arbitrary-values` | Arbitrary Tailwind values | Error; allow necessary layout values intentionally |
| `shadcn/no-inline-styles` | Ordinary inline styling, raw custom-property colors, style elements | Error; carry runtime values through CSS custom properties where appropriate |
| `shadcn/require-static-classes` | Class values the analysis cannot read | Error on controlled component call sites |
| `shadcn/no-unknown-classes` | Classes the installed Tailwind cannot generate | Begin at warn while checking external styles and theme loading, then tighten |

These are local adoption defaults, not an upstream preset. The [rule reference](https://github.com/shadcn-ui/lint/blob/53de86f0e7dcc341a9cb45c383a9f2c454d1e958/docs/rules.md) owns syntax and option semantics.

Inside the actual primitive component directory, disable `no-restyle`, `no-arbitrary-values`, and `require-static-classes` as needed for component implementation. Keep `no-raw-colors` and `no-inline-styles` enabled. Do not disable the whole plugin there. A feature component is not automatically a primitive merely because placing it in that directory avoids errors.

A rule's `contracts` match component names; anchor exact names such as `^Button$`. The last matching contract applies. It inherits top-level keys it does not write, not preceding contracts. An exception in one rule does not exempt another rule.

## Respect dependency safeguards

A published version can still be excluded by the package manager's minimum release-age policy. When an exact-version install reports no matching version before a cutoff date, check registry publication metadata and the relevant policy setting. Preserve the guard; use an eligible version if one supports the required API, or report the blocked execution. Do not silently override the cutoff or describe the package as nonexistent.

## Data visualization and runtime styling

A data-driven width is not the same design decision as a one-off decorative color. The inspected inline-style rule permits dynamic CSS custom properties, for example a numeric width carried in `--panel-width` and consumed by a Tailwind class. Declared color variables pass; hardcoded colors in custom properties are checked. Animation-library properties can have narrow, documented exceptions.

Chart libraries may generate style attributes and SVG internally. This linter analyzes authored source, not the rendered DOM; determine which authored files and properties are actually reported. Inspect the delivered chart separately. Do not globally allow all inline styles or disable color checking to make a chart pass.

## Prove the feedback loop

After activating policy, use a disposable fixture importing a real project component. Confirm an intentional violation produces the expected rule diagnostic, then replace it with the intended variant/token and confirm that diagnostic disappears. Remove or isolate the fixture from production. Check that relevant source files are included and that imports/theme discovery succeeded.

Run the ordinary project checks and inspect the rendered result after correction. New variants, exceptions, and primitive edits need diff review: a zero count alone cannot show that the intended design survived.

Upstream [evals](https://github.com/shadcn-ui/lint/blob/53de86f0e7dcc341a9cb45c383a9f2c454d1e958/docs/evals.md) report fewer violations and lower correction costs in their trials. Those measurements motivate diagnostic feedback; they do not establish performance for a new project or judge the clarity of its writing.
