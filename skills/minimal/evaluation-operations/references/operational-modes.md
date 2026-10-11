# Operational Modes

Read this reference when the requested authority, recovery route, queue movement, or monitoring behavior is unclear. Choose the narrowest mode that accomplishes the request; the modes are decision boundaries, not a mandatory pipeline.

## Status or diagnosis

Status and diagnosis are read-only. Locate the campaign’s authoritative records, reconcile live and durable evidence, and report supported facts, contradictions, and unknowns. Do not edit source records, alter a queue, launch or restart work, rescore, rerun, cancel, or clean up resources. A careful diagnosis can still identify the exact next action that would be safe if it were separately authorized.

## Resume or execute

Treat a request to resume or execute as limited to work already approved for the named campaign’s targets, data, configuration, cost or budget, resources, and stated limits. An authorized runtime model or API call required by that campaign is part of the execution and does not need repeat approval. Reuse existing session grants rather than requesting them again. Before action, re-check current priorities, prerequisites, target and resource limits, budget, and verified ownership.

Use the project’s claim, lease, reservation, or ownership mechanism when it exists. For simple serial work, verified single ownership is enough; do not require a new lease system. If an authorized operation needs its first durable task or attempt record, add the smallest record through the project’s ordinary practice. Make a non-idempotent dispatch bounded and traceable in that durable record. If an attempted action fails deterministically again, stop retrying. Preserve the failure and return the smallest missing correction, input, or authority rather than widening the campaign on your own.

New costly experiments, model or API use outside the approved campaign or its limits, external publication, scheduler installation, destructive cleanup, and unapproved hosts remain separate authorization even when they might appear to unblock progress.

## Resume, rescore, or rerun

Resume an existing item when it is still the correct owned attempt and live or recovery evidence supports continuing it. Do not treat a missing handle as a stop signal without checking the project’s available runtime, scheduler, and log evidence.

Rescore only when raw output is sufficient, the intended data, configuration, labels, scorer, and input lineage are correct, and the scoring operation is authorized. Store the outcome as a linked derived result; do not overwrite the prior score.

Rerun only after evidence shows raw output is absent or unusable under the project’s rules, or an approved campaign requires a new execution. Confirm that no existing live attempt would duplicate it and that the replacement remains within all approved limits. Never infer gold-label isolation from an output shape; verify the project’s stated separation and access controls before making that claim.

## Monitoring or sustain work

Monitoring alone permits observation, not dispatch, retries, rescoring, cancellation, or durable-record changes. A request to keep approved execution moving may grant both monitoring and execution; apply each grant to its corresponding actions without asking again. If observation reveals a repair that is not authorized, report the supported diagnosis and proposed action while continuing any useful authorized observation.

Monitoring is available when the request includes it and the current harness or project runtime offers a real sustained-observation mechanism. Prefer the harness's supported native wait with fresh project-state reads when it suffices; an existing project scheduler or runtime observation route is also valid. A project-specific daemon or scheduler is not a prerequisite. Define a terminal condition. When the request is to continue until completion, sustain observation with that real mechanism until the terminal condition occurs. Use a bounded period or event condition only when the request, runtime, or authority actually supplies it. Report at meaningful state changes, including completion, a new block, a priority change that changes dispatch, a failure requiring action, or the terminal condition.

If neither the harness nor the project provides a usable sustained mechanism, state the real runtime or authority blocker, make any safe immediate observation in scope, and state that monitoring ends with the current task. Do not imply a background monitor continues. Idle resources are not proof of progress or permission to start work.

When execution is also authorized, re-anchor to revised priorities before each new dispatch. Running work may require a targeted, separately authorized stop or cancellation; do not make that change merely because a higher-priority item appears.

## Finish honestly

Finish status work when the evidence-backed picture and uncertainty are usable. Finish execution when the requested approved actions reach their terminal state or a real blocker prevents further authorized work. Finish monitoring at the specified terminal condition or a bound explicitly supplied by the request, runtime, or authority. In every case, identify active handles or equivalent live references, durable evidence, and the next approved action.
