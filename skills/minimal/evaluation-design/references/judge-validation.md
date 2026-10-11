# Judge Validation

A model judge is an instrument with its own error rates. Validation measures those rates against an independent reference for the one failure mode the judge checks, binds them to the judge's exact configuration, and states when they stop applying. Numbers below are defaults from the named sources, not gates; the decision's smallest difference sets what is enough.

## Reference labels and splits

Label outputs of the system under test for one failure mode at a time, by a domain expert or by independent annotators whose disagreements are resolved and recorded. Split the labelled outputs into three disjoint sets, by the unit of generalization so one source does not straddle them:

- **train:** clear-cut pass and fail cases, the only source of few-shot examples in the judge prompt (evals-skills default: 10 to 20 percent);
- **dev:** used repeatedly while revising the judge and never placed in the prompt (about 40 to 45 percent);
- **test:** held out until the judge is final (about 40 to 45 percent).

Include enough failures to estimate the failure-class rate even when real prevalence is skewed. evals-skills suggests about 50 pass and 50 fail examples and notes that intervals widen below about 60 in total.

## Error rates chosen by the cost of each error

Report class-conditional rates, never raw accuracy or percent agreement alone. The sources disagree on which pair:

- evals-skills uses the true positive rate and true negative rate because they feed prevalence correction, and rejects precision, recall, and Cohen's kappa for judge against reference. Its target is above 90 percent on both, with 80 percent as a minimum.
- PyRIT and garak use precision, recall, and F1, and Eugene Yan recommends classification metrics for binary judges. PyRIT advises precision when false positives are costly (benign content flagged) and recall when misses are costly (a violation passed).
- Anthropic's eval audit asks for agreement near 90 percent on clear-cut cases.

Choose by what each error costs the decision and say why: TPR and TNR when the output is a rate that will be corrected and reported, recall on the failure class when a missed failure is the expensive error, precision when flagged items go to costly review. Inspect every disagreement. A false pass means the fail definition is too weak, a false fail means the pass definition is too strict, and a cluster on one input type calls for a targeted train example or a narrower criterion. Inconsistent reference labels mean the rubric needs repair before the judge does.

## Test split run once

Iterate on dev only. Run the final judge once on test and report those numbers, not dev numbers. A revision made after seeing test results needs fresh dev data, and its final number needs a test set the revision has not seen.

## Known negatives, format, and determinism

- Feed an empty answer, "I don't know", and a confident answer to a different question; the judge should fail all three (Anthropic).
- Present the same content in other valid formats (code fences, an answer wrapped in a sentence, units, number formats, field order) and confirm the verdict holds. A judge or parser whose verdict follows format is measuring format.
- Score the same output twice. If the verdict changes, measure judge variance and report it apart from target variance.

## Biases

- **Position:** in pairwise judging, randomize order per case or score both orders.
- **Verbosity:** instruct against rewarding length and test with padded copies of the same answer.
- **Self-preference:** judges favor outputs from their own family. Anthropic advises against the model under test judging itself; evals-skills holds that the task model can judge because judging is a narrower task. When the judge compares that model's outputs with a rival's, use a different family or a small panel.
- **Label deference and injection:** do not reveal which response is the reference or baseline, and treat candidate text as data, not instructions.

## Judge identity and re-validation

A validation result applies to one judge identity: prompt and rubric text, few-shot set, model snapshot by dated identifier rather than a floating alias, decoding settings, and output parser. Record it with a hash over those fields, as PyRIT does. Re-validate when any of them changes, when the rubric or reference label set changes, when the system under test or the input distribution shifts (a new model family, task family, or language), or when intervals on judge-scored results widen unexpectedly.

## Reporting judge-scored rates

Keep the judge's uncertainty distinct from the target's performance. Prevalence correction is an option when reporting a judge-scored rate: the Rogan-Gladen estimate `theta = (p_obs + TNR - 1) / (TPR + TNR - 1)`, clipped to [0, 1], with a bootstrap interval over the test labels (evals-skills). It is undefined when TPR + TNR is near 1. Label which number is raw and which is corrected.

## Harm-severity judges

When severity is the measured quantity, validate a normalized or ordinal severity scale against human severity labels (PyRIT):

- mean absolute error against the human score, beside the error of a constant guess at the median human score; a judge that does not beat the constant has not learned the scale;
- Krippendorff's alpha among human raters (label quality), across repeated judge trials (consistency), and between judge and humans;
- review of the two failures PyRIT reports: benign text that only sounds dangerous scored as harmful, and harmful content masked by disclaimers scored as benign.

Binary judges remain the default for decision gates.
