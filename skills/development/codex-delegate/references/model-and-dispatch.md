# Model and Dispatch

GPT-6 Astra owns delegated work that requires investigation, interpretation, design, implementation judgment, review, or synthesis. This is the pack owner's routing policy, not a claim that CLI availability or model quality was established for every account.

## Selection

| Work | Default model | Effort |
| --- | --- | --- |
| Judgment-bearing or ambiguous mission | `gpt-6-astra` | `xhigh` |
| Fixed procedure with mechanical acceptance | `gpt-6.1-sol`, when deliberately selected | Task-appropriate supported value |
| Explicit user model or effort choice | User selection | User selection |

A mechanical packet fixes the inputs, procedure, output, and acceptance. Running an already selected command and returning its exit code can fit. Choosing commands, selecting decisive evidence, interpreting failures, reviewing code, and implementing a fix require judgment. Short tasks can still require Astra.

Use Astra when uncertain. Do not make a cheaper trial a prerequisite, lower frontier effort automatically, or impose an arbitrary limit on frontier consultations. Honor the actual mission's cost, time, and concurrency limits. If the requested route is unavailable, report the limitation or use an already authorized alternative.

The launcher passes model and `model_reasoning_effort` explicitly. A resume preserves recorded settings unless the host overrides them. Inspect a legacy Sol source before resuming: retained history does not make its old route appropriate for new judgment-bearing work. Pass `--model gpt-6-astra` and record a reason such as `resume-policy-migration` when applying the current policy. A user's deliberate model choice still wins.

## Service tier

New runs use `--fast-requested no`, which records `tier=default`. An explicit Fast request permits `yes`, which records `tier=priority`. The assertion records the host's authorization decision; the script cannot verify a conversation it does not receive. Resume may preserve the grant for the same mission. A legacy source with no assertion defaults to `no`.

The current [configuration reference](https://developers.openai.com/codex/config-reference) describes `fast` as mapping to request tier `priority`. Requested settings in provenance are not a server receipt. Inspect CLI warnings when availability matters and report an unsupported tier rather than claiming it was applied. Service tier does not change the selected reasoning effort.

## Internal subagents

An Astra delegate uses the sibling `gpt6-astra-model-routing` skill for available roles, model settings, and host-specific overrides. Mission work is eligible for useful internal delegation. The former mission exclusion does not apply.

- Default every judgment-bearing child to Astra, including unnamed and nested workers.
- Use Sol 6.1 only for fixed execution with mechanical acceptance and no semantic decisions.
- Preserve the mission's authority, data boundary, and resource limits at every depth.
- Follow the runtime's supported model-override contract. Do not invent roles, pass unsupported overrides, or install global agent defaults as part of a task launch.
- If the routing skill is absent, apply those same defaults directly through supported tools. If suitable subagent tools are unavailable, work sequentially.

Delegate independent work with a clear integration owner. Shared writes need isolated workspaces or disjoint ownership that the lead can integrate safely. Account for host roots and internal children together when a resource limit matters. No fixed root count disables useful children automatically.

Before handoff, the delegate integrates child evidence and waits for or intentionally stops its active children. A root event log exposes only partial child state; it does not certify every descendant's completion.

## Host launch ownership

The main host owns the packet, model route, authority, source workspace, run path, observation, result acceptance, and recovery decision. Calling the deterministic launcher directly is sufficient for a durable run.

An optional native host subagent can launch a fixed packet or batch. Its inputs are packet paths, absent run paths, and resolved scalar settings. It returns the manifest unchanged and stops. It does not interpret reports, rewrite packets, widen authority, or retry. For GPT host helpers, the same Astra/Sol policy applies; their mechanical role may qualify for Sol 6.1. Other host model families follow the user's applicable routing policy.

Lost manifest delivery does not establish failed execution. The main host first settles the launcher and then recovers the exact run. A recovered run retains its original `host_route` and `host_model`; recovery must not relabel how it was launched.

## Durability and evidence

A separate process session keeps Codex outside the launching command's process group. The script uses util-linux `setsid -f` or Perl's POSIX `setsid`. It detaches standard input and redirects wrapper diagnostics to `launcher.log`. `&` or `nohup` alone does not establish this separation.

Historical package checks on CLI 0.145.0 observed a detached run surviving its launching command and a SIGINT-interrupted thread retaining context on resume. Current deterministic fixtures exercise the wrapper lifecycle. Neither establishes every host's process cleanup behavior or current model performance. A host that kills all descendants or containers may require its supported durable-job mechanism.

CLI help was inspected on 0.159.3 on 2026-10-06. [Non-interactive mode](https://developers.openai.com/codex/noninteractive) documents JSONL events, output capture, and explicit-session resume. The [GPT-6 instruction guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) supports outcome-led prompts and conditional scaffolding; the local mission and authority contract remains this skill's responsibility.
