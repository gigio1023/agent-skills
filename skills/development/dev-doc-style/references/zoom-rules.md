# Zoom-Level Repair Patterns

Use only the section that matches the observed problem. These patterns are
examples, not mandatory syntax.

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

Do not split a sentence merely because it contains two clauses. Split when the
reader must disentangle separate claims or when a source interrupts the claim.

## Bullet

Use parallel items for parallel facts. Nest only when the parent label genuinely
groups several children.

```markdown
<!-- Hard to scan -->
- Runtime: Python 3.13, uv for dependencies, pytest for tests, Ruff for linting.

<!-- Easier to scan -->
- **Runtime**: Python 3.13.
- **Dependencies**: uv.
- **Checks**: pytest and Ruff.
```

A single compact bullet is better when the details form one unit. Avoid
mechanically converting every comma into a nested list.

## Section

The opening should help the reader act or understand, not announce that the
section exists.

```markdown
<!-- Weak -->
## Authentication

This section describes how authentication works in this project.

<!-- Useful -->
## Authentication

Set `API_TOKEN` before starting the server.

```bash
export API_TOKEN="replace-me"
```
```

Architecture and rationale sections may need a short explanatory paragraph
before a diagram or decision. "Code first" is not a universal rule.

## Page

Give the page one primary reader job. Supporting context is allowed when it
helps complete that job.

A README can contain orientation, a verified start path, and navigation. Move a
deep API catalogue or migration history only when another maintained page is a
better owner and links remain clear.

Do not split solely because a page crosses a line-count threshold.

## Cross-Page

Consolidate facts that are volatile, duplicated in full, and already drifting.

```markdown
<!-- Entry page -->
Run `uv run pytest` for the default suite. See
[test options](docs/testing.md) for markers and integration setup.
```

A short summary plus a link is not harmful duplication. Keep repetition where
the page must stand alone, especially safety procedure, setup prerequisite, or
offline reference material.

## Links and Surfaces

Prefer link text that names the destination's purpose:

```markdown
See [retry behavior](transport.md#retries).
```

Raw URLs and paths are fine when they are themselves data. Notes and collapsible
blocks are fine only if the renderer supports them and the content remains
discoverable and safe.
