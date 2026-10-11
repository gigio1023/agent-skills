# Prior Art

What was surveyed before writing this pack, what was taken, and what was left. Kept so that a later change can start from "this was already considered" rather than from scratch.

Roughly thirty agent workflow systems, skill packs, and planning harnesses were read at source level across eight research rounds, plus first-party documentation and measured claims. Nothing was adopted wholesale. Every system below contributed either a mechanism or a counter-example.

This historical survey used the earlier six constraints; the current [principles](principles.md) supersede conflicting workflow conclusions below. A rejection here means "does not fit this pack's constraints," not "is a bad system." Several rejected systems are excellent at what they set out to do.

## What the survey confirmed

These were already the plan and survived contact with the evidence:

- **Three record types** — a slow identity document, short-lived plan files, and pointers. One surveyed system had already codified "the plan file is working memory, not a deliverable; gitignore it and promote deliberately." Most others lean everything durable and suffer committed-artifact bloat as a result.
- **Intent-first review in a separated context.** Measured research supports it: tuning file structure did not move instruction-following rates, whereas session length and generation volume did. The budget belongs in re-grounding and separated review, not in polishing documents.
- **Strong-model autonomy as the default.** The clearest counter-example in the survey was a system that structurally forbids going back from execution to planning — even when the model has concluded the plan needs rewriting.
- **Markdown-only.** Two systems in real daily operation run on nothing but markdown, one mirroring across eight harnesses.
- **Execution as an explicit invocation.** Nine of ten implementations read separate it; the one that didn't is a thousand-line outlier.
- **Planning-time ownership partitioning.** Verified by a real incident in one project's issue history.
- **A pack of about five to a dozen skills.** One project abandoned its own orchestration layer after significant adoption — supporting the rule that the execution skill must not redo decomposition and ordering.

## What the survey changed

1. **Pointer wiring.** Claude Code does not read `AGENTS.md`. Planting must be a pair: `AGENTS.md` plus a `CLAUDE.md` bridge (first-line import or symlink).
2. **Body placement is the compaction-survival path.** Only paths imported from the root `CLAUDE.md` get re-injected from disk after compaction and inherited by subagents. Content placed in path-scoped rules or nested files silently disappears. Principle: **pointers where they get re-injected, bodies in the file that gets re-read.**
3. **Review needs input independence, not just context independence.** One system's judge had genuinely fresh context but was fed the executor's own self-description, which made it powerless. LLM judgment of completion claims measured weak across five judges and five prompts. So the reviewer's job is not to judge — it is to (a) collect independent evidence by re-checking files, runs, and environment state, and (b) compare item by item against the identity document. The second is text comparison, which models do well.
4. **Question wording.** "Why does this exist" is forced to be a **diagnosis** — one concrete incident of why the current state doesn't work — rather than an aspiration. "The most important open question" is forced to be a **risk** — what, if wrong, collapses everything.
5. **Cheap packets pass paths, they don't compile content.** One project deleted its eight-section assembled brief in a controlled evaluation and replaced it with three path slots, reaching equal quality at a fraction of the prompt size. Inlined bytes go stale the moment the file is edited. So the plan file is written to be self-sufficient, and the packet carries paths plus execution discipline only.

## Mechanisms adopted

| Mechanism | Where it landed |
| --- | --- |
| Stable append-only IDs, never renumbered | Plan template |
| `files` / `action` / `acceptance` / `verification` separated per task | Plan template |
| Requirement ↔ task coverage table, so a missing requirement shows structurally | Plan template |
| Plan-time SHA plus freshness diff | Plan template, execution skill |
| Three prerequisite edge types (blocking / related / derived) | Plan template |
| Forbidden-files list with a mandatory reason | Plan template |
| Append-per-round execution log | Plan template |
| Two verification layers: task acceptance plus project-wide criteria | Plan template, review skill |
| Judgment rules anchored to the actual decision that produced them | `PROJECT.md` structure |
| Human-owned section tag | `PROJECT.md` two-speed structure |
| A decisions section that later sessions may not re-litigate | `PROJECT.md` |
| Fail-open start check | Execution skill |
| Worker prohibition list (no recursive spawning, absolute paths, never mark failure complete) | Worker preamble |
| Loud fallback — a silent fallback is a test failure | Execution skill |
| Deviation recorded twice: central four-field log plus an inline breadcrumb at the change site | Notes convention |
| Just-in-time planning — detail only the next stage | Planning skill |
| Ground-truth evaluation, and the courage to delete a feature that fails it | Repository maintenance |

## Not adopted

| Concept | Reason |
| --- | --- |
| State machines, transition tables, stop-hook session control | Structure refusing the model's judgment is the exact failure this pack is built against. Violates C2 and C4 |
| Multi-stage intent rewriting pipelines | Intent lives in one document. Every rewrite dilutes the original utterance — that dilution *is* the pain being solved |
| Full bootstrap injection at every session start | A permanent cost. A pointer plus re-reading the file achieves the same thing more cheaply |
| Mandatory TDD, forced red→green | Previously rejected; unchanged |
| Persona role-play and ceremony-heavy halts | Violates zero-homework and generation tolerance |
| Hard dependency on a CLI binary | Cross-harness only holds if plain markdown plus skills is enough |
| A canonical artifact registry with a consistency-check suite | Once the state set grows, maintaining consistency becomes its own subsystem. This is why there are only three record types |
| Separate receipt files by default | Review verdicts flow back into the plan file and the identity document instead |
| Automatic ambiguity scores and numeric exit thresholds | Delegating to a number does not replace a strong model's judgment |
| Per-session persona limits and similar weak-model compensations | A strong model can use the same lens twice in different ways. Violates C2 |
| Build-time prompt assembly | Measured amplification of nearly seven times in one system |
| Instructing primitives the model does not have, via prompt | Gossip and consensus protocols described in prose do not become real |
| Undocumented or unwired commands | One surveyed project documented hundreds of lines of commands that did not exist |
| Any number presented without a measurement | — |

## Deferred, worth revisiting

Not adopted now because each adds a device, but the underlying problem is real. Revisit if real usage produces the corresponding symptom:

- **Three-state memory transitions** (active / stale / hardened) — dropping a lesson from context once it graduates into a rule. Revisit if the identity document's lower section bloats.
- **Hard section budgets for a notepad.** Same trigger.
- **Verified vs agent-reported markers** as an explicit display convention. Revisit if review output starts blurring the two.

## Open tension

**No successful instance of parallel *writing* was found in the entire survey** — only read-only parallelism, unverified claims, or implementations belonging to the abstraction-heavy designs this pack rejects. The decision to support parallel execution stands, but it is the single least evidence-backed decision here, and the pilots exist largely to measure it.

The counter-argument on record: workers may need context accumulated across tasks, in which case the plan file is not a sufficient handoff medium. That is the second thing the pilots measure.

## Ecosystem caution

- Read `SKILL.md` before installing anything. A methodology hides in the breadth of an auto-trigger description — a wide description means that pack's philosophy seeps into every task.
- Pin a revision. A published security survey found a meaningful share of public skills carrying critical issues.
- Popularity is a weak signal. Inspect substance.
- A package-install failure is a human checkpoint, not something to retry through.

## Terminology workflow adopted (2026-09-10)

Source: a completed project terminology curation and modularization task, followed by the user's request to package its maintenance and application separately. This is observed workflow provenance and user-selected policy, not a claim that the new skills have passed model trials. Private source texts, project names, and workspace paths are excluded from the public package.

Adopted: established English terminology with contextual explanations; primary-source verification matched to the claim; distinctions between field usage, source-specific definitions, internal names, and editorial choices; local preservation of newly discovered relevant papers with version, hash, extraction status, and linked metadata; a short root reference with topic, anti-pattern, and source records; stable finding IDs; correction of encountered managed documents within existing authority; and explicit project instructions for ongoing use.

Excluded from the reusable method: the original task's model selection, parallel subagent count, corpus size, private examples, and a universal ban inferred from a local expression preference. The skills do not install hooks, ship a domain glossary, publish collected material, or start a repository-wide audit merely because a phrase is unfamiliar.

The user's 2026-09-10 revision supersedes the initial activation choice: both terminology skills apply on every task. It also makes representative source selection explicit: widely adopted projects, influential papers and recognized preprints, maintainer and author blogs, active paper discovery/read tools, and rejection of AI-generated derivative prose as a wording authority. The named projects are user-provided cautionary examples, not a fixed exclusion list or independently established authorship findings. Their role is to motivate heightened scrutiny across AI-related project documentation. Expression research now includes verbs, collocations, sentence patterns, and how a system's purpose and components are explained. Kubernetes and Helm documentation provide small linked examples; no domain corpus or model trial was added.

## Terminology workflow narrowed (2026-10-03)

Collections built under the 2026-09-10 method turned into writing rulebooks: rows for undisputed field terms, sentence templates, project explanations, and caveats on what not to write. The revision keeps the layout, the two-skill split, local-name confirmation, scoped user bans, and scrutiny of AI-generated sources. It drops expression research, the Kubernetes and Helm examples, literature saving, and the every-task descriptions, and adds competitor product documentation as a source class beside established projects and papers. Paper search and saved copies now point to literature-research in research-credo; claim-strength repair points to copydesk in agent-skills.

## Documentation skills (2026-09-10)

Surveyed before writing `share-internal-doc` (then named `write-internal-doc`): about thirty public skills in twenty-five repositories, cloned and read at source level, plus the author's own retired documentation skills recovered from agent-skills history. Verdicts per skill are in the local Korean record (`docs/design/internal-doc-skill/`).

**Where the ecosystem converges.** Conclusion first, with the same two exceptions everywhere (chronology as content, a hostile reader). One primary reader chosen before drafting, with familiarity setting the level of detail. A cold read by a reader with no context. Confidence that decides the wording, with locators a reviewer can reopen. Never invent a number. Decide, then mark for review, instead of an open-questions section. Figures that answer one question and carry a caption. HTML for human attention, Markdown for line review.

**Taken.** The Minto gate question and its exceptions; the confidence table from a source-integrity skill, rewritten as prose because the author bans bracket tags; the fresh-context reader test with predicted questions; the silent-read margin questions; tables for reference data and prose for reasons; the chart discipline of Tufte-style reports; action titles and one accent color; the medium rule that a wide HTML page beats a narrow column for a desktop reader; recording failed searches rather than filling gaps.

**Left.** Harness-thick skills whose bodies are mostly telemetry and prompt protocol (the exact shape the principles reject); mass-produced skill farms; generic API-documentation templates the author's own retired skills already exceeded; Diátaxis quadrant purity, which fits product documentation sets rather than research reports and memos; scoring rubrics inside skill bodies; rules about em dashes and horizontal rules, which are a linter's concern.

**Covered by no public skill.** Reading records without treating absence as fact; a two-axis sharing pass (company risk and the poster's own risk) with "facts keep names, evaluations lose them"; bilingual figures translated against a glossary and numerically re-checked; moving session narration into a methods appendix; a standalone spine with an opening block and an about-this-document close. These are what the new skill adds; everything else it delegates.

## Python standards source selection (2026-09-10)

The owner selected the official [pydantic skill at 9e9390ee24d44b32cf5379c58acaebd7563f5f86](https://github.com/pydantic/skills/blob/9e9390ee24d44b32cf5379c58acaebd7563f5f86/skills/pydantic/SKILL.md) as an external companion and requested local authorship for the other Python rules. The upstream repository is MIT-licensed; its general Pydantic skill is distinct from Pydantic AI and Logfire skills. No upstream payload is copied into this repository.

The survey also inspected [Sylla coding standards](https://github.com/Sylla-BV/sylla-skills/blob/768c89cde09dae68a30ed6264b411c4f0e98980d/python/coding-standards/SKILL.md), [reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill/blob/018b4d66d5e879e447654076cab7dadf935fee87/SKILL.md), and [AGNTCY schema generation](https://github.com/agntcy/coffeeAgntcy/blob/ab8430eec963c39ebcd77924fff8ee3588d6f395/.agents/skills/jsonschema-to-pydantic-lungo/SKILL.md). They establish that related public skills exist; none is adopted, forked, or required by this pack. The local skill is written from the owner's selected preferences and primary Python, Pydantic, and tool documentation, linked in its own references.

Retained decisions: repository precedence, explicit enum values, deliberate validation/serialization boundaries, semantic module responsibilities, behavior-preserving extraction, and proportional checks. The 500/1,000-line reminders are local review preferences, not source-backed universal limits. No external Python pack installer, mandatory tool migration, or model trial is included.

The subsequent owner clarification selects Pydantic-first records, explicit Python 3.12+ annotations including locals and SDK values, uv project management, and source-local explanations. These are local preferences, not claims that Python or Pydantic requires them. Python's typing documentation and PEP 526 establish legal annotation forms; uv's official documentation establishes dependency groups and locking behavior. Sources and syntax belong in the skill's colocated references. Intent-oriented docstrings and comments follow the existing Python documentation practice without copying or requiring an additional external skill.
