# Decision Log

Historical direction changes, in the order they happened. These older entries use four fields; current work does not require this reporting template:

**what the plan said → what reality revealed → the conservative choice taken → when to revisit.**

The point of keeping the reversals is that they are the expensive part. Most entries below record something being thrown away.

---

## Central controller architecture rejected

- **Plan:** adopt one root controller from an existing workflow system and layer a language router, an evidence contract, and an executor compiler beneath it.
- **Reality:** building a harness and slotting the real harnesses into it was the wrong shape. The framing of a controller owning authority was already too much. Agent skills plus concepts common to every harness is the ceiling.
- **Choice:** keep the goals (plan durability, drift propagation, verification, delegation to weaker models). Demote the controller candidates from installation to sources worth mining for artifact shapes. Replace the controller pilot with a much cheaper probe: apply skills-only conventions to one real task.
- **Revisit:** if skills-only discipline repeatedly fails in real projects, widen ambient enforcement first — do not reopen the controller question.

## Restated the original request

- **Plan:** the discussion had drifted from controller pilot to skills-only to vocabulary cleanup.
- **Reality:** the original request had been four capability items all along, and controller adoption was a means nobody had asked for.
- **Choice:** reuse the research output as raw material for the actual four items rather than as a plan of record.
- **Revisit:** re-check the four items against a real project after building.

## Resume automation scoped down

- **Principle:** for the specific problem of resuming work, high-quality records make deterministic restore machinery unnecessary — the model reconstructs from the record. This is not a general "records first" principle.
- **Effect:** invalidates resume automation as a selling point in the systems that lead with it, while leaving the value of their record formats intact.

## Survey verdict: no external pack adopted wholesale

- **Result:** every candidate came back mine-only. Recurring disqualifiers were bundled hooks, broad auto-triggering descriptions, commands that presuppose each other, and record quality no better than a hand-written convention.
- **Decision:** the answer to the original request is a hand-written record convention, with mining sources identified at file level.
- **Revisit:** if a real cycle fails acceptance, strengthen convention fields first, then ambient enforcement. No controller reconsideration.

## Premise correction: the problem is supervision visibility, not planning discipline

- **Plan:** the record convention assumed a "next big project starts" trigger.
- **Reality:** the big projects were already running, model-driven and continuous. The actual pain was different: (1) no way to notice when the instruction was wrong or the model made a mistake, and (2) work evaporating with the session instead of accumulating structure. The only tool in real daily use was the one that paid off immediately, in flow.
- **Choice:** look for structure on the way *out* (audit, with records as a by-product) rather than on the way *in* (planning).
- **Revisit:** if records still don't accumulate after that, revisit ambient enforcement.

## Standalone audit skill discarded

- **Plan:** treat `unknowns pass → plan seed → ambient upkeep → audit → receipts` as a finished delegation loop, run one cycle on a real repository, then promote it.
- **Reality:** the audit skill was deleted by hand. Not because reviewing has no value — because a lone skill whose role before and after is invisible has no value. The assembly's real usage count was zero, and the documentation had recorded it as "built" far too early.
- **Choice:** do not restore or improve it. Define the connected map first: direction forming → a user-owned source of truth → readiness judgment → execution → intent-based review → the same source updated. Strong models run autonomously on thin instruction; detail is added only when handing direction-resolved mechanical work to a weaker executor.
- **Revisit:** after one real project has run both a strong-model path and a constrained weak-executor path from the same source, judge what else is needed.

*This entry is the origin of the pack's "nothing is recorded as done before it has been used" rule.*

## Loop correction: remaining judgment means not ready

- **Plan:** under "choose an execution mode," one branch was "judgment remains → strong model and human explore."
- **Reality:** remaining judgment does not mean picking an executor type. It means the work is not ready to execute and must go back to direction forming. And what is needed after execution is not code review or mechanical verification but a comparison of intent, background, goals, decisions, and non-goals against the actual result.
- **Choice:** correct the topology to `direction forming ↔ work map → readiness judgment → execution → intent-based review → map update`. Review results route to direction forming (premise problem), re-execution (execution problem), or map update (accepted).
- **Revisit:** confirm in a real project that readiness judgment actually blocks unresolved judgment, and that review doesn't collapse into output inspection.

## Single-agent assumption dropped; parallel fan-out promoted into the plan structure

- **Plan:** the unified design assumed the planning skill writes a plan and the same agent executes it, with delegation handled separately by a six-step strong→weak protocol.
- **Reality:** the default working style is aggressive parallel subagent fan-out, and a plan written for that is structurally different from one that isn't. Re-survey found: mature references all separate lead from worker; parallelism comes from the plan file's data structure (stage / prerequisite / owned files), not prompt wording — measured, instruction alone produced zero multi-dispatch; conflict prevention is planning-time ownership partitioning, not locking, and one system's lock machinery turned out to be dead code. The six-step protocol's step 4 also duplicated an already-installed skill verbatim, and a supporting claim from an earlier wave was found to be a misreading.
- **Choice:** add four lines per work item (stage / prerequisite / owned files / delegable) as **facts rather than instructions**, so the same file survives both solo execution and parallel dispatch. Move the execution contract into the planning skill and discard the six-step protocol. Delegate decomposition and merge by name to the orchestration skill. Reject large-abstraction designs and write down "markdown a human can read and fix by hand" as a principle.
- **Revisit:** observe real out-of-scope-edit requests and blocked reports in pilots before fixing a reassignment policy.

## Execution split into its own explicitly invoked skill

- **Plan:** keep execution as a section inside the planning skill; assume "plan file plus ambient guidance" is enough to run on.
- **Reality:** the operating principles you want at the moment of execution were scattered across global skills, so "read the plan and figure it out" gave no guarantee they would fire together. Of ten implementations read, nine separated execution into its own invocation unit; the one that didn't was a 1,000-line outlier. One system explicitly forbade execution from its always-loaded skill; another had 435 always-loaded lines and no invocation verb — knowledge present, activation impossible.
- **Choice:** create the execution skill. Four reasons to separate: the two postures are incompatible (planning asks and stops; execution does not stop — merged, they average out); preflight cannot live inside the plan file; a new session must be able to enter alone and survive compaction; resume logic belonged to the execution side in every reference that had it. Activation is triple: two lines of ambient routing, a one-line pointer in the plan file header, and the description boundary.
- **Revisit:** watch activation rate in pilots — does the plan-file header pointer actually trigger a new session — and how often preflight catches a mismatch.

## Extended survey: no confirmed decision overturned

- **Result:** a wider sweep of local and newly cloned systems overturned nothing. It produced additions: plan-time SHA and freshness check, forbidden-files with mandatory reason, three prerequisite edge types, an append-per-round execution log, two verification layers (task acceptance plus project-wide criteria), and a decisions section carrying a no-re-litigation rule.
- **Counter-evidence gained:** one system's own admission that a dispatch which isn't real makes progress reports fiction supports the built-in-delegation-only decision. Another's self-abandonment of its orchestration layer supports "the execution skill does not redo decomposition and ordering."
- **Revisit:** no successful instance of parallel *writing* was found anywhere in the survey — only read-only parallelism or unverified claims. Measure the actual benefit in pilots.

## Weak-executor path gets explicit activation and a guidance bundle

- **Plan:** hand detail-heavy prompts to weak executors; keep strong models thin.
- **Reality:** task-level detail alone may not be enough for a weak model — over-implementation, scope expansion, reimplementing what exists, and skipped verification also need addressing. But applying that same discipline to a strong model damages its autonomy.
- **Choice:** the strong path stays the default. The weak path and its guidance bundle activate **only** when the user explicitly chooses a lower-capability executor. Never classify automatically by model name, price, or speed. Do not adopt any always-on enforcement, and do not let the bundle substitute for intent-based review.
- **Revisit:** confirm in a real weak-model pilot that the bundle reduces over-implementation and missing evidence, that packet-writing cost stays below the saving, and that the rules don't leak into the strong path.

## Renamed for purpose and outcome; migrated skills preserved

- **Plan:** two naming tiers plus three renames were assumed sufficient.
- **Reality:** review found the names still abstract — purpose and outcome were not in the name. Skills should follow the pack's own skill-authoring reference rather than a norm invented for the pack. And the migrated skills were already individually well-built; combining them into a pack must not erode that.
- **Choice:** fix the naming principle as "purpose and outcome in the name" and rename accordingly. Author the core four to the skill-authoring rules (decision rules over transcripts, 400–2,500 tokens, sibling-discriminating descriptions). Edit migrated skills minimally — one to four focused edits each, adding interlocks only, never rewriting the body.
- **Revisit:** watch for misfires between planning and execution in pilots.

## "Contract steps, not cognition steps" adopted

- **Plan:** the pack was considered finished; next was piloting.
- **Reality:** a strong model follows a badly designed procedure just as faithfully as a good one, so the opportunity cost of an unnecessary step grows every generation. For a pack that had codified a large number of prescriptions, that is a structural threat. A self-audit found roughly thirty real violations.
- **Choice:** keep the structure — the four-station pipeline is exactly the auditable fixed pipeline the rule endorses, and the pack's four sources of value (storage, boundary, verification, concurrency) are orthogonal to model strength. Write the principle down in the repository rules, create the [rule ledger](rule-ledger.md), and run an improvement pass across every skill (detection delegated, judgment and edits kept with the lead). Add "steps the lead demonstrably did not need" to the pilot observation list.
- **Revisit:** re-verify the ledger's measured-workaround rows at the next model generation.

## Pack cut from 24 skills to 13

- **Plan:** move every development-related skill — the work loop, craft skills, and pack-maintenance meta skills.
- **Reality:** review of the assembled catalog showed the pack had swallowed more than it should. Craft and meta skills are independent of the work loop.
- **Choice:** cut to 13 (four core, two discovery, four execution support, three outbound). Eleven skills returned to their original repository as canonical home. The cut line is clean — zero references from the remaining 13 to any of the 11. General-purpose improvements made during the session were ported back to the originals rather than lost; pack-specific modifications were discarded.
- **Revisit:** observe in pilots how often the lead actually calls craft skills from outside the pack.

## Name settled: gigio-pack

- **Plan:** narrow metaphor-word candidates from a corpus of 500+ references.
- **Reality:** every external word was rejected as odd. The cause was over-optimizing for metaphor precision, which surfaced only unfamiliar words — while the reference points the owner actually admired were all familiar words. One leading candidate was disqualified because it reads as an unrelated word in Korean; another was already taken by a product in the same category. The only word that cannot feel awkward is the owner's own handle.
- **Choice:** `gigio-pack`, with `gigio-` as the prefix for the four core skills only. Three renames for clarity: the orchestration skill gained a verb; the session handoff skill adopted the term used by a major agents SDK; and the weak-executor skill was renamed to restore the original intent — a handoff to a less capable AI, not to an in-harness worker. The two handoff skills are now a deliberate pair, with the target in the name.
- **Revisit:** at public release, reconsider — eponym to product name is a standard rebranding path.

## Design record separated from the published repository

- **Plan:** publish the repository with its full working record.
- **Reality:** the record is candid Korean working material containing local filesystem paths, private project names, and workplace-boundary notes. A privacy review confirmed the skills themselves were clean and the exposure was confined to that directory.
- **Choice:** keep the raw record local and unpublished. Distill its durable content into three public documents — [principles](principles.md), [rule ledger](rule-ledger.md), and this log — plus a [prior-art](prior-art.md) summary, so that improving the pack later does not require digging through chat sessions. History was rewritten so the record was never published.
- **Revisit:** if the pack is ever handed to someone else, these four documents are what they get; check whether they are enough to make a change safely.

## Acceptance separated from the check command

- **Plan:** every task carries a `check` command, and a task whose check you cannot state is not plannable yet.
- **Reality:** the loop had quietly taken the shape of repository work. The four core skills carry about thirty lines of test, build, and commit vocabulary and none for research or open-ended work, while `find-unknowns` already classifies a result as executable or comprehension-checked and had nowhere downstream to send that classification. Two domains invert the rule outright. An experiment's check *is* the measurement, so a negative result is the deliverable rather than a defect to repair, and retrying it with a stronger model is the wrong response to a hypothesis that did not hold. Work judged by feel has an acceptance and no command at all. The [principles](principles.md#keep-context-usable) page had already required acceptance and verification as separate axes; the plan template had collapsed them into one field.
- **Choice:** add `acceptance` to the task fields and keep `check` as verification only. Treat a check that ran with its acceptance met as done even when the result is negative. Classify work built as planned whose result still misses the goal as a direction finding rather than one of the review's three lists. No new skill — a fourteenth name costs more than the fit it buys while none of this has been measured.
- **Revisit:** at the pilots, one of which should be non-engineering so the experiment case is measured rather than argued. Deliberately left untouched: completion still requires changed owned files under git, and file ownership is still the only parallel split. Both are wrong for a configuration sweep, where the unit of work is a run and sibling runs share an output directory — change them from a real run, not from this entry.

## Direction changes batch at the review station

- **Plan:** intent contradiction discovered mid-run stops the work and routes to the user — renegotiation as an exceptional event.
- **Reality:** the two pilot installs showed that outside ordinary engineering the flow reverses: the artifact rewrites the intent as the main path. One pilot opened with six of its seventeen settled decisions already superseded by play; the other's methodology is literally that observation selects the next study. Per-finding stops would make the human-owned boundary a bottleneck or teach sessions to route around it.
- **Choice:** user-set policy. Execution records intent contradictions in the Run log and keeps going unless continuing is certain waste; the review station batches all direction findings into one proposed top-half amendment diff, each line backed by the play or observation behind it, settled by a single approval. The boundary keeps its authority; it loses its per-event interruption cost.
- **Revisit:** pilot closeout — count amendment proposals per review. If the user keeps intervening mid-run anyway, the batching is theater; revisit.

## Git-created worktrees stay inside the repository

- **Plan:** prefer a harness's native worktree feature whenever it exists and send manual Git worktrees to another untracked location when the repository's local directory is not already ignored.
- **Reality:** the fallback permitted sibling directories such as `<repository>-worktree`, which scattered workspaces across the parent folder. A named branch created with Git remains usable by ordinary GitHub PR discovery; native creation mainly adds harness-owned placement and lifecycle behavior.
- **Choice:** explicit mechanism and directory preferences win. With no stated preference, create a Git worktree under the repository's `.worktrees/` directory and use the local Git exclude file when needed. Never leave the repository merely to avoid a tracked ignore edit. Choose native creation when the user asks for its handoff, restoration, or cleanup behavior.
- **Revisit:** if either primary harness makes manually linked worktrees unable to expose ordinary branch and PR state, record the observed version and move only that behavior into a dated harness-specific rule.

## PR bodies optimized for first-time readers

- **Plan:** use a prose-led `Summary` followed by `Validation`, with local checks listed directly in the body.
- **Reality:** PRs produced from active sessions assumed context that reviewers did not share, grew into long narratives, and repeated command lists or test output already represented by CI. The extra validation text did not help a reviewer decide whether the change was sound.
- **Choice:** repository templates remain authoritative. Without one, use `Context` and `Changes` as the two-section fallback. Add `Validation` only for manual results CI cannot prove or a material CI caveat; keep live CI status in the checks interface and collapse long supporting details. Add reviewer notes, user impact, migration, rollout, performance, or screenshots only when the change triggers them. The body must stand alone for a reader without the authoring session.
- **Revisit:** if reviewers repeatedly need another field across unrelated repositories, consider it for the fallback. Keep project policy in repository templates rather than growing the shared default.

## Skills gated to explicit invocation

- **Plan:** descriptions would carry a `Use when …` trigger precise enough that the harness would open the right skill at the right moment, and C4 ("explicit invocation plus ambient prose only") would hold because the pack shipped no hooks or daemons.
- **Reality:** C4 constrained the mechanism and left the trigger alone. Several descriptions named a *situation* rather than a request — "sizable work needs a written plan", "a large task has independent workstreams", "the user starts substantial work in territory they don't know well" — and a situation is something the model decides it is looking at. In daily use the pack activated across conversations that had asked for none of it, research and other non-engineering talk included, where an answer was the whole job. The prior-art survey had already recorded broad auto-triggering descriptions as a disqualifier in other packs, and this pack had shipped the same defect.
- **Choice:** state the gate in all 13 descriptions. A skill opens when the user names it, when the user asks for what it does, or when another pack skill name-calls it inside a run the user already started — and on nothing else. Each description carries the rule in its own words, since the harness reads them one at a time. Accept the loss: a user who would have benefited from a pass they did not know to ask for will not get it, which is cheaper than charging every conversation for one it did not want. Skill bodies are unchanged apart from `gigio-project-setup`, whose installed `AGENTS.md` block described routing as a standing instruction to plan sizable work.
- **Revisit:** if a pilot shows the pack going unused where it clearly would have paid off, widen the wording of the specific skill's request forms — never restore situational triggers, and never add an always-on instruction that recreates them from outside the pack.

## Invocation gate narrowed from thirteen skills to eight

- **Plan:** state the gate in all 13 descriptions, on the reasoning that deciding a procedure runs is the user's call in every case.
- **Reality:** applied to all 13 it was too wide. Five skills cost nothing when they open uninvited. Four of them — `deep-interview`, `commit-and-push`, `draft-pr`, `git-worktree-setup` — already described a request rather than a situation, so a harness matching the description was already the user asking, and the added gate text bought nothing. The fifth, `find-unknowns`, was the real error: gating it removed the one case where an unrequested pass is worth more than it costs, since it exists to fire before the user knows to ask and its worst misfire is a paragraph that can be skipped. The complaint that started this had never been about that skill.
- **Choice:** restore the five descriptions to their pre-gate text and keep the gate on the eight whose misfire lands on disk or on the bill — the four core skills, `session-handoff`, and the three that change who executes the work (`orchestrate-subagents`, `small-model-handoff`, `fable5-model-routing`). The deciding question is not who owns the decision but what an unwanted opening costs. `find-unknowns` is recorded as an explicit exception, the only skill here allowed a situational trigger.
- **Revisit:** if `find-unknowns` starts opening on conversations that only wanted an answer, narrow its situations rather than gating it, and check the always-on instruction layer outside this pack first — an `AGENTS.md` paragraph mandating the same behavior outranks any description.

## PR publication made forge-aware

- **Plan:** route Forgejo publication through its REST API or authenticated web UI because the `forgejo` binary is a server administration CLI and Gitea's `tea` does not prove Forgejo compatibility.
- **Reality:** the Forgejo project now publishes the `fj` user CLI. Version 0.6.0 creates, views, edits, assigns, checks, and merges PRs, including an explicit squash method. It uses API authentication separate from Git transport. Its create command has no draft flag, body edit has no body-file option, draft detection recognizes `WIP:`, and merge has no confirmation prompt.
- **Choice:** resolve the provider plus exact head and target repositories before mutation. Keep commit and push provider-neutral, use `gh` for GitHub, and require authenticated `fj` for Forgejo. Create Forgejo drafts with a verified `WIP:` title, use exact `owner/repo#index` references for management, and allow squash merge only after a separate explicit merge request and remote state gates. On GitHub, preserve `gh`'s native draft, body-file, required-check, head-OID match, and merge-queue behavior. Never install or authenticate a CLI implicitly. Delete a head branch only on explicit request.
- **Revisit:** simplify the adapter when `fj` exposes a native draft flag, body-file editing, structured output, a bounded check wait, or a merge confirmation mode.

---

## Preserve authorization across requested stages (2026-09-05)

- **Plan:** keep a hard stop between stations and treat a preflight mismatch as a new user decision.
- **Reality:** static review found clauses that also stop combined requests, unrelated dirty files, and work with settled permissions. The handoff template could turn an existing grant back into a confirmation requirement.
- **Choice:** retain the separate skills and their outputs, reuse established authorization, inspect discrepancies before asking, and carry grants plus pending operations into handoffs. Keep consequential unknowns, overlapping ownership, and unapproved external effects as boundaries. Remove the required comprehension quiz and automatic worktree cleanup.
- **Revisit:** use real execution feedback to assess unnecessary pauses and missed boundaries. This is an instruction audit, not a successful runtime pilot or a measured performance claim.

## Separate terminology curation from application (2026-09-10)

- **Plan:** keep domain craft outside the pack and preserve project decisions through the existing work-loop records.
- **Reality:** a completed terminology workflow needed a durable reference for definitions, accepted expressions, sources, and historical corrections. The user explicitly requested separate skills for defining/updating/recording and looking up/using that reference. Applying an existing decision should not start another research pass.
- **Choice:** add `curate-terminology` and `use-terminology`, bringing the pack to 15 skills. Ship the portable workflow and an adaptable standing-instruction example; keep domain definitions and mutable literature in each project. English terms remain primary, source scope remains explicit, and local editorial restrictions remain local decisions. Honor explicitly requested ongoing compliance without making installation an always-on policy. Preserve originals and identifiers while correcting authorized managed prose during the task.
- **Revisit:** if real use shows duplicate retrieval, unclear authority, or records that require maintenance outside current work. Static package validation does not establish a successful runtime pilot.

## Both terminology skills become standing policy (2026-09-10)

- **Plan:** the initial terminology pair would activate on request or a separately requested standing instruction.
- **Reality:** the user requires both on every task and wants curation to study expressions beyond nouns, with stronger source selection that filters generated derivative writing.
- **Choice:** supersede the initial opt-in terminology policy. Make both skills default to every task and wire them during project setup. Curate relevant changes in context; preserve explicit read-only restrictions and avoid artificial writes. Prefer established project documentation and maintainer blogs, influential papers including recognized preprints, and their author explanations. Use available paper tools actively. Record positive verbs, collocations, and project explanation patterns with their conditions. The initial treatment of the user-named projects as exclusions is superseded by the source-scrutiny clarification below.
- **Revisit:** use real tasks to check missed application, unnecessary research, source quality, and semantic transfer. Static checks cannot prove runtime loading or authorship.

## Confirm local company usage separately (2026-09-10)

- **Plan:** prefer established external sources and distinguish internal labels in terminology records.
- **Reality:** a small set of company proper names and familiar terms with local meanings is legitimate, and external documents cannot establish what the company intends by them.
- **Choice:** check existing records, ask the user concise questions about unresolved local cases, and record meaning, scope, audience, and dated confirmation. Preserve confirmed local usage and clarify it for other audiences. Keep intended meaning distinct from implementation claims; source filtering does not erase company conventions.
- **Revisit:** when a recorded answer conflicts with new information or the audience or product context changes. Do not repeat settled questions on every task.

## Treat AI-project examples as a source-quality warning (2026-09-10)

- **Plan:** interpret the named projects as a fixed source exclusion list.
- **Reality:** the user clarified that those names illustrate a broader concern about AI slop in AI-related project documentation.
- **Choice:** retain the examples and replace name-based exclusion with heightened scrutiny of provenance, primary-source support, definitions, and correspondence with implementation. Filter unsupported wording across comparable projects without treating the examples as exhaustive or judging authorship from style alone.
- **Revisit:** when actual source passages and implementation checks support changing their eligibility as terminology references. Keep local naming conventions separate from claims of general industry usage.

## Standardize terminology storage and reference records (2026-09-10)

- **Plan:** a short root reference and optional topic files would follow each project's existing paths, with source and maintenance records grouped as needed.
- **Reality:** the user wants a predictable structure that scales beyond one file while keeping representative terms visible at the project root, and requires a separate document for references.
- **Choice:** use root `terminology.md` for representative definitions and the index; store detailed Markdown documents under `docs/terminology/`; keep `docs/terminology/references.md` for source records only. Link new or changed entries to stable reference IDs, including dated local decisions. Keep source records separate from definitions and maintenance history. Preserve working links and source IDs during authorized migration, and honor an explicitly mandated legacy layout until it is migrated.
- **Revisit:** when the root summaries or topic files become difficult to navigate. Split detail by reader need while preserving the entry point and source traceability.

## Scope redrawn: the document exit is loop work (2026-09-10)

- **Plan:** the pack holds the loop and nothing else; writing style, diagram conventions, and other craft belong to domain skills (Scope, 2026-07-26).
- **Reality:** a week of daily use showed that research and analysis work leaves a session as a document, and that documents were the artifact the author corrected most. Across eight days and four harnesses the same corrections recurred several times each: the document had to stand alone without the session, lead with conclusions and structure without losing depth, state up front that an absent record is not absent work, carry a source link on every material claim with a link policy that changes by audience, keep figures that answer one question, and pass a two-axis sensitivity review before upload. No installed writing skill carried those house rules; the loop had exits for code (`commit-and-push`, `draft-pr`) and none for findings.
- **Choice:** redraw Scope instead of carving an exception. The exits from a session are In: next session, weaker model, code as a PR, findings as a document. Prose style and figure craft stay Out. `share-internal-doc` (named `write-internal-doc` until 2026-09-10) is the fourth exit skill, with an explicit request trigger like the other procedural skills; it owns reader, shape, format, claim status, sharing, and medium, and delegates prose to `slop-aware-writing`, Korean to `korean-clarity`, styling to `notion-doc`, and figures to the gigio-figures skills, naming them conditionally because they live outside the pack. Rules were harvested from the author's own corrections (Korean record in `docs/design/internal-doc-skill/`, gitignored) and checked against a survey of about thirty public documentation skills ([prior-art.md](prior-art.md#documentation-skills-2026-09-10)).
- **Revisit:** after the first five shared documents produced with it. If its rules read as generic writing advice by then, move it to agent-skills; if the sharing pass, the reading rule, and the house vocabularies are what earned the place, keep those and cut the rest.

## Local Python standards with an official Pydantic companion (2026-09-10)

- **Plan:** keep language craft outside the pack and consider composing existing Python, Pydantic, and modularity skills.
- **Reality:** source review found useful official Pydantic guidance and several overlapping community skills, but the owner selected only Pydantic for external reuse and explicitly requested locally authored Python rules in gigio-pack.
- **Choice:** add `python-coding-standards`, bringing the pack to 17 skills alongside the document exit. Keep one reusable Python task entry with colocated references for types and enums, module boundaries, Pydantic integration, and correctness/testing. Preserve repository decisions and public behavior. Use the official external `pydantic` skill for its library guidance, with a pinned source and version-matched fallback; do not vendor other Python skills or install global packages as part of publication. Existing loop skills and their invocation policy remain intact.
- **Revisit:** after actual Python implementation and review tasks reveal missing decisions, duplicated guidance, or over-broad activation. Package checks and discovery do not establish model behavior or complete the two work-loop pilots.

## Python defaults favor consistency and source-local explanations (2026-09-10)

- **Plan:** the initial Python skill offered internal dataclasses and typed dictionaries alongside Pydantic, required annotations mainly at public interfaces, and preserved existing tooling without a preferred setup workflow.
- **Reality:** the owner wants organized code rather than impressive architecture, Pydantic-centered data models, explicit Python 3.12+ types even on locals and complex SDK objects, uv-managed project environments, and explanations that do not create document synchronization work.
- **Choice:** supersede those initial defaults. Use Pydantic for application-owned records, with concrete-need exceptions for other representations; require explicit declarations and preserve legal binding syntax; prefer uv metadata, lockfiles, and purpose-specific development groups, with pip-style installs reserved for documented exceptional environments. Put needed intent and background in module, class, model, and function docstrings or local comments. Keep policy and information that needs a cross-file view in separate documents, without duplicating implementation. Preserve external skill selection, compatibility boundaries, and existing publication authority.
- **Revisit:** when actual tasks reveal an interoperability requirement, conflicting supported runtime, misleading annotation, or explanation that cannot be maintained close to code. Package and example checks remain distinct from model behavior.

## Shared-document references follow concrete decisions (2026-09-14)

- **Plan:** keep document principles in the entry point and detailed guidance in conditional references.
- **Reality:** rereading the reinstalled Astra guide and Skill Builder showed that the draft still repeated reference explanations and used conditions such as preparing content for recipients that apply to almost every document. Reader questions remained in an output-template path even though they were instructions for review.
- **Choice:** consolidate the routine principles and give each reference a concrete reading condition and purpose. Keep recipient safeguards, publication authority, source preservation, and the dark default in the entry point. Move reader questions into a review reference, and keep specialized handling for substantial structure changes, difficult claims, rendering, and sensitive distribution in their respective references. Preserve the session-supported preferences without imposing a length quota or Astra-specific runtime behavior.
- **Revisit:** when an ordinary document task exposes a missing essential instruction or a reference condition that loads too much or too little. Package checks can verify structure and links; this change does not claim measured model behavior.

## Shared-document principles apply across media (2026-09-14)

- **Plan:** preserve accumulated document corrections in one internal-sharing skill, including a fixed review spine, house wording rules, and HTML/Notion production guidance.
- **Reality:** repeated corrections in original Codex and Claude Code conversations distinguish reader context from session narration, depth from verbosity, synthesis from fact lists, and explanatory figures from decoration. The package had mixed those durable preferences with individual report formats and conflicting instructions. Official Astra guidance also recommends concise discovery, contextual loading, clear decision boundaries, and explicit completion.
- **Choice:** keep the requested internal-document scope and rewrite its core around independently understandable, supported, usable documents in any medium. Make structure, sources, sharing, and rendering separate conditional references. Replace the outline asset with reader questions and add illustrative editorial repairs. Preserve the dark screen-document and figure default while respecting print and destination behavior. Keep private transcript records outside the public package; publish reusable findings and source guidance. Retain actual review requirements and existing authorization without adding a pause to every rewrite.
- **Revisit:** after real documents expose a missed condition or a remaining conflict. This revision uses historical task feedback, package checks, and static review; it does not claim a new behavioral trial or completion of the existing pilot.

## Shared documents default to dark (2026-09-10)

- **Plan:** the harvested medium rule said light color scheme unless the reader asked otherwise, with dark mode as optional support; the figure skills the document exit delegates to default to light as well.
- **Reality:** the pages and figures produced under that rule read as too bright to the author, and the one dark render made earlier had needed a contrast repair after the fact.
- **Choice:** dark is the default for the page and for every figure in it, with one token set shared by text, tables, and figures. Light is a separate render made only when the user asks for it or names print, and the page does not follow the reader's operating-system theme unless an adaptive page was requested. Requests to `data-chart`, `technical-diagram`, and `mermaid-diagrams` name the scheme because their defaults differ. The skill was renamed `share-internal-doc` the same day so that a search by purpose finds it.
- **Revisit:** at the five-document review already scheduled for this skill, and if the external figure skills adopt a dark default, when the per-request instruction becomes redundant.

## Plan file generalized beyond repository code, top half handed to the user (2026-09-11)

- **Plan:** the plan file assumed a Git repository — `Planned at: commit`, `owns-files`, completion judged by `git log` — and its anchor was PROJECT.md, skipped silently when absent. The template had no section the user owned; the whole file was planner-written.
- **Reality:** three real plans were written between 2026-09-05 and 2026-09-10 in a multi-repository workspace that is not itself a Git repository; two were outside ordinary code work (a document review with Notion publication, a dataset curation run). Where the format did not fit, the planner improvised: a snapshot hash in place of a commit, Notion pages and review memos under `owns-files`, a `git log` completion rule that could not run. None had a PROJECT.md; one wrote "judged by AGENTS.md and terminology.md" inline, and a vault project wrote a handoff instead of a plan because `find-unknowns` routed only repository work to planning. The `acceptance` field, by contrast, was filled without strain in all three. The user then said the deciding thing: the plans had drawn almost no corrections because the user did not trust them, so their recurring contents are the model's habits, not measured need. The pack's own principle already says every rewrite dilutes the user's utterance.
- **Choice:** fix only what the format could not express, and give the user the top of the file. `Planned against` replaces the single commit with dated, re-verifiable anchors — commit, snapshot hash, dataset or document revision, a named model or tool — and an anchor that no longer holds blocks its tasks; a similar input is not a substitute. `owns` and `avoid` replace `owns-files` and `avoid-files` and cover paths, run output directories, and external resources by URL or ID; completion reads the named artifact or resource where `git log` cannot. `Judged against` names the intent documents a plan answers to when PROJECT.md is absent, and a plan that narrows a broader design names it there instead of copying it. Goal, Out of scope, and Judged against are marked human-owned and written in the user's words; the planner names its proposed lines in the announcement. Out of scope now also carries the side effects the executor may not cause. `find-unknowns` hands every accepted brief to planning, not only repository work. The review station reads the user's half first, quotes the line each finding ties to, checks that the inputs actually used are the ones named under Planned against, and lists work resting on planner-proposed lines the user never confirmed as its own class, **unconfirmed basis**; the plan carries those lines in one plain sentence at the end of Judged against until the user confirms or edits them. Not added: separate Authority, Environment, and Evidence-rules sections, although all three recurred in the three plans — recurrence in planner-written text is not user need.
- **Revisit:** after the next three plans written with this template, one of them outside code. Keep the sections the user read and corrected; drop what stayed as written. Decide the three withheld sections then, from the same measurement, and ask the user directly what made the earlier plans untrustworthy — length, paraphrase, or results that never came back. The count of proposed lines the user confirmed, edited, or left untouched by review time is the trust measurement.

## Explanations and visuals must earn the reader's attention (2026-09-15)

- **Plan:** preserve source limitations and standalone readability through the shared-document principles and conditional references.
- **Reality:** direct feedback identified accurate but unhelpful prose about snapshot behavior, record interpretation, and chart interactions. Even the revised source still required a generic reading rule. The supplied [dashboard critique](https://kucharski.substack.com/p/ten-reasons-your-vibe-coded-dashboard) also showed how repeated metrics, equal-weight panels, and unselected data leave the reader to find the point.
- **Choice:** require a concrete reader use for an explanation. Keep consequential qualifications beside their claims; delete redundant defenses, familiar definitions, and self-appraisal. Let dates, labels, and controls convey necessary interface state. Select and prioritize figures around the question, and keep captions consistent with displayed results. Update the linked references and rule ledger without changing the dark default, privacy handling, or source-preservation obligations.
- **Revisit:** when a real document either retains reader-irrelevant scaffolding or loses a condition needed to interpret its conclusion. Static package checks and editorial examples do not establish improved model behavior.

## Historical open items before September 17

The table records the earlier state. The September 17 decision below resolves or supersedes several defaults, including multi-repository context, adaptive experiments, digest updates, and immediate direction discussion.

| Item | Default | Decide when |
| --- | --- | --- |
| Plan directory name | `.plans/` | On first friction |
| Where to plant intent for non-repository projects | Plans name their intent sources under Judged against (AGENTS.md, a design document, a brief), and `.plans/` sits under the root the user works from, repository or not (2026-09-11). Whether PROJECT.md's six questions fit a multi-repository workspace or a vault is undecided | First PROJECT.md written for a workspace or vault |
| Information boundary for work-context projects | Undecided | First such application |
| Deferred concepts (three-state memory transitions, hard notepad budgets, verified-vs-reported markers) | Not adopted | If real usage shows the corresponding problem |
| Experiment-shaped work beyond the basics: run manifests, seeds, quota fields, mid-sweep triage | Runs are tasks owning their output directory (adopted 2026-07-26); a run's named model or dataset is a Planned against anchor that blocks when absent (2026-09-11); nothing further | First real experiment loop — one pilot's planned three-model comparator sweep is exactly this shape |
| Decisions-digest growth in high-reversal domains: one pilot opened with 17 decision rows plus 6 supersessions on day one, and no compression or retirement rule exists | Keep appending, supersede never delete | First time loading the table becomes a burden |
| Whether batched direction amendments actually hold — or the user keeps intervening mid-run regardless | Policy adopted (see "Direction changes batch at the review station"); count proposals per review | Pilot closeout |
| Whether `share-internal-doc` stays in the pack or moves to agent-skills | Merged into `technical-report-writing` and removed from the pack (2026-09-24) | Closed |
| Whether Authority, Environment, and Evidence-rules sections earn a place in the plan file | Not added (2026-09-11). Out of scope carries forbidden side effects in the user's words; Planned against carries named inputs; nothing carries "what a check does not prove" | After the next three plans: keep only what the user read and corrected |
| Why earlier plans drew no user corrections — length, paraphrase, results that never came back | Top half in the user's words (2026-09-11); ask the user, then count corrections | After the next three plans |

**Historical pilot proposal.** At that point, two pilot projects were proposed before claiming the workflow had been demonstrated. The current instruction changes remain unproven by behavioral pilots; that does not block publishing them for review. Pilots measure four things: whether parallel writing actually pays off, whether the plan file carries enough for handoff between workers, which steps the lead demonstrably did not need — a removal list, not a success list — and what the acceptance field actually gets filled with outside ordinary code work.

## Research-capable project continuity (2026-09-17)

- **Earlier model:** project records and plans emphasized repository changes, fully ordered stages, and implementation checks.
- **Finding:** research, training, data review, and benchmark work can advance by changing what is understood; their next useful action often depends on results. A Git repository does not define the whole project.
- **Decision:** maintain user-owned direction separately from current understanding, plan through the next useful decision, and interpret negative or inconclusive evidence without demanding code changes. Quick checks stay autonomous within existing grants. New direction or newly proposed long activity needs the user's decision. Keep research methods in Research Credo and harness/coding helpers in Agent Skills.
- **Revisit:** when a real continuation loses a decisive finding, repeats an abandoned approach, or cannot locate its sources. Add a targeted correction instead of reinstating a universal stage or reporting template.

The current [principles](principles.md), [rule ledger](rule-ledger.md), and [migration](migration.md) supersede conflicting older entries. These are design decisions and static review results, not measured model improvements.

## Document craft and shared delivery (2026-09-20)

- **Plan:** use one writer for general documents and a sharing skill for colleague-facing requirements.
- **Reality:** generic reader-value guidance left explicit editorial preferences weak, and source links could shift essential explanation into inaccessible working records.
- **Choice:** keep editorial defaults and genre-aware structural examples in technical-report-writing. Apply it once from share-internal-doc for substantive writing, then check recipient context, actual citation destinations, and delivered rendering. Preserve existing publication and source-retention boundaries.
- **Revisit:** when a real document loses a required explanation, repeats authoring narration, overloads tables or figures, or requires inaccessible sources to understand its main point.

## share-internal-doc retired into the writer (2026-09-24)

- **Context:** the skill was adopted 2026-09-09 with a review point after five shared documents. By 2026-09-23 its editorial content had already moved to `technical-report-writing`, leaving recipients, source access, the latest shared copy, the sharing pass, and delivery. Every one of those is the last stage of a document task; no request delivers without a document, so the two skills were always loaded together, and the writer's own sharing section repeated the same rules.
- **Choice:** move the remaining rules verbatim into the writer's `references/sharing-and-delivery.md` in agent-skills and remove the package from this pack. The sharing pass keeps its status as user-set policy from the September 5 and 6 review rounds. A request that names `share-internal-doc` is served by the writer. `docs/rule-ledger-history.md` keeps the harvest history.
- **Consequence:** the pack no longer ships a document exit; code leaves a session as a PR through `draft-pr`, findings leave it through the writer. Installed copies are removed with the Skills CLI.

## Handoff file becomes a task the successor executes (2026-10-03)

- **Plan:** the published skill wrote `handoff.md` at the project root from a fifteen-section template. It stated its requirements three times (the skill's list, the template's headings, and an operating contract inside the file), split what comes next across four sections, and carried plan-loop wording such as "next useful decision". An unpublished 2026-09-24 rewrite added provenance, an environment block, a successor-model reference, and runtime settings, and grew the skill from 13 KB to 30 KB.
- **Reality:** on 2026-09-24 the user set the `.handoff/<date>-<time>-<task>.md` policy because a root `handoff.md` collided across concurrent tasks, and said the successor, often in another harness, receives the file as its only input. On 2026-10-03 the user said the skill read as much more complex than intended and named the failure: given only a handoff path, a successor often improves the handoff file instead of doing the work. The user asked for a concise file that says what was being done, what is to be done next, and which concrete questions to put to the user, shaped by find-unknowns.
- **Choice:** the generated file opens with a bold instruction that it is the reader's task and must not be edited, summarized, reviewed, or improved unless the user asks to revise the handoff. The description gains a NOT clause for a given handoff path or "continue from this handoff", and the skill body says the same in one line. The template has eight short sections with a single Next Actions section and a Questions for the User table (question, why it changes the work, options with a recommended default, what to do if unanswered) that applies the find-unknowns mini-interview rules without requiring that skill. Kept from the 2026-09-24 draft: the `.handoff/` path, supersession by a new dated file with a one-line forward pointer in the old one, the same treatment for a legacy root `handoff.md`, harness-internal state recorded as ended with only externally checkable handles listed as running, origin harness and session id for transcript recovery, dated verbatim user quotations, and the writer's scope. Dropped: the in-file operating contract, the successor-model reference, the runtime-settings block, the separate environment section, and most source notes. The skill is about 7 KB.
- **Revisit:** after the next three handoffs given to a successor by path alone. If a successor still edits the file, strengthen the opening instruction rather than adding sections; if a successor had to ask the user for something the writer knew, add that row to the template.

## Terminology skills narrowed to a naming glossary (2026-10-03)

- **Plan:** the 2026-09-10 entries "Both terminology skills become standing policy" and "Standardize terminology storage and reference records" made both skills apply to every task through their descriptions and had curation record verbs, collocations, sentence patterns, project explanations, and expression corrections, each with conditions and neighboring concepts.
- **Reality:** the user found the result far more complex than intended. Many entries prompted "do we really need to collect this?", the records read like teaching sentences to a toddler, and the intended work, surveying industry projects, academia, and competitors to settle one standard name, did not get done. Collections built under the skill admitted undisputed field terms and attached a "do not write X" caveat to nearly every row. Competitor products appeared nowhere in the source policy. The descriptions also did not produce every-task use: across 3,930 Claude Code transcripts, curate-terminology was invoked in 6 and use-terminology in 11. Projects got every-task behavior from their instruction files and their own `terminology.md`.
- **Choice:** supersede the expression-research, claim-discipline, and every-task-description parts of those entries. Keep the two-skill split, the root `terminology.md` with `docs/terminology/` and a reference-only `docs/terminology/references.md`, terms in the field's language with meanings in the reader's language, user-confirmed local names, scoped user wording bans, and scrutiny of AI-generated sources. A row now enters only for competing names, a local meaning that differs from the field's, or an explicit user decision, and takes one line: Term, Meaning, Elsewhere called, Reference. Curation surveys established projects, papers, and competitor products. use-terminology only reads and applies, and hands gaps to curation. Every-task use comes from a two-line snippet in the project's instruction file. Claim strength and sentence style belong to copydesk; paper search and saved copies belong to literature-research. curate-terminology shrank from 43KB in 8 files to about 11KB in 4, and use-terminology from 8.5KB to about 1.2KB.
- **Revisit:** when a collection built under this version misses a name the project needed, or fills again with rows that fail the inclusion test.
