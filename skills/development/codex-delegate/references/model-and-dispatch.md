# Model and Dispatch

Which model and reasoning effort a delegated run gets, and how the managing
subagent that launches it stays alive until it ends.

## Contents

- [Model and effort](#model-and-effort)
- [Fast mode](#fast-mode)
- [Sol packets](#sol-packets)
- [Internal parallelism](#internal-parallelism)
- [Dispatch — a managing subagent](#dispatch--a-managing-subagent)

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

## Dispatch — a managing subagent

The main session authors the packet and hands it to a dedicated subagent on
the host's light tier; the subagent manages the run and returns pointers. It
relays and manages — it never judges. Three seats, fixed:

- **Main session** — authors the packet, grants authority, judges the result.
  Mission-level work never drops below the main session's tier.
- **Managing subagent** — light tier (in Claude Code, Sonnet), model pinned:
  launches, watches, waits, returns. Cheap on purpose; its work is mechanical.
- **Codex** — frontier model, `gpt-5.6-sol` at `high` by default: does the
  mission. How deeply it may reason or opine there is the packet's grant, not
  this skill's ruling.

### The completion contract

Whoever launches the run owes the answer to "is it finished?". A delegation is
long enough that the host will do other things meanwhile, so the launch itself
has to be what wakes the host when the run exits. Otherwise the host reports
back while codex is still working, and the user is left asking whether it ever
finished.

A background shell in the launching session satisfies this: the harness
re-invokes that session when the command exits, and the completion wakes it
even from idle (verified live with a 75-second background probe — the idle
host resumed on its own at exit).

What fails is not the subagent but the wait. Measured live: a subagent
launched an 8m14s run with the harness's background facility, correctly, then
ended its turn to "wait for the notification". Background children do not
count as keeping a subagent alive, so it was marked complete 74 seconds in;
when codex exited, its completion notification fired on time but its owner no
longer existed. The orphaned notification fell into the host session's queue —
which an idle host does not consume — and sat unread for 22 minutes until the
next user message forced a turn. The host learned of completion from the user,
not from the run.

A subagent's own completion does wake an idle host (observed in the same
incident). That asymmetry is the whole design rule: a subagent's return is a
wake signal, an orphaned background task's notification is not — so a subagent
must still be alive when its runs end, i.e. it waits by blocking, never by
ending its turn.

### The subagent's job

It owns the delegation end to end: creates the run directories and
`result.txt` provenance lines, writes the packets it was handed, launches one
or several runs (concurrent writers in separate worktrees, per the concurrency
rules), watches through the renderer, runs the packets' mechanical
verification commands — exit codes, files existing, checks passing — and
returns a digest of pointers: run directory, thread ID, `result.txt` line, and
report path per run, with a line or two of status each. The main session sees
one call out and one digest back instead of per-run launch mechanics.

The one hard requirement: **stay alive until every run is terminal**, because
the subagent's own completion is the only wake-capable signal it can produce.
Launch codex in the background — a foreground launch is killed at the
harness's per-command ceiling — then hold the turn open with a bounded
foreground wait on the provenance file:

```bash
until grep -q '^exit=' "$RUN/result.txt"; do sleep 10; done
```

Verified live: a foreground until-loop with a real condition is permitted
where a bare `sleep N` is refused. One call is bounded by the per-command
ceiling, so a long run takes several waits in sequence — re-issue the same
loop until every `result.txt` is terminal. Ending the turn to "wait for the
notification" is the orphan trap in the incident above.

Posture: hand back the files rather than a retelling of them, and leave
mission-level decisions — rewriting packets, widening authority, judging
results — with the main session. Inside that posture, use judgment: fixing an
obvious mechanical slip in the launch command, flagging a run that died
instantly, or retrying a clean transport failure are all fine when reported
plainly. A subagent that fully re-reads and re-tells the reports has spent the
context the pattern exists to save.

Set the subagent's model explicitly to the host's light tier (in Claude Code,
Sonnet) — launching, waiting, and mechanical verification are light work. A
subagent inherits the parent session's model unless told otherwise, so an
unset model quietly runs the errand on the most expensive tier available.
The tier floor runs the other way for the mission itself: packet authoring,
result judgment, and anything mission-level stay at the main session's tier.

### Edge case

A seconds-long probe — a capability check, a smoke — may skip the subagent
and run inline or as a background shell in the main session, whose own
background completions do wake it (verified). Never build a polling wrapper
that returns between checks — the until-loop above is the wait itself, held
inside one live turn.
