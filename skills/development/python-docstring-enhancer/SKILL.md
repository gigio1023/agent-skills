---
name: python-docstring-enhancer
description: >
  Use when adding, correcting, auditing, or reviewing Python docstrings and
  explanatory comments, especially for public APIs, async and generator
  semantics, context-manager lifecycle, protocols and callbacks, side effects,
  exceptions, ordering, invariants, fallbacks, and compatibility constraints.
  Trigger for "docstring 추가", "주석 보강", "Python 주석", and "문서화해줘"
  when the target is Python source. NOT for general Markdown docs, annotation or
  API redesign, behavior-changing refactors, generated code, or comments that
  merely narrate statements.
---

# Python Docstring Enhancer

Document caller-visible contracts and maintenance-critical rationale that names,
annotations, and code structure do not reveal. Preserve runtime and tooling
behavior and follow the repository's established docstring convention.

## Modes and Quick Start

- **Edit** adds or corrects documentation in the requested Python scope.
- **Review** reports misleading, missing, redundant, or stale documentation
  without editing. “Review”, “audit”, and “check” select this mode unless the
  user also asks for fixes.

1. Read repository instructions, target files, public import surfaces, nearby
   documented APIs, tests, and doc configuration in `pyproject.toml`, Ruff,
   pydocstyle, Sphinx, or equivalent files.
2. Determine the local format and requested public surface.
3. Map only non-obvious, evidenced contract fields: inputs, result or yields,
   failures, side effects, lifecycle, concurrency, and invariants.
4. Add the smallest useful docstring or block-local rationale comment. Do not
   rewrite executable code to make documentation easier.
5. Parse changed files, run configured checks, validate claims with focused
   tests when proportionate, and verify that doc-only work did not change
   executable AST or tooling directives.

Documentation work does not authorize signature, annotation, decorator,
control-flow, dependency, or API changes.

## Select the Right Surface

Do not equate “public” with “name lacks an underscore”. Inspect:

- package exports, `__all__`, re-exports, and documented import paths;
- functions, classes, properties, protocols, abstract methods, overloads, and
  callbacks used outside their module;
- entry points registered by decorators, plugins, dependency injection,
  serialization, configuration, or command routing;
- protected subclass hooks whose override contract matters;
- private helpers only for non-obvious invariants or fragile external rules.

## Ground the Contract

Prefer accepted specifications and explicit user requirements, then
implementation with tests and call sites, then schemas, framework registration,
maintained docs, and issue history. Implementation shows current behavior but
not always intended public policy. When sources conflict, document only what is
certain and report the unresolved contract.

Never invent rationale for a sleep, retry, cache, order, lock, or fallback
because it looks plausible.

## Contract Map

Include only applicable caller-visible semantics:

| Area | Document when it is not obvious |
| --- | --- |
| Purpose | effect, responsibility, abstraction boundary |
| Inputs | units, accepted forms, normalization, sentinel, ownership, mutation |
| Return/yield | ordering, laziness, ownership, mutability, empty behavior |
| Failure | deliberately exposed exceptions, partial success |
| Side effects | I/O, persistence, logging, caching, global state, callbacks |
| Lifecycle | acquire/release, cleanup, idempotency, reentrancy |
| Concurrency | cancellation, scheduling, thread safety, locking, retry boundary |
| Inheritance | subclass obligations, override/extension, protocol guarantees |
| Compatibility | legacy forms, deprecation, external constraints |

Do not duplicate annotation types unless the local format or generator requires
them. Add semantic meaning such as identifier namespace, units, ownership, or
why `None` is returned.

## Resolve Style Without Churn

Choose the format from explicit repository configuration, then generator
requirements, neighboring public APIs, then the dominant convention in the
requested files. Preserve the selected Google, NumPy, Sphinx/reStructuredText,
or project-specific fields. If nearby code conflicts, follow configuration and
report the inconsistency instead of converting unrelated docstrings.

Use exact signature parameter names and a summary useful to generated indexes.

## Inline Comments

Comments should explain why an order or branch is required, which invariant is
preserved, why an alternative is unsafe, which external constraint applies, or
what a fallback distinguishes. Place them immediately above the smallest
relevant block.

Avoid `Step 1` narration, comments that repeat the next line, banners around
routine code, and guessed intent. Preserve `# type:`, `# type: ignore`, `# noqa`,
formatter, linter, type-checker, import-sort, and coverage directives unless the
user explicitly requests the corresponding tool-behavior change.

## Python-Specific Contracts

| Surface | Caller-relevant questions |
| --- | --- |
| Coroutine | cancellation, cleanup, retry eligibility; never imply atomicity |
| Generator | call vs first-iteration effects, yield order, early-close cleanup |
| Context manager | acquired/yielded object, cleanup, reentrancy, suppression |
| Protocol/callback | implementer obligations, timing, re-entry, sentinel values |
| Overload | variant-specific semantics without duplicating shared behavior |
| Property/descriptor | access effects, caching, mutation, failure |

Use [contract-patterns.md](references/contract-patterns.md) when one of these
contracts is difficult to phrase.

## Review Findings

Order findings by caller impact: false or stale contracts first; then missing
failure, side effect, lifecycle, concurrency, ownership, or sentinel behavior;
then speculative duplication and low-value restatement. Each finding names the
symbol and location, evidence, impact, and smallest repair. Do not report every
undocumented private helper as a defect.

## Verification

Apply [review-checklist.md](references/review-checklist.md). At minimum:

- parse or compile every changed Python file;
- run configured docstring, lint, docs-build, type, or focused test checks;
- inspect the diff and re-read each claim against final code and tests;
- for Git-backed doc-only edits, run:

  ```bash
  python3 scripts/verify_doc_only_diff.py --base HEAD -- path/to/file.py
  ```

The guard removes standard runtime docstrings, compares executable AST, and
rejects changed semantic-directive text or counts. It fails closed on invalid or
missing files; attribute docstrings remain AST changes. Inspect the diff for
directive placement and prose correctness even after a pass.

## Output

Lead with documented files or review findings. Report contracts clarified,
checks run, unresolved intent, and whether executable code changed.

## Reference Files and Tooling

| File | Read or run when | Purpose |
| --- | --- | --- |
| [contract-patterns.md](references/contract-patterns.md) | A Python contract is hard to phrase | Focused examples and anti-patterns |
| [review-checklist.md](references/review-checklist.md) | Reviewing or delivering edits | Selection, evidence, style, scope, validation |
| `scripts/verify_doc_only_diff.py` | A Git base exists for doc-only edits | AST and tool-directive comparison |
| `scripts/smoke_test.sh` | Maintaining this skill | Positive and negative guard fixtures |

Run scripts from the skill directory or resolve paths relative to the active
`SKILL.md`.

## Gotchas

- More documentation creates more synchronization obligations.
- Incidental lower-level exceptions are not automatically public guarantees.
- Examples may become doctests; keep them deterministic and policy-compatible.
- “Thread-safe”, “idempotent”, and “guaranteed cleanup” require direct evidence.
- Comments can affect tools even when Python ignores them.
