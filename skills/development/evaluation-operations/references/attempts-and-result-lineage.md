# Attempts, Results, and Rescoring

Read this reference when reconstructing a campaign, reporting a result, or deciding whether to resume, rescore, or rerun. It preserves evidence and comparability without imposing a common data schema.

## Identify the thing being compared

Use the project’s available provenance to distinguish an actual attempted configuration from a label that may later change. Capture, when applicable, the provider or target, model identity, exact revision or mutable alias, runtime, prompt or configuration, data version and evaluation unit, case and repeat, raw-output origin, scorer identity and version, and validation policy or label boundary.

An exact revision is evidence only when the project records it as fixed. A mutable alias remains a mutable alias even if it currently resolves to a known target. Do not guess a missing revision, data version, scorer version, or runtime from a familiar name. State it as unknown and describe how that limits comparison.

## Preserve attempt history

An attempt is historical evidence even when it did not produce a usable result. Retain incomplete, failed, cancelled, blocked, and excluded attempts with their observed reasons, ownership or handle history, raw-output references, and relevant conditions within the project's retention and access rules. Do not erase an attempt simply because a later retry succeeds.

Auditability does not override privacy or retention obligations. Preserve the permitted lineage and record when raw evidence has expired or become unavailable, with the resulting limit on reproduction or validation. Do not reconstruct missing output from a summary. Cleanup or deletion requires its own authority and the project's retention procedure; a general preservation instruction is not a reason to keep restricted content indefinitely.

Keep denominators with the conditions that define them. A missing, null, unreadable, or excluded value is not a zero value and is not automatically a pass or failure. If a project policy gives it a meaning, cite that policy; otherwise preserve the unknown or exclusion explicitly.

## Treat scoring as a derived operation

When raw output is sufficient and a new scorer or corrected scoring input is authorized, create a distinct derived result through the project’s normal record mechanism. Link it to the original raw attempt, the exact scorer or scoring configuration observed, the input and label lineage, and the reason for rescoring. Keep the previous score and its provenance available for audit under the retention rules above.

Do not call a score validated or comparable merely because it exists. Check that the raw output belongs to the intended attempt, the data and configuration match the requested comparison, the scorer and input lineage are known enough for the claim, and the project’s gold-label separation and validation rules have actually been satisfied. A record alone cannot prove that labels were inaccessible during generation; use the project-defined access and separation evidence.

## Choose recovery from evidence

Resume when the same owned execution is credibly live or recoverable and its approved inputs and limits remain correct. Rescore when sufficient raw output is available and the requested scoring operation is both correct and authorized. Rerun only when raw evidence is unavailable or unusable under the project’s policy, or when an approved campaign explicitly needs new execution.

Before a rerun, reconcile live state, durable attempt history, and raw outputs. An unavailable handle or stale process reference leaves the state uncertain; it does not prove that the work ended. Avoid blind retries, especially for non-idempotent operations. Stop after repeated deterministic failure and report the smallest correction, input, or authority needed to proceed.

The resulting report should name the exact evidence that supports each conclusion and distinguish a proposed command, source location, synthetic fixture, observed execution, and validated result.
