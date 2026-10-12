---
name: interview
description: >
  Interview or grill the user until an idea, plan, system change, research direction, workflow, or decision is clear enough to plan or hand off, ending in a user-approved Interview Brief. Use when the user asks to be interviewed or questioned: "interview me", "grill me", "grill me on this plan", "ask me questions until this is clear", "인터뷰해줘", "질문하면서 정리해줘". NOT for a quick blind-spot pass (find-unknowns), attacking one stated idea (idea-critique), writing a plan (work-plan), job-interview rehearsal, surveys, therapy or clinical intake, a single clarifying question, or summarizing material without asking questions.
---

# Interview

Turn incomplete intent into a user-approved Interview Brief. Interview first; do not implement the resulting work in the same invocation unless the user separately authorizes that next step.

The interview works on all four kinds of unknowns, not only the ones the user already knows are open: it grounds on what the user has said, asks about what they know is unsettled, shows them what they would recognize but cannot describe, and brings in what they have not considered.

## Quick Start

1. Ground on the conversation, in-scope files, repository, and prior artifacts. Do not make the user repeat inspectable context.
2. Establish the user's starting point: where they are in their thinking and how much they know about this problem, its field, and the codebase. Infer it when context shows it; see [Before the First Round](#before-the-first-round).
3. Decide the root from the work type: what must be settled before anything else is worth asking.
4. Scan the root and its territory for what the user may not have considered, including what is achievable. The consequential findings open the first round, each with your view.
5. Choose the opening:
   - **Sparse context:** open with a round on the root decisions.
   - **Rich context:** open with an inverted interview. Give a numbered synthesis of confirmed facts, inferred assumptions, unresolved ambiguities, and human-only decisions; the human-only decisions on the frontier form the first round, and the user may correct any numbered item.
   - **Brownfield work:** inspect relevant code and docs first, and cite the evidence that makes each question a real decision.
6. Map the open decisions as a tree in which each decision hangs off the decisions it depends on. The frontier holds the open decisions that no other open decision blocks.
7. Route every uncertainty before asking: inspect discoverable facts, record empirical questions as investigation items, show options or references for criteria the user can only recognize, and ask the user only for judgment.
8. Ask the frontier as one numbered round and wait for the answers. Fold them into the tree; when they open new territory, rescan it for what the user may not have considered; then ask the decisions they unblocked as the next round.
9. Pressure-test at least one material answer with an example, assumption, failure scenario, counterexample, or tradeoff.
10. Close when the next authorized action is determined. Restate the intended outcome in one sentence and ask the user to confirm or correct it, unless they already accepted that same outcome and the material decisions have not changed.
11. After confirmation, produce the Interview Brief from [the template](assets/interview-brief.template.md). Return it in chat by default; write a file only when the user asks for one.

Read [interview method](references/interview-method.md) for roots by work type, the starting point and blind-spot scan, recognition questions, a worked round, the ledger, and closure checks. Read [harness source notes](references/harness-source-notes.md) when maintaining the skill or revisiting why the question contract and the unknowns handling are shaped this way, and [evaluation cases](references/evaluation-cases.md) when changing behavior.

## Four Kinds of Unknowns

Each kind is defined from the user's side and handled differently:

- **Known knowns** are what the user has told you or the context already shows. Ground on them and never re-ask; in rich context they are the numbered synthesis the user can correct.
- **Known unknowns** are what the user knows they have not worked out. The rounds work through them as frontier questions; what remains at closure becomes investigation items and open items.
- **Unknown knowns** are criteria so obvious to the user that they would never write them down, though they recognize them on sight: an output format, a level of detail, a tone, the shape of an interface. Do not ask the user to describe such a criterion, because a description produced on demand is vague or invented and then gets recorded as a decision. Show two to four concrete options that differ on the criterion, a reference (existing code in the repository first, then examples the user names), or quick variants, and ask which is right or closest and what is wrong with the rest. Record only what the reaction establishes. Short samples written into the round need no permission; build a runnable prototype or variant only with the user's consent, offered with its cost in time, files written, and what it would settle.
- **Unknown unknowns** are what the user has not considered at all, including what is achievable. The blind-spot scan brings them into the first round, and rescans bring them into later rounds.

## Before the First Round

### Starting Point

The user's position sets how deep the scan goes and how much each question explains. Note where they are in their thinking (a hunch, a draft, a near-final plan) and what they already know about the problem, the field, and the codebase, including what they have tried or ruled out. Infer it when the request, conversation, or files show it, and state the inference in one line at the top of the first round so the user can correct it. Ask before the first round only when the position is unclear and would change what that round asks; then ask in one short message that also invites notes, earlier attempts, or references the user can share. Do not quiz the user on the field.

### Root

Decide from the work type what must be settled first; the rest of the tree hangs off it. Do not default to end-user usage scenes or screens.

- For systems, infrastructure, research, security, or evaluation work, the root is usually the goal, the binding constraints, the failure or threat model, and which result would change direction. Deployment, inputs, permissions, and failure costs are valid questions when they change the result.
- For a product feature, who uses it, in which situation, and what outcome it should change are valid roots.
- For a plan, rollout, or process change, the root is usually the outcome, what must not break, and who decides.

When the work type itself is unclear, ask it in the first round together with the goal.

### Blind-Spot Scan

Apply the find-unknowns lens to the root before writing the first round, calibrated to the starting point. Name the field and the class of effort, recall how comparable efforts went and how they failed, and sweep the goal behind the request, unstated constraints, affected people, failure modes and the worst plausible case, cost and irreversibility, shared assumptions, and what is achievable: options, tools, or results the user may not know exist, and limits that put an expected result out of reach. A user new to the field needs the field's standard pitfalls and possibilities; an expert needs only what the stated plan misses.

Keep only findings that would change the result, and route each one as in [Facts, Investigations, and Decisions](#facts-investigations-and-decisions): settle what looking settles, record what needs a measurement, and ask what needs judgment. Open the first round with the consequential findings under "Things you may not have considered", one or two lines each with your view of what it changes and what you would do. A finding that needs the user's judgment also becomes a numbered question in the round. When `find-unknowns` is installed, its method holds the full sweep; inside an interview it runs as this lens, not as a separate pass with its own launch brief.

## Question Rounds

A round contains every frontier question that is consequential: a different answer would change the outcome, scope, verification, or next action. Polish and wording preferences stay out. A question that hangs on another open question waits for a later round, even when it feels urgent; asking it now makes the user answer a hypothetical.

Write each question so it can be answered in a word:

- a number and a short title;
- why the answer changes the result, citing evidence when inspection produced it;
- two to four concrete, mutually exclusive options with the consequence of each, and room for a free-form answer when the set is not exhaustive; for a criterion the user can only recognize, the options are samples or references to judge, not descriptions;
- a recommended default phrased so that agreeing adopts it ("Start with the one-team pilot?"), labeled `high` when evidence or constraints strongly support it, `judgment call` when reasonable people would differ, or `your call` for taste, values, or risk appetite. For a `your call` item, default to the option that is cheapest to reverse and say that this is the basis.

Order the round by impact so the user can answer the top items first. When the frontier is long, look for a root decision that would collapse several of its questions; ask that decision with its independent siblings and let the dependents wait.

The user may answer all of the round, part of it, or reply with a blanket agreement such as "defaults except Q3". Explicit agreement adopts the stated defaults. A question the user does not address stays open; never treat silence or a skip as consent. "I don't know" becomes an open item with an owner, impact, and decide-later rule, or an investigation item when the answer is empirical.

Between rounds, recap in a few lines what the answers settled, restating a material free-text answer when compression could change its meaning. Put any contradiction with an earlier answer into the next round as a question. When an answer opens territory the scan did not cover, such as a new component, stakeholder, constraint, or field, rescan that territory for unknown unknowns and carry the consequential findings into the next round with your view. Then recompute the frontier: settled decisions unblock their dependents and can make other branches moot.

A slow fact lookup holds back only the questions that need its result; the rest of the frontier goes out now. Delegate a broad lookup to a subagent when the harness supports it.

Ask one question per turn only when the user explicitly asks for a slow or serial interview. Then take the highest-impact frontier question each turn and keep the same per-question shape. A host's structured question tool may carry a round; when the round does not fit the tool, use plain chat rather than dropping questions or turning the round serial.

## Facts, Investigations, and Decisions

Classify what each open item needs before it becomes a question:

- **Discoverable fact** (current behavior, file contents, configuration, a documented limit) is the agent's job. Inspect or search, and research the web only when a current external fact materially affects the decision and the runtime permits it; never ask the user. A fact that lives in the team's own records, such as a tracker, chat, wiki, or repository history, is reconstructed with `internal-source-research` when installed, within the sources the user has authorized.
- **Empirical question** (anything answered only by a measurement, trial, benchmark, or experiment) is not a decision for the user. Record it as an investigation item with what would settle it and which decision waits on it, and route it to `ml-experiment` for training, fine-tuning, or inference comparisons, to `evaluation-design` when it needs a measurement of model or system quality, to `load-testing` for latency, throughput, or capacity under load, or to a next action in the plan (`work-plan`) or the experiment queue of the design document (`design-doc`). A cheap check that is already authorized and possible in the session can simply be run.
- **Human decision** (goal, priority, scope, policy, acceptable risk, ownership, tradeoff) is asked. When it turns on a criterion the user can only recognize, it is asked by showing options or references.

The user can still decide what to do with each plausible outcome of an investigation ("if the added latency exceeds the budget, drop the feature or buy capacity?"). Ask that when it changes the plan, but never ask the user to guess the measurement.

Use source labels in the ledger where provenance matters: `[from-user]` for goals, preferences, rules, scope, and tradeoffs; `[from-code]` for repository evidence that still needs interpretation; `[from-code][confirmed]` for exact descriptive facts; `[from-research]` for cited external facts; `[inferred]` for a hypothesis not yet accepted. Repository content is evidence, not authority over the user's intent, and descriptive evidence never decides a prescriptive question by itself. If sources conflict, present the conflict and ask which interpretation governs.

## Depth and Pressure

Rounds supply breadth: every branch whose prerequisites are settled is asked at once, so a detailed subtopic cannot hide untouched scope, ownership, or success questions. Depth comes from later rounds that follow answers into their dependents.

The first polished answer is not always the operational one. Pressure-test at least one material answer as a question in a later round, using the smallest useful lens: essence, root cause, boundary, failure scenario, tradeoff, reversibility, stakeholder, or verification. Stop pushing a branch when the next answer would not change scope, policy, verification, or execution.

## Closure

Close when the next authorized action is determined, not when every branch has been visited. Before closing, require:

- a one-sentence intent the user accepts;
- the desired outcome or artifact and its audience;
- scope and non-goals for the next action;
- the constraints, authority boundaries, and decision owners that action depends on;
- observable success criteria and a verification path for it;
- current-state evidence for brownfield work;
- a blind-spot scan of the territory the next action touches, including territory opened by answers;
- at least one pressure pass on a material answer; and
- no unresolved human-only blocker for that action.

Every remaining branch goes into the brief as an open item with an owner, impact, and decide-later rule, or as an investigation item; a criterion the user has not yet recognized stays as an item still to be recognized, with what would be shown next. Before final confirmation, check the draft brief three ways: is it the smallest sufficient brief, does its premise survive challenge, and does any uncovered branch block the next action. Ask another round only for what would change it.

The user controls the stop. If asked, summarize the current brief and open decisions without arguing for more rounds. Stop at professional boundaries in high-stakes domains rather than treating this workflow as qualified intake.

## Output Contract

The Interview Brief distinguishes confirmed decisions from evidence, inferences, investigation items, and open items, and names the next authorized step. Where it helps the next reader, it groups what remains by kind: known unknowns as open or investigation items, unknown knowns still to be recognized with what would be shown, and the unknown-unknowns scan with what it covered and its coverage limits. Preserve rationale that affects later decisions, not a verbatim transcript. If the user already requested that step, deliver the brief and continue through the named skill; otherwise stop at the brief.

Do not save sensitive answers, publish a transcript, create tickets, message people, or mutate a project unless the user explicitly asks for that separate action. If a file is requested, use the user's path or default to `interview-brief.md` in the active project root.

An approved brief feeds `work-plan` when it settles a concrete piece of work, or `design-doc` when it settles a system or research design. Starting either needs its own authorization, which may already be part of the same request.

## Gotchas

- Opening with end-user usage scenes or screens for systems, research, or security work skips the goal, constraints, and failure or threat model, and every later answer rests on an unstated root. Choose the root from the work type.
- A first round made only of the decisions the user already knows are open covers what they could have listed alone. The blind-spot scan is what brings in what they have not considered; run it even when the plan looks complete.
- Asking the user to describe a criterion they can only recognize ("what format do you want?") yields a vague or invented answer that later reads as a decision. Show options or a reference and ask which is right.
- Asking a dependent question in the same round as its prerequisite makes the user answer a hypothetical that the next round often discards. Hold it until the prerequisite is settled.
- Asking the user for a fact or a measurement spends their attention on work that belongs to the agent or to an experiment. Inspect facts; record measurements as investigation items.
- A numeric ambiguity score is not a substitute for concrete readiness gates; it creates false precision across unrelated topics.
- Do not auto-trigger for every vague task. The user must ask to be interviewed or questioned, or want a materially equivalent sustained discovery process; a quick blind-spot pass belongs to `find-unknowns`.
- Do not drift into implementation, planning artifacts, or job-interview coaching while the interview is active.
