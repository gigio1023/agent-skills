# Docstrings and Comments

Read this when adding, correcting, auditing, or reviewing Python docstrings and explanatory comments, or when a change makes an existing explanation stale. Document caller-visible contracts and maintenance-critical rationale that names, annotations, and code structure do not reveal. Preserve runtime and tooling behavior and follow the repository's established docstring convention.

## Contents

- Modes and authority
- Select the surface
- Ground the contract
- Contract map
- Python-specific contracts
- Style without churn
- Inline comments and tool directives
- Patterns
- Anti-patterns
- Review findings
- Checklist
- Doc-only diff guard

## Modes and authority

- **Edit** adds or corrects documentation in the requested Python scope.
- **Review** reports misleading, missing, redundant, or stale documentation without editing. "Review", "audit", and "check" select this mode unless the user also asks for fixes.

Documentation work does not authorize signature, annotation, decorator, control-flow, dependency, or API changes. Do not rewrite executable code to make documentation easier. When a code change is in scope and it invalidates an explanation, update or remove that explanation in the same change rather than leaving a stale claim or adding a second account.

A documentation request starts from the repository's instructions, the target files, public import surfaces, nearby documented APIs, tests, and doc configuration in `pyproject.toml`, Ruff, pydocstyle, Sphinx, or mkdocstrings, which fix the local format and the public surface. From there, map only the non-obvious, evidenced contract fields (inputs, result or yields, failures, side effects, lifecycle, concurrency, invariants), add the smallest useful docstring or block-local comment, and finish by parsing the changed files, running the configured checks, and running the doc-only guard when a Git base exists. A focused test is added only when a documented claim needs one.

## Select the surface

Do not equate "public" with "name lacks an underscore". Inspect:

- package exports, `__all__`, re-exports, and documented import paths;
- functions, classes, properties, protocols, abstract methods, overloads, and callbacks used outside their module;
- entry points registered by decorators, plugins, dependency injection, serialization, configuration, or command routing;
- protected subclass hooks whose override contract matters;
- private helpers only for a non-obvious invariant or a fragile external rule.

A well-named private helper with a clear signature next to its only caller often needs no docstring; a public function that a caller must use correctly nearly always does.

## Ground the contract

Prefer accepted specifications and explicit user requirements, then implementation with tests and call sites, then schemas, framework registration, maintained docs, and issue history. Implementation shows current behavior but not always intended public policy. When sources conflict, document only what is certain and report the unresolved contract.

Never invent rationale for a sleep, retry, cache, order, lock, or fallback because it looks plausible. "Thread-safe", "idempotent", and "guaranteed cleanup" require direct evidence.

## Contract map

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

Do not duplicate annotation types unless the local format or generator requires them. Add semantic meaning such as identifier namespace, units, ownership, or why `None` is returned. A model field description can supply non-obvious meaning to callers or generated schemas without maintaining a separate field catalog.

## Python-specific contracts

| Surface | Caller-relevant questions |
| --- | --- |
| Coroutine | cancellation, cleanup, retry eligibility; never imply atomicity |
| Generator | call vs first-iteration effects, yield order, early-close cleanup |
| Context manager | acquired/yielded object, cleanup, reentrancy, suppression |
| Protocol/callback | implementer obligations, timing, re-entry, sentinel values |
| Overload | variant-specific semantics without duplicating shared behavior |
| Property/descriptor | access effects, caching, mutation, failure |

## Style without churn

Choose the format from explicit repository configuration, then generator requirements, neighboring public APIs, then the dominant convention in the requested files. Preserve the selected Google, NumPy, Sphinx/reStructuredText, or project-specific fields. If nearby code conflicts, follow configuration and report the inconsistency instead of converting unrelated docstrings.

Use exact signature parameter names and a summary line useful to generated indexes. Examples may become doctests; keep them deterministic and policy-compatible.

## Inline comments and tool directives

Comments explain why an order or branch is required, which invariant is preserved, why an alternative is unsafe, which external constraint applies, or what a fallback distinguishes. Place them immediately above the smallest relevant block. A comment that introduces a section inside a function body is a signal that the section wants to be a named function; extract it when the section has its own decision or product, and keep the comment only when the ordering itself is the point.

Avoid `Step 1` narration, comments that repeat the next line, banners around routine code, and guessed intent.

Comments can affect tools even when Python ignores them. Preserve `# type:`, `# type: ignore`, `# pyright: ignore`, `# mypy:`, `# ty: ignore`, `# pyrefly: ignore`, `# noqa`, `# ruff:`, `# fmt:`, `# isort:`, `# pragma: no cover`, and coverage or security-scanner directives unless the user explicitly requests the corresponding tool-behavior change.

## Patterns

Adapt these to the repository's format. The semantics matter more than the headings.

### Public function

```python
def reserve(items: list[Item], limit: int | None = None) -> list[Item]:
    """Reserve available items in input order.

    Args:
        items: Candidates; unavailable items are ignored and not mutated.
        limit: Maximum reservations, or `None` for no limit.

    Returns:
        Newly reserved items in the same order as `items`.

    Raises:
        ReservationError: If the backing store rejects a reservation.

    Side effects:
        Persists each successful reservation before returning.
    """
```

Annotations already carry container types. The docstring adds ordering, ownership, sentinel behavior, public failure, and persistence.

### Coroutine and cancellation

```python
async def publish(batch: Batch) -> Receipt:
    """Publish one batch and wait for broker acknowledgement.

    Cancellation before acknowledgement leaves the batch eligible for retry.
    Cancellation during receipt persistence is delayed until the receipt is
    durable.
    """
```

Write cancellation guarantees only when the implementation and tests establish them. "Async" alone does not promise concurrency, atomicity, or thread safety.

### Generator laziness

```python
def iter_pages(source: Source) -> Iterator[Page]:
    """Yield source pages in ascending cursor order.

    The source is opened on first iteration, not when this function is called.
    Closing the iterator early closes the source without fetching another page.
    """
```

Call time and iteration time are different API boundaries. Document when I/O, validation, and cleanup occur when callers depend on it.

### Context manager lifecycle

```python
@contextmanager
def locked(record: Record) -> Iterator[Record]:
    """Yield `record` while holding its process-wide lock.

    The lock is released on normal exit and exceptions. This context manager is
    not reentrant and does not suppress exceptions from the managed block.
    """
```

Name the acquired resource, yielded value, cleanup, reentrancy, and exception suppression only when applicable.

### Protocol and callback

```python
class ProgressSink(Protocol):
    def __call__(self, completed: int, total: int | None) -> None:
        """Receive monotonic progress for one operation.

        Implementations must return promptly and must not call back into the
        operation. `total` is `None` when the final size is unknown.
        """
```

Put shared obligations on the protocol or callback type. Implementations document deviations or additional effects instead of copying this text.

### Overloads

```python
@overload
def read(key: Key, *, raw: Literal[False] = False) -> Record: ...

@overload
def read(key: Key, *, raw: Literal[True]) -> bytes: ...

def read(key: Key, *, raw: bool = False) -> Record | bytes:
    """Read a record, returning encoded bytes when `raw` is true.

    Raises:
        MissingRecord: If `key` is not present.
    """
```

Let annotations express the type relationship; do not repeat the shared failure and side-effect contract on every overload.

### Property and cache

```python
@property
def schema(self) -> Schema:
    """Return the parsed schema, caching it after the first successful load.

    Failed loads are not cached.
    """
```

The useful contract is cache timing and failure behavior, not "The schema."

### Fallback boundary

```python
def load_policy(path: Path) -> Policy:
    """Load a policy, falling back only when the file is absent.

    Invalid policy files raise `PolicyError`; they are not replaced by the
    default because that would hide configuration mistakes.
    """
```

Distinguish absence, invalid data, transient failure, and intentional fallback.

### Inline rationale

```python
# Persist the cursor before publishing so a restarted worker cannot emit the
# same page twice.
store_cursor(next_cursor)
publisher.publish(page)
```

The comment explains the ordering invariant. It does not narrate either call.

## Anti-patterns

### Restating types and code

```python
def find(user_id: int) -> User | None:
    """Find a user.

    Args:
        user_id (int): User ID.

    Returns:
        User | None: The user.
    """
```

Explain the identifier namespace, visibility rules, or why absence returns `None`; otherwise the annotations and name already carry the information.

### Guessing rationale

```python
# Sleep to avoid overloading the database.
time.sleep(1)
```

Without supporting evidence, this may be rate limiting, backoff, test timing, or a workaround. Do not turn a guess into maintained documentation.

### Treating directives as ordinary comments

```python
result = dynamic_call()  # type: ignore[no-any-return]
unused = prepare()  # noqa: F841
```

Changing or moving these comments can alter type-checker or linter behavior even though the Python AST is otherwise unchanged.

## Review findings

Order findings by caller impact: false or stale contracts first; then missing failure, side effect, lifecycle, concurrency, ownership, or sentinel behavior; then speculative duplication and low-value restatement. Each finding names the symbol and location, the false, missing, redundant, or speculative contract, the caller or maintenance impact, the supporting evidence, and the smallest repair. Do not report every undocumented private helper as a defect, and do not inflate a review with style preferences the repository does not enforce.

## Checklist

Apply to the requested symbols and changed files.

Surface selection:

- [ ] Public exports, re-exports, protocols, abstract methods, callbacks, and framework entry points were considered.
- [ ] Private helpers were documented only for a non-obvious invariant or external constraint.
- [ ] Generated, vendored, migration, and third-party files remain untouched unless explicitly in scope.

Contract accuracy:

- [ ] Purpose describes effect or responsibility rather than repeating the name.
- [ ] Parameter text adds units, accepted forms, sentinel, ownership, mutation, or normalization semantics instead of duplicating annotations.
- [ ] Return or yield text covers ordering, laziness, ownership, mutability, and empty behavior when callers need them.
- [ ] Exceptions are intentionally exposed API behavior, not an exhaustive list of incidental lower-level failures.
- [ ] Side effects, partial success, cleanup, retry, caching, and fallback claims have implementation, test, spec, or user evidence.
- [ ] Async cancellation, generator timing, context-manager lifecycle, protocol obligations, and subclass behavior are covered when applicable.

Style and placement:

- [ ] Repository configuration or generator requirements determined the format.
- [ ] Exact signature parameter names are used.
- [ ] Summary lines are useful to generated indexes.
- [ ] Nearby conflicts did not trigger an unrelated format conversion.
- [ ] Inline comments sit above the smallest relevant block and explain why, invariants, or external constraints.
- [ ] Tool directives remain unchanged unless their behavior was explicitly in scope.

Scope and verification:

- [ ] Signatures, annotations, decorators, imports, control flow, and executable statements did not change during a doc-only request.
- [ ] Changed files parse or compile.
- [ ] Required repository checks and applicable docstring, lint, or docs-build checks ran; type or runtime tests were added only for a specific claim or tool-sensitive change.
- [ ] The doc-only diff guard passed when a Git base was available.
- [ ] Each final claim was re-read against current code and tests.
- [ ] Skipped checks and unresolved intent are reported where material.

## Doc-only diff guard

For Git-backed doc-only edits, run from the repository being edited, resolving the script path from this skill's directory:

```bash
python3 <skill-dir>/scripts/verify_doc_only_diff.py --base HEAD -- path/to/file.py
```

The guard removes standard runtime docstrings, compares the executable AST, and rejects changed semantic-directive text or counts. It fails closed on invalid or missing files. Attribute docstrings (a bare string after an assignment) remain AST changes, so a guard failure on one is expected and must be reviewed by hand. Inspect the diff for directive placement and prose correctness even after a pass. `scripts/smoke_test.sh` exercises the guard's positive and negative fixtures when maintaining this skill.
