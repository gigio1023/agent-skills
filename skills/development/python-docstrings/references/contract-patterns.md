# Python Contract Documentation Patterns

Adapt these examples to the repository's established Google, NumPy,
Sphinx/reStructuredText, or project-specific format. The semantics matter more
than the headings.

## Contents

- Public Function
- Coroutine and Cancellation
- Generator Laziness
- Context Manager Lifecycle
- Protocol and Callback
- Overloads
- Property and Cache
- Fallback Boundary
- Inline Rationale
- Anti-Patterns

## Public Function

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

Annotations already carry container types. The docstring adds ordering,
ownership, sentinel behavior, public failure, and persistence.

## Coroutine and Cancellation

```python
async def publish(batch: Batch) -> Receipt:
    """Publish one batch and wait for broker acknowledgement.

    Cancellation before acknowledgement leaves the batch eligible for retry.
    Cancellation during receipt persistence is delayed until the receipt is
    durable.
    """
```

Write cancellation guarantees only when the implementation and tests establish
them. “Async” alone does not promise concurrency, atomicity, or thread safety.

## Generator Laziness

```python
def iter_pages(source: Source) -> Iterator[Page]:
    """Yield source pages in ascending cursor order.

    The source is opened on first iteration, not when this function is called.
    Closing the iterator early closes the source without fetching another page.
    """
```

For generators, call time and iteration time are different API boundaries.
Document when I/O, validation, and cleanup occur when callers depend on it.

## Context Manager Lifecycle

```python
@contextmanager
def locked(record: Record) -> Iterator[Record]:
    """Yield `record` while holding its process-wide lock.

    The lock is released on normal exit and exceptions. This context manager is
    not reentrant and does not suppress exceptions from the managed block.
    """
```

Name the acquired resource, yielded value, cleanup, reentrancy, and exception
suppression only when applicable.

## Protocol and Callback

```python
class ProgressSink(Protocol):
    def __call__(self, completed: int, total: int | None) -> None:
        """Receive monotonic progress for one operation.

        Implementations must return promptly and must not call back into the
        operation. `total` is `None` when the final size is unknown.
        """
```

Put shared obligations on the protocol or callback type. Implementations should
document deviations or additional effects instead of copying this text.

## Overloads

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

Avoid duplicating the shared failure and side-effect contract on every overload.
Let annotations express the type relationship.

## Property and Cache

```python
@property
def schema(self) -> Schema:
    """Return the parsed schema, caching it after the first successful load.

    Failed loads are not cached.
    """
```

The useful contract is cache timing and failure behavior, not “The schema.”

## Fallback Boundary

```python
def load_policy(path: Path) -> Policy:
    """Load a policy, falling back only when the file is absent.

    Invalid policy files raise `PolicyError`; they are not replaced by the
    default because that would hide configuration mistakes.
    """
```

Distinguish absence, invalid data, transient failure, and intentional fallback.

## Inline Rationale

```python
# Persist the cursor before publishing so a restarted worker cannot emit the
# same page twice.
store_cursor(next_cursor)
publisher.publish(page)
```

The comment explains the ordering invariant. It does not narrate either call.

## Anti-Patterns

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

Explain the identifier namespace, visibility rules, or why absence returns
`None`; otherwise the annotations and name already carry the information.

### Guessing rationale

```python
# Sleep to avoid overloading the database.
time.sleep(1)
```

Without supporting evidence, this may be rate limiting, backoff, test timing, or
a workaround. Do not turn a guess into maintained documentation.

### Treating directives as ordinary comments

```python
result = dynamic_call()  # type: ignore[no-any-return]
unused = prepare()  # noqa: F841
```

Changing or moving these comments can alter type-checker or linter behavior even
though the Python AST is otherwise unchanged.
