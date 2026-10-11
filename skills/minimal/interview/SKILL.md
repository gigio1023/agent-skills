---
name: interview
description: >
  Use when the user asks to be interviewed or questioned until something is
  clear: "interview me", "grill me", "grill me on this plan", "ask me questions
  until this is clear", or requirements discovery for a vague idea, plan,
  product, system change, research direction, workflow, or decision before it
  is planned or handed off. Grounds on available context first, asks the
  independent consequential questions together in rounds with options and a
  recommended default, and ends with a user-approved Interview Brief. Formerly
  deep-interview. NOT for a light unknowns or blind-spot pass (find-unknowns),
  attacking one stated idea with objections (idea-critique), writing a plan
  (work-plan), job-interview rehearsal, surveys, therapy or clinical intake, a
  single clarifying question, or summarizing existing material without asking
  questions.
---

# Interview

Turn incomplete intent into a user-approved Interview Brief. Interview first; do not implement the resulting work in the same invocation unless the user separately authorizes that next step.

## Quick Start

1. Ground on the conversation, in-scope files, repository, and prior artifacts. Do not make the user repeat inspectable context.
2. Decide the root from the work type: what must be settled before anything else is worth asking.
3. Choose the opening:
   - **Sparse context:** open with a round on the root decisions.
   - **Rich context:** open with an inverted interview. Give a numbered synthesis of confirmed facts, inferred assumptions, unresolved ambiguities, and human-only decisions; the human-only decisions on the frontier form the first round, and the user may correct any numbered item.
   - **Brownfield work:** inspect relevant code and docs first, and cite the evidence that makes each question a real decision.
4. Map the open decisions as a tree in which each decision hangs off the decisions it depends on. The frontier holds the open decisions that no other open decision blocks.
5. Route every uncertainty before asking: inspect discoverable facts, record empirical questions as investigation items, and ask the user only for judgment.
6. Ask the frontier as one numbered round and wait for the answers. Fold them into the tree, find the decisions they unblocked, and ask those as the next round.
7. Pressure-test at least one material answer with an example, assumption, failure scenario, counterexample, or tradeoff.
8. Close when the next authorized action is determined. Restate the intended outcome in one sentence and ask the user to confirm or correct it, unless they already accepted that same outcome and the material decisions have not changed.
9. After confirmation, produce the Interview Brief from [the template](assets/interview-brief.template.md). Return it in chat by default; write a file only when the user asks for one.

Read [interview method](references/interview-method.md) for roots by work type, a worked round, the ledger, and closure checks. Read [harness source notes](references/harness-source-notes.md) when maintaining the skill or revisiting why the question contract is shaped this way, and [evaluation cases](references/evaluation-cases.md) when changing behavior.

## Root Before the First Round

Decide from the work type what must be settled first; the rest of the tree hangs off it. Do not default to end-user usage scenes or screens.

- For systems, infrastructure, research, security, or evaluation work, the root is usually the goal, the binding constraints, the failure or threat model, and which result would change direction. Deployment, inputs, permissions, and failure costs are valid questions when they change the result.
- For a product feature, who uses it, in which situation, and what outcome it should change are valid roots.
- For a plan, rollout, or process change, the root is usually the outcome, what must not break, and who decides.

When the work type itself is unclear, ask it in the first round together with the goal.

## Question Rounds

A round contains every frontier question that is consequential: a different answer would change the outcome, scope, verification, or next action. Polish and wording preferences stay out. A question that hangs on another open question waits for a later round, even when it feels urgent; asking it now makes the user answer a hypothetical.

Write each question so it can be answered in a word:

- a number and a short title;
- why the answer changes the result, citing evidence when inspection produced it;
- two to four concrete, mutually exclusive options with the consequence of each, and room for a free-form answer when the set is not exhaustive;
- a recommended default phrased so that agreeing adopts it ("Start with the one-team pilot?"), labeled `high` when evidence or constraints strongly support it, `judgment call` when reasonable people would differ, or `your call` for taste, values, or risk appetite. For a `your call` item, default to the option that is cheapest to reverse and say that this is the basis.

Order the round by impact so the user can answer the top items first. When the frontier is long, look for a root decision that would collapse several of its questions; ask that decision with its independent siblings and let the dependents wait.

The user may answer all of the round, part of it, or reply with a blanket agreement such as "defaults except Q3". Explicit agreement adopts the stated defaults. A question the user does not address stays open; never treat silence or a skip as consent. "I don't know" becomes an open item with an owner, impact, and decide-later rule, or an investigation item when the answer is empirical.

Between rounds, recap in a few lines what the answers settled, restating a material free-text answer when compression could change its meaning. Put any contradiction with an earlier answer into the next round as a question. Then recompute the frontier: settled decisions unblock their dependents and can make other branches moot.

A slow fact lookup holds back only the questions that need its result; the rest of the frontier goes out now. Delegate a broad lookup to a subagent when the harness supports it.

Ask one question per turn only when the user explicitly asks for a slow or serial interview. Then take the highest-impact frontier question each turn and keep the same per-question shape. A host's structured question tool may carry a round; when the round does not fit the tool, use plain chat rather than dropping questions or turning the round serial.

## Facts, Investigations, and Decisions

Classify what each open item needs before it becomes a question:

- **Discoverable fact** (current behavior, file contents, configuration, a documented limit) is the agent's job. Inspect or search, and research the web only when a current external fact materially affects the decision and the runtime permits it; never ask the user.
- **Empirical question** (anything answered only by a measurement, trial, benchmark, or experiment) is not a decision for the user. Record it as an investigation item with what would settle it and which decision waits on it, and route it to `ml-experiment` for training, fine-tuning, or inference comparisons, to `evaluation-design` when it needs a measurement of model or system quality, or to the experiment queue of the plan (`work-plan`) or design document (`design-doc`). A cheap check that is already authorized and possible in the session can simply be run.
- **Human decision** (goal, priority, scope, policy, acceptable risk, ownership, tradeoff) is asked.

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
- at least one pressure pass on a material answer; and
- no unresolved human-only blocker for that action.

Every remaining branch goes into the brief as an open item with an owner, impact, and decide-later rule, or as an investigation item. Before final confirmation, check the draft brief three ways: is it the smallest sufficient brief, does its premise survive challenge, and does any uncovered branch block the next action. Ask another round only for what would change it.

The user controls the stop. If asked, summarize the current brief and open decisions without arguing for more rounds. Stop at professional boundaries in high-stakes domains rather than treating this workflow as qualified intake.

## Output Contract

The Interview Brief distinguishes confirmed decisions from evidence, inferences, investigation items, and open items, and names the next authorized step. Preserve rationale that affects later decisions, not a verbatim transcript. If the user already requested that step, deliver the brief and continue through the named skill; otherwise stop at the brief.

Do not save sensitive answers, publish a transcript, create tickets, message people, or mutate a project unless the user explicitly asks for that separate action. If a file is requested, use the user's path or default to `interview-brief.md` in the active project root.

An approved brief feeds `work-plan` when it settles a concrete piece of work, or `design-doc` when it settles a system or research design. Starting either needs its own authorization, which may already be part of the same request.

## Gotchas

- Opening with end-user usage scenes or screens for systems, research, or security work skips the goal, constraints, and failure or threat model, and every later answer rests on an unstated root. Choose the root from the work type.
- Asking a dependent question in the same round as its prerequisite makes the user answer a hypothetical that the next round often discards. Hold it until the prerequisite is settled.
- Asking the user for a fact or a measurement spends their attention on work that belongs to the agent or to an experiment. Inspect facts; record measurements as investigation items.
- A numeric ambiguity score is not a substitute for concrete readiness gates; it creates false precision across unrelated topics.
- Do not auto-trigger for every vague task. The user must want an interview or a materially equivalent discovery process.
- Do not drift into implementation, planning artifacts, or job-interview coaching while the interview is active.
