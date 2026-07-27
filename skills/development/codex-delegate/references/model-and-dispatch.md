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

### A. Background shell in the launching session — for a single run

The session that owns the mission launches the canonical template in a
background shell and keeps working; the run's exit re-invokes it, even from
idle. Context cost is small by construction — the template already sends
stdout to `events.jsonl` and stderr to `stderr.log`, so almost nothing reaches
the transcript. Render for progress when you want it, and verify when the exit
wakes you. For one bounded run this is the cheapest correct dispatch: the
packet is mission content the main session authors either way, and a subagent
would add spin-up without removing work.

### B. Managing subagent — the pattern for scale

Delegating in bulk is where a dedicated subagent earns its place. It owns the
delegation end to end: creates the run directories and `result.txt` provenance
lines, writes the packets it was handed, launches one or several runs
(concurrent writers in separate worktrees, per the concurrency rules), watches
through the renderer, runs the packets' mechanical verification commands, and
returns one digest of pointers — run directory, thread ID, `result.txt` line,
and report path per run — with a line or two of status each. The main session
sees one call out and one digest back instead of per-run launch mechanics.

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

### Choosing

One bounded run → A: the wake path is proven and nothing is saved by
indirection. Several runs, a campaign, or a main session that must stay clean
for other work → B, with the blocking wait above. Both launch the same
template and produce the same run directories. Never build a polling wrapper
that returns between checks — B's until-loop is the wait itself, held inside
one live turn.
