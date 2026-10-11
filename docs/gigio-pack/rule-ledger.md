# Rule Ledger

Current rules below supersede conflicting rows in the [historical ledger](rule-ledger-history.md). History records why an old rule existed, not an instruction to keep it after a changed requirement.

| Rule | Owner | Reason and current treatment |
| --- | --- | --- |
| User-owned direction; maintained current understanding | gigio-project-setup | Preserve intent while updating empirical understanding without a new interview for each finding |
| Next-decision planning | gigio-write-plan | Later research work depends on results; known dependencies remain useful |
| Bounded adaptive execution | gigio-execute-plan | Fast follow-up work can proceed within the question and grant |
| Bounded adaptive discovery | find-unknowns | Short techniques can be combined within the objective and grant; no fixed technique count, output layout, or automatic setup sequence |
| Ask before changing direction or starting long new work | planning and execution | User controls direction and resource commitments; two to three days is an example, not permission for all shorter work |
| Inspect sources relevant to the current action | execution and review | Avoid stale inputs and duplicate jobs without rerunning irrelevant historical checks |
| Match verification to the claim | execution and review | Findings can be valid without code edits or command outputs |
| Preserve actual attempts and consequential changes | execution and handoff | A successor needs current understanding and reliable source records |
| A handoff is one `.handoff/<date>-<time>-<task>.md` file that opens by telling its reader to execute it, records only externally checkable live state, and lists the questions for the user | session-handoff | User-set 2026-09-24 and 2026-10-03: a root `handoff.md` collided across concurrent tasks; successors given only the path improved the file instead of doing the work; harness-internal handles die with the session |
| Partition shared writes before parallel work | execution | Concurrency correctness; does not require planning every future stage |
| Delegation: an explicit user choice governs; otherwise the lead decides and dispatches ready independent work once direction is settled | execution and review, with orchestrate-subagents (agent-skills) | Lead-initiated delegation is expected rather than exceptional; questions that change the work are settled before dispatch; delegation adds no authority |
| Independent review when useful | review | Separate self-inspection from independent evidence; no false independence claim |
| Recipient suitability and authorized delivery | copydesk (agent-skills), `references/sharing-and-delivery.md`; formerly share-internal-doc | Keep private records separate and verify usable source destinations and the actual shared copy |
| Contested names settled from project, paper, and competitor usage; recorded names applied | curate-terminology, use-terminology | A glossary row only for competing names, local meanings, or user decisions; every-task use comes from the project instruction snippet |
| Distinct repository ownership | all | Tool methods live in agent-skills; research methods in research-credo |

## September 17, 2026 supersessions

Removed universal staged planning, mandatory changed paths plus command output for completion, a blanket worker ban on relevant skills, final-review-only handling of direction problems, and Git commit as the sole persistence test. Preserved authority, source verification, actual job ownership, and the distinction between missing execution and negative findings.

Moved seven execution helpers without renaming them. Replaced duplicate sharing editorial references with writer composition. Updated project instructions and templates together. These are instruction and package changes, not evidence of improved model performance.

## September 20, 2026 document ownership

Kept recipient suitability, source preservation, sensitive attribution, and authorized delivery. Narrowed the sharing workflow to these responsibilities and explicit composition with copydesk. Removed reliance on linked working documents for essential explanation. The writer owns editorial defaults across media; genre changes the needed depth, not whether established preferences apply. No separate style skill, installation, or new approval stage is required.

Recipient review distinguishes useful ownership from decorative author framing and checks that internal names are understandable. Delivery verification preserves row identity and list hierarchy through conversion. The writer owns the detailed corrections and complete synthetic examples; the sharing skill does not maintain a second style guide.

The changed packages receive metadata, resource-link, discovery, and editorial consistency checks. Model behavior comparisons remain a separate requested activity.

## September 21, 2026 shared-copy continuity

Use the current user-edited shared copy as the revision baseline and reconcile it with generated sources before publication. The writer owns the interpretation of editorial deletions and optional-section design. Sharing verification checks that equations and collapsible content survive delivery, distinguishing retrieved content from rendered inspection. This adds no publication grant, approval stage, or duplicate editorial workflow.

## October 3, 2026 terminology narrowing

The user wanted a short glossary of settled names and got a writing rulebook. Superseded the historical rows that ran both terminology skills on every task by description and recorded expressions, sentence patterns, and project explanations. A row now needs competing names, a differing local meaning, or a user decision; curation surveys established projects, papers, and competitor products; use-terminology only reads. Every-task use comes from the project instruction snippet. Preserved the root and `docs/terminology/` layout, reference-only source records, user-confirmed local names, scoped wording bans, and AI-source scrutiny. Verification was static package validation and link checks.

## Generation audit

Revisit measured workarounds against the active harness and actual task failures. Do not impose an instruction-size quota or run unrequested model comparisons. Keep applicable verification and user boundaries even when simplifying a procedure.

## October 6, 2026 discovery adaptation

The authorized audit replaced the single-technique rule and separate approval for a second short technique with bounded adaptation within the same objective and resources. Removed fixed question, option, variant, and artifact counts; made the launch-brief template optional; replaced mandatory notes files with authorized existing records. An accepted brief can continue already-authorized work and does not trigger setup or planning by itself.

Preserved evidence-backed findings, explicit user choices, the limited discovery trigger, and gates for new direction, resource commitments, access, external actions, or long new work. Static package and resource-link checks passed for all nine packages, and Skills CLI discovered nine names. Diff and editorial findings were reviewed; model behavior was not tested.

## October 7, 2026 delegation and discovery alignment

agent-skills #88 made an explicit user choice about delegation govern and left the decision to the lead otherwise; #102 and #103 made maximum useful parallelism the default once direction is settled, after the questions that would change the work are answered. gigio-execute-plan, gigio-review-results, the principles, and the repository guidance still required a delegation request or authorization, and execution was described as sequential. They now follow that precedence and point to orchestrate-subagents for dispatch defaults instead of restating them. gigio-write-plan no longer limits find-unknowns to an unresolved human choice: since #34 that skill also covers unnoticed unknowns and option maps, and the plan's questions are asked together before work is detailed.

Preserved shared-write and live-job partitioning, sequential handling of dependent steps, the ban on calling self-review independent, and every gate on direction changes, long new work, resources, and external effects; delegation grants no new authority. README and migration now describe the 2026-09-17 repository migration as complete. The historical ledger keeps its original wording. Verification was static package validation, Skills CLI discovery, and link checks; model behavior was not tested.

## Deletion and compression record

Earlier changes remain in [rule-ledger-history.md](rule-ledger-history.md#deletion-and-compression-record). New entries state the requirement, changed behavior, preserved limits, and verification actually performed.
