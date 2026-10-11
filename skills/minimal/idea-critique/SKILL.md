---
name: idea-critique
description: >
  Steelman and attack one stated idea, hunch, or design claim, name the
  cheapest measurement that would decide it, and record its status as
  supported, contradicted, or unmeasured. Use when the user asks to poke holes
  in an idea, steelman it, or play devil's advocate, asks "will this work?" or
  "is this idea any good?", says "이거 될까", "반박해봐", or "약점 찾아줘", or
  when design exploration hands over a stated hunch. NOT for a broad unknowns
  pass in any domain (find-unknowns), opening a design space
  (design-exploration), interviewing the user (interview), or a prior-art
  search alone (literature-research).
---

# Idea Critique

Test one idea the user holds before anyone spends on it. The result is the strongest case for the idea, the strongest case against it, the measurement that would decide between them, and a status tied to evidence.

The division of labor follows a large blind-review study in which LLM-generated research ideas were rated more novel than experts' ideas but slightly less feasible, LLM generation lost diversity as more ideas were produced, and LLM self-evaluation of ideas was unreliable ([Si, Yang, and Hashimoto, arXiv 2409.04109](https://arxiv.org/abs/2409.04109)). The agent supplies mechanisms, evidence, and attacks. Choosing which ideas to pursue stays with the user.

## Scope

An idea is one claim someone could be wrong about: a research hypothesis, a design choice, a mechanism expected to work, a prediction about a model's or agent's behavior, or the key assumption under a plan. Run on the user's request, or when another skill such as `design-exploration` hands over a hunch the user stated. When a message carries several ideas, critique them one at a time, starting with the one the others depend on.

Route nearby requests elsewhere. A user with no single idea yet who wants the space opened needs `design-exploration`. A paper's argument belongs to `credo-paper-plan` when it is installed. A verdict on a built evaluation, or on a result before it informs a decision, belongs to `evaluation-audit`. Turning an idea that survived critique into a resourced bet belongs to `praxis-direction`.

## Claim restatement

Restate the idea in the user's words as one testable sentence: what changes, on which system or population, measured how, compared with what, and under which conditions. Fill gaps from the conversation and project files before asking. Ask the user to confirm only when two readings would lead to different attacks or a different deciding measurement; otherwise state the reading being tested and continue. A vague magnitude such as "a lot better" gets an explicit reading the user can correct. If no reading is testable, the first finding is what the claim must specify to become testable.

## Steelman

Build the version a capable proponent would defend, not the weakest wording. Give the mechanism by which it would work, the supporting evidence with locations, and the conditions under which it most plausibly holds. A repair that keeps the same core bet, such as narrowing the scope or adding a control the idea needs, belongs in the steelman; a different bet is an alternative idea (see Rules). When the steelman is narrower than the stated claim, say what was narrowed. The attack targets the steelman, because defeating a weaker version says nothing about the idea.

## Attack

Look for what would make the steelman false, and lead with the attack that would most change the user's decision if it held.

- **Counter-evidence:** results that contradict the mechanism or the claim, with locations. Search for it with the same effort spent on support.
- **Closest prior work and the delta:** run `literature-research`'s prior-art check, or reuse a current one the effort already holds, rather than searching again here. Prior work that covers the idea is not automatically fatal: say whether its result transfers to the user's conditions and what the idea adds. A check that found nothing covers the searched sources on that date; it is not evidence that the idea is new or that it works.
- **Hidden assumptions:** what must be true that the claim does not state, and how each could fail. In systems whose behavior comes from a trained model or an agent loop, they often hide in whether the metric or judge measures the claimed property, whether evaluation data resembles deployment inputs, whether the baseline got the same budget and tuning, whether the effect exceeds seed and sampling variance, and, for a defense, whether an adaptive adversary was assumed away.
- **Failure conditions:** where the idea stops working, such as scale, distribution shift, cost or latency limits, an adaptive adversary, or interaction with another component. State each as a condition someone could check.

Report the prior-art delta even when it leaves the decision unchanged. Among the other attacks, keep only those that could change the decision; weak objections padded onto the list hide the ones that matter. For each attack, say what observation would rule it out.

When the idea concerns a defense or an attack method, write the attacks in methodology terms: boundary, objective category, metric, judge, environment, and budget. Do not write attack procedures or concrete adversarial inputs. How adversarial evaluations are scoped and judged belongs to `evaluation-design` and its red-team reference.

## Deciding measurement

Name the measurement whose outcome differs depending on whether the steelman or the strongest attack is right. A test for which both sides predict the same result decides nothing, however cheap it is. Specify what is measured, on which data, against which baseline or control, the result that would count as support, and the result that would count as contradiction. Write those predictions before anything runs, so the outcome cannot be reinterpreted afterward. Some tests can only contradict: showing that the failures the idea targets are common proves there is room for a gain, not that the idea delivers it. Say so when that is the case.

Prefer the cheapest test that discriminates, looking in this order: evidence the effort already has (run logs, failure samples, earlier results) reread with the new question; a small probe, ablation, or slice analysis; an evaluation on an existing set; then new training or data collection. Give a rough cost. When the decisive test is too expensive, name the cheaper test that would move confidence and what it cannot settle.

Reading existing results is part of the critique. Running new experiments needs the user's request. Their design and execution belong to `ml-experiment` for training and serving comparisons and to `evaluation-design` for what an evaluation measures, its comparison conditions, and how it is judged.

## Status and record

Give a status, not a verdict:

- **supported:** a measurement or source at the claim's conditions matches the support prediction.
- **contradicted:** a measurement or source at the claim's conditions matches the contradiction prediction.
- **unmeasured:** no evidence yet at the claim's conditions. This is the normal status of a fresh hunch; argument alone leaves an idea unmeasured however strong it is.

Supported and contradicted cite the evidence location: a file path, a run identifier, or a paper with its section. Evidence from a different model, dataset, or scale moves the steelman or the attack, not the status. Give no overall score, probability, or go or no-go call; the study above found LLM evaluation of ideas unreliable, and the choice belongs to the user.

When the effort the idea belongs to already keeps a critique record, such as a critique file in its research folder or the decision log of a design document, append one dated entry in that record's existing format with the claim as tested, the status, the evidence location, the deciding measurement with its predictions, and the attacks still open. A later status is a new entry; earlier entries stay. Otherwise answer in chat, and create a record file only when the user asks.

## Rules

- **No new ideas unless asked.** Do not answer a critique with alternative ideas. The study above suggests the agent's own ideas are less feasible and less diverse than they look, and a critique that drifts into proposals replaces the user's idea with the agent's. When the user asks for alternatives, `design-exploration` generates them.
- **Full strength, no hedges.** State each attack once at its real strength. Uncertainty belongs in the label below, not in softeners such as "might possibly" or "one could perhaps argue". Do not inflate support either: a plausible mechanism is inference, not evidence.
- **Label every point.** Mark each supporting or attacking point as evidence (an observed result or a source, with its location), inference (reasoning from evidence), or speculation (plausible, with nothing behind it yet). Hold the steelman and the attack to the same standard.
- **Update on substance.** When the user disputes an attack, revise it for a new fact or argument and say what changed. Without one, keep the attack and record the disagreement as open; insistence is not evidence.

## Output

Answer in chat with this shape, scaled to what the decision needs:

```text
Claim tested: one sentence in the user's terms, with the reading of any vague magnitude
Steelman: mechanism; supporting points, each labeled
Attacks: ordered by impact; each labeled, with the observation that would rule it out
Closest prior work: the delta, with the check's search date and location
Deciding measurement: the test; support if ...; contradiction if ...; rough cost
Status: supported | contradicted | unmeasured; evidence location or none; record location if appended
```

Read [the worked example](references/example.md) when the depth or shape of a full critique is unclear.
