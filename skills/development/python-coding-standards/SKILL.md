---
name: python-coding-standards
description: >
  Use when writing, refactoring, structuring, or reviewing Python code or a
  Python project: choosing the project shape and package layout, splitting
  functions and modules, defining data models, adding or auditing docstrings
  and comments ("docstring 추가", "주석 보강", "문서화해줘" on Python source),
  or setting up dependencies and checks. Carries this pack's defaults: named
  responsibilities, the smallest architecture that fits, Pydantic
  models, explicit annotations including locals, and uv. NOT for a standalone
  formatting command, generated code unless explicitly in scope, non-Python
  documentation, or starting a plan or audit merely because Python files
  exist; gigio-review-results owns comparison of finished work against project
  intent.
---

# Python Coding Standards

Produce Python a colleague can follow: named pieces with clear intent, the smallest project shape that fits, direct control flow, ordinary names, and an explanation wherever code cannot show the reason. Review or diagnosis returns findings without implementing them. A change request includes its relevant local checks and nothing more: no repository-wide migration, cleanup, restructuring, or publication, and a pre-existing problem met on the way is a follow-up in the summary, not a change.

## Start from the repository

Read the project instructions, Python support range, dependency constraints, nearby implementation and tests, and configured checks before choosing syntax, layout, or tools. Existing public imports, accepted inputs, serialized values, and persisted data stay compatible unless the request includes a migration. The current request takes precedence, then explicit repository constraints, then this skill's defaults, which apply to new and changed code; mixed existing style is not an exemption. Preserve configured formatters, linters, type checkers, and test runners unless their change is in scope, and report a conflict with older Python or incompatible tooling instead of breaking support.

## Name the responsibilities

Give each function a caller-visible responsibility and make data flow and side effects clear. When a new module or multi-phase task has unclear boundaries, a skeleton of annotated signatures and short contract docstrings can expose them before implementation. Use it when it helps; an existing cohesive function or a small change does not need a separate skeleton pass. Revise boundaries as the implementation supplies evidence. Names that only describe position (`step_two`, `process_data`, `helper`) prompt a review of the responsibility. Resolve a consequential contract ambiguity from the request or repository; do not turn an unverified assumption into a promised docstring contract.

A block is its own function when a reader would otherwise have to work out what it does and it hands back one named value, decision, or effect through a small signature. Call count decides nothing: a responsibility called once still earns a function, and a "one-time operation" that needs no helper is a statement or two, not a named step of the algorithm. Keep a block inline when extracting it would need more than about four inputs, return several unrelated locals, or leave either function unreadable without the other. Flatten before splitting, with early returns and a mapping or `match` in place of an `if`/`elif` chain over constants. Keep parsing, computation, and output as phases joined by a model; I/O and mutation of shared state live in the orchestrating function, the computation beneath stays pure, and a function that mutates says so in its name or docstring. A comment that says what a block does is a prompt to extract or rename; a comment that says why stays.

A finished function has a name and contract that express one coherent responsibility, a caller whose flow and side effects are clear from its callees, and a boundary that improves understanding. A conjunction such as "and" can describe related parts of one responsibility; inspect the meaning rather than banning a word. A complexity or statement-count lint finding prompts a review of decomposition under the repository's rules, never a split by line ranges into numbered helpers or a bare `noqa`. Read [functions and modules](references/functions-and-modules.md) for an optional skeleton, the intent tests, the lint gates a new project adopts, and the measured function sizes behind them.

## Choose the project shape

Pick the row from the project kind before creating files, and choose per feature: a CRUD feature stays flat beside a feature with ports.

| Project kind | Shape |
| --- | --- |
| Script or notebook-adjacent code | One module: models, pure rules, I/O helpers, `main()` |
| CLI tool | Flat package: `cli.py`, one module per capability |
| Library or SDK | Public surface in `__init__.py` over private `_` modules |
| HTTP service with little domain logic | Framework-native routes, ORM models, schemas, query functions; by feature once it grows |
| Application with real rules and several integrations | Feature packages: pure `model.py`, `service.py` use cases, `ports.py` Protocols for real seams, `adapters/`, one composition root |
| Data or ML pipeline, experiment code | Functional core plus entry scripts as the shell |
| Long-running worker or agent | Loop shell, handler functions, pure decisions, ports for the model client, queue, and store |

Escalate only on a named trigger: a second entry point or importer, a rule worth testing without I/O, a second implementation of an integration, or a test that would otherwise mock a vendor library. No file, package, interface, or base class before it has content or a second implementation; no repository over an ORM for CRUD, no service that only forwards, no dependency-injection container while the composition root fits on one screen. State the chosen row and its trigger in the change summary when creating a project or a package. Read [architecture selection](references/architecture-selection.md) for layouts, the growth path, ports and wiring, import-direction contracts, and each pattern's own limits.

## Manage the project with uv

Use uv's project workflow for setup and dependency changes: `pyproject.toml`, `uv.lock`, `uv add`, `uv sync`, `uv run`. `pip install` and `uv pip install` are not routine setup, a shortcut, or a retry after failed resolution; an exceptional environment needs a concrete reason and a reproducible dependency record. A new project starts on CPython's current bugfix line (3.14 as of 2026-10-07; 3.15.0 was still at release candidate 3), or one line older when a dependency lags; 3.12 is the syntax floor for `type` aliases and type parameters, not a baseline. Keep runtime dependencies and development groups distinct. Read [project environment](references/project-environment.md) when setting up Python, changing dependencies, or arranging groups.

## Types and data boundaries

Annotate functions, returns, model fields, attributes, module-level values, and local variables, even when the value makes the type inferable. The local annotation is for the reader, not the checker: in a diff, a review, or a long function passing external-library values around, the declared type says what a name holds without a language server, and the need grows with every library involved. Use `dict[str, int]`, `list[Item]`, and `Item | None`, never `typing.Dict` or `typing.List`; import an SDK's real client, request, response, and stream types instead of `Any`; add no cast or suppression merely to make an annotation present. Past a handful of parameters, the rest are keyword-only. Read [types and enums](references/types-and-enums.md) for binding syntax, SDK types, and narrow exceptions.

Pydantic `BaseModel` is the default for application-owned structured data: internal models, configuration, inputs, results, values passed between phases, domain entities and value objects. That default is for applications, services, tools, pipelines, and agents that already depend on Pydantic. Two cases differ and say so beside the record: a library or SDK whose users must not inherit a Pydantic dependency, and a measured hot path where construction or validation cost dominates; there, records are dataclasses, `NamedTuple`, or plain classes, which is why fastapi and attrs keep Pydantic at their boundary. Otherwise `TypedDict`, dataclasses, and dictionaries are not competing record representations: one model per meaning, no parallel layers. Services and resource owners stay ordinary classes. A closed string vocabulary that is persisted or transmitted is an `enum.StrEnum` with explicit values; provider-extensible strings stay open. Read [Pydantic integration](references/pydantic-integration.md) to load the official external `pydantic` skill and for this pack's choices on unknown fields, enum values, domain models, and compatibility.

## Modules that remain easy to change

A module owns one responsibility a reader can state in a sentence; split by reason to change, never by kind or line count. New modules start private (`_name.py`), and `__init__.py` re-exports the public surface through `__all__` or `from ._x import Name as Name`; a public module keeps the names callers import while its machinery lives in a private module beside it. Order a file by importance, put a private helper directly below its only caller, and let a split-out module say why in its docstring. Exceptions, constants, and small shared types live in leaf modules that import nothing from the package, so the import graph stays acyclic; files that depend on each other in both directions are one module split badly.

Module length is a review prompt: at about 500 handwritten first-party lines, check that the module is still many small units around one concept; at 1,000, split at a boundary you can name or say in the change summary why it stays together. The libraries measured for this skill keep files of 1,000 to 3,900 lines whose functions stay at a median of 5 body lines; none has one function that carries a file. Repository limits win. Read [functions and modules](references/functions-and-modules.md) before moving code or changing public imports; preserve import direction and visible behavior.

## Explain what the code cannot show

Add the explanation where a maintainer meets the decision: a module docstring for what the file owns, a class or model docstring for its role and invariants, a function docstring for the contract a caller depends on (units, ordering, ownership, sentinels, failures, side effects, lifecycle, cancellation), and a block comment for a reason, ordering constraint, workaround, or rejected alternative. A public name without a docstring is a defect; a private helper whose name and signature say everything needs none. Do not repeat types the annotations carry, narrate statements, or invent rationale for a sleep, retry, or fallback; "thread-safe", "idempotent", and "guaranteed cleanup" need evidence. Follow the repository's docstring convention and preserve tool directives such as `# noqa`, `# type: ignore`, `# ty: ignore`, and `# pragma: no cover` unless that tool's behavior is in scope.

A docstring-only or comment-only request authorizes no signature, annotation, control-flow, or dependency change, and "review", "audit", or "check" returns findings without edits. After a doc-only edit in a Git repository, run the guard from inside that repository, resolving the directory that holds this `SKILL.md`: `python3 <skill-dir>/scripts/verify_doc_only_diff.py --base HEAD -- path/to/file.py`. It fails on any executable AST change or changed tool directive. Read [docstrings and comments](references/docstrings-and-comments.md) for the contract map, Python-specific contracts, patterns, the review checklist, and the guard's limits.

## Correctness and verification

A package has one exception root, subclassed by what the caller would do differently, carrying the facts a caller acts on as fields, with transport and library exceptions translated at one seam. Resource ownership and async cancellation are explicit. Read [correctness and testing](references/correctness-and-testing.md) when changing error handling, I/O, concurrency, project documents, or verification strategy.

Run the repository's checks relevant to the changed behavior, through `uv run` in uv-managed projects. When public imports, accepted and rejected inputs, serialized fields and enum values, error behavior, or cleanup paths change, run the real entry point on fixed input. Keep or add focused tests for meaningful caller-visible contracts, with expected results from a requirement, documented contract, independent calculation, or reproduced bug. Do not copy expected values from the implementation under test. A test failure during refactoring needs diagnosis before any test is changed or removed. A formatter cannot establish runtime correctness, a type checker cannot establish external-data validation, and a passing complexity linter cannot establish that a function is readable.

Finish when the requested result is implemented or reviewed and the relevant checks have run or their exact limitation is reported. State the behavior changed, the module or architecture decisions with their triggers, checks and results, and anything not verified. No plan file or report template for ordinary Python work. Continue an already-requested publication through `draft-pr`, or an already-requested commit and push through `commit-and-push`.

## Reference files and tooling

| File | Read or run when | Content |
| --- | --- | --- |
| [functions and modules](references/functions-and-modules.md) | Writing a multi-phase function or a module, splitting or moving code, choosing lint gates | Optional skeleton, intent tests, size prompts and gates, Ruff block, move procedure |
| [architecture selection](references/architecture-selection.md) | Starting a project, adding a package, introducing an interface, wiring integrations | Decision table, layouts, growth path, ports and wiring, import-linter contracts, stop rules, pattern catalog |
| [docstrings and comments](references/docstrings-and-comments.md) | Adding, correcting, or reviewing docstrings and comments | Modes, contract map, Python-specific contracts, patterns, checklist, guard limits |
| [types and enums](references/types-and-enums.md) | Defining types, integrating a typed SDK, changing enum values | Annotation forms, representation table, stable enum values |
| [Pydantic integration](references/pydantic-integration.md) | Changing models, validation, or serialization | External skill loading, unknown-field policy, enum values, domain models, the library exception |
| [project environment](references/project-environment.md) | Setting up Python, changing dependencies, arranging groups | uv workflow, groups, locked runs, exceptions |
| [correctness and testing](references/correctness-and-testing.md) | Changing errors, resources, async code, docs, or checks | Error hierarchy, cleanup, concurrency, checks that establish behavior |
| [reference repositories](references/reference-repositories.md) | A rule needs its evidence, or a large unit needs a precedent | Nine measured packages, numbers, quoted explanations, what not to imitate |
| `scripts/verify_doc_only_diff.py` | After a doc-only edit with a Git base | AST and tool-directive comparison; `scripts/smoke_test.sh` exercises it |

## Gotchas

- A prompt that discourages helpers "for one-time operations", read literally as "inline every single-caller step", produces the giant function it warns against. A one-time operation is a statement or two; a named responsibility called once is still a function.
- Annotating every local is a readability rule, not a type-checking rule. Every measured library annotates 0% to 17% of locals, and the rule holds anyway.
- Pydantic-first is an application default. A library that must not impose the dependency, or a measured hot path, uses dataclasses or plain classes with the reason beside them; neither case transfers to the other.
- A docstring can be runtime data: an `argparse` description, a Pydantic schema description, a click help text. The doc-only guard cannot see those consumers.
- Incidental lower-level exceptions are not public guarantees; examples may become doctests; comments can change what a tool does even though Python ignores them.
