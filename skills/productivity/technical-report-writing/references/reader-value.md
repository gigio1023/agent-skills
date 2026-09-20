# Reader-Value Decisions

Use when accurate text still obscures the document's point, or when removing a caveat, definition, receipt, or attribution could change meaning. Select information by its contribution to the intended reader's task. The same sentence can be unnecessary in a comparison and essential in a reproduction protocol.

## Diagnose the function

Ask what the passage lets the reader understand or do, then what consequential misunderstanding its omission would cause. “It is true” and “we checked it” are not sufficient reasons to keep it. Do not invent every possible misuse to justify another qualification.

| Reader-visible problem | Useful question | Default action | What changes the decision |
| --- | --- | --- | --- |
| Production narration displaces the result | Does the build or check detail establish identity, comparability, or a required action? | Delete the narration and self-assessment. | Retain a relevant artifact mismatch, failed check, version, or observation period. |
| A blanket caveat leaves the actual limit unclear | Which claim is limited, and how? | Rewrite the supported limit beside that claim. | Keep required wording and placement when an applicable disclosure rule specifies them. |
| A definition repeats shared knowledge | Does the reader need a new meaning or measurement boundary here? | Delete the familiar definition. | Define an unfamiliar concept or a nonstandard boundary at its first useful use. |
| A UI tour repeats visible labels and behavior | Can the reader use the control correctly without the paragraph? | Delete redundant narration. | Keep accessible labels and non-obvious input rules near the control. |
| Neutralization erases an event or responsibility | Did the edit remove what happened, who acted, or an assigned next step? | Restore supported actions, effects, and ownership. | Use an object subject or a local attribution gap when the actor is unknown. |
| Compression makes a result look better | Did failures, denominators, contrary evidence, or conditions disappear? | Restore the comparison's material facts and supported strength. | Remove a duplicate explanation once the necessary condition remains clear. |

Choose among four edits. **Retain** information already doing useful work. **Rewrite locally** when needed information is unclear. **Delete** information with no reader contribution. **Relocate** only when a specific reproduction, audit, operational, or lookup task needs a different level of detail. Use an existing authorized record when it already serves that purpose; moving information is not inherently better than deleting prose.

For a claim or figure intended to circulate independently, retain the conditions needed to interpret that view. Otherwise use the actual reading context: surrounding text, a clear label, or appropriate code or documentation may already explain the point. A shared methods note can carry a common rule; do not repeat it as a defensive caveat. State a core definition when this reader cannot reasonably recover it, or when its meaning differs from the ordinary one.

## Paired examples

All examples below are independently synthetic teaching cases. They are not anonymized work records. “Delete the paragraph” is an editing action, not text to insert into the document.

### Author framing and useful metadata

**Draft:** “Alex's synthesis and proposal, as of this week. I reviewed the available options and propose a bounded queue.”

**Technical proposal:** Delete the author introduction and write “Use a bounded queue to limit outstanding requests.” Keep the proposed status in the section heading or recommendation wording. Do not replace the removed byline with an impersonal sentence announcing that this document contains a synthesis.

A measurement date that defines the observation window, an assigned action owner, or required publication credit serves a different purpose. Keep it where that purpose is clear. Page ownership and the act of sharing usually do not need another sentence in the body.

### Research narration and subject methods

**Draft:** “We completed several rounds of research, saved the original materials locally, and checked the evidence folders. All figures are reported by their respective authors.”

**Technical explanation:** Delete this paragraph. Present the relevant mechanism and comparison, with citations attached to the claims. Do not replace it with a shorter research diary or a generic source disclaimer.

**Requested collection audit:** The reader has explicitly asked what was retrieved and what is missing. Provide the inventory and actual gaps. A collection count now answers the requested question.

**Important distinction:** The algorithm being explained, the experiment's workload, and the observed incident chronology are subject matter. Preserve their necessary steps and conditions. The author's search order, extraction tools, and storage layout are production history and stay out unless requested.

### Production receipt: comparison versus artifact identity

**Same draft:** “This report was generated from a frozen catalog. The catalog passed its schema check, and its content hash was recorded after the build. The results and full settings are available through the navigation links. This carefully validated report provides a comprehensive overview.”

**Configuration reader:** The report already identifies the evaluated release and links the source data; the paragraph contains no failed check or comparison condition. Delete the paragraph, with no replacement and no new appendix. Show the actual comparison where the paragraph used to be.

**Release reviewer:** The task is to establish that the tested build is the release candidate, and two builds share a display name. Retain the verified artifact identifier and identity-check result in the release evidence. If they differ, put that failure where it affects the release decision. Still remove the generic self-praise and navigation tour. Identity evidence now answers the reader's question.

### Snapshot: completed comparison versus current action

**Same draft:** “This page is a fixed snapshot and does not automatically reflect later execution state.”

**Retrospective reader:** The document compares a completed exercise and already states its period. Later state does not affect that comparison. Delete the sentence.

**Operator:** The same table is being used to choose work to start now, but it contains yesterday's observations. Write beside the status table: “Status was observed yesterday; check the target's current state before starting work.” Use the actual observation time when available. Retrieval time and build time do not establish when the underlying state was observed.

### Definition or UI instruction: familiarity versus a consequential distinction

**Same draft:** “Latency is the time between a request and a response.”

**Experienced performance reader:** Delete the generic definition. It adds no information about this comparison.

**Reader comparing full-response completion:** If the chart actually measures time to first byte, write: “Latency here ends at the first response byte; it does not measure full-response completion time.” For a beginner, the ordinary concept may also need a short explanation.

Apply the same test to UI prose. A paragraph saying that the visibly labelled Region control selects a region adds nothing. A date input that excludes its final day needs the local instruction “The end date is excluded.” Preserve accessible labels when removing redundant prose.

### Missing record: bounded fact versus unsupported absence

**Draft:** “No rollback owner exists. The information may be incomplete, and the report cannot guarantee exhaustive coverage.”

**Evidence and task:** A migration reviewer is checking a checklist with an empty owner field. The documented process requires the release coordinator to fill it before migration.

**Rewrite:** “The migration checklist has no rollback owner recorded. The release coordinator must assign one before migration.”

**Changed evidence or question:** If another inspected record names an owner, report the discrepancy rather than calling the role unassigned. If the question is whether an owner exists anywhere, the limited search cannot answer it; identify that specific gap. A general disclaimer does not repair an overbroad first sentence.

### Better-looking result: remove the caveat, preserve the failure

**Draft:** “A is faster than B. As with any benchmark, results may vary.”

**Evidence and task:** A service owner cares about reliable request handling. In this synthetic run, A completes 72 of 90 requests with a successful-request median of 140 ms; B completes all 90 at 190 ms. A's remaining requests time out.

**Rewrite:** “A's median was 140 ms among its 72 completed requests, compared with 190 ms for B's 90 completed requests. A also timed out on 18 of 90 requests; B had no timeouts in this run. The lower successful-request median does not establish better performance for reliable request handling.”

**Changed comparison:** If both configurations complete every request and the decision concerns only successful-request latency, a direct median comparison may suffice. Keep observed variation when it affects the decision; do not manufacture a confidence interval or append a generic warning.

### Accountability: remove judgment, retain what happened

**Draft:** “An issue occurred during deployment. No individual should be blamed, and these things can happen in a complex system. Appropriate follow-up will be considered.”

**Evidence:** The record establishes an empty destination, a default-mailbox fallback, a rollback, and the team assigned to the fix.

**Rewrite:** “The deployment accepted an empty destination and sent reports to the default mailbox. The release operator rolled back the change. The platform team owns the destination-validation fix.”

**Changed evidence:** If the record identifies a configuration change but not its author, “The configuration was changed” can be the accurate sentence. Do not invent an actor to make the prose active. Keep the attribution gap explicit when attribution is the reader's question.

## Preserve required records without reproducing them everywhere

Distinguish the report from its production record. Include build details, timestamps, revisions, and verification receipts when the reader needs them to compare, reproduce, audit, or act. For a decision summary, the necessary sample filter may belong beside the result while seeds and parameters remain in a linked methods record. For the reproduction protocol itself, those parameters belong in the normal reading path. If nobody needs an extra detail and no retention rule applies, omit the prose instead of creating a new archive of it.

Required disclosures and material notices keep their required content and placement. Do not invent a legal judgment about whether a notice is required. An uncertain requirement that affects delivery warrants clarification; ordinary editing preferences do not override it.
