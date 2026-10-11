# Eval Cases and Labels

## What a case represents

Name what one case represents (a task, conversation, episode, document, or request) and the population the result should generalize to, and keep counts in that unit. Draw cases from observed failures, intended behaviors, and their boundaries rather than only easy examples or a leaderboard convention. Describe the actual source coverage and the populations that are missing. If balancing or oversampling changes the mix, keep construction counts apart from deployment prevalence. Mark synthetic cases with their generator and review scope; a generator's diversity claim is not measured coverage. Generating along stated dimensions, such as user type, task type, and difficulty, spreads cases better than free generation, and a defect found in generated cases is fixed in the generator, because patching items leaves siblings of the same defect.

## Coverage in both directions

For each behavior, include cases where it should occur and cases where it should not: refuse and comply, call the tool and leave it alone, escalate and resolve directly. In a safety eval, benign requests that resemble disallowed ones measure over-refusal, scored as their own outcome. Behavioral forms are options when they fit the task: a minimum capability test, invariance under a change that should not matter, or an expected direction of change under one that should (CheckList).

## Verifiable success conditions

- State the observable condition that makes a case pass, precisely enough that two careful experts would agree on a given output.
- Ship at least one reference solution that passes the scorer. A case that every variant fails is more often broken than hard.
- Let difficulty come from the problem rather than obscure wording, and for agentic cases give what a user would plausibly report, not the investigation.
- Keep ground truth out of reach of the system under test: not in the prompt, the few-shot examples, a readable file, or repository history.
- Check whether cases about named entities can be answered from memory when the intent is to test retrieval or tool use, and record when answers that depend on live facts were last verified.

## Labels

Write the operational label definition with positive, negative, and ambiguous examples, and pilot it on real in-scope items before broad labelling when ambiguity is costly. Record who or what produced each label and which judgments were independent. A model-generated label is a candidate until the review the decision requires establishes it. Never use the outputs of a model under comparison as gold for that comparison, since reference matching then rewards imitating it (Anthropic). An adjudicated label is an approved dataset decision, not unquestionable truth, and generated cases, criterion assignments, or a formatting pass do not make a gold-labelled set.

## Disagreement

Review disagreement for a definition problem, missing context, or true ambiguity before treating it as annotator error. Keep ambiguous items marked with their competing labels rather than forcing them into a clean label; they show where the definition needs repair and make useful borderline examples. Aggregate agreement can hide failure on a rare label, so inspect it by class. Inter-rater statistics compare human raters with each other; a judge against its reference follows [judge validation](judge-validation.md).

## Splits and leakage

Set the split boundary by the unit of intended generalization: source, entity, conversation, task family, or time. Split before data-dependent augmentation, or keep source-group identity so descendants cannot cross the boundary. Check exact and near-duplicates across it, and review borderline matches rather than trusting one similarity threshold. Cases used to tune the system, its prompt, or a judge are no longer independent of that tuning, so report on cases that were not. Document actual access, since a name like test or gold does not show isolation.

## Versions

Give cases stable identifiers, record the reason for each changed label, exclusion, or transform, and version the case set and its grader together, since scores from before and after a grader change are not comparable. Check both the loader's output and representative original records: a structural check finds missing fields, while semantic review decides whether a case and its label fit the task. A case set may later serve as a standing regression suite or be refreshed from production traces; that lifecycle follows project practice.

## Synthetic example

A refusal eval for a coding assistant holds 200 requests that should be declined and none that resemble them but should be answered. A system that declines everything scores perfectly. Adding near-boundary benign requests, scored as a separate over-refusal outcome, exposes the degenerate policy, and splitting both kinds by source repository keeps near-identical requests from straddling the tuning and report sets.
