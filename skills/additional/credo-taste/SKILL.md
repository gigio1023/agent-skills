---
name: credo-taste
description: "For work aimed at a paper or a publishable research claim, think through the direction one question at a time: which problem is worth pursuing, whether to start or continue a project (best-case conclusion, one idea, months ahead, riskiest sub-problem, continue / kill / pivot), and how to read a rejection. Use when the user names credo-taste or asks whether a paper-bound research direction is worth it. Reasons in prose, no scores. NOT for tickets, bugs, product evaluations, routine execution of a settled task, for planning paper text (credo-paper-plan), for reading a paper (literature-research), or for a direction decided inside an organization and the failure-mode pass on a new system (praxis-direction)."
disable-model-invocation: true
---

# Credo: Taste

Outcome: the user states, in their own words, what they will do and why, after being asked the questions Nicholas Carlini asks himself at the same moment in [How to win a best paper award](https://nicholas.carlini.com/writing/2026/how-to-win-a-best-paper-award.html). The agent asks, offers an episode from his career as an analogy when one fits, and stops when the judgment is articulated. It does not hand down a verdict or compute a score; the essay's point is that taste is trained, not computed.

## Scope

Use only when both hold: the work is aimed at a paper or a publishable research claim, and the value of the direction is still uncertain. A ticket, a bug, a customer deadline, a product evaluation, or this week's task is not in scope, even when it involves a model, a benchmark, or the word research; do that work well with the work-track skills and move on. When it is unclear whether the work aims at a paper, ask that one question before anything else. For a direction decided inside an organization, where the result is a product or capability decision rather than a paper, use praxis-direction.

The bar is the essay's, not a softened one: one or two projects a year may be great and the rest are practice. Do not lower a question to fit applied work; applied work belongs to the work-track skills. Do not reopen a settled question. Infer the decision from context and ask only for missing human judgment.

## How the conversation runs

- One question per turn. End the turn after asking; do not list several questions at once.
- Pick the moment from the table below, then ask only its questions, skipping any the user has already answered.
- Offer an analogy only when the user's situation resembles an episode; read [references/episodes.md](references/episodes.md) at that point, not before. Say which episode and what the move was, then ask what the analog is here.
- No scores, weights, or rubric totals. If asked for one, say why not and give the reasons in prose instead.
- Read [references/tenets.md](references/tenets.md) only when the user asks what the principles are or challenges one; the questions below already carry them.

Stop rules: stop when the user can say what they will do and why; stop after about six questions without convergence and summarize what is and is not settled; if the user answers "I don't know" twice in a row, stop asking and propose the cheapest experiment that would answer the question instead.

## Moments and questions

| Moment | Questions |
| --- | --- |
| Looking for a problem | What in this literature makes you want to shout that everyone is doing it wrong? If you do not do this, how many months until someone else does? Is this a corner where you are unusually strong, or a hot area where you would be one of many? |
| Starting or continuing one project | Run the gate below. |
| Stuck or drifting | Is the core idea failing, working but unimportant, or has something more important appeared? For the last: new ideas always look better than the one you have lived with; what specifically makes this one more important? What would you salvage if you killed it today? |
| A new system, dataset, API, or agent appears | Hand off to praxis-direction, which owns the failure-mode pass and its fixed list. |
| A work result might become a paper | Which one relationship does it isolate that prior work blurred, and would it hold outside this product on a setting a reviewer can rerun? What is the delta from the two or three closest papers? Run the literature-research prior-art check before answering. What can be released under the project's records, customer, and disclosure constraints? The product decision stays with the work; the paper is a separate artifact with its own bar. |
| Rejected or discouraged | Did reviewers misunderstand the argument, or reject the premise as too early? Most of his awarded papers were rejected first. What in the writing would make a confused reviewer understand? A rejection is one sample from a distribution you do not control; what in the distribution would you change? |
| Considering collaboration | Have you done enough to send a partial solution rather than admiration? Are you hiding the idea from people who could help, and why? Ideas are cheap; execution is hard. |
| About to write | Hand off to credo-paper-plan. |

## The gate for one project

Ask in order, one per turn, and stop early when an answer settles it.

1. If every experiment turned out exactly as you hope, what does the conclusion say? If it says only that a number went up, say so: that is not yet a conclusion. What does the reader learn or become able to do? If the best-case conclusion adds nothing beyond its results, drop the project.
2. What is the one idea? Write it down now; every experiment, paragraph, and figure should connect to it. A conjunction alone does not mean two papers; ask which idea the current decision concerns.
3. How many months until the next person would find this, and is this a corner where you are unusually strong? A result others would reach next month is practice, not one of the one or two great projects a year.
4. Which part is most likely to fail, and what is the smallest thing you could try in days that would tell you? Weeks spent on the part already understood is the first finding.
5. For a running project: is it failing, working but not mattering, or displaced by something more important? Apply the pull-of-the-new check above.
6. What will you do: continue, kill, pivot, or de-risk first? If killing, what is salvaged: a workshop note, a post, or a journal entry.

When a project is ending well, ask once more: what will a skeptical reader ask, and which experiment answers it before they ask? An obvious missing experiment, domain, or objection belongs in this paper. The standard is going to lengths a reasonable person would not: the extra trials, the controlled confounder, the hours spent turning "sometimes" into "usually". Small follow-ups can stay open for others.

## Closing

No fixed form. Reflect the user's answers in one short paragraph they could paste into their notes: decision, reasons in their words, and the prediction to revisit. When the user wants the prediction kept, name credo-journal; it runs on the user's request. Preserve decisions in the project's existing context record when that maintenance is part of the task; do not start another interview or duplicate journal entry for every experiment.
