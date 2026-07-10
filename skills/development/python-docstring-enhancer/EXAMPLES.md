# Python Documentation Examples

Use these patterns only when they match the repository's docstring format.

## Contents

- Public Function Contract
- Non-Obvious Invariant
- Fallback Semantics
- Callback and Lifecycle Contract
- Data Model Contract
- Long Function Phases
- What Not to Add

## Public Function Contract

```python
def reserve(items: list[Item], limit: int | None = None) -> list[Item]:
    """Reserve available items in input order.

    Args:
        items: Candidates; unavailable items are ignored.
        limit: Maximum reservations, or `None` for no limit.

    Returns:
        Newly reserved items in the same order as `items`.

    Raises:
        ReservationError: If the backing store rejects a reservation.

    Side effects:
        Persists each successful reservation before returning.
    """
```

The annotation already carries container and scalar types. The docstring adds
ordering, sentinel behavior, failure semantics, and the side effect.

## Non-Obvious Invariant

```python
# Persist the cursor before publishing so a restarted worker cannot emit the
# same page twice.
store_cursor(next_cursor)
publisher.publish(page)
```

This explains why the apparently slower order is required.

## Fallback Semantics

```python
def load_policy(path: Path) -> Policy:
    """Load a policy, falling back only when the file is absent.

    Invalid policy files raise `PolicyError`; they are not replaced by the
    default because that would hide configuration mistakes.
    """
```

The comment distinguishes absence from invalid input instead of saying only
"fall back to default."

## Data Model Without Duplication

```python
class ExportRequest(BaseModel):
    """Parameters for one asynchronous export job."""

    destination: str = Field(description="Object-store URI for the result")
    overwrite: bool = Field(
        default=False,
        description="Replace an existing object at the destination",
    )
```

If the project documents fields in class docstrings rather than
`Field(description=...)`, follow that convention instead.

## Stable Phase Labels

A long function may benefit from a few semantic headings:

```python
# Normalize caller input before calculating the cache key.
normalized = normalize(request)

# Reuse only entries created under the current policy revision.
cached = cache.get(key_for(normalized, policy.revision))
```

Do not add `# Step 1`, `# Step 2`, and so on when the labels merely repeat
the next statement.

## Anti-Patterns

### Restating code

```python
# Iterate over users.
for user in users:
    # Add the user ID.
    ids.append(user.id)
```

The comments add no contract or rationale.

### Guessing intent

```python
# Sleep to prevent the database from being overloaded.
time.sleep(1)
```

Unless evidence establishes that rationale, document only observable behavior
or leave an open question.

### Duplicating annotations

```python
def find(user_id: int) -> User | None:
    """Find a user.

    Args:
        user_id (int): User ID.

    Returns:
        User | None: The user.
    """
```

A useful version would explain which identifier namespace is expected and why
`None` is returned.
