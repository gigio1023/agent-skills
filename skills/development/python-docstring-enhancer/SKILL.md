---
name: python-docstring-enhancer
description: >
  Use when adding, correcting, or reviewing Python docstrings and explanatory
  code comments, especially for public APIs, non-obvious invariants, side
  effects, fallbacks, ordering, and complex control flow. Trigger for
  "docstring 추가", "주석 보강", "Python 주석 달아줘", and "문서화해줘" when
  the target is Python source. NOT for general Markdown documentation,
  behavior-changing refactors, or comments that merely restate code.
---

# Python Docstring Enhancer

Document the behavior a reader cannot reliably infer from names, types, and
code structure. Preserve runtime behavior and the repository's existing
docstring convention.

## Quick Start

1. Read repository instructions, the target Python, neighboring documented
   code, and docstring/lint configuration such as `pyproject.toml`.
2. Identify public surfaces and non-obvious behavior in the requested scope.
3. Add the smallest docstrings or comments that explain the contract, rationale,
   invariant, side effect, or failure behavior.
4. Do not change executable code, signatures, annotations, or formatting beyond
   what the documentation edit requires unless the user requested a refactor.
5. Parse the changed files and run the repository's focused documentation,
   lint, type, or test checks when available.

## What Deserves Documentation

Prioritize:

- public modules, classes, functions, methods, protocols, and callbacks;
- parameters whose meaning, units, accepted forms, or sentinel values are not
  obvious from the type;
- return/yield semantics, ordering, ownership, mutability, and empty behavior;
- intentional exceptions, side effects, I/O, caching, concurrency, and retry or
  fallback behavior;
- invariants and constraints enforced outside the visible block;
- surprising compatibility or performance choices.

Usually leave these alone:

- trivial private helpers whose name and type fully describe behavior;
- assignments, loops, and conditionals that the code already states clearly;
- type information already expressed by annotations, unless the repository's
  docstring format requires it;
- speculative rationale not supported by code, tests, issues, or user context.

## Docstring Contract

Follow the local Google, NumPy, Sphinx, or project-specific style. Do not convert
an entire module to a new format during a targeted documentation request.

A useful docstring contains only applicable fields:

1. one-line purpose or contract;
2. necessary context or invariants;
3. parameter semantics not carried by names and types;
4. return or yield semantics, including units and sentinel/empty behavior;
5. exceptions deliberately exposed to callers;
6. observable side effects or lifecycle requirements;
7. a short example when usage is otherwise ambiguous.

For a data model, describe the model's role once. Put field-specific text in
the mechanism used by that project, such as dataclass metadata, Pydantic
`Field(description=...)`, or the class docstring; avoid maintaining the same
field definition twice.

## Inline Comment Contract

A comment should answer one of these questions:

- Why is this branch or order required?
- What invariant is preserved?
- Why is the obvious alternative unsafe or incorrect?
- What external constraint or compatibility behavior applies?
- What outcome does a fallback distinguish?

Place the comment immediately above the smallest relevant block. Avoid a
comment on every condition, numbered `Step N` labels for ordinary flow, and
banner comments around metrics or observability code unless the repository
already uses that convention.

For a long function with stable phases, a few semantic headings can help
navigation. If phase labels merely narrate sequential code or are likely to
drift, omit them. Do not refactor the function unless the user requested it.

See [EXAMPLES.md](EXAMPLES.md) for focused patterns.

## Scope and Grounding

- Use the requested language or the language already used in nearby docstrings.
- Preserve domain terms and exact API identifiers.
- Derive claims from implementation, tests, schemas, and project documentation.
  Mark unresolved intent instead of inventing "why".
- In review-only mode, report findings without editing.
- In edit mode, touch only the requested source files and closely coupled
  documentation metadata.

## Verification

At minimum:

- parse or compile changed Python files;
- run configured docstring/lint checks that cover them;
- run focused tests when a docstring describes behavior that tests can confirm;
- inspect the diff to ensure only strings/comments changed unless broader edits
  were authorized;
- re-read each comment against the final code so names, order, and exception
  behavior still match.

Report commands actually run and skipped checks. A successful parse does not
prove behavioral claims.

## Output

Lead with the documented files or review findings. For edits, report:

- public contracts and non-obvious behaviors clarified;
- checks run and results;
- any intent that could not be established;
- whether executable code changed (normally: no).

## Gotchas

- More comments can make code harder to maintain; documentation volume is not a
  quality metric.
- "Why" comments are harmful when the rationale is guessed.
- Listing every possible lower-level exception creates a false API guarantee;
  document exceptions intentionally exposed to callers.
- Examples in docstrings can become executable documentation. Keep them small,
  deterministic, and compatible with the repository's doctest policy.
- Generated files, vendored code, and third-party stubs should not be edited
  without explicit scope.
