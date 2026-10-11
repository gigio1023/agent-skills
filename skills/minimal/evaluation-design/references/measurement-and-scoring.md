# Measurement and Scoring

## Capability and cases

Describe the observable behavior that counts as success and the cases likely to distinguish competent from superficial performance. Separate the construct from its proxy. Exact match can be valid for a structured answer but inappropriate where multiple answers are acceptable. Conversely, semantic similarity can reward a plausible response that violates a decisive requirement. Case construction and labels are covered in [cases and labels](cases-and-labels.md).

## Metrics and outcome classes

Define numerators and denominators before implementation. State how failures, abstentions, invalid outputs, duplicates, repeated trials, and missing records enter the result. Missing is not zero unless the metric explicitly defines that treatment.

Define outcome classes before running and count each one: refusal, truncation or budget exhaustion, infrastructure or external failure, grader failure, and verified success or failure. Attribute before excluding. Outcomes the system is responsible for (a refusal, an invalid format, no response, a file it was told to write and did not) are graded and stay in the denominator, each reported as its own class so refusal zeros and capability zeros are not summed. Instrument failures (a grader error, an infrastructure error) are exclusions reported beside the rate, and a grader failure is retried in the grader, not the target (Inspect, Anthropic). Whether truncation at a token or turn budget counts as failure is a stated choice of the contract. Distinguish a system asserting a negative ("nothing found") from one producing no answer; if both land on one label, a runner that errors on every input scores like one that searched carefully.

Use macro or micro aggregation according to the target question and show a meaningful subgroup when a summary could reverse the interpretation. For rare high-stakes behaviors, fail-on-any or worst case can fit the decision better than a mean diluted by easy cases. Latency conditioned on successful responses is a different quantity from reliable request completion. Record both when the decision needs both; do not require every report to reproduce every field.

## Uncertainty and resolution

Estimate uncertainty at the actual independent unit. Repeated paraphrases or requests from one case are not necessarily independent samples. Use paired comparisons when the same cases allow them. Resampling, confidence intervals, and significance tests require assumptions; choose and explain the method instead of adding a generic interval to every score.

Compare the noise floor with the smallest decision-relevant difference and with the headroom between baseline and ceiling. Anthropic's eval audit gives a default for a pass rate: the half-width of the paired-difference 95 percent interval is roughly `1/sqrt(n * R)` for n cases and R repetitions, so 25 cases with 2 repetitions resolve about 14 points and 100 cases with 2 about 7. Measure it from a baseline at the real repetition count once one exists. Cases and repetitions draw on one budget, so set them together.

## Scorers

Test canonical correct, incorrect, boundary, invalid, and missing outputs. Check normalization, parsing, units, aggregation, and any scorer version change. A scorer that is too rigid rejects a correct answer in another valid form; one that is too lenient accepts a wrong but plausible answer, so write one and confirm it fails. Keep raw outputs so permitted rescoring can produce linked derived results rather than overwrite history. Model judges follow [judge validation](judge-validation.md); one judge's score is not a general quality measurement without it.

## Comparison and adaptation

Record which changes came from development feedback. A held-out assessment reused for selection is no longer independent of that selection. Differences in prompt, tools, sampling, execution budget, or compute may be part of the intended system comparison; identify them rather than pretending the checkpoint alone caused the result.

If an evaluation reveals that its own method is misleading, state the observed issue and propose the correction. User confirmation is needed when the correction changes the research direction or success criterion, not for every local scorer bug fix already authorized.

## Synthetic example

A scorer counts a malformed answer as absent and drops it from the denominator. The resulting accuracy describes only parseable answers. Hand-worked invalid-output cases expose the mismatch if the intended measure is success over all submitted cases. Correcting the method is separate from rerunning the model, which may be unnecessary if retained raw outputs support rescoring.
