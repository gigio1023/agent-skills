# Harness Portability

Use this before adding syntax or behavior that may belong only to Claude Code or
Codex. The portable package follows the stricter common contract; adapters may
add user experience or enforcement without becoming required for correctness.

## Contents

- Shared loading model
- Discovery and frontmatter
- Locations and invocation
- Resources and script paths
- Tools, permissions, and side effects
- Subagents and long-running work
- Adapter placement

## Shared Loading Model

Both harnesses use progressive disclosure:

1. Skill metadata is visible for discovery.
2. The full `SKILL.md` loads when selected.
3. Supporting references and scripts are used as needed.

Once loaded, every line in the body consumes working context. Put the normal
path and routing map in `SKILL.md`; put detailed API material, examples, and
maintenance sources in directly linked resources.

## Discovery And Frontmatter

| Contract | Portable rule |
| --- | --- |
| Required metadata | Use only `name` and `description` in shared frontmatter |
| Name | Lowercase letters, numbers, and hyphens; maximum 64 characters |
| Description | Front-load what and when; include an adjacent NOT-for boundary; stay within 1024 characters |
| Body | Keep under 500 lines and preferably around 8KB or less |
| References | Link each one directly from `SKILL.md`; add a contents map to long files |

Codex budgets its initial skill listing and can shorten descriptions when many
skills are installed. Claude Code also truncates discovery text. Put the most
discriminative trigger in the first sentence; do not spend the opening on a
workflow summary.

Claude Code accepts optional frontmatter such as invocation control, tools,
arguments, path filters, forked context, and hooks. Codex supports optional
`agents/openai.yaml` policy, dependency, and interface metadata. Neither set is
the portable contract. Keep shared frontmatter at the two-field intersection.

## Locations And Invocation

| Concern | Codex | Claude Code |
| --- | --- | --- |
| Repo skill | `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| User skill | `$HOME/.agents/skills/<name>/SKILL.md` | `$HOME/.claude/skills/<name>/SKILL.md` |
| Explicit invocation | `$name` or the current skill picker | `/name` or the current skill picker |
| Implicit invocation | Matches `description` | Matches `description` and optional Claude-only discovery metadata |

Keep canonical source in the repository's documented package location. Use an
installer or verified symlink/copy to expose it to both harnesses. Installation
documentation may name these locations; the portable `SKILL.md` should not.

Do not tell an executing skill to invoke itself with `/name` or `$name`. Those
forms are for user and harness entry, not the task workflow.

## Resources And Script Paths

- Use forward-slash relative paths in the package.
- Say when a reference should be read and whether a script should be executed.
- Document commands from the skill root, or tell the agent to resolve the
  directory containing the active `SKILL.md` before running them.
- Do not require `${CLAUDE_SKILL_DIR}`, dynamic `!` command injection, a fixed
  Codex installation path, or the current project working directory in the
  portable path.
- Detect prerequisites and provide a safe fallback. Do not install global
  packages merely because a command is missing.

Claude Code adapters may use `${CLAUDE_SKILL_DIR}` or dynamic injection. Codex
adapters may declare dependencies in `agents/openai.yaml`. These can improve the
native experience but must not be the only runnable path.

## Tools, Permissions, And Side Effects

Tool names and approval systems differ. Portable prose names the capability:
read a file, search a repository, inspect a rendered artifact, query the
configured source, or run a non-destructive test. Name an exact CLI or API only
when it is part of the domain contract.

For MCP or connectors, describe the required service and capability. Put exact
namespace/dependency mapping in a harness adapter unless the package controls a
stable, fully qualified tool contract.

Claude Code hooks, `allowed-tools`, and invocation-control metadata can enforce
or narrow a workflow. Codex policies, approvals, config, and plugin metadata can
do similar work. A prompt instruction is not mechanical enforcement. If an
invariant must be guaranteed, ship a deterministic validator/hook adapter where
supported and keep the portable authority rule as defense in depth.

External writes, destructive changes, purchases, secret exposure, and material
scope expansion require explicit authority regardless of adapter availability.

## Subagents And Long-Running Work

Both harnesses can provide isolated workers, but availability, inheritance,
permissions, nesting, and communication differ. A portable skill states:

- which work is independent;
- the evidence packet each worker returns;
- ownership boundaries for shared files;
- a sequential fallback;
- that delegation does not broaden authority.

Do not hard-code a built-in subagent type. Claude Code subagents can start with
fresh context and preloaded skills; Codex subagents/threads follow the current
surface's configuration. Put native orchestration details in a dedicated
orchestration skill or harness reference.

For long work, specify sparse evidence-backed progress and a real completion
condition. Harness-specific user-message or progress channels are adapters for
that contract, not portable tool calls.

## Adapter Placement

Use these homes:

- `SKILL.md`: shared domain workflow and safety/evidence contract.
- `references/`: domain detail and dated model/harness maintenance material.
- `.claude/` docs or plugin metadata: Claude Code installation and native extras.
- `.codex/` docs or `agents/openai.yaml`: Codex installation and native extras.
- hooks or deterministic scripts: mechanical enforcement and repeatable checks.
- dedicated routing/orchestration skills: model, effort, cost, and agent topology.

If an adapter is removed, the skill should lose convenience or enforcement, not
its meaning, normal execution path, or safety boundary.
