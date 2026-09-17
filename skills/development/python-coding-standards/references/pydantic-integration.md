# Pydantic Integration

Read this when the task changes Pydantic models, validation, or serialization. Pydantic-specific modeling guidance comes from the official external `pydantic` skill; the Python and module-design rules in this package are authored locally. This pack's Pydantic-first representation policy takes precedence over optional alternatives in upstream examples; use upstream guidance for correct library behavior.

## Load the official skill

Use the installed `pydantic` skill when its source is the official [pydantic/skills repository](https://github.com/pydantic/skills). The reviewed source is [skills/pydantic/SKILL.md at 9e9390ee24d44b32cf5379c58acaebd7563f5f86](https://github.com/pydantic/skills/blob/9e9390ee24d44b32cf5379c58acaebd7563f5f86/skills/pydantic/SKILL.md), checked 2026-09-10. Read it for field constraints, validators, coercion, model hierarchies, and serialization choices rather than copying its API guide into this package.

If the skill is unavailable locally, read that upstream file for the current task without installing it. If upstream retrieval is unavailable, use the version-matched official Pydantic documentation and report that the external skill could not be loaded; continue work whose behavior can be verified locally. A missing skill is not a reason to add dependencies or guess an unfamiliar API. Match advice to the project's installed Pydantic version. A newer installed skill may be used after checking its relevant API assumptions; do not silently upgrade the application to match it.

The official `building-pydantic-ai-agents` skill serves applications using `pydantic_ai`; it is not a substitute for general `BaseModel` work. This integration does not require Pydantic AI, Logfire, a cloud account, or the other skills in the upstream repository. Skill installation and Python package installation are separate operations.

## Local modeling and boundary policy

Default to Pydantic v2 `BaseModel` for application-owned structured data, including internal records and external validation or serialization. Reuse the same model across a boundary when the meaning and exposure rules are unchanged. Do not create parallel `TypedDict`, dataclass, dictionary, and Pydantic versions of one record. Alternative representations require a specific need such as an SDK input type, a framework's dataclass requirement, a genuine dynamic-key mapping, an existing compatibility promise, or a measured constraint. Keep the reason near the exceptional code. A v1 application needs a scoped migration before adopting incompatible APIs; do not silently change a supported dependency range.

Pydantic-first modeling does not mean every class inherits `BaseModel`: services and resource owners are behavior, not data records. Prefer simple models with explicitly annotated fields, and explain non-obvious field semantics, units, defaults, or invariants in the model docstring or appropriate field description. A name and type that already explain the field need no paraphrase. Keep custom validators and shared base models limited to real shared behavior; do not build a model framework for anticipated needs.

Choose unknown-field handling deliberately:

| Boundary requirement | Appropriate policy |
| --- | --- |
| Owned input with a closed schema | Usually `extra="forbid"` |
| Independently versioned input whose unknown fields may safely be discarded | `extra="ignore"`, with that loss intentional |
| Data that must retain unknown fields for forwarding, round trips, or audit | `extra="allow"` or preservation of the original payload alongside the validated view |

Select strictness by source and field. Configuration text and JSON do not necessarily share coercion requirements. Test allowed and rejected values; neither blanket strictness nor silent default coercion settles the intended behavior.

Keep enum members in runtime models unless a specific existing interface requires primitive values. Do not set `use_enum_values=True` on a shared base model just to produce JSON: it changes values during validation. Prefer an explicit JSON-compatible dump or JSON-text serialization at output, and test the actual result. A localized primitive-storage exception must also handle enum defaults consistently.

Do not treat `model_construct()` or `model_copy(update=...)` as validation of new untrusted values. Validate the input through the intended boundary. Keep authorization and I/O outside schema validation; valid fields do not imply an allowed action. Select output fields deliberately so internal or subclass-only data is not exposed accidentally.

Use `TypeAdapter` when a boundary needs validation of a container, union, or an already-required non-model type. It is a validation/serialization adapter, not a field annotation or a reason to choose `TypedDict` or dataclasses for new application records.

When changing these behaviors, test the affected field names and aliases, unknown-field retention, coercion, enum values and runtime types, rejected input, and output exposure. Add only cases relevant to the change; do not duplicate existing coverage.

## Source scope

These official references were checked on 2026-09-10 and supplement the external skill's coverage:

- [Configuration](https://pydantic.dev/docs/validation/latest/api/pydantic/config/): `extra`, `use_enum_values`, and validation of defaults.
- [Serialization](https://pydantic.dev/docs/validation/latest/concepts/serialization/): Python mode versus JSON mode, aliases, and subclass serialization.
- [Strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/): call, field, and model-level strictness, including input-source differences.
- [Models](https://pydantic.dev/docs/validation/latest/concepts/models/): model construction and validation behavior.
- [TypeAdapter](https://pydantic.dev/docs/validation/latest/concepts/type_adapter/): validation and serialization without defining a `BaseModel`.

The upstream skill is MIT-licensed and remains external. This package contains no vendored copy, updater, or installer. Install instructions belong to the pack's distribution documentation, and using this skill does not refresh global skill directories.
