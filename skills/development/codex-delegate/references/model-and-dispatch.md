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

Two ways to run the canonical launch template from a host session. Choose on
the completion contract first and token economy second.

### The completion contract

Whoever launches the run owes the answer to "is it finished?". A delegation is
long enough that the host will do other things meanwhile, so the launch itself
has to be what wakes the host when the run exits. Otherwise the host reports
back while codex is still working, and the user is left asking whether it ever
finished.

A background shell satisfies this: it keeps running across turns and re-invokes
the launching session when the command exits (in Claude Code, Bash with
`run_in_background`). A subagent does not. A background child started inside a
courier outlives the courier's turn, and the courier's completion notification
fires when the *courier* stops — not when codex exits.

Measured on codex-cli 0.145.0: a courier launched an 8m14s research run, ended
its turn 74 seconds in, and was never re-invoked. The host got a "completed"
notification with seven minutes of the run still to go, and the user had to ask
by hand whether it had finished.

### A. Background shell in the launching session — the default

The session that owns the mission launches the canonical template in a
background shell and keeps working; the run's exit re-invokes it. Context cost
is small by construction — the template already sends stdout to `events.jsonl`
and stderr to `stderr.log`, so almost nothing reaches the transcript. Render
for progress when you want it, and verify when the exit wakes you.

### B. Courier subagent — delegation of the whole errand, and it must block

A dedicated subagent, in its own context, owns the run: it creates the run
directory and the `result.txt` provenance line, writes the packet it was handed
to `$RUN/prompt.md`, launches the canonical template, watches through the
renderer, and returns pointers — run directory, thread ID, the `result.txt`
line, and the `$RUN/report.md` path — plus a line or two of status.

Because its return is the host's only completion signal, **a courier must not
return while the run is live**: launch in the foreground and let the call
block. In Claude Code that caps a courier-dispatched run at the Bash timeout
ceiling of 10 minutes, so a longer mission belongs in pattern A.

Its posture is courier, not editor: hand back the file rather than a retelling
of it, and leave mission-level decisions — rewriting the packet, widening
authority, judging the result — with the main session. Inside that posture, use
judgment: fixing an obvious mechanical slip in the launch command, flagging a
run that died instantly, or retrying a clean transport failure are all fine
when reported plainly. A courier that fully re-reads and re-tells the report
has spent the context the pattern exists to save.

Set the courier's model explicitly to the host's light tier (in Claude Code,
Sonnet). A subagent inherits the parent session's model unless told otherwise,
so an unset model quietly runs the errand on the most expensive tier available
— the opposite of the pattern's purpose.

### Choosing

Default to A. It is what the wake-up semantics reward, and B saves less than it
looks: the packet is mission content, so the main session authors it either
way, and the run's noise already lands in files rather than in anyone's
context.

Reach for B when the host genuinely must not be interrupted, when several runs
are being shepherded at once, or when the courier has real work of its own
beyond launching — and only when the run fits inside the blocking ceiling.
Never build a polling or waiting wrapper around either.
