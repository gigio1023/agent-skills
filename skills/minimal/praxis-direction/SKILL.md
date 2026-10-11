---
name: praxis-direction
description: >
  Turn an organization's research agenda into one resourced bet (outcome,
  measure, intervention, cheapest test, compute ladder, kill condition), run
  the failure-mode pass on a new system, or set up the praxis profile the bet
  draws on. Use when the user asks for a bet, asks whether a new system or
  dataset holds one, asks to set up praxis, or names praxis-direction. NOT for
  task planning, a ticket, settled work, paper direction (credo-taste), or
  experiments (ml-experiment).
---

# Praxis: Direction

Outcome: the user can state one bet in their own words: the organizational outcome it serves, the number that will move, the intervention, the first cheap test, the resources it may spend, and the observation that ends it. The agent asks one question per turn, uses the organization's profile for what only the organization knows, and stops when the bet is articulated. It does not run experiments, spend money, or hand down a verdict.

## Scope

Use when a research direction is decided inside an organization and the result is a product, customer, or capability decision rather than a paper. A direction usually arrives as an agenda: "improve X capability", "we should look into Y", "the team needs Z". An agenda names an area; a bet names a number, an intervention, and a cost. This skill turns the first into the second.

The gate runs on a request: the user asks for a bet, or choosing what to pursue is itself the task. An agenda or a new model release mentioned in passing is not that request. Do not reopen a settled bet or turn ordinary implementation into an interview. For a paper-direction decision use credo-taste; both have a gate, but they answer to different readers.

## The profile

Read the organization's praxis profile before asking anything it already answers. Resolve it in this order: a path named in the project's `AGENTS.md` or `PROJECT.md`; otherwise `praxis-profile.md` found by walking up from the working directory; otherwise none. State the resolved path once.

Without a profile, run the gate with the generic questions, mark the closing block `profile: none`, and offer the setup below once. Do not block on the missing file.

The profile is the organization's data. The gate only reads it; setup and audit write it on request, and its content never goes into an installed skill.

## The gate

Ask in order, one per turn, skipping what the user or the profile has already answered. Stop early when an answer settles the bet.

1. **Outcome.** Which organizational outcome changes if this works: a decision someone makes, a deliverable a customer receives, a claim the company can make? Name the person or the deliverable. If nothing changes, this is an agenda, not a bet; ask what the agenda is standing in for.
2. **Operational definition.** Which task family, measured by which evaluation the organization accepts as evidence, at what number today, and what number would count as success? Until the unit of measurement is fixed, "capability" is not a noun. If the number today is unknown, measuring it is the first bet.
3. **Intervention and the question it answers.** Interventions answer different questions, so they order themselves. Removing a suppression (a refusal direction, a filter, a prompt constraint) answers "is the capability present but held back"; it does not add capability. Training on new data answers "can the capability be added". Prompting and retrieval answer "can the model be told". Ask which question this bet is about, then which cheap test separates the answers before anything expensive runs. Read [references/example.md](references/example.md) for a worked case when the ordering is unclear.
4. **Compute ladder and spend gate.** What can be learned at each tier the profile names, typically always-on resources, one accelerator-day, and a paid burst? Each tier states what it answers and the condition for climbing to the next. Before a paid burst the user writes one sentence predicting the result, and the profile's approval threshold applies. A time estimate alone does not authorize spend.
5. **In-house assets.** Which one question, put to which expert in the profile, would change the plan most? Which internal data applies, and what does its size support: an evaluation set first when the count is small, a few-shot pool next, a training seed only when the count and the license allow it?
6. **Deliverable and kill condition.** What form does the result take, in how many weeks, and what observation ends the bet early?

Stop rules: stop when the user can state the bet; stop after about six questions without convergence and summarize what is and is not settled; if the user answers "I don't know" twice in a row, propose the cheapest measurement that would answer the open question and stop.

No scores or weighted rubrics. If asked for one, give the reasons in prose instead.

## A new system, dataset, or agent appears

When the question is "is there anything here", run the failure-mode pass instead of the gate. Read [references/threat-list.md](references/threat-list.md) for the ten items and the row format, then:

1. Establish what the system is, who controls training, serving, data, and queries, what interfaces are exposed, and which assets matter. Mark unknowns and proceed.
2. Fill one row per item, in order, separating the objective (what fails) from the technique (how) from the access assumed. Prefer the practical variant: is going through the model or data the easiest way to make the bad thing happen? "None known" for prior work means you did not find one.
3. Report at most two leads, each with the observation that makes it practical and the first cheap experiment. If nothing applies, say so in one sentence. Add a disclosure note when a lead is real: patchable by the owner or not.

This is analysis. Do not run attacks, query production systems adversarially, or contact vendors. A lead that survives becomes a bet and goes through the gate.

## Set up or audit the profile

Run this only when the user asks for setup or audit, or accepts the offer above. Resolve the target from a path the user names, then a path named in `AGENTS.md` or `PROJECT.md`, then `praxis-profile.md` at the workspace root. If the file exists, audit it instead of interviewing again.

Before writing, check where the file will land. Refuse a path inside an installed skill directory. If the workspace's Git remote points at a public host and the target is not ignored, say so and offer an ignored path or a private location: the profile names customers, budgets, and people. Do not edit `.gitignore` without asking.

Read [references/profile-template.md](references/profile-template.md) for the fields and a synthetic example. Ask one field per turn in the template's order, skip a field the workspace's documents already answer, and cite where the answer came from. Record what the user says, not what the agent would prefer; a field the user cannot answer yet is written as `undecided` with the date. Keep the profile within about forty lines: one line per outcome, one row per tier, expert role, and dataset. Refer to people by role unless the user wants names.

Write the file, then add one line naming its path to `AGENTS.md` or `PROJECT.md`, for example `Praxis profile: praxis-profile.md`, without restructuring that file. Report the path and the fields left undecided.

On an audit, compare each field with the current facts the user or the workspace supplies and append a dated line under each changed field rather than rewriting history; the gate reads the latest line. Flag a tier, threshold, or dataset that no longer exists, and never remove past values. Setup does not run the gate, create plans, or record predictions.

## Closing

Reflect the answers in one Goal block the user can paste into the project's plan, in their words:

- bet: one sentence
- outcome served: the decision or deliverable, and whose
- measure: evaluation, number today, target
- intervention: what changes and the question it answers
- first test: the cheapest discriminating check and its tier
- ladder: what each tier answers and the climb condition; the spend gate
- assets: the expert question and the data with its supported use
- deliverable and kill condition: form, weeks, ending observation
- prediction: the user's one sentence, dated
- profile: path, or none

When the project uses plan files, the block belongs in the plan's Goal or equivalent section; do not create a second record. Record the prediction where the profile says predictions live. Broader direction changes remain the user's decision.
