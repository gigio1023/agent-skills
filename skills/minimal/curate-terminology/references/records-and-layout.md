# Records and Layout

Paths are relative to the consuming project's root.

```text
terminology.md            index: terms, local names, wording decisions, topic links
docs/terminology/
  <topic>.md              one Terms table per topic once the root grows
  references.md           source records only
```

## Root index

```markdown
# Terminology

Terms follow the field's standard usage; meanings are in <reader language>. Sources are in [references](docs/terminology/references.md).

## Terms

| Term | Meaning | Elsewhere called | Reference |
| --- | --- | --- | --- |
| subagent definition | The configured record that fixes a subagent's model, tools, and instructions | Codex: role; Claude Agent SDK: `AgentDefinition` | [R002](docs/terminology/references.md#r002) |

## Local names

| Name | Meaning here | Field meaning | Audience | Confirmed |
| --- | --- | --- | --- | --- |
| Atlas | The internal evaluation service | none (proper name) | Internal; explain at first use for customers | 2026-10-03, user ([R010](docs/terminology/references.md#r010)) |

## Wording decisions

| Avoid | Use instead | Scope | Exceptions | Decided |
| --- | --- | --- | --- | --- |
| lane | subagent, task, route, or tier, by sense | Reader-facing prose in this repository | Quotations, Mermaid syntax, SIMD lanes | 2026-09-20, user ([R011](docs/terminology/references.md#r011)) |

## Topics

- [Agents](docs/terminology/agents.md)
```

The example rows show the shape; replace them with the project's own entries.

## Rules for rows

- A concept has one row in one table. When the root Terms table passes about 40 rows, move a topic's rows to `docs/terminology/<topic>.md` with the same columns and link it under Topics. Wording decisions stay in the root because they apply to all prose.
- An unresolved row starts its Meaning with "Unresolved:" and names what would settle it.
- A recurring misuse gets one bullet under its table: the term in bold, then one line.
- A wording decision is the user's editorial choice for its scope. It does not claim the word is wrong in other fields. A later decision supersedes it by a new row that names the old one; the old row is not silently edited.
- Links from the root use `docs/terminology/references.md#r001`; links from a topic file use `references.md#r001`.

## Reference records

`docs/terminology/references.md` holds one record per source and nothing else. IDs and anchors stay stable across revisions.

```markdown
<a id="r002"></a>
## R002 Claude Agent SDK, "Subagents"

- Anthropic, product documentation: https://code.claude.com/docs/en/agent-sdk/subagents
- Checked 2026-09-20; passage: the `AgentDefinition` type
- Supports: subagent definition
```

Every source named under Elsewhere called has a record. A user decision is a record with its date and the decision in one line. A source that was not actually read is not recorded as support.

## Existing collections

An existing collection keeps its layout and IDs until the user asks to change them. When the user asks to prune one, remove rows that fail the inclusion test, including sentence patterns, project explanations, and "do not write" advice; reference records may stay. Keep recorded user decisions and confirmed local names.
