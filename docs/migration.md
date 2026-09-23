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

## Publication and installation

Merge the Research Credo destination first, then this change, then the Gigio source removals. Install and verify the merged writer before archiving the slop-aware-writing repository. Review destination contents before removing source packages.

Publishing PRs does not install them. During a separately requested refresh, use `install-skill-pack` to select the available destination revision, add the moved names, and verify tracked repository/path metadata and the intended harness destinations. A same-name installed directory alone does not prove migration; old source metadata cannot follow a moved path automatically. Preserve customizations, avoid duplicate names, and never uninstall first or hand-edit installer locks.

The writer remains `technical-report-writing`; `share-internal-doc` remains in Gigio as the full internal-document entry. `slop-aware-writing` and `korean-clarity` are merged into the writer; their repository remains the MIT license source and will be archived after the merged skill is installed and verified. See [writing composition](writing-skills.md).
