# Project Binding

Read this reference before operating a campaign whose authoritative sources or simple coordination are unclear, incomplete, or contradictory. It helps bind the work to existing project practice without prescribing a manifest format, database layout, scheduler, or registry.

## Build a source map or coordination record from the project

Identify the project-defined source or explicit coordination for each fact needed by the request. Typical categories are campaign scope, approved priority or queue, durable attempt history, raw outputs, derived results, live runtime state, ownership or lease state, resource and budget limits, and validation policy. Some projects combine these categories; others split them. A simple serial campaign may establish scope through approved coordination, a verified single owner, and a small task record rather than a bespoke manifest or lease system. Do not create a universal mapping or assume a file is authoritative merely because it is nearby.

For every source used, record what it can establish and its observation time where the project supports that information. A launch record can establish that a request was made. A runtime record can establish a currently observed handle. Raw output can establish only the output it contains and its provenance. A validation record can establish validation only under the policy and inputs it names. A source location without readable evidence establishes neither execution nor success.

Keep durable per-run history in the project's canonical registry or log, outside this replaceable skill package. If an authorized operation needs the first task or attempt record, create only the smallest record supported by the project's normal location and practice. Do not create a parallel spreadsheet or copy private runtime state into the skill so that its installation becomes a source of truth. Keep private inputs, results, source maps, and credentials within the approved sharing scope and out of the package.

## Reconcile instead of collapsing disagreement

Compare live observations with durable history and raw outputs before deciding whether work is running, complete, recoverable, or safe to retry. If they disagree, retain both observations, identify their limits, and use the project's documented recovery route. For example, a durable record may still be pending while a live source reports a handle, or a handle may be unavailable while a raw-output location has new material. Neither discrepancy justifies inventing a terminal state.

Treat these as independent claims:

- prerequisites and infrastructure are ready;
- inference has completed for a defined attempt;
- scoring has completed for defined raw inputs;
- validation and comparison conditions have been met.

Do not convert project fields into a new global state machine. The purpose is to prevent a broad status label from hiding a missing fact, not to require a common enum.

## Re-anchor priorities and ownership

Treat the latest approved priority source as authoritative for new dispatch. When a user changes priorities while a worker is active, first reconcile what it owns, what it has already started, and what can safely remain in progress. Do not stop or cancel an identified job unless that action is explicitly authorized.

Before moving a ready item, find the project-defined claim, lease, reservation, or ownership record. Verify it is current enough for the operation and that the item still fits target, resource, prerequisite, and budget limits. For simple serial work, a verified single owner can provide sufficient coordination. If concurrent work needs stronger coordination and none exists, use an established path if one is available; otherwise report the risk rather than silently creating a competing mechanism.

## When the binding is missing

For a read-only request, report the narrow missing mapping and the facts that remain unknown. For an authorized operation, complete independent inspection and preparation, then stop before an action that needs the absent source or coordination. Ask for the smallest source, decision, or authority that would resolve it. Do not infer an approval from idle resources, a prepared configuration, or prior work in another session.

The binding is sufficient when another operator can see which project records support each material claim, which live state was checked, and which fact still needs evidence.
