---
name: find-unknowns
description: >
  Use when the user starts substantial work in territory they don't know well
  (a new project, research direction, investment or money-management
  strategy, career or life plan, product or game idea, or an unfamiliar part
  of a codebase) with no spec, plan, or reference yet, or asks, at the start
  or partway through other work, what they are missing: "what am I missing",
  "what haven't I considered", "blind spots", "consider things I didn't think
  of", "내가 고려 못한 점", "놓친 거 없어?", an unknowns pass, an option map,
  throwaway variants, or a launch brief. Scans broadly with field knowledge
  for hidden goals, constraints, failure modes, and assumptions, leads with
  its own view, and asks the consequential questions together and early. NOT
  for well-specified or small tasks unless asked, sustained interviewing (use interview,
  formerly deep-interview), attacking one stated idea (use idea-critique),
  research-grounded technical design exploration (use design-exploration), or
  packaging session state (use session-handoff).
---

# Find Unknowns

Find what neither the user nor you have noticed yet: the hidden problems, goals, constraints, and considerations that would change the result. Work from the assumption that at least one consequential unknown exists, and look for it with the field's breadth of cases and expert practice rather than only the material in view. Then give your own view first, ask the user the consequential questions together and early, and carry on with the work already authorized.

The pass applies to any subject, technical or not. It runs either as a separate pass before work starts or as a lens inside other work, such as a plan, a design, a review, or delegated work. Inside other work, put the result where that work keeps its findings and open questions instead of producing a separate document.

## Method

### 1. Inspect before asking

Read what is available before forming questions: the conversation, named files and artifacts, the repository or data involved, prior decisions, and the sources the request points to. A fact that inspection or a quick search can settle is your job, never a question. Note what the request takes for granted and what it leaves unsaid; the scan starts from those gaps.

### 2. Scan broadly with field knowledge

Name the field and the class of effort the work belongs to, then reason from how efforts of that class usually go:

- Recall how comparable efforts went, including how they failed and what they cost.
- Ask what an experienced practitioner in this field checks first, which pitfalls are standard, and which terms of art a practitioner would use that the request does not.
- Run a premortem: assume the result later failed or disappointed, and name the most plausible reasons.
- List the assumptions behind the request and behind your own reading of it, and ask what changes if each one is false.

When the field is unfamiliar to you or the stakes are high, search for comparable cases, practitioner guidance, standards, or rules where search is available and within the task's authority.

Sweep every dimension below before concluding that nothing consequential is hidden. Dismiss a dimension quickly when it plainly does not apply, but do not skip one because the request looks narrow or the first checks came back clean. Most of the sweep is reasoning from field knowledge and costs little; spend inspection and search where cost, irreversibility, or unfamiliarity is high.

- **Goal:** what the user is actually trying to achieve, what success means and who judges it, and what would make a correct-looking result useless.
- **Hidden constraints:** rules, deadlines, budgets, access, compatibility, policies, and norms the request does not state.
- **Affected people:** who else uses, approves, maintains, pays for, or bears the consequences of the result, and whose incentives differ from the user's.
- **Failure and worst case:** how the work goes wrong, how bad the worst plausible outcome is, and how comparable efforts failed.
- **Cost, irreversibility, and timing:** what is expensive or impossible to undo, which windows or deadlines apply, and where the order of steps matters.
- **Second-order effects:** what the result changes downstream and what it makes harder later.
- **Shared assumptions:** what both the user and you take for granted, and what evidence would contradict it.
- **Practitioner's first checks:** the checks and quality bars someone experienced in the field applies before anything else.

The dimensions guide the sweep. They are not an output template.

### 3. Sort each finding

Keep only findings that could change the result, then sort each one:

- **Resolve by looking:** inspection, search, or a quick read settles it. Do it now and report the answer.
- **Needs a measurement or trial:** only new evidence settles it. Propose the cheapest check that would, such as a sample, a small run, a quote, or a prototype. Run it now when it is cheap and within the current grant; otherwise list it as an investigation item with what its result would change. It is not a question for the user.
- **User's decision:** it turns on a goal, preference, priority, risk tolerance, or authority that only the user holds. Ask it.

### 4. Lead with your view

Open with what you think matters most and why: your read of the situation, the finding most likely to change the result, and the direction you would take. Then give the few other findings that matter, each with its evidence or reasoning, and what you resolved by looking. Scan broadly and present briefly: show the findings that change the result, not an inventory of what you checked, so that an unneeded pass costs the user one paragraph to skip. Explain how the field works only as far as a finding needs it, and define any term of art you introduce when the user's familiarity is unclear.

### 5. Ask the consequential questions together and early

Ask every user decision in one batch, before the work it affects, with the hardest to reverse first. Give each question why its answer changes the result, concrete options, and a recommended default worded so that agreeing is easy.

An unanswered question stays open with a decide-later rule: the point by which it must be decided and what happens until then, such as proceeding with the default on reversible parts or holding the parts that depend on it. Silence or "I don't know" is never consent to a consequential or irreversible step. Ask a question that depends on an earlier answer in a later round, once its premise is settled. When the user's choices need sustained back-and-forth, offer `interview` and let the user choose it.

### 6. Continue authorized work

The pass informs the work and does not block it. Continue the authorized work that does not depend on open answers, and hold only the parts that do. The pass grants no new authority: ask before changing direction, exceeding resources or access, taking a new external action, or starting a long new activity.

The pass is complete when the user has your view, the findings that change the result with their evidence, the checks you ran or propose, and one batch of questions with defaults, and the authorized work is moving.

## Scope and Optional Tools

Skip an unrequested pass for small or mechanical edits, well-specified work, and requests to proceed without discussion. An explicit request for blind spots runs the pass even on specified work, since a specification does not establish that its assumptions hold. When a domain-specific skill owns the task, follow it and apply this pass to what it does not cover.

Read [discovery tools](references/discovery-tools.md) when the scan shows that the dominant unknown is one direct questions handle poorly: an unsettled direction (option map), taste the user can recognize but not describe (throwaway variants), a want best shown by an existing example (reference request), or dependent choices that need a short follow-up exchange (mini-interview). The same file covers the comprehension check, which runs only when the user cannot verify the result directly and wants one.

## Results and Records

Return the result in chat by default. Write a launch brief only when the user asks for one or the work is being handed to another session, agent, or plan; adapt [the template](assets/launch-brief.template.md) and drop the parts that do not apply. When the user asks for a plan, use `work-plan` with these findings instead of another discovery round. To transfer the session itself, use `session-handoff`. Record findings in a file or in the project's existing records only when the user asks or the task already maintains them.

## Gotchas

- **Narrowing while scanning.** A request that looks well defined invites stopping after a few clean checks, and the unnoticed unknown usually sits in a dimension nobody looked at. Finish the sweep, quickly where a dimension plainly does not apply.
- **Teaching instead of finding.** A tour of how the field works reads as useful but changes nothing. Each finding names what it changes in this work.
- **Presenting the inventory.** Listing every dimension checked buries the one finding that matters. Report the scan's results, not its coverage.
- **Defaults becoming decisions.** A recommended default the user did not accept stays an open item with its decide-later rule.
