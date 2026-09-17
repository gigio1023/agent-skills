# Types and Enums

Read this when defining types, integrating a typed SDK, selecting a data representation, replacing string constants, or changing enum values. Apply the Python 3.12+ baseline without silently breaking an existing support requirement.

## Make annotations explicit

Annotate every function and method parameter and return, including private helpers and `-> None`. The implicit `self` and `cls` receivers may retain their normal form; use `Self` when a return type depends on the concrete subclass. Annotate model fields, instance and class attributes, module constants, and local variables at declaration or first assignment. Keep element types explicit and use `ClassVar` for actual shared class state. A plainly inferable right-hand side is not a reason to omit a declaration's type.

Use `list[T]`, `dict[K, V]`, `set[T]`, `tuple[...]`, and `T | None`, and import abstract interfaces such as `Sequence` from `collections.abc`. Use Python 3.12's `type Alias = ...` and type-parameter syntax when an alias or generic is useful; do not add them just to make the code look advanced. Do not use `typing.List` or `typing.Dict` in new annotations. Check runtime annotation consumers before changing forward references; `typing_extensions` cannot make newer parser syntax work on older Python.

Python does not allow an annotation directly in every binding position. For tuple unpacking, loops, `with ... as`, and `except ... as`, declare the named variables with annotations before the binding in the same scope. Use an explicitly typed loop or helper when a comprehension or lambda would hide declarations that need annotations. Do not generate invalid syntax or change variable lifetime accidentally. Imports, enum members, type aliases, and implicit receivers are not ordinary local-value declarations; keep their language-defined forms rather than decorating every identifier with a colon.

For complex external modules such as the OpenAI SDK, inspect the installed version's public types and method signatures. Import and annotate the actual client, request parameters, response, pagination, and stream/event types, including local bindings. Preserve sync versus async and streaming versus non-streaming distinctions. SDK-owned `TypedDict` inputs or model classes are a necessary interface exception, not a reason to recreate their schemas or replace precise types with `dict[str, Any]`. Do not invent an import path from memory or copy a vendor model merely to annotate it. If typing is genuinely absent or wrong, keep the smallest verified adapter or local stub, state the limitation beside it, and avoid letting `Any` spread into application models.

A checker accepting inferred types does not prove this annotation policy is met. Inspect changed declarations as well as running the configured checker. Narrow values or fix an inaccurate interface before adding a cast or suppression.

## Choose the representation

| Need | Usually fits | Limit |
| --- | --- | --- |
| Application-owned structured record, internal or external | Pydantic `BaseModel` | Default; reuse a model with the same meaning instead of duplicating representations |
| Closed, named string values used at runtime | `enum.StrEnum` | Python 3.11+; values must remain stable when persisted or transmitted |
| Closed values used only in annotations | `Literal` | No runtime validation by itself; useful for discriminators when a schema requires literals |
| Values an external provider may extend | `str` or a validated value object | Validate documented syntax without silently narrowing an open vocabulary |
| Nominal distinction between same-shaped identifiers | `NewType` | A static distinction, not runtime validation or a runtime class |
| Opaque named values that should not compare as strings | `Enum` | Use an explicit conversion when an external representation is needed |
| Stateful service or resource owner, not a data record | Ordinary class | Do not turn clients, locks, or file handles into data models just for uniformity |
| Framework-required dataclass or dictionary-shaped interface | Required dataclass, `TypedDict`, or SDK type | Exception only; identify the concrete requirement near the use |
| A genuine lookup table with dynamic keys | `dict[K, V]` | Mapping semantics, not an unnamed record with a fixed set of fields |
| A structural interface between implementations | `Protocol` | Use for an actual interface, not as another data-model representation |

Dataclasses, `TypedDict`, and record-shaped dictionaries are not equal default alternatives to Pydantic in this pack. Required interoperability, an existing compatibility promise, or a measured runtime constraint can justify them; taste, fewer imports, and speculative performance cannot. Converting a model to the representation an external API requires at the boundary does not create a competing internal model.

## Keep enum values stable

The following example separates internal member names from external values and annotates local declarations:

```python
from enum import StrEnum


class JobState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"


def parse_job_state(raw: str) -> JobState:
    state: JobState = JobState(raw)
    return state


def parse_job_states(raw_states: list[str]) -> list[JobState]:
    states: list[JobState] = []
    raw_state: str
    for raw_state in raw_states:
        state: JobState = parse_job_state(raw_state)
        states.append(state)
    return states


assert parse_job_state("queued") is JobState.QUEUED
assert JobState.QUEUED.value == "queued"
assert parse_job_states(["queued", "running"]) == [
    JobState.QUEUED,
    JobState.RUNNING,
]
```

Parse strings at the input boundary and use members consistently inside typed code. Unknown closed-set values should produce the boundary's documented error, not be mapped to a plausible success or active state. If unknown values must survive forwarding, represent that requirement explicitly rather than coercing them into an enum.

At output, emit the defined value through `.value` or a serializer whose behavior is verified. `StrEnum` is a `str` subclass, but an API that requires exactly `str` may need `str(member)` or `.value`. String operations on a member return ordinary strings. Member names, repr output, and incidental enum iteration order are not substitutes for an external schema.

`auto()` is appropriate only when the concrete value has no external meaning. With standard-library `StrEnum`, it lowercases the member name. A rename can therefore change stored data without an obvious string edit.

## Compatibility changes

Before replacing an enum implementation or value, inspect API payloads, database mappings, configuration, event consumers, generated schemas, and existing fixtures that depend on it. Preserve old accepted values until the requested migration defines how readers and writers move. Where a transition accepts legacy spellings, keep acceptance aliases separate from the canonical output and test both. A Python enum alias alone does not define a producer/consumer rollout or database migration.

Distinguish `from enum import StrEnum` from `from strenum import StrEnum`. The third-party package's base `StrEnum` preserves member-name case for `auto()`, while the standard-library class lowercases it. Do not replace the import without checking actual values. For Python below 3.11, preserve the repository's existing approach; an explicit `class Status(str, Enum)` can represent string values, but its `str()` and formatting behavior are not automatically identical to standard-library `StrEnum`.

## Sources and local choices

Checked 2026-09-10. These sources establish language behavior; representation choices and stable-value requirements above are this pack's policy.

- [Python enum reference](https://docs.python.org/3/library/enum.html): member names and values, `StrEnum`, `auto()`, exact-string caveat, and version-dependent membership behavior. Construct the enum to parse a value instead of relying on containment behavior across Python versions.
- [Python typing reference](https://docs.python.org/3/library/typing.html): `Literal`, `NewType`, `TypedDict`, `Protocol`, and annotation-version requirements.
- [Python 3.12 typing](https://docs.python.org/3.12/library/typing.html) and [PEP 526](https://peps.python.org/pep-0526/): modern annotation forms and variable-binding syntax. Requiring explicit locals is the owner's preference, not a Python requirement.
- [Python dataclasses reference](https://docs.python.org/3/library/dataclasses.html): generated methods, frozen instances, and hashing conditions.
- [Third-party StrEnum reference](https://strenum.readthedocs.io/en/latest/api_ref.html): the separate package's value-generation behavior.

Recheck the affected API when the repository changes its Python support range or enum implementation. The checked date is not a requirement to browse for every Python edit.
