> Imported on 2026-10-12 from [gigio-pack](https://github.com/gigio1023/gigio-pack) at `3b206a1`. Its skills now live under `skills/minimal/` and `skills/additional/` in this repository; the skill links below point at the original repository at that commit. This copy is kept as the source record.

# Gigio Pack

Keep a project's purpose, direction, current understanding, and next decisions available across sessions, models, and harnesses.

A project can be research, model development, dataset review, a benchmark, a document, or software. It can span repositories and servers. Progress may be a finding or a better-supported decision without a code change.

## Work from the next decision

PROJECT.md or an existing equivalent holds user-owned direction and an agent-maintained digest of current understanding. Plans detail the next useful work, then adapt to findings. Existing experiment records, research indexes, and operational logs keep their own jobs.

Fast follow-up checks within the current question and allowed resources can proceed. Changes of direction and long new work, such as a two-to-three-day activity, need a user decision unless already authorized. Cost, access, and other project limits still apply.

Use only the skills the request needs. Setup, planning, execution, and review are distinct responsibilities, not a mandatory sequence for every task.

An early discovery pass can combine short techniques within the same objective and authorized resources. `find-unknowns` returns the evidence and choices needed for the next action, without requiring setup, a fixed question count, or a prescribed brief layout.

## Skills

| Skill | Responsibility |
| --- | --- |
| [gigio-project-setup](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/gigio-project-setup) | Establish or audit purpose, direction, constraints, current understanding, and source locations |
| [gigio-write-plan](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/gigio-write-plan) | Detail the work needed for the next decision |
| [gigio-execute-plan](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/gigio-execute-plan) | Execute, interpret findings, and continue within the established grant |
| [gigio-review-results](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/gigio-review-results) | Assess progress and whether the next decision is supported |
| [find-unknowns](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/find-unknowns) | Resolve consequential gaps before expensive work |
| [deep-interview](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/deep-interview) | Interview when sustained requirements discovery is explicitly wanted |
| [session-handoff](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/session-handoff) | Write one file a successor executes: current state, next actions, and questions for the user |
| [curate-terminology](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/curate-terminology) | Settle contested names from project, paper, and competitor usage and record them with sources |
| [use-terminology](https://github.com/gigio1023/gigio-pack/tree/3b206a1/skills/use-terminology) | Apply recorded terms, local names, and wording decisions |

## Related capabilities

[agent-skills](https://github.com/gigio1023/agent-skills) supplies harness use, delegation, coding, Git delivery, writing, and visualization. [research-credo](https://github.com/gigio1023/research-credo) supplies research direction, literature, experiments, datasets, evaluation methods, and operations. Their methods can be used directly or within a requested Gigio project.

The repository split separates responsibility without prescribing a fixed sequence. Relevant companions are used when available; missing optional tooling does not require another framework or an unrequested install.

## Install

Historical; install from gigio-skills instead (see the [root README](../../README.md)).

Install selected skills, or this pack's nine skills, for the intended agents:

```bash
npx --yes skills add 'gigio1023/gigio-pack#main' --global --agent claude-code codex cursor --skill '*' --yes
```

Publication does not refresh installed copies. Use install-skill-pack when an installation or update is requested.

## Migration

Seven tool-oriented skills moved to agent-skills with their existing names on 2026-09-17: orchestrate-subagents, small-model-handoff, fable5-model-routing, git-worktree-setup, commit-and-push, draft-pr, and python-coding-standards. See [migration](migration.md) for the moved packages and installation-source changes.

Old plans remain readable. Their known dependencies and completed records still matter; future stages can be revised as findings arrive. No bulk conversion of project files is required.

## Maintenance

Skills and project records are readable Markdown. The pack adds no daemon, database, or required runtime. Keep original data and confidential work out of the public skill sources.

Read [principles](principles.md), [rule ledger](rule-ledger.md), [decisions](decisions.md), and [contributing](CONTRIBUTING.md) when changing the pack. The terminology pair reaches every task in a project through the instruction snippet in curate-terminology, not through its descriptions.
