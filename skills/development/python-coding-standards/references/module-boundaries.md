# Module Boundaries

Read this for a large-file decision, module extraction, package reorganization, or a public-import change. The desired result is a responsibility that can be changed and tested locally, with fewer dependencies to understand.

## Find a boundary worth keeping

A split is useful when two parts have different reasons to change, different dependencies, distinct resource lifecycles, or an interface that callers can use without knowing the implementation. Describe what the proposed module owns and which details it hides. If that description is just "the first half" or "all helpers," the boundary needs more work.

Keep orchestration small by letting it compose behavior owned elsewhere. Keep a feature's closely related models, operations, and tests discoverable together; use the repository's existing package organization rather than introducing layers or a `src/` migration as a side effect. Extract a shared module only when the shared meaning is stable. Similar-looking code may have different reasons to change.

Avoid catch-all `utils.py`, `common.py`, or project-wide `models.py` files that accumulate unrelated responsibilities. These names are review signals, not reasons to rename a cohesive existing module. Conversely, a file per class can scatter one responsibility across many imports without improving it.

The size reminders in the main skill apply to in-scope handwritten first-party code. Review the actual responsibility and dependency graph before deciding to split; a cohesive parser, declarative schema, or test matrix can legitimately be large. Put any split-or-retain rationale in the existing change summary, not a boilerplate comment or a new architecture document.

## Preserve behavior while extracting

When code moves across modules, these operations have a useful order:

1. Identify callers and the public surface: documented imports, package re-exports, entry points, type stubs, serialization names, and tests. Record the behavior to preserve using existing tests or focused characterization tests where coverage is missing.
2. Move the smallest cohesive responsibility and update its internal consumers. Keep an existing public import working through an intentional re-export or compatibility facade unless the user requested its removal.
3. Check affected imports and configured dependency rules, then run focused tests and the repository's applicable static checks. Broaden checks when the moved code is shared, imported for side effects, or otherwise affects a wider surface.

`__all__` controls star imports; it is not an access-control mechanism or a requirement for every module. Follow the repository's public-export conventions. Keep `__init__.py` imports intentional so that a compatibility facade does not introduce expensive initialization, cycles, or hidden registration effects.

Preserve the runtime dependency direction. Do not introduce a new runtime import cycle to complete an extraction. Type-only imports can use `TYPE_CHECKING` when runtime introspection does not need them; do not use it to hide a real dependency or break Pydantic's annotation resolution. Lazy imports can be intentional for optional dependencies or startup cost, but they need a reason beyond masking a bad boundary.

If the proposed split adds forwarding layers, forces tests to mock more internals, or makes routine changes touch more files, retain or revise the boundary. A file-length target does not justify that cost.

## Project checks and sources

Use existing import-linter or architecture checks when configured; do not add a new checker merely because this skill mentions one. For Ruff C901, use the project's configured complexity threshold when enabled. Complexity and line counts identify code to inspect, not an automatic refactoring recipe.

Sources checked 2026-09-10:

- [Python modules](https://docs.python.org/3/tutorial/modules.html): packages, imports, and `__all__` semantics.
- [PEP 8](https://peps.python.org/pep-0008/): project guidance and compatibility take precedence over stylistic uniformity.
- [Ruff C901](https://docs.astral.sh/ruff/rules/complex-structure/): function complexity rather than module architecture.
- [Pylint too-many-lines](https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/too-many-lines.html): file length as a readability signal.

The 500-line review and 1,000-line split-or-rationale reminders are local preferences, not thresholds established by Python, Ruff, Pylint, or an architectural standard. No external modularity skill is required or bundled.
