---
name: design-exploration
description: >
  Open the design space for a module or system that has no design yet,
  especially one whose core behavior comes from a trained model or an agent
  loop or that must hold against an adversary: root the work in its threat
  model, attack objective, or research question, turn current limits into
  questions, gather mechanisms from the literature, and lay out candidate
  concepts that differ in what they bet on, each with its weakest assumption
  and cheapest discriminating experiment, for the user to choose from. Use
  for "explore designs for X", "how could we build X", "brainstorm approaches
  grounded in research", "I don't have a design yet", "설계 방향 탐색", or
  "어떻게 만들지 감이 안 와". NOT for a quick unknowns pass in any domain
  (find-unknowns), attacking one stated idea (idea-critique), writing the
  design document (design-doc), a mechanism or literature survey alone
  (literature-research), a task plan (work-plan), or a product feature spec.
---

# Design Exploration

Open the design space for a module before anyone converges on one design, and give the user material for intuition: what the module must hold, where the current approach falls short, which mechanisms exist, and which concepts are worth testing. The work ends in one of two ways. The user picks concepts to test and each goes to the skill that converges or tests it, or the exploration closes lightly with the consequential unknowns and next checks when that is all the work needs.

The agent supplies breadth, mechanisms, and attacks; the user chooses. In a blind comparison involving more than a hundred NLP researchers, LLM-generated research ideas were judged more novel than experts' ideas but slightly less feasible, LLM self-evaluation of ideas was unreliable, and LLM ideas lost diversity as more were generated ([Si, Yang, and Hashimoto, arXiv 2409.04109](https://arxiv.org/abs/2409.04109)). So during exploration do not narrow to a single recommendation or rank concepts by the agent's own score, and get breadth from different mechanisms rather than from generating more ideas.

Skip a step that existing material already answers, and name that material. Breadth belongs to scanning; when presenting, show the few items that change the user's thinking, not an inventory.

## Root the work by its type

Before mechanisms or concepts, settle what the module must achieve in the terms its work type requires. Infer the root from the request, the repository, and prior records.

- **Defensive module**, such as a spam or fraud classifier or a monitor that must hold against an adaptive adversary: the threat model and the guarantee the module claims, stated so that a violation is observable. Establish the threat model with praxis-direction's failure-mode pass and its threat list rather than writing a new list.
- **Attack or red-team agent**, such as an automated penetration-testing agent: the objective category, the scope and boundary it acts within, and how success is judged. Judging belongs to evaluation-design and its red-team reference; take the criterion from there rather than inventing one here.
- **Research module**, whose behavior is learned from data or produced by an agent loop with no adversary in scope, such as a document-retrieval model or a web-navigation agent: the question the work answers and which result would change direction.

A module with two types, such as a defensive classifier that a red-team agent will test, states both roots. A system with neither a learned core nor an adversary is rooted like a research module: the property it must hold and the result that would show it does not.

Do not start from end-user usage scenes, screens, or user stories. They suit product feature work and pull the design toward interface choices before anyone knows whether the core can work. Facts about the setting do belong in the root and are often needed: where the module is deployed, which inputs reach it and who controls them, what it is permitted to do, what each kind of failure costs, and which population it is evaluated on.

## Turn current limits into questions

Read the run evidence and prior results that exist: evaluation reports, error analyses, run logs, earlier research records. State each limit as a question that names the observation, its condition, and where the evidence lives. "Why does recall fall on documents longer than the chunk window (evaluation report, long-document slice)?" is usable; "recall is low" is not. Mark a limit suspected without evidence as unmeasured. When no system exists yet, take the limits of the strongest existing approach. Do not run new measurements here; a limit that needs one becomes a next check.

## Look for what nobody has noticed

Apply the find-unknowns lens to the root and the limits, as a lens inside this work rather than a separate pass with its own brief. Settle what inspection can settle now, carry what needs a measurement into the concepts' experiments, and keep what only the user can decide for a question round.

Ask consequential questions together and early. Each says why it changes the exploration, gives concrete options, and offers a recommended default. When the root itself is unclear, ask those questions in one round before gathering mechanisms; otherwise hold questions for the intuition turn. Never ask for a fact that inspection or search can settle, and do not ask the user to decide what only a measurement can answer.

## Gather mechanism material

Name the problem axes from the root and the limits, such as where the signal is lost, what the adversary can change cheaply, or which failures the agent loop cannot recover from. Reuse an existing mechanism map when the project or its research library has one covering those axes, and extend it rather than starting over. Otherwise ask literature-research for its mechanism-map mode on the named axes, with a budget the user knows; that mode collects and preserves the sources, covers adjacent fields that solved a structurally similar problem, and marks conventions the field inherits without justification. When the user asked for exploration grounded in research, request the map directly; otherwise offer it with its axes and budget. Do not build the map inside this skill.

When the user wants a quick slate and the mechanisms are familiar to both sides, proceed without a new map and say which axes a map would cover.

## Intuition turn

Before proposing concepts, give the user material to think with and ask for their hunches. Present a few items, each with its source location:

- surprises: a result that contradicts what the field or the user expected;
- conflicts: results that cannot both hold as stated, with the condition that might reconcile them;
- unexplained gaps: a limit without a known cause, an axis without a mechanism, a combination nobody has tried.

Separate evidence, inference, and speculation. Then ask, in the same round as any open questions from the unknowns lens, whether the user has a hunch about where the answer lies. A hunch is the user's; do not write the agent's conjectures into it. Send a stated hunch to idea-critique and keep the status it returns (supported, contradicted, or unmeasured) beside the hunch. A user with no hunch, or one who asks to skip ahead, goes straight to concepts.

## Diverge into concepts

Lay out candidate concepts that differ in what they bet on. Each answers a load-bearing question differently: where the signal is, what the defense relies on, which component learns and which stays fixed. If two candidates would be compared by sweeping one setting of the same structure, they are one concept; fold them and put the sweep into its experiment. Draw concepts from different axes and mechanisms of the map, from the user's hunches, and from adjacent fields. When new candidates start repeating a bet already on the table, stop adding. Include the strongest simple approach when it is plausible, since it sets the bar the others must clear.

Each concept carries:

- **Core bet:** the claim that must be true for the concept to work.
- **Mechanisms:** what it relies on, with map or source locations.
- **Weakest assumption:** where it most likely breaks, stated as plainly as its strengths.
- **Cheapest discriminating experiment:** the smallest check whose result would separate this bet from the alternatives, with its rough cost.

A synthetic example: a document-retrieval model misses answers in long documents. Chunk sizes of 256, 512, and 1,024 tokens are one concept with a parameter. Concepts with different bets are: the answer is split at chunk boundaries, so segment by document structure; the query lacks the document's vocabulary, so expand queries from the corpus; the ranker cannot score long passages, so add a late-interaction reranker; and, as the strongest simple approach, hybrid lexical and dense retrieval. For a fraud classifier facing adaptive fraudsters, decision thresholds are parameters, while features the adversary cannot cheaply change, frequent retraining on fresh labels, label-free anomaly detection, and added friction that makes evasion cost more than it gains are different bets.

Present the concepts side by side with their trade-offs and no winner. When the user asks which one the agent would pick, answer with the reasons and the result that would change the answer, and keep the other concepts open.

A runnable throwaway prototype is allowed when it answers a design question faster than argument, such as whether a scoring rule orders hard synthetic cases as a concept assumes or whether an agent loop recovers from a failed step. Read [throwaway prototypes](references/throwaway-prototype.md) before proposing or building one.

Threat models, attack-agent concepts, and their records stay in methodology language: boundary, objective category, metric, judge, environment, and budget. Do not write reproducible attack procedures or concrete adversarial inputs into concepts, prototypes, or records; point to the preserved source instead.

## Close the exploration

The exploration ends when the user picks concepts to test. Hand each selected concept, with its root, concept card, hunch status, and map location, to the skill that owns its next step:

- design-doc, when the concept should converge into a design document;
- ml-experiment, when its bet is decided by a training, fine-tuning, or serving comparison;
- evaluation-design, when its bet is decided by measuring behavior, including the scope and judging of an adversarial evaluation.

When the selected direction needs the organization's resources committed as one bet, praxis-direction's gate turns it into one. A request for a plan goes to work-plan. A handoff carries no new authority; each receiving skill keeps its own spend and write gates.

When the work only needed to know what is unknown, end lightly: the consequential unknowns, the next check for each, and the result that would change direction. No concept slate is required.

## Record the exploration

Record which concepts the user selected and rejected, with the user's reasons in their words; write "no reason given" rather than supplying one. Keep the root, the limits as questions, the map location, the hunches with their critique status, the concept cards, and the next checks with that record. Do not propose a rejected concept again unless the condition behind its rejection has changed, and say what changed. In a later round, read the earlier record before diverging. design-doc can draw its alternatives from the rejected concepts.

Write a file only when it has content, in the project's existing research layout: the effort's folder or the research directory its instructions name. Without such a layout, give the record in chat and offer to save it; do not create a research tree unasked.
