# Model and Dispatch

Which model, reasoning effort, and speed tier a delegated run gets, and who
owns the run once it is launched.

## Contents

- [Selection order](#selection-order)
- [Model and effort](#model-and-effort)
- [Speed — the Fast tier](#speed--the-fast-tier)
- [GPT-5.6 packets](#gpt-56-packets)
- [Judgment ownership](#judgment-ownership)
- [Internal parallelism](#internal-parallelism)
- [Dispatch — durable runs, disposable watchers](#dispatch--durable-runs-disposable-watchers)

## Selection order

1. An explicit user choice of model, effort, or Fast mode wins.
2. Otherwise start a new run with `gpt-5.6-sol` at `xhigh` and
   `service_tier="default"`.
3. Route to Terra, another supported model, or another effort only when task
   shape or availability supplies a concrete reason.
4. A resume starts from the original model and effort. Reconsider them when the
   resumed turn has materially different work or the original route is no
   longer available.

Record the resolved model, effort, and service tier in `result.txt`. Name the
reason for any non-default route in the host's reply. The launcher also records
`host_route`, `host_model`, `routing_reason`, and `packet_sha256` so later audits
do not have to infer the host path from retained transcripts.

## Model and effort

Default: `gpt-5.6-sol` at `xhigh` reasoning effort. A delegation must not
silently inherit a machine default: pass both values explicitly and record them
on the `result.txt` provenance line.

`codex exec` has no reasoning-effort flag. Effort moves only through config,
which makes `-c model_reasoning_effort="…"` a sanctioned `-c` override. The
rest of the `-c` rule is unchanged: it must never touch `sandbox_mode` or the
approval policy, and any override you use is declared visibly in your reply
and appended to the provenance line.

Use `gpt-5.6-terra` at `xhigh` only when a bounded implementation, inventory,
extraction, or evidence-collection mission does not need Sol's stronger
judgment. Keep Sol when uncertain. Difficult debugging, adversarial review,
high-stakes judgment, and work where a missed consideration is the expensive
failure stay on Sol.

Model and effort remain contextual dials. Lower effort only for well-specified
mechanical work that is cheap to verify or retry. Use another supported model
or effort when availability or task fit gives a concrete benefit; do not make a
quota-saving or latency-saving downgrade silently.

The key name and its accepted values belong to the CLI, not to this skill. If
a run rejects the override, trust `codex exec --help` and the current codex
config documentation over this list, and note the drift.

## Speed — the Fast tier

Codex calls the `priority` service tier Fast. The canonical template derives
`service_tier` from `FAST_REQUESTED`: `no` maps to `default`, and `yes` maps to
`priority`. Set `FAST_REQUESTED=yes` only when the user explicitly requests
Fast. Do not infer that request from urgency, task size, or an effort choice.

Fast and reasoning effort are independent. Keep the selected effort unchanged
when enabling Fast unless the user or task separately justifies an effort
change. Record both the host's explicit-request assertion and the derived tier
in provenance. A resume may preserve `yes` for the same mission; a legacy run
without that assertion resumes non-Fast unless the user asks. If the CLI rejects
a tier, trust its current help and config documentation and report the drift.

## GPT-5.6 packets

Model-specific prompting is not restated here. When the packet targets a
GPT-5.6-family model, load the sibling skill `gpt56-sol-prompting-guide` (same
pack, `skills/development/gpt56-sol-prompting-guide/`) and shape the packet
with it before dispatch. This skill owns the mission contract — objective,
scope, authority, verification, response contract; that skill owns how the
prompt is worded for the model. On wording, the prompting guide wins; on
authority, this skill does.

## Judgment ownership

The host decides how much judgment Codex owns by writing the mission packet.
The grant may be narrow execution under fixed decisions, bounded judgment
under named criteria, or end-to-end ownership of investigation, judgment, and
decisions. No level is the universal default for every mission.

Keep the grant broad enough to benefit from two capable AIs working together.
The packet names consequential decisions reserved to the host and material
pause conditions; it does not try to pre-authorize every minor choice. Inside
the granted scope, Codex makes ordinary reversible decisions without asking.
When the packet grants end-to-end ownership, Codex should reach and support
the decision instead of returning options merely for ceremonial approval.

Internal subagents inherit the same grant. Spawning one never widens scope,
sandbox, credentials, external effects, or authority.

## Internal parallelism

Codex can spawn its own subagents. Grant that capability in the packet's
Authority block only when the work has genuinely independent branches:

> Internal subagents are allowed when independent investigation,
> implementation, or verification branches justify them. Choose their number
> and topology; keep dependent steps and conflicting writes sequential.
> Synthesize their evidence into one result.

This is task-shaped permission, not a standing recommendation. A small
sequential task uses none. Nothing outside Codex changes: the same sandbox, run
directory, mission authority, and host verification still apply.

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

The detached launch in `SKILL.md` removes the coupling. On systems with the
util-linux command, `setsid -f` forks and starts the run in a new session. The
fallback does the same through Perl's POSIX module, which covers macOS where
the `setsid` command is absent. The Perl branch was verified with PPID 1 and
PGID equal to its own pid; a real 53-second run survived its launcher being
SIGTERMed at 15 seconds and appended its own `exit=0`.

With the run durable, waiting becomes trivial. Arm a background shell in the
session that wants the notification, holding one condition loop:

```bash
while :; do
  grep -q '^exit=' "$RUN/result.txt" 2>/dev/null && break
  PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt" 2>/dev/null)
  [ -n "$PG" ] && ! kill -0 -"$PG" 2>/dev/null && break
  sleep 10
done
```

Its exit is the completion signal: the harness re-invokes the session that
owns it, and that wakes an idle host (verified with a 75-second probe). If the
watcher is killed first, nothing is lost — re-arm it, or just read `--status`.
If the run dies before writing `exit=`, the process-group check ends the
watcher instead of leaving it asleep forever; `--status` then reports `DIED`.

Ownership is the one subtlety. Arm the watcher from the session that wants the
notification, because an orphaned background task's notification cannot wake
anything: it queues unread until the next user message forces a turn, measured
at 22 minutes in one incident.

### Host-side launcher subagent contract

`Host-side launcher subagent` names the role of a native subagent in Claude
Code, Cursor, or another host harness. It is distinct from the per-run `run.sh`
wrapper and from subagents created inside Codex. Use it as the default execution
path for a single run or a batch whenever the host exposes native subagents.
The main session still writes every packet and resolves model, effort, sandbox,
Fast, network, worktree, and authority before dispatch.

Give the launcher subagent immutable packet paths, a main-selected absent run
path, and fixed scalar inputs. When the harness supports per-subagent model
selection, use its reliable lightweight model for this mechanical role. A
Sonnet-class model is the intended Claude Code route. Escalate only when the
light model is unavailable or fails the manifest contract. Retained history
shows a Sonnet launcher starting a production-like Codex run and another
Sonnet launcher completing a synthetic end-to-end check. One production
completion handoff was lost after launch. The new launch-and-manifest-only
route therefore remains unverified in production.

The launcher subagent calls `scripts/launch-run.sh`, verifies each manifest and
initial provenance line, and returns the manifest unchanged. It does not decide
to retry, resume, cancel, interpret a report, or change authority. When the main
session authorizes a resumed turn, it sends the new immutable packet path and
exact source run directory; the launcher uses the same script with
`--resume-from`. The decision and authority remain with the main session.

Because the runs are durable, the launcher subagent does not stay alive to
protect or monitor them. It returns as soon as the launch manifest is recorded,
and the main session arms one watcher over the set. Actual host history showed
the runs completing safely after launcher-subagent transcripts ended, but no
reliable completion handoff returned to those subagents; the file artifacts and
main-session watcher are the source of truth:

```bash
for r in $RUNS; do
  while :; do
    grep -q '^exit=' "$r/result.txt" 2>/dev/null && break
    PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$r/result.txt" 2>/dev/null)
    [ -n "$PG" ] && ! kill -0 -"$PG" 2>/dev/null && break
    sleep 10
  done
done
```

Sequential in form, concurrent in fact: the runs overlap, so this finishes
with the slowest one. Do not glob the whole `.agent-runs/` directory: an
unrelated old run would trigger a misleading notification.

Launcher-first is an operational default, not a claim that it has a higher
success rate than direct main-host launch. Retained main-host traces also show
stable batches of writers, reviewers, and a resume. Keep the direct path as a
recovery mechanism.

The main session selects every run path before dispatch and passes it through
`--run-dir`. If launcher output is missing or incomplete, inspect that exact
path before deciding what failed:

1. When the path exists, call `launch-run.sh --recover-manifest` with the same
   immutable packet. Matching packet hash and host provenance means launch
   succeeded, so adopt the run and arm the watcher.
2. When the path exists but recovery fails, stop with a contract failure. Do
   not overwrite the directory or start another run.
3. When the path is absent, invoke the normal launcher command directly with
   the same path and record `host_route=direct-main` plus the fallback reason.

This fallback preserves one launch contract and avoids making subagent
availability or manifest delivery a correctness dependency. It also prevents
the lost-output case from creating a duplicate Codex run.

Do not turn recovery into automatic retry. The main session classifies the
evidence first:

- a manifest-delivery failure uses the verified existing run;
- `DIED` or a transport failure resumes the exact thread when possible;
- `handoff=incomplete` inspects events, then resumes only to repair the final
  handoff;
- a reserved `report.md` collision, workspace drift, or deleted deliverable
  requires workspace inspection before any resume;
- missing or mismatched provenance is a contract failure.

Replaying the same packet without this classification can duplicate edits or
repeat an external effect.

The host must also budget total fan-out. When it already launches five or more
Codex roots, internal subagents default off unless a packet names a branch that
still needs isolated evidence or review and gives it a bounded child count.
This prevents host-level parallelism from multiplying unnoticed inside every
root.

Two failure modes justify any of this, and nothing else does: Codex crossing a
judgment boundary the packet reserved to the host, and launch mechanics
displacing high-context work. Guard those; do not add ceremony beyond them.
