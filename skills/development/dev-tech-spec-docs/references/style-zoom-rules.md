# Style Zoom Repair Patterns

Use the smallest section that matches the observed documentation problem. The
patterns are examples, not mandatory syntax.

## Sentence

Keep the main assertion visible and preserve conditions that affect truth.

```markdown
<!-- Dense -->
The client retries writes, when retry mode is enabled, after transient failures,
as described in the transport guide.

<!-- Clear -->
When retry mode is enabled, the client retries writes after transient failures.
See [retry behavior](transport.md#retries).
```

Do not split a sentence merely because it has two clauses. Split when readers
must disentangle separate claims or a source interrupts the claim.

## Bullet

Use parallel items for parallel facts. Nest only when a parent genuinely groups
several children.

```markdown
<!-- Hard to scan -->
- Runtime: Python 3.13, uv for dependencies, pytest for tests, Ruff for linting.

<!-- Easier to scan -->
- **Runtime**: Python 3.13.
- **Dependencies**: uv.
- **Checks**: pytest and Ruff.
```

Keep one compact bullet when the details form one unit. Do not convert every
comma into a list.

## Section

The opening should help the reader act or understand.

```markdown
<!-- Weak -->
## Authentication

This section describes how authentication works in this project.

<!-- Useful -->
## Authentication

Set `API_TOKEN` before starting the server.
```

Architecture and rationale sections may need explanation before a diagram or
decision. “Command first” is not universal.

## Page

Give the page one primary reader job. A README can orient, provide a verified
start path, and link deeper. Move an API catalogue or migration history only
when another maintained page is a better owner and navigation remains clear.

Do not split solely because a page crosses a line-count threshold.

## Cross-Page

Consolidate facts that are volatile, duplicated in full, and already drifting.

```markdown
Run `uv run pytest` for the default suite. See
[test options](docs/testing.md) for markers and integration setup.
```

A summary plus a link is useful duplication. Keep required local context in
safety procedures, setup prerequisites, and offline reference material.

## Links and Renderer Surfaces

Prefer descriptive link text such as `[retry behavior](transport.md#retries)`.
Raw URLs and paths are fine when they are data. Introduce notes, tabs, diagrams,
or collapsible blocks only when the renderer supports them and hidden content
remains discoverable and safe.
