---
name: python-coding-standards
description: >
  Use when writing, refactoring, or reviewing Python application or library
  code, defining data models, splitting a large Python module, or setting up
  a Python project. Prefers straightforward Pydantic models, explicit Python
  3.12+ annotations including locals, uv project management, and explanations
  close to code. Uses the official external pydantic skill for library guidance.
  NOT for docstring-only edits,
  a standalone formatting command, generated code unless explicitly in scope,
  or starting a plan or audit merely because Python files exist;
  gigio-review-results owns comparison of finished work against project intent.
---

# Python Coding Standards

Produce straightforward, organized Python code that is easy to follow and maintain. The aim is not clever or impressive architecture: prefer direct control flow, ordinary names, and the fewest responsibilities and abstractions needed for the task. For review or diagnosis, return findings and their consequences without implementing them. A change request includes its relevant local checks; it does not imply a repository-wide migration, cleanup, or publication.

## Start from the repository

Read the applicable project instructions, Python support range, dependency constraints, nearby implementation and tests, and configured checks before choosing syntax or tools. Existing public imports, accepted inputs, serialized values, and persisted data remain compatible unless the requested change includes a migration. An instruction to adopt a new style does not by itself authorize breaking those interfaces.

The user's current request takes precedence, then explicit repository constraints. Apply this skill's defaults to new and changed code; existing mixed style alone is not an exemption. Use Python 3.12 or later for new projects, select a supported version compatible with deployment and dependencies, and record the support range in `pyproject.toml`. If an existing project requires older Python or incompatible tooling, identify the conflict instead of silently breaking support or migrating unrelated code. Preserve configured formatters, linters, type checkers, and test runners unless their change is in scope.

## Manage the project with uv

Prefer uv's project workflow for Python setup and dependency changes: `pyproject.toml`, `uv.lock`, `uv add`, `uv sync`, and `uv run`. Do not use `pip install` or `uv pip install` as routine setup, a convenience shortcut, or a retry after resolution fails. An exceptional environment restriction needs a concrete reason and a reproducible dependency record. Read [project environment](references/project-environment.md) when setting up Python, changing dependencies, or arranging test and lint groups. Keep runtime dependencies and development groups distinct; adding this skill does not itself authorize project migration or global tool installation.

## Types and data boundaries

Type annotations are required for functions and methods, return values, model fields, attributes, module-level values, and local variable declarations, even when the assigned value makes the type inferable. Use Python 3.12-compatible forms such as `dict[str, int]`, `list[Item]`, and `Item | None`, not legacy `typing.Dict` or `typing.List`. Include precise SDK client, request, response, stream, and result types rather than omitting them because an external library is complex. Read [types and enums](references/types-and-enums.md) for binding syntax, SDK types, and narrow exceptions. Do not use `Any`, a cast, or a suppression merely to make an annotation present.

Use Pydantic `BaseModel` as the default for application-owned structured data, including internal models, configuration, inputs, and results. Do not choose `TypedDict`, dataclasses, or dictionaries as competing record representations unless a concrete interface, behavior, or measured constraint makes them necessary. Reuse one model when the meaning is unchanged instead of adding parallel dictionary, dataclass, and model layers. Services and resource owners can remain ordinary classes; scalar values and real key-value mappings do not need artificial model wrappers. Explain necessary exceptions near the code.

For Pydantic-specific work, load the official external `pydantic` skill as described in [Pydantic integration](references/pydantic-integration.md). That reference also records this pack's choices about input retention, enum representation, and compatibility. It is not a second Pydantic API guide.

Use standard-library `enum.StrEnum` for a closed string vocabulary that needs named runtime members. Assign explicit values for API, database, event, configuration, and other persisted or transmitted tokens. Member names may change independently of those values; `auto()` must not make a public value depend on a Python identifier. Keep provider-extensible strings open unless a versioned schema actually defines a closed set. The types reference covers compatibility with older runtimes and third-party `strenum`.

## Modules that remain easy to change

Keep related behavior with the module that owns its meaning. A useful split separates responsibilities, dependencies, or lifecycles and leaves a small interface between them. A class, helper, or extra layer should earn its place through state, an independent responsibility, or a useful boundary; neither one class per file nor one global `models.py` is a default architecture.

For a growing module, inspect the affected responsibilities before adding another one. As a local fallback, 500 handwritten first-party lines prompts a decomposition review; at 1,000, split at a meaningful boundary or explain why the module should stay together in the change summary. Repository limits win. These are review reminders, not automatic split rules, and they do not authorize unrelated restructuring. Generated files, vendored code, migrations, declarative tables, and cohesive test matrices need contextual review rather than automatic extraction.

Read [module boundaries](references/module-boundaries.md) before moving code between modules, changing public imports, or deciding how to split an oversized file. Preserve import direction and externally visible behavior; avoid a new runtime import cycle. A shorter file is not a successful refactor if understanding it requires more cross-file navigation.

## Explain what the code cannot show

Treat code as the source of truth for implementation. When names, annotations, and structure do not explain enough, add intent and background at the relevant file, class, model, function, or code block. Use module and symbol docstrings for responsibilities and non-obvious behavior, and nearby comments for reasons, constraints, or tradeoffs. Explain why an order, representation, or exception is necessary; do not narrate obvious statements or invent historical intent.

Keep implementation explanations in code, docstrings, and comments. Separate policy documents may state decisions independent of implementation. Use `docs/` for information code alone cannot convey or a useful explanation that must bring several files together; do not generate parallel per-file walkthroughs, model catalogs, or change reports that need continual synchronization. Update an existing document when the change affects it, but prefer links to authoritative symbols over copied code or schemas. Read the documentation section of [correctness and testing](references/correctness-and-testing.md) when adding explanations.

## Correctness and verification

Keep error translation at a boundary where callers can act on it. Make resource ownership and async cancellation explicit. Read [correctness and testing](references/correctness-and-testing.md) when changing error handling, I/O, concurrency, or verification strategy.

Run the repository's checks relevant to the changed behavior, through `uv run` in uv-managed projects. Public imports, accepted and rejected inputs, serialized fields and enum values, error behavior, and cleanup paths deserve focused compatibility tests when they change. Review annotation completeness as well as type correctness: a checker may infer an unannotated local without reporting it. Reuse tests that already establish the behavior; do not add tests that merely mirror helpers or satisfy a coverage quota. A formatter result cannot establish runtime correctness, and a type checker cannot establish external-data validation.

Finish when the requested result is implemented or reviewed and the relevant checks have run, or their exact limitation is reported. State the behavior changed, material compatibility or module decisions, checks and results, and anything not verified. Avoid inventing a plan file or a standard report template for ordinary Python work. Continue an already-requested publication through `draft-pr`, or an already-requested commit and push through `commit-and-push`.
