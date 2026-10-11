# Model Adaptation

Adapting a model to change one behavior while preserving the rest is a comparison, not a delivery. The same measurement rules apply whether the changed behavior is a task capability, a style, or a safety property such as refusal: the questions are whether the intended behavior actually changed, whether the capabilities you meant to keep survived, and whether either effect reaches beyond the examples you trained on.

No public source gives a method template for this work. The papers below establish that the effects are real and that narrow edits have broad consequences; none prescribes a recipe. This reference is therefore a set of measurement rules, not a procedure. It contains no technique, no prompts, and no steps for removing a behavior. What goes in the project is the comparison design and its evidence.

## Measure the two outcomes separately

The intended behavior change and the retained capability are different claims and need different held-out sets. Measure each on its own set, held out from whatever produced the adaptation, and do not let a gain on one stand in for the other. A model that acquires the intended behavior while losing unrelated capability has not succeeded; a model that keeps its capability without the intended change has not either. Report both numbers with the conditions they were measured under.

LoRA Learns Less and Forgets Less (Biderman et al. 2024, arXiv 2405.09673) is the reason to measure retention on its own set: it reports that an adaptation method can underperform on the target domain while better preserving out-of-domain performance, so target-domain gain and source-domain retention move independently and a single aggregate hides the trade-off.

## Count refusal as its own outcome

Refusal is a graded outcome, never a capability failure. A model that declines a request has not failed a capability test, and scoring a refusal as a wrong answer conflates a policy response with an inability. Record refusal as its own metric, separate from task success, so a change in refusal rate is visible and is not summed into a capability number in either direction. Refusal in Language Models Is Mediated by a Single Direction (Arditi et al. 2024, arXiv 2406.11717) reports that refusal in the open chat models it studied is carried by one direction in the residual stream, separable from general capability; refusal and capability can therefore move independently, and neither can be read off the other.

Over-refusal is the matching failure and needs its own cases: a model can become more willing on the target distribution while refusing benign requests it should answer, or the reverse. XSTest (Röttger et al. 2023, arXiv 2308.01263) measures exactly this exaggerated-safety direction with a suite of safe prompts a calibrated model should accept alongside unsafe contrasts; the lesson for adaptation is to test both the should-answer and should-decline directions, not one.

## Baseline before any weight edit

Run a prompting-only or scaffold-only comparison before changing any weights. A different system prompt, a decoding change, or a retrieval or tool scaffold can produce the intended behavior without a weight edit, and if it does, the edit's effect must be measured against that baseline rather than against the untouched model. Attributing the whole change to the weight edit when a prompt alone would have moved the number is the confound this baseline rules out.

## Test generalization beyond the training distribution

Measure whether the change holds outside the training distribution, because narrow training can have broad and unintended effects. Emergent Misalignment (Betley et al. 2025, arXiv 2502.17424) reports that finetuning on a narrow task produced broad behavior change on unrelated prompts in the strongest cases, and that a dataset change framing the same task differently prevented the effect; the controls that isolated it, such as a reframed dataset and a trigger-gated variant, are the model for showing a narrow edit did not move behavior you did not intend to touch.

Fine-tuning Aligned Language Models Compromises Safety (Qi et al. 2023, arXiv 2310.03693) is the companion warning: it reports that even benign, common finetuning data degraded safety alignment, so a retention set must include the behaviors you are not trying to change, not only the target task, and a held-out safety measurement belongs in the comparison even when safety was not the edit's purpose.

## Bind card numbers and pin provenance

A published model-card number is bound to the serving configuration and mode it was measured under, and does not transfer to a different stack or mode. Carry the measurement conditions with any card figure you reuse, or do not reuse it; a reasoning-off figure on one engine does not predict a reasoning-on deployment on another.

Record the provenance of every base checkpoint at its pinned revision: the source, the resolved revision rather than a mutable alias, the license and permitted use, and the configuration and tokenizer that came with it. A comparison across checkpoints is only interpretable when each one's identity and revision are fixed; a silent revision change invalidates the comparison the same way a served-model mismatch does.
