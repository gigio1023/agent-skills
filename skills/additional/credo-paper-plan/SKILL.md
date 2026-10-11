---
name: credo-paper-plan
description: "Plan or critique a research paper's argument: the idea, reader, claim-evidence map, closest prior work, introduction, figure storyboard, and section order, or plan the response to peer reviews of a submitted paper. Use when the user asks to plan a paper or section, fix a paper draft that lacks a coherent argument, or answer reviewers of a submission. NOT for reports, design documents, product write-ups, PR review comments, line editing, or submission checks (credo-release)."
---

# Paper Plan

Produce an argument the author can draft from, or critique a draft against its intended argument. Adapted from the writing sections of Carlini's research essay; background episodes come from the credo-taste package when it is installed. Read an episode only when using it; the plan does not depend on them.

Scope: a paper, or a section of one, whose argument the author will defend to reviewers, at any distance from its deadline. A report, design document, or product write-up is a document task for the writing skill, not a paper plan.

Use existing evidence and decisions. Ask one consequential missing question at a time when the user wants an interview; otherwise propose a plan with unresolved choices clearly identified. Do not require another interview for information already available.

## Plan the argument

- **Idea and reader:** state the one idea and the reader's starting understanding. The default reader is the author six months ago unless the project names another. Multiple related results can support one argument; an “and” is not by itself evidence of two papers.
- **Claims and evidence:** keep a claim-evidence map with one row per claim: the claim, its evidence, its assumptions and scope, any applicable comparator or control, and where it appears. Every abstract claim has a row. Match evidence to the claim type: a causal claim needs a comparison that isolates the cause, a generality claim needs varied conditions, and an improvement claim needs a credible baseline. A theoretical claim needs a proof or explicit argument appropriate to the claim, with stated assumptions; a qualitative claim needs a traceable analysis with supporting material. A claim without matching evidence is narrowed or becomes unresolved work.
- **Closest prior work:** state what the paper adds beyond each of the two or three nearest papers, grounded in what the results deliver rather than what the introduction promises. A claim of novelty from general knowledge stays unverified until a prior-art check confirms it.
- **Conclusion:** answer "so what": what the evidence lets the reader learn or do. It is not the abstract in the past tense. Separate a hoped-for conclusion from what has actually been established.
- **Introduction:** start where the reader stands and build the argument for the contribution. About two pages is a useful working target when it fits the venue, audience, and argument. Respect venue limits and preserve the mechanism and evidence the reader needs; shorten repetition before removing necessary explanation. When the claim is heretical, lay out the evidence and let the reader arrive at it.
- **Figures:** storyboard the comparisons or relationships that carry the argument. For each figure name the question it answers, the comparison held fixed, and the caveat its caption must carry. Each figure is understood from its caption alone.
- **Sections:** give each a purpose and explain the order. Omit a section that does no work for the argument.
- **Abstract:** state the problem, concrete contribution, established result, and significance at the strength the evidence supports. Use a number when it expresses a material quantitative result, with the conditions needed to interpret it. A theorem with its assumptions or a supported qualitative finding can state a specific contribution without a numeric result. Preserve uncertainty and limits that change the claim; remove vague claims, not meaningful qualifications. An early abstract may identify intended claims, but must distinguish them from established results and name the evidence still needed.
- **Unresolved work:** identify evidence or author decisions that would change the outline. The finished paper sits at a local optimum, with no obvious experiment a reader will wish for; route each such gap to a bounded experiment rather than pretending a prose edit settles it.

## Critique and deliver

Read a draft against the intended reader and argument. Identify concrete mismatches and their effect, each with its location, the observation, the criterion, and the requested change; preserve claims and evidence strength. A critique can recommend changes without rewriting unrequested prose.

For a pre-submission critique, get the strongest rejection argument from a reader who sees only the draft files, not the agent's summary or the conversation: a fresh subagent where the harness offers one, otherwise a reread of the files alone. The reader commits to one argument a reviewer could reject the paper on; then each of its points is marked answered by the current text, partly answered, or unresolved. When an advocate and a skeptic disagree, report the crux the introduction must win instead of averaging them. No scores.

For reviews of a submitted paper, read [peer-review response](references/peer-review-response.md) and plan the response from it. Whether to revise, resubmit, or stop belongs to credo-taste.

Return the useful outline, storyboard, or critique. Stop at planning when that is the request. If the user also asks for drafting, continue within that authorization, using `copydesk` when available for production; the skill's ownership of planning does not reserve all prose for the human. Submission checks belong to `credo-release`.
