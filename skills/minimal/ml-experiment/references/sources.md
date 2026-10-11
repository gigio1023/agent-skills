# Sources and Scope

The experiment, training-data, and interpretation methods were reviewed September 17, 2026; the serving, interpretation-rival, and model-adaptation sources were verified October 3, 2026 by fetching each arXiv abstract page.

## Method and data

- [Google Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook): inspected the initial-configuration, incremental-tuning, exploration, and experimental-goal sections. Adopted narrow informative rounds, separation of scientific and nuisance settings, and explicit compute tradeoffs. It assumes a working training pipeline and sufficient tuning resources; its batch-size and optimizer advice is not imposed on every architecture.
- [Gebru et al., Datasheets for Datasets](https://arxiv.org/abs/1803.09010): inspected abstract and metadata. The stated motivation, composition, collection, and recommended-use framing informs concise training-data documentation. It does not require filling an entire datasheet for each small review.
- [Kapoor and Narayanan, Leakage and the Reproducibility Crisis in ML-based Science](https://arxiv.org/abs/2207.07048): inspected abstract and publication metadata. It motivates explicit review of data dependence, leakage, and the information boundaries a claim relies on; this package does not claim to have reproduced the paper or its survey, or that a particular dataset is contaminated.

## Interpretation and rival explanations

- [K-Dense scientific-agent-skills, hypothesis-generation](https://github.com/K-Dense-AI/scientific-agent-skills/tree/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/skills/hypothesis-generation): inspected the SKILL.md at revision `1549884` (2026-10-01), section "Generate rivals before choosing tests". Adopted the practice of generating rival explanations from genuinely different classes (measurement artifact, confound, selection, reverse causation) and preferring tests where rivals predict different outcomes. The skill's biomedical preregistration machinery, templates, and scripts are not adopted.

## Model adaptation

No public source gives a method template for changing one behavior while preserving capability; these establish that the effects are real and bound the claims, and are cited in `model-adaptation.md` as measurement rules, not a recipe.

- [Arditi et al., Refusal in Language Models Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717): inspected abstract (v1 2024-06-17, v3 2024-10-30). Used for one measurement rule: refusal is carried separately from general capability in the models it studied, so refusal and capability are measured as separate outcomes. The paper's intervention is not reproduced or described here.
- [Qi et al., Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!](https://arxiv.org/abs/2310.03693): inspected abstract (2023-10-05). Used for the finding that even benign finetuning data degraded safety alignment, hence a retention set must include behaviors not being changed. No attack data or procedure is taken.
- [Biderman et al., LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673): inspected abstract (v1 2024-05-15, v2 2024-09-20). Used for the point that target-domain gain and source-domain retention move independently, so each needs its own held-out set.
- [Betley et al., Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs](https://arxiv.org/abs/2502.17424): inspected abstract (2025-02-24, v7 2026-01-20). Used for the finding that narrow finetuning produced broad out-of-distribution behavior change, and for its control design (reframed dataset, trigger-gated variant) as a model for isolating unintended effects.
- [Röttger et al., XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours](https://arxiv.org/abs/2308.01263): inspected abstract (v1 2023-08-02, v3 2024-04-01). Used for measuring over-refusal as its own direction (250 safe prompts, 200 unsafe contrasts). The suite itself is an evaluation artifact owned by the evaluation skills; here it supports the rule that refusal and over-refusal are separate outcomes.

The workflow, unit-of-analysis checks, serving-comparison rules, and synthetic examples are independently authored. Runtime commands come from the actual project's implementation and version-specific framework documentation; a project supplies its own label rules, permitted data, and quality criteria. The sources do not establish that these instructions improve model behavior, and package validation does not establish dataset quality or any experimental result.
