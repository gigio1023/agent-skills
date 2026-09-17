# Correctness and Testing

Read this for changes to source explanations, errors, resources, async behavior, or the checks that establish a Python change. Use the repository's existing test and documentation conventions.

## Keep explanations with their implementation

Code is the source of truth for implementation, but it cannot always explain the intent or external constraint behind a decision. Add the missing explanation where a maintainer will encounter the decision: a module docstring for a file's responsibility and non-obvious context; a class or model docstring for its role and invariants; a function docstring for non-obvious inputs, results, side effects, errors, or lifecycle; and a block-local comment for a reason, ordering constraint, workaround, or rejected alternative. Include background only when it explains the current choice. Do not invent history, intent, or guarantees.

Follow the existing docstring style. Describe semantics that annotations do not carry, such as units, ownership, unknown-value handling, partial success, or cancellation. Do not repeat parameter types, obvious names, or each statement in prose. A model field description can supply non-obvious meaning to callers or generated schemas without maintaining a separate field catalog.

Policy may live outside code. Put other material under `docs/` only when source-local explanations cannot convey it or a reader needs a view assembled across multiple files, such as a cross-component lifecycle or an external operational constraint. Maintain one useful explanation, link to authoritative symbols, and avoid copying code, signatures, schemas, or per-file walkthroughs. Do not create a Markdown implementation report for each task. When the change invalidates an existing explanation, update or remove that explanation in scope rather than leaving stale claims or adding a second account.

Check explanations against code, tests, call sites, and the stated requirement. For documentation-only Python edits, preserve executable behavior and tool directives, parse the changed files, and run applicable documentation checks; add behavioral tests only when a claim needs them. Source explanations should reduce the need to reconcile documents with code, not create another maintenance routine.

## Errors and resource ownership

Catch the specific failures the current layer can handle. Translate an exception where it becomes meaningful to a caller, preserve its cause with `raise ... from ...` when wrapping it, and keep cancellation or programming errors from becoming an ordinary success result. A broad catch is appropriate only for an intentional boundary with a defined recovery, reporting, or re-raise policy.

The code that acquires a resource should make its release visible through a context manager or a reliable `finally` path. Tests for changed cleanup behavior should include failure, not just successful completion. Do not scatter logging and re-raising through every layer; avoid duplicate reports and sensitive payloads in logs or public errors.

In async code, distinguish cooperative cancellation from operational failure. `asyncio.CancelledError` inherits from `BaseException`; catching `Exception` does not cover it. Cleanup must still run, and cancellation should normally propagate. Structured concurrency depends on this behavior.

Choose concurrency semantics before choosing an API. `TaskGroup` cancels sibling tasks when a member fails with a non-cancellation exception; `gather` can suit operations whose failures are collected independently. Neither is a universal replacement for the other. Bound external waits and concurrency when required by the operation, and do not block an event loop with synchronous I/O. Thread offloading does not automatically accelerate CPU-bound Python code.

Retry only operations whose replay semantics are understood, with a bounded policy appropriate to the dependency. Do not retry deterministic schema failures or non-idempotent effects merely because the exception is catchable.

## Tests that establish behavior

Choose tests from the change's observable effects:

| Changed surface | Useful check |
| --- | --- |
| Public imports or entry points | Existing consumer imports still resolve; entry point behavior is preserved |
| Validation or parsing | Accepted and rejected inputs, including source-specific coercion and unknown-field policy |
| Serialized or persisted data | Actual output values, aliases, omissions, unknown-field retention, and compatibility with existing fixtures |
| Error translation | Exception type and meaningful caller behavior, not incidental wording unless wording is public behavior |
| Resource or async lifecycle | Failure and cancellation release owned resources and preserve intended cancellation |
| Module extraction | The same behavior through a stable caller-facing boundary, plus relevant import checks |

Use characterization tests when the behavior of code being moved is insufficiently covered. Prefer public behavior and fakes at external dependencies over mocks that encode the old helper layout. Keep fixtures deterministic and isolated; do not require a live service when a local test proves the relevant behavior. Live, paid, or state-changing integration runs need the authority applicable to that environment.

Tests and type checks answer different questions. An annotation does not validate a provider response, a successful import does not exercise a cleanup path, and a passing linter does not establish compatibility. Conversely, avoid new tests for prose-only, formatting-only, or trivial mechanical changes when existing checks are sufficient.

## Use configured checks

Discover commands from project instructions, CI, and tool configuration. Use `uv run` with the appropriate declared groups in uv-managed projects. Keep one configured formatter and the repository's selected type-checking strategy; do not migrate checkers or impose a new strict-mode configuration as a side effect. New and changed declarations require explicit types, including locals and SDK objects; inferred-type acceptance by a checker is insufficient. Broader changes to untouched code remain scoped to the request.

Run the smallest set that covers the changed surface, including repository-required checks. Broaden when a shared API or dependency warrants it. Report a missing prerequisite or a pre-existing failure distinctly from a passing result. Do not apply unsafe lint fixes automatically, weaken a check to obtain a pass, or repeat unchanged successful checks without a new reason.

## Sources

Checked 2026-09-10:

- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html): exception handling, chaining, cleanup, and context managers.
- [Python task cancellation and concurrency](https://docs.python.org/3/library/asyncio-task.html): cancellation propagation, `TaskGroup`, `gather`, and thread offloading.
- [Ruff configuration](https://docs.astral.sh/ruff/configuration/): project settings and discovery.
- [Ruff fix safety](https://docs.astral.sh/ruff/linter/#fix-safety): fixes whose behavior may change runtime semantics.
- [pytest good integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html): test layout and import behavior when pytest is the selected runner.

The proportional test policy is this pack's choice. These references do not mandate a coverage percentage, a specific test framework, or test-first development for every change.
