# Model and Dispatch

Which model and reasoning effort a delegated run gets, and which of the two
host-side patterns launches it.

## Contents

- [Model and effort](#model-and-effort)
- [Fast mode](#fast-mode)
- [Sol packets](#sol-packets)
- [Internal parallelism](#internal-parallelism)
- [Dispatch patterns](#dispatch-patterns)

## Model and effort

Default: `gpt-5.6-sol` at `high` reasoning effort. A machine's global Codex
config may already set both, but a delegation should not silently depend on an
environment you have not read — when the environment default is unknown, pass
`-m gpt-5.6-sol` explicitly and record it on the `result.txt` provenance line.

`codex exec` has no reasoning-effort flag. Effort moves only through config,
which makes `-c model_reasoning_effort="…"` the second sanctioned `-c`
override, alongside `sandbox_workspace_write.network_access=true`. The rest of
the `-c` rule is unchanged: it must never touch `sandbox_mode` or the approval
policy, and any override you do use is declared visibly in your reply and
appended to the `result.txt` provenance line.

Effort follows the mission, not the model:

- **Bounded mechanical edits** — a rename, a mechanical migration, a fix whose
  shape is already known: `-c model_reasoning_effort="medium"`.
- **Standard implementation or investigation** — the default case:
  `-c model_reasoning_effort="high"`.
- **Adversarial review, hard debugging, judgment-heavy synthesis** — where the
  expensive failure is a missed consideration, not a slow run:
  `-c model_reasoning_effort="xhigh"`.

The key name and its accepted values belong to the CLI, not to this skill. If
a run rejects the override, trust `codex exec --help` and the current codex
config documentation over this list, and note the drift.

## Fast mode

Never chosen by default. A fast run — the family's fast variant, or the same
family at a lower effort — happens only when the user asks for speed, and the
user picks which of the two. Neither is a quiet substitution: name what you
ran and put it on the provenance line.

## Sol packets

Model-specific prompting is not restated here. When the packet targets a
Sol-family model, load the sibling skill `gpt56-sol-prompting-guide` (same
pack, `skills/development/gpt56-sol-prompting-guide/`) and shape the packet
with it before dispatch. This skill owns the mission contract — objective,
scope, authority, verification, response contract; that skill owns how the
prompt is worded for the model. On wording, the prompting guide wins; on
authority, this skill does.

## Internal parallelism

Codex can spawn its own subagents. When the mission has genuinely independent
parts — several modules to survey, several repositories to read, a test matrix
— grant that explicitly in the packet's Authority block instead of leaving it
implicit:

> You may spawn internal subagents to parallelize independent subtasks; the
> report stays single-authored.

The grant is per mission, not standing: for a tightly sequential mission, or
one whose whole value is a single careful pass, leave it out or write
`Internal subagents: not needed`. Either way nothing outside Codex changes —
same sandbox, same run directory, same host doing the verifying.

## Dispatch patterns

Two ways to run the canonical launch template from a host session.

### A. Courier subagent — the default

A dedicated subagent, in its own context, owns the codex run. Token economy is
the point: the courier's work is light, so it runs on the host's light tier
(in Claude Code, Sonnet) while the main session keeps its context for intent
and verification. Its usual shape:

1. create the run directory and the `result.txt` provenance line;
2. write the packet it was handed to `$RUN/prompt.md`;
3. launch the canonical template;
4. watch progress through the renderer;
5. return pointers — run directory, thread ID, the `result.txt` line, and the
   `$RUN/report.md` path — plus a line or two of status.

The default posture is courier, not editor: hand back the file rather than a
retelling of it, and leave mission-level decisions — rewriting the packet,
widening authority, judging the result — with the main session. Inside that
posture, use judgment: fixing an obvious mechanical slip in the launch
command, flagging a run that died instantly, or retrying a clean transport
failure are all fine when reported plainly. The reason to stay light is
practical, not ceremonial — a courier that fully re-reads and re-tells the
report has spent the context the pattern exists to save.

### B. Background shell

The main session launches the template in a background shell (in Claude Code,
Bash with `run_in_background`) and checks the renderer between other work. Do
not build a polling or waiting wrapper around it — that is true of both
patterns.

### Choosing

Default to A. Drop to B when the mission is trivial or short enough that its
noise will not crowd the main context, or when the harness offers no subagent
facility. Both launch the same command and produce the same run directory:
the choice is about where the run's noise lands, not about what Codex may do.
