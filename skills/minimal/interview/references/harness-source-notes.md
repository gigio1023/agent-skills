# Harness Source Notes

Research refreshed on 2026-07-10 from temporary local checkouts. Every repository was updated with a fast-forward-only pull before review. The revisions below make the research basis reproducible; they are not runtime dependencies of the skill. On 2026-10-07 every cited repository still existed unarchived and every pinned revision still resolved; the material was not re-reviewed. On 2026-10-12 the skill was renamed from `deep-interview` to `interview` and its question contract changed from one question per turn to dependency-ordered rounds; see [Question contract revision](#question-contract-revision-2026-10-12). The same day it took on the four kinds of unknowns and its description narrowed to explicit interview requests; see [Unknowns revision](#unknowns-revision-2026-10-12).

## Primary Source

[Q00/ouroboros](https://github.com/Q00/ouroboros) at `98d3d66d4123` is the primary method source. Reviewed `skills/interview/SKILL.md`, the Socratic agent, context-first and interview-hardening RFCs, convergence contracts, and the ambiguity/ontology implementation. The portable skill keeps:

- focused Socratic questions (asked one per turn until 2026-10-12, now in dependency-ordered rounds);
- inverted, context-first intake for rich prior material;
- facts-versus-human-decisions routing and explicit provenance;
- separate ambiguity tracks and pressure passes;
- ontological, root-cause, lateral, and closure lenses;
- explicit user confirmation before crystallizing the brief.

The portable skill intentionally drops Ouroboros-specific state files, commands, agent names, mandatory subagents, and synthetic numeric convergence thresholds.

## Comparative Harness Review

| Repository and revision | Material reviewed | Durable contribution |
| --- | --- | --- |
| [NomaDamas/Codexplain](https://github.com/NomaDamas/Codexplain) `0e9a987fb8b9` | `README.md`, explanation UX method | Answer-first, scan-friendly summaries that preserve exact evidence and uncertainty |
| [obra/Superpowers](https://github.com/obra/Superpowers) `d884ae04edeb` | `skills/brainstorming/SKILL.md` | Inspect context first, one question at a time, alternatives and approval before implementation |
| [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops) `267dfb707987` | interview practice and debrief modes | Adaptive follow-up, evidence-backed claims, honest gap capture; also defines the job-rehearsal near-miss boundary |
| [Yeachan-Heo/clawhip](https://github.com/Yeachan-Heo/clawhip) `b9fc36d7b765` | native event and question-request contracts | Keep question payloads bounded and public-safe; preserve approval and routing identity |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) `40927950c49f` | planner and spec-miner agents | Ground requirements in repository evidence, dependencies, risks, edge cases, and verifiable behavior |
| [gmickel/flow-next](https://github.com/gmickel/flow-next) `e38604ebd3a7` | interview/prospect skills and question banks | Classify facts before asking, show stakes and option consequences, track skipped decisions and branch depth |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) `dae602ccd1a3` | graph query and extraction references | Distinguish extracted evidence from inference and make source expansion auditable |
| [garrytan/gstack](https://github.com/garrytan/gstack) `7c9df1c568a9` | `office-hours` and `spec` skills | Smart-skip answered questions, pressure-test polished answers, challenge premises, and force explicit choices |
| [mattpocock/skills](https://github.com/mattpocock/skills) `d574778f94cf` | grilling, grill-me, and to-spec skills | Walk a decision tree in dependency order, inspect facts, keep interview separate from execution |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) `95c9d2121fa2` | deep-interview skill and prompt builder | Target the weakest material dimension, cite brownfield evidence, preserve an explicit handoff gate |
| [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) `5d43a5bf6f00` | deep-interview skill, planner, and gate code | Preflight context, non-goals and decision-boundary gates, pressure ladder, and explicit execution contract |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) `14a0d79548d4` | `ponytail-review` skill | Remove ceremony that does not change the result; keep findings and output contracts compact |
| [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) `75c88e88c2db` | specification workshop and requirements guide | Use value, implementation, and verification perspectives plus concrete Given/When/Then failure scenarios |

## Synthesis Decisions

- Ouroboros remains the center; comparative sources sharpen question ergonomics, provenance, evidence, adversarial review, and stop rules.
- Until 2026-10-12 the skill asked one question per turn even though some compared workflows batch questions, on the reasoning that each answer may redirect the next branch. That decision is superseded by the revision below, which keeps the redirect property through dependency ordering.
- Numeric ambiguity scores were rejected. Topic-independent weights imply a precision the interviewer cannot justify; qualitative materiality gates are observable and portable.
- Harness-specific question tools, state stores, slash commands, and file paths were rejected. Native structured input is useful when available, but the question contract must also work in plain chat.
- User autonomy overrides workflows that insist on more questions after the user asks to stop. Early closure preserves open decisions and their impact.
- Automatic transcript, spec, or code generation was rejected. The default is a chat brief; durable or downstream mutations require explicit user authority.
- Job-interview coaching was kept out of scope despite useful patterns in career-ops. The subject here is the user's intent, product, plan, workflow, or decision, not their performance as a candidate.

## Question Contract Revision (2026-10-12)

**Decision.** Ask the independent consequential questions together in one round, each with why it changes the result, concrete options, and a recommended default that a one-word agreement adopts. Questions that depend on an open answer wait for a later round. One question per turn remains available only when the user explicitly asks for a slow or serial interview.

**Reason.** The pack's standing preference is to ask consequential questions "together and early rather than one at a time mid-run". One question per turn costs a round trip per decision, hides the full set of decisions so the user cannot see which matters most, and lets consequential questions surface late, after work has been shaped around a guess. The earlier reason for serial questioning, that each answer may redirect the next branch, is preserved by dependency ordering: only questions whose prerequisites are settled join a round, so an answer still redirects everything downstream of it.

**Source.** The design tree, the frontier of decisions whose prerequisites are settled, asking the whole frontier per round with a recommended answer, keeping fact lookups on the agent's side, and not blocking unrelated questions on a pending lookup come from the `grilling` skill in [mattpocock/skills at 49dd158](https://github.com/mattpocock/skills/tree/49dd158/skills/productivity/grilling) (MIT License, Copyright (c) 2026 Matt Pocock). The ideas were rewritten for this skill, not copied. This skill differs from that source in four ways: it closes when the next authorized action is determined rather than when the frontier is empty, routes empirical questions to investigation items instead of asking them, picks the root from the work type, and keeps the Interview Brief, provenance labels, confidence labels, and decide-later items.

**Related changes in the same revision.**

- Root before the first round. A product-style opening about end-user usage scenes or screens does not fit systems, research, or security work, where the goal, constraints, failure or threat model, and the result that would change direction must be settled first. The root is now chosen from the work type; users and usage remain valid roots for a product feature.
- Empirical questions. A measurement is not a preference, and asking the user to guess one turns an estimate into a recorded decision. Such questions become investigation items routed to `ml-experiment`, `evaluation-design`, a next action in the plan (`work-plan`), or the experiment queue of a design document (`design-doc`); the user may still set a rule for each plausible outcome.
- Defaults on preference questions. The earlier contract withheld a recommendation for a personal preference. Batched rounds need a default that a one-word agreement adopts, so a `your call` item now defaults to the option cheapest to reverse and says that this is the basis; it is a way to proceed, not a judgment of the user's taste.
- Closure. Interviewing past the point where the next authorized action is determined spends the user's attention on branches that action does not touch. Those branches stay in the brief as open items with decide-later rules.

**Evaluation status.** The pack's 2026-07-10 evaluation of the earlier skill scored a baseline that asked several numbered questions at once as a failure, because the contract under test was one question per turn. That verdict does not carry over to this contract. The batching dimension has not been re-measured; [evaluation cases](evaluation-cases.md) holds the updated rubric for the next comparison.

## Unknowns Revision (2026-10-12)

**Decision.** The interview works on all four kinds of unknowns rather than only the decisions the user already knows are open. Before the first round it establishes the user's starting point (inferred from context when possible) and runs a blind-spot scan, the find-unknowns lens, whose consequential findings open the first round as things the user may not have considered, each with the agent's view. A criterion the user can recognize but not describe is asked by showing options, references (existing code first), or quick variants; a runnable prototype or variant needs the user's consent, offered with its cost. When answers open new territory, that territory is rescanned before the frontier is recomputed. The brief may group what remains by kind, and closure requires a scan of the territory the next action touches. The description narrows to explicit requests to be interviewed or questioned and sustained discovery; a quick standalone blind-spot pass belongs to `find-unknowns`.

**Reason.** A round built only from what the user knows is open covers questions the user could have listed alone; the value of a questioning partner lies in what the user has not considered and in criteria they cannot state. A description of a tacit criterion produced on demand is vague or invented, and once recorded it reads as a decision; recognition on sight is faster and closer to what the user means. The narrower description keeps the quick pass and the sustained interview from competing for the same request, while the interview still applies the pass internally.

**Source.** Thariq Shihipar, ["A field guide to Claude Fable 5: Finding your unknowns"](https://claude.com/resources/articles/a-field-guide-to-claude-fable-finding-your-unknowns) (Anthropic, 2026-07-06). Adapted and rewritten here: the four quadrants (known knowns, known unknowns, unknown knowns, unknown unknowns, the last including what is achievable); a blind-spot pass for unknown unknowns that starts from context about the user and what they already know; brainstorms, prototypes, and references for unknown knowns, which people recognize on sight, with source code as the best reference; and interviewing to resolve ambiguities, putting first the questions that would change the architecture, which matches this skill's impact ordering. This skill differs from the article in two ways. The article interviews one question at a time; this skill keeps batched rounds of independent questions, the pack's standing preference recorded in the question contract revision above, and goes serial only on explicit request. It also builds a runnable prototype only with the user's consent, because a prototype writes files and spends time the user did not grant. The article's other techniques, such as implementation plans, are not adapted here.

**Evaluation status.** The quadrant behavior has not been measured. [Evaluation cases](evaluation-cases.md) adds cases for a tacit output format, an unconsidered constraint, and territory opened between rounds, plus a rubric item for the next comparison.
