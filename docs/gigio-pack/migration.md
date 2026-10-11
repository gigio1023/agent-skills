# Repository Responsibilities and Migration

The migration completed on 2026-09-17 and keeps the three repositories independent. Gigio maintains project context; agent-skills maintains reusable execution and production capabilities; research-credo maintains research methods.

## Moved packages

| From Gigio Pack | Destination |
| --- | --- |
| orchestrate-subagents | agent-skills/skills/development/orchestrate-subagents |
| small-model-handoff | agent-skills/skills/development/small-model-handoff |
| fable5-model-routing | agent-skills/skills/development/fable5-model-routing |
| git-worktree-setup | agent-skills/skills/development/git-worktree-setup |
| commit-and-push | agent-skills/skills/development/commit-and-push |
| draft-pr | agent-skills/skills/development/draft-pr |
| python-coding-standards | agent-skills/skills/development/python-coding-standards |

Names and helper resources are preserved. No duplicate discoverable compatibility packages remain in Gigio. Existing local project records are not migrated or deleted.

## Publication and installation

The three pull requests merged on 2026-09-17 in dependency order: research-credo #5, agent-skills #57, then Gigio Pack #22. The agent-skills change also moved evaluation-operations and internal-source-research into research-credo.

Use the existing install-skill-pack workflow to add the moved names from the destination repository and verify that the installed source metadata points there. Same-name installs may overwrite the old deployed copy: preserve local customizations first. A source removal alone does not remove an installed skill or update its tracked origin.

Installations are separate from PR publication. Do not uninstall first or install two competing copies of the same name.

## Existing plans and shared documents

Old plan fields remain readable. No migration script rewrites user goals, results, or active jobs. New rounds use the current understanding and next decision rather than demanding all future stages.

General document methods live in copydesk. share-internal-doc was retired on 2026-09-24; its recipient, source-access, sharing-pass, and delivery rules moved verbatim to that writer's `references/sharing-and-delivery.md` in agent-skills. Remove the installed package with the Skills CLI; a request that names share-internal-doc is served by the writer. Preserve existing project source workflows and useful figures.

The writer was renamed from `technical-report-writing` to `copydesk` in agent-skills on 2026-09-24; `docs/decisions.md` keeps the name in use at each decision.
