# Research method migration

`internal-source-research` and `evaluation-operations` move from [agent-skills](https://github.com/gigio1023/agent-skills) to this repository without renaming their skill handles. Their reference resources move with them.

| Previous source | New source |
| --- | --- |
| `skills/productivity/internal-source-research/` in agent-skills | `skills/internal-source-research/` |
| `skills/development/evaluation-operations/` in agent-skills | `skills/evaluation-operations/` |

These packages were copied from the companion agent-skills writer branch at `ba51fcc1cecf2bfb64de39d907df21a14547cc9e`, retaining its reader-record improvements. Their earlier development remains in that repository's Git history. The same change added `credo-experiment`, `credo-dataset`, and `credo-evaluation` for experimental design, data suitability, and measurement, without duplicating campaign state management; the restructure below later reorganized them into `ml-experiment`, `evaluation-design`, and `evaluation-audit`.

## Publication order

This sequence is complete and kept as a record: the two source packages left agent-skills by 2026-09-17 (agent-skills #57).

Merge this destination before the companion agent-skills change removes the two source packages. Then merge the agent-skills change that receives Gigio's seven harness and coding helpers, before Gigio removes those sources. The slop revision companion can follow the writer's availability.

Draft publication is not installation. Existing copies continue to exist at their installed paths, but old tracked source paths will no longer be update targets after migration. During a separately requested refresh, use `install-skill-pack` to select the published repository and revision, reinstall these exact names from the new source, and verify their source metadata and intended harness destinations. Do not rely on a same-name directory alone or manually edit installation lock files. Avoid discoverable duplicate compatibility packages.

Existing project journals, libraries, run ledgers, and source archives remain project data. A skill refresh must preserve them and any user-customized installed content.

## Threat list ownership

The fixed list of ten failure modes moved from `skills/credo-taste/references/threat-list.md` to `skills/praxis-direction/references/threat-list.md` when the organization track was added. `credo-taste` hands the failure-mode pass to `praxis-direction`; an installation that carries only the paper track no longer includes the list.

## Restructure into eleven skills

The paper track regained its scope test, and the work track was reorganized around the moment in evaluation work: design, audit, and operation. The `credo-` prefix now marks exactly the paper track.

| Previous skill | Now |
| --- | --- |
| `credo-experiment` | `ml-experiment` |
| `credo-dataset` | training data in `ml-experiment`; eval cases and labels in `evaluation-design` |
| `credo-evaluation` | `evaluation-design`; readiness and trust verdicts in the new `evaluation-audit` |
| `credo-research` | `literature-research` |
| `credo-read-then-forget` | `literature-research`, Read one paper section |
| `praxis-setup` | `praxis-direction`, Set up or audit the profile section |

The topical references moved into the skill that owns their request. A refresh installs the eleven names and removes the six previous ones; project libraries under `research/`, journals, praxis profiles, and experiment records stay where they are.
