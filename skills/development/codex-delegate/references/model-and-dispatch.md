# Model and Dispatch

Which model, reasoning effort, and speed tier a delegated run gets, and who
owns the run once it is launched.

## Contents

- [Model and effort](#model-and-effort)
- [Speed — the Fast tier](#speed--the-fast-tier)
- [Sol packets](#sol-packets)
- [Internal parallelism](#internal-parallelism)
- [Dispatch — durable runs, disposable watchers](#dispatch--durable-runs-disposable-watchers)

## Model and effort

Default: `gpt-5.6-sol` at `high` reasoning effort. A machine's global Codex
config may already set both, but a delegation should not silently depend on an
environment you have not read — pass `-m gpt-5.6-sol` explicitly and record it
on the `result.txt` provenance line.

`codex exec` has no reasoning-effort flag. Effort moves only through config,
which makes `-c model_reasoning_effort="…"` a sanctioned `-c` override. The
rest of the `-c` rule is unchanged: it must never touch `sandbox_mode` or the
approval policy, and any override you use is declared visibly in your reply
and appended to the provenance line.

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

## Speed — the Fast tier

Codex exposes a service tier its UI calls Fast. In the CLI's own model
registry it is `{"id": "priority", "name": "Fast", "description": "1.5x speed,
increased usage"}`. The GPT-5.6 family (sol, terra, luna) carries it, as do
5.5 and 5.4; 5.4-mini and 5.2 do not, and no model enables it by default
(`default_service_tier` is null).

It rides the third sanctioned `-c`: `-c service_tier="priority"`, declared and
recorded like the others.

**Keep it on.** Speed and reasoning are independent dials. Fast buys
wall-clock at the price of quota and changes nothing about how hard the model
thinks, so it never trades against `model_reasoning_effort` — a `xhigh`
adversarial review can and should also be Fast. Turn it off when a run is long
and unhurried and the remaining quota matters more than the wait.

A machine's global config may already set the tier, which is precisely why the
template passes it explicitly.

Verifying it applied, without guessing: an unsupported value produces an
`error` item — `Configured service tier … is not advertised as supported for
model … and will be omitted from requests` — and the run continues anyway. The
absence of that item is therefore positive evidence that the tier reached the
request (verified on codex-cli 0.145.0, both branches).

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

## Dispatch — durable runs, disposable watchers

One rule carries the whole design: **make the expensive thing durable and the
cheap thing disposable.** A run is expensive — a frontier model working for
minutes, often with edits already on disk. Whatever watches it is cheap.

The harness kills a command's entire process group. Measured with a 15-second
command ceiling: a child started with `&` died with the command, a `nohup`
child died with it too, and only a child in a new session survived. Any launch
that leaves codex inside the launcher's group therefore couples the two. When
the launcher is killed the run dies mid-turn, `result.txt` never receives its
terminal line, and the state becomes indistinguishable from "still working".
That is the failure this skill hit twice in real use, once losing a run that
had already written a 25 KB report and six patches.

The detached launch in `SKILL.md` removes the coupling. `perl` forks, the
child calls `setsid`, and the run lands under pid 1 in its own session
(verified: PPID 1, PGID equal to its own pid). A real 53-second run survived
its launcher being SIGTERMed at 15 seconds and appended its own `exit=0`.

With the run durable, waiting becomes trivial. Arm a background shell in the
session that wants the notification, holding one condition loop:

```bash
until grep -q '^exit=' "$RUN/result.txt"; do sleep 10; done
```

Its exit is the completion signal: the harness re-invokes the session that
owns it, and that wakes an idle host (verified with a 75-second probe). If the
watcher is killed first, nothing is lost — re-arm it, or just read `--status`.

Ownership is the one subtlety. Arm the watcher from the session that wants the
notification, because an orphaned background task's notification cannot wake
anything: it queues unread until the next user message forces a turn, measured
at 22 minutes in one incident.

### When a subagent earns its place

A single run does not need one. The main session writes the packet, launches,
arms the watcher, and later reads the report. There is no event noise to
quarantine, because nobody polls.

Several runs at once do. Hand them to a subagent pinned to the host's light
tier — read from the current harness at dispatch time (Sonnet in Claude Code
today; other hosts have their own lineup), with an explicit user choice always
winning. Pin it, because an unset model silently inherits the parent's tier.
It creates the run directories, writes the packets it was handed, launches
each run, and returns pointers: run directory, thread ID, provenance line, and
report path per run. It relays and manages; judgment stays with the main
session.

Because the runs are durable, that subagent no longer has to stay alive to
protect them. It returns as soon as the launches are recorded, and the main
session arms one watcher over the set:

```bash
for r in $RUNS; do until grep -q '^exit=' "$r/result.txt"; do sleep 10; done; done
```

Sequential in form, concurrent in fact: the runs overlap, so this finishes
with the slowest one. Do not glob the whole `.agent-runs/` directory — a
`DIED` run from an earlier session has no terminal line and would block the
loop forever.

Two failure modes justify any of this, and nothing else does: a weak model
quietly making a judgment call the main session never inspects, and a
delegation whose noise burns main-session tokens. Guard those; do not add
ceremony beyond them.
