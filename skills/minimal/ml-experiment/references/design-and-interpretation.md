# Design and Interpretation

## Make the comparison answer the question

Separate an intervention, an outcome, and the unit being compared. If the question is whether a training change improves a model, an implementation check is a prerequisite, not the outcome. If the question is whether a reported result can be reproduced, distinguish reproducing its artifact, measurement, and claimed interpretation.

Choose the strongest relevant existing baseline within the permitted resources, or explain why a cheaper proxy is being used. Do not compare a tuned candidate with an untuned baseline and attribute the whole gap to the candidate's method. Match budgets according to the claim: examples, optimization steps, wall time, and accelerator-hours answer different questions.

An ablation can isolate a component when removing it leaves a meaningful comparison. Jointly changing data, objective, decoding, and scoring cannot isolate any one effect. When factors interact, a small factorial or paired comparison may be more informative than changing one setting blindly.

## Model development

Start from an established training setup where possible. Choose a small diagnostic configuration for iteration without claiming it establishes full-scale behavior. Treat model size, learning rate, regularization, batch size, and training duration as interacting choices. A feasible batch size is not proof of better validation performance.

Record which configurations were tried and how the selected one was chosen. Keep final assessment separate from repeated validation-based tuning. If evaluation feedback influenced training choices, reflect that in the scope of the claim.

## Read the outcome

Compare examples or groups consistently when possible. Look at error patterns and relevant variation before choosing an aggregate explanation. Decide whether another repeat could change the decision, rather than requesting repetitions solely to satisfy a template.

Distinguish a failed run, a completed run with a negative result, and a completed comparison that lacks precision to choose. “No reliable difference observed” is weaker than “the methods are equivalent.” Prefer the simpler explanation only when the available evidence supports it, not because it makes the report shorter.

## Synthetic example

Two classifiers differ only after their text truncation settings changed. Recheck the intended comparison and measure the truncation effect before attributing the result to the new optimizer. If this is a quick check within the current grant, perform it. If it reveals that the dataset no longer represents the intended problem, propose a direction change before launching a new study.
