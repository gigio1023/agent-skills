# Terminology

Use the English names and contextual meanings recorded here in the pack's skills, references, and documentation. Detailed entries live under `docs/terminology/`; preserve their usage conditions and scope.

## Common rules

- Names follow the harness documentation or paper that owns the concept. Explanations use plain English, the working language of this pack's skills.
- A word found in model-written prose is not evidence of usage. Check official documentation, maintainer writing, or papers before adopting a noun, and record the source.
- A decision to retire a word is an editorial choice for this pack's reader-facing prose. It is recorded with its date, scope, reason, and exceptions in [anti-patterns](docs/terminology/anti-patterns.md); it does not claim the word is wrong in another field.

## Representative terms

| Term | Concise meaning and scope | Reference |
| --- | --- | --- |
| subagent | An agent a lead spawns to handle a delegated task; the running instance. Claude Code, Codex, Cursor, and Anthropic's engineering writing all use it. | [R001](docs/terminology/references.md#r001), [R003](docs/terminology/references.md#r003), [R005](docs/terminology/references.md#r005) |
| subagent definition | The configured record that fixes a subagent's model, effort, tools, and instructions. Say "agent file" when pointing at its path. Codex calls the same thing a custom role or agent type. | [R002](docs/terminology/references.md#r002), [R004](docs/terminology/references.md#r004) |
| task | The unit of work a lead delegates; "delegated task" on first use when the parent task is also in view. | [R001](docs/terminology/references.md#r001), [R003](docs/terminology/references.md#r003) |
| dispatch | The act of handing a task to a subagent, and the one-line statement of its tier, `agent_type`, model, effort, source, and runtime status that the routing skills require. | [R010](docs/terminology/references.md#r010), [R011](docs/terminology/references.md#r011) |
| route | A standing assignment of a class of work to a model at an effort. Say "assignment" for one spawn's decision. The routing literature's word. | [R008](docs/terminology/references.md#r008), [R009](docs/terminology/references.md#r009) |
| tier | One of the four difficulty classes in the routing skills: mechanical collection, bounded execution, judgment-adjacent support, judgment core. Reserved for difficulty, never for a model class. | [R010](docs/terminology/references.md#r010), [R011](docs/terminology/references.md#r011) |
| role | Codex's noun for a named subagent configuration: the `[agents.<name>]` table and the role files under `agents/`. Use it in Codex-specific text. | [R004](docs/terminology/references.md#r004) |

## Index

- [Detailed terms](docs/terminology/terms.md)
- [Anti-patterns](docs/terminology/anti-patterns.md)
- [References](docs/terminology/references.md)
