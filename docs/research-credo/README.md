> Imported on 2026-10-12 from research-credo at `6217cd0`. Its skills now live under `skills/minimal/` and `skills/additional/` in this repository; the skill links below point at the skill in this repository that now carries each package's duty; the original repository is archived and private. This copy is kept as the source record. This repository, including the imported skills, is [MIT-licensed](../../LICENSE).

# Research Credo

Eleven skills in three tracks, split by who reads the result. The paper track answers to reviewers and a venue and holds one researcher's credo at its full bar. The work track answers to the person deciding whether to launch, ship, adopt a model, or tell a customer, and is split by the moment in the work. The organization track sharpens an agenda into a resourced bet. A paper can arise inside a company and a company eval is not a paper, so the split follows the deliverable, not the workspace.

## Paper track

Only for work aimed at a paper or a publishable research claim, at the essay's bar: one idea, a conclusion beyond a number going up, a result months ahead of the next person, and unreasonable effort. `credo-taste` and `credo-journal` run only when invoked (`/credo-taste` in Claude Code, `$credo-taste` in Codex) because they interview the user or write to the journal; the other two trigger on a paper or a LaTeX submission.

| Skill | Use it to |
| --- | --- |
| [credo-taste](../../skills/additional/credo-taste/) | Choose a research direction, decide whether to continue, pivot, or stop, or judge whether a work result could become a paper |
| [credo-paper-plan](../../skills/additional/credo-paper-plan/) | Plan the argument, claim-evidence map, closest prior work, and figures; critique a draft; plan the response to peer reviews |
| [credo-journal](../../skills/additional/credo-journal/) | Record research ideas, predictions, and hindsight |
| [credo-release](../../skills/additional/credo-release/) | Check a paper before submission or release |

Paper claims need evidence appropriate to their type. Abstracts state specific quantitative, theoretical, or qualitative contributions and preserve the assumptions and uncertainty that affect their meaning.

## Work track

Everyday research and evaluation work, meant to be selected in ordinary tasks, so it carries no `credo-` prefix. The three evaluation skills split by moment: design builds the instrument, audit decides whether it or its result can be trusted, and operations runs an approved campaign. The design skill never declares its own instrument ready.

| Skill | Use it to |
| --- | --- |
| [literature-research](../../skills/minimal/literature-research/) | Read a paper for a purpose, check prior art for a claim, survey open models or datasets at pinned revisions, and preserve sources |
| [ml-experiment](../../skills/minimal/ml-experiment/) | Design, run, or interpret training, adaptation, serving, or reproduction experiments and their training data |
| [evaluation-design](../../skills/minimal/evaluation-design/) | Design what an eval measures: failure modes, cases and labels, code checks, judges and their validation, comparison conditions |
| [evaluation-audit](../../skills/minimal/evaluation-audit/) | Give a launch, hold, or report verdict on a built eval, judge, harness, scoring change, or result, including results bound for a customer |
| [evaluation-operations](../../skills/minimal/evaluation-operations/) | Operate approved evaluation campaigns with durable attempt and result records |

| Request | Owner |
| --- | --- |
| Design or redesign an eval, its cases, or its judge; validate a judge against new labels | `evaluation-design` |
| Is this eval, harness, judge, or scoring change ready; can this result be trusted or shown to a customer | `evaluation-audit` |
| Run, resume, monitor, or diagnose an approved campaign | `evaluation-operations` |
| Adapt or train a model; compare serving configurations before a full run | `ml-experiment` |
| Which open models or datasets exist; has this claim been done before | `literature-research` |
| Could this work result become a paper | `credo-taste` |

`literature-research` keeps fetching, hashing, and file checks apart from source selection, triage, reading, and prior-art judgment when it delegates.

Adversarial evaluation lives in references inside the evaluation skills rather than in a skill of its own, because adversarial cases run through design, audit, and operation alike rather than forming a separate moment. Harness feature work, eval framework choice, infrastructure, and incidents are outside the pack.

## Organization track

| Skill | Use it to |
| --- | --- |
| [praxis-direction](../../skills/minimal/praxis-direction/) | Sharpen an agenda into one bet, run the failure-mode pass on a new system, or set up and audit the praxis profile |
| [internal-source-research](../../skills/minimal/internal-source-research/) | Reconstruct work context from authorized internal sources |

The organization track runs when someone asks for it. Its skills are public and generic; what only the organization knows lives in a one-page `praxis-profile.md` in the organization's own workspace, written and read by praxis-direction. The [template](../../skills/minimal/praxis-direction/references/profile-template.md) shows the fields with a synthetic example. Nothing from a real organization belongs in this repository.

Internal research distinguishes mechanical retrieval from source selection, critical reading, and synthesis. The active routing policy owns model and effort choices. Delegation preserves the task's source, provider, and external-action boundaries.

## Install

Historical; install from gigio-skills instead (see the [root README](../../README.md)).

```bash
npx --yes skills add gigio1023/research-credo \
  --skill '*' --agent claude-code codex --global --yes
```

Omit `--global` for a project install or replace `'*'` with selected names, for example the work and organization tracks alone for a company workspace. Installation does not enable all methods in every conversation. Adapt [AGENTS.source.md](AGENTS.source.md) into project instructions only when setup is requested; ask praxis-direction to set up the profile once per organization, outside the installed package.

An install from before this restructure still carries six names that no longer exist. Remove them after installing so the old and new sets are not both discoverable:

```bash
npx --yes skills remove credo-experiment credo-dataset credo-evaluation \
  credo-research credo-read-then-forget praxis-setup --global --yes
```

## Repository boundaries

Gigio Pack owns project purpose, current understanding, constraints, adaptive plans, and continuity across repositories and sessions. [Agent Skills](https://github.com/gigio1023/agent-skills) owns harness operation, prompting, installation, delegation, coding helpers, and artifact production. Research Credo owns research and evaluation methods.

[Migration](migration.md) records the incoming packages, the restructure into eleven skills, and the coordinated publication and installation sequence. The earlier [six-skill diagram](research-credo.svg) is a historical view of the initial collection.

## Development and provenance

```bash
npx --yes skills add . --list --full-depth
```

Discovery should find eleven unique names. Validate changed skills and their resources. Package validation and illustrative scenarios are not behavioral evaluations.

The original collection was independently inspired by Nicholas Carlini's [research essay](https://nicholas.carlini.com/writing/2026/how-to-win-a-best-paper-award.html) and [research log](https://nicholas.carlini.com/writing/2024/my-research-logfile.html); not affiliated. Method references identify their own sources. Licensed under this repository's [MIT license](../../LICENSE).
