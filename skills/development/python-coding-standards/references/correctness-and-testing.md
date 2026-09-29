# Correctness and Testing

Read this for changes to errors, resources, async behavior, project documentation, or the checks that establish a Python change. Use the repository's existing test and documentation conventions. Docstrings and comments have their own reference, [docstrings and comments](docstrings-and-comments.md).

## Documents outside the code

Policy may live outside code. Put other material under `docs/` only when source-local explanations cannot convey it or a reader needs a view assembled across multiple files, such as a cross-component lifecycle or an external operational constraint. Maintain one useful explanation, link to authoritative symbols, and avoid copying code, signatures, schemas, or per-file walkthroughs. Do not create a Markdown implementation report for each task. When the change invalidates an existing explanation, update or remove that explanation in scope rather than leaving stale claims or adding a second account.

## Errors and resource ownership

Give a package one exception root and subclass it by what the caller would do differently, not by where the error was raised; a case raised from more than one place earns a named subclass. Errors carry the facts a caller acts on as fields (`status_code`, `path`, the offending value), never as text to parse. Use the builtin exceptions, `TypeError` and `ValueError`, for plain misuse of a function, and the package's own errors for the package's logic. Translate transport and library exceptions into the package's errors at one seam, such as the single function that performs a request or the context manager that wraps a driver call, so no other layer needs to know the driver's exception types.

Catch the specific failures the current layer can handle. Translate an exception where it becomes meaningful to a caller, preserve its cause with `raise ... from ...` when wrapping it, and keep cancellation or programming errors from becoming an ordinary success result. A broad catch is appropriate only for an intentional boundary with a defined recovery, reporting, or re-raise policy. A retry loop catches a named tuple of transient error types, not `Exception`, because the broad form also retries programming errors.

The code that acquires a resource should make its release visible through a context manager or a reliable `finally` path. Tests for changed cleanup behavior should include failure, not just successful completion. Do not scatter logging and re-raising through every layer; avoid duplicate reports and sensitive payloads in logs or public errors.

In async code, distinguish cooperative cancellation from operational failure. `asyncio.CancelledError` inherits from `BaseException`; catching `Exception` does not cover it. Cleanup must still run, and cancellation should normally propagate. Structured concurrency depends on this behavior.

Choose concurrency semantics before choosing an API. `TaskGroup` cancels sibling tasks when a member fails with a non-cancellation exception; `gather` can suit operations whose failures are collected independently. Neither is a universal replacement for the other. Bound external waits and concurrency when required by the operation, and do not block an event loop with synchronous I/O. Thread offloading does not automatically accelerate CPU-bound Python code.

Retry only operations whose replay semantics are understood, with a bounded policy appropriate to the dependency. Do not retry deterministic schema failures or non-idempotent effects merely because the exception is catchable.

## Checks that establish behavior

Verify a change through its observable effects, by running the real entry point on fixed input. A test whose expected values are read off the code just written passes by construction and breaks on the next refactor, so do not write one.

| Changed surface | Useful check |
| --- | --- |
| Public imports or entry points | Existing consumer imports still resolve; entry point behavior is preserved |
| Validation or parsing | Accepted and rejected inputs, including source-specific coercion and unknown-field policy |
| Serialized or persisted data | Actual output values, aliases, omissions, unknown-field retention, and compatibility with existing fixtures |
| Error translation | Exception type and meaningful caller behavior, not incidental wording unless wording is public behavior |
| Resource or async lifecycle | Failure and cancellation release owned resources and preserve intended cancellation |
| Module extraction | The same behavior through a stable caller-facing boundary, plus relevant import checks |

When code being moved is insufficiently covered, run its caller-facing entry point on the same fixed input before and after the move and compare the outputs instead of leaving characterization tests behind. Add a test only when its expected values come from a spec, a hand calculation, or a reproduced bug that fails before the fix, and losing it would let a security, money, data-loss, or reported-number bug through. Prefer fakes at external dependencies over mocks that encode the helper layout. Keep fixtures deterministic and isolated; do not require a live service when a local run proves the relevant behavior. Live, paid, or state-changing integration runs need the authority applicable to that environment.

Tests and type checks answer different questions. An annotation does not validate a provider response, a successful import does not exercise a cleanup path, and a passing linter does not establish compatibility. Conversely, avoid new tests for prose-only, formatting-only, or trivial mechanical changes when existing checks are sufficient.

## Use configured checks

Discover commands from project instructions, CI, and tool configuration. Use `uv run` with the appropriate declared groups in uv-managed projects. Keep one configured formatter and the repository's selected type-checking strategy; do not migrate checkers or impose a new strict-mode configuration as a side effect. New and changed declarations require explicit types, including locals and SDK objects; inferred-type acceptance by a checker is insufficient. Broader changes to untouched code remain scoped to the request.

Run the smallest set that covers the changed surface, including repository-required checks. Broaden when a shared API or dependency warrants it. Report a missing prerequisite or a pre-existing failure distinctly from a passing result. Do not apply unsafe lint fixes automatically, weaken a check to obtain a pass, or repeat unchanged successful checks without a new reason.

## Sources

Checked 2026-09-29:

- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html): exception handling, chaining, cleanup, and context managers.
- The exception-hierarchy and single-seam rules follow the practice measured in httpx and the OpenAI and Anthropic SDKs; see [reference repositories](reference-repositories.md).
- [Python task cancellation and concurrency](https://docs.python.org/3/library/asyncio-task.html): cancellation propagation, `TaskGroup`, `gather`, and thread offloading.
- [Ruff configuration](https://docs.astral.sh/ruff/configuration/): project settings and discovery.
- [Ruff fix safety](https://docs.astral.sh/ruff/linter/#fix-safety): fixes whose behavior may change runtime semantics.
- [pytest good integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html): test layout and import behavior when pytest is the selected runner.

The test policy is this pack's choice: verify end to end, and add a test only when its expected values come from outside the code under change. These references do not mandate a coverage percentage or a specific test framework.
