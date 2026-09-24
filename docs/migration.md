# Package ownership and source migration

Agent Skills provides harness, prompting, installation, delegation, coding, and artifact-production methods. [Gigio Pack](https://github.com/gigio1023/gigio-pack) retains project purpose, current understanding, constraints, adaptive plans, and continuity. [Research Credo](https://github.com/gigio1023/research-credo) owns research methods and operations. These remain separate repositories.

## Incoming from Gigio Pack

The following names and their helper resources move from Gigio's `skills/<name>/` into this repository's `skills/development/<name>/`:

- `orchestrate-subagents`
- `small-model-handoff`
- `fable5-model-routing`
- `git-worktree-setup`
- `commit-and-push`
- `draft-pr`
- `python-coding-standards`

The migration starts from Gigio main at `ada2fa6`. Earlier package history remains in Gigio. Orchestration and bounded handoff wording is adjusted to support the current decision round without requiring a fully fixed project plan.

## Outgoing to Research Credo

| Current source | Destination source |
| --- | --- |
| `skills/development/evaluation-operations/` | research-credo `skills/evaluation-operations/` |
| `skills/productivity/internal-source-research/` | research-credo `skills/internal-source-research/` |

The names and resources are preserved, including the reader-record refinements from the writer branch. No duplicate discoverable compatibility packages remain here. Research methods are independent of whether their result changes code.

## Renamed and removed on 2026-09-23

The owner stopped using GPT-5.6 models, and OpenAI publishes one prompting guide for the GPT-6 family.

| Before | After |
| --- | --- |
| `skills/development/gpt6-astra-prompting-guide/` | `skills/development/gpt6-prompting-guide/`, covering GPT-6 Astra and Sol |
| `skills/development/gpt56-sol-prompting-guide/` | Removed; GPT-6 Sol prompts use `gpt6-prompting-guide` |
| `gpt6-astra-model-routing` Codex roles `terra-scout`, `luna-clerk` | `sol-scout`, `sol-clerk`, both on `gpt-6-sol` |

The Skills CLI tracks installed skills by path, so an update does not rename them. After this change merges, install `gpt6-prompting-guide`, confirm it is discovered, and remove the old global names only when the owner asks: `npx --yes skills remove --global gpt6-astra-prompting-guide gpt56-sol-prompting-guide --yes`. Codex role files already copied to `~/.codex/agents/` keep their old names until they are replaced.

## Publication and installation

Merge the Research Credo destination first, then this change, then the Gigio source removals. The merged writer was installed and verified before the slop-aware-writing repository was archived on 2026-09-24. Review destination contents before removing source packages.

Publishing PRs does not install them. During a separately requested refresh, use `install-skill-pack` to select the available destination revision, add the moved names, and verify tracked repository/path metadata and the intended harness destinations. A same-name installed directory alone does not prove migration; old source metadata cannot follow a moved path automatically. Preserve customizations, avoid duplicate names, and never uninstall first or hand-edit installer locks.

The writer remains `technical-report-writing`; `share-internal-doc` was merged into it on 2026-09-24 as `references/sharing-and-delivery.md` and retired from Gigio Pack. `slop-aware-writing` and `korean-clarity` are merged into the writer; their repository was archived on 2026-09-24 and remains the MIT license source. See [writing composition](writing-skills.md).
