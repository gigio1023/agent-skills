# Training Data Construction and Review

This reference covers data a training recipe consumes. Evaluation case sets and the review of evaluation labels are designed in evaluation-design, not here; its reference on eval cases and labels holds the evaluation-side rules a shared corpus also has to keep.

## Population and selection

Name what one item represents and what the training set should let the model generalize to. A user's sessions, a document's excerpts, and independently collected documents have different dependence, and counts should follow the chosen unit.

Describe actual source coverage and meaningful missing populations. Sampling weights and oversampling change the distribution the model learns, so distinguish construction counts from deployment prevalence when they differ. Keep synthetic material identified, with its generation and review scope when relevant. A generator's diversity claim is not measured coverage.

When review of generated training items finds a defect, such as a wrong label pattern, a template artifact, or a topic the generator keeps repeating, repair the generator (its prompt, template, or filter) and regenerate or refilter the affected output by the same rule. Editing only the items the review happened to sample leaves the same defect in every unreviewed item the generator made alongside them.

## Annotation

Write the operational label definition with positive, negative, and ambiguous examples. Pilot it on actual in-scope items before broad annotation when ambiguity could be costly. Identify who or what produced each label, which judgments were independent, and how unresolved disagreement is handled.

Review disagreements for a definition problem, missing context, or true ambiguity before treating every difference as annotator error. Aggregate agreement can conceal rare-label failure, and label noise is a quantity to measure, not an assumption to wave away. Preserve the examples needed to repair the instruction, subject to privacy rules.

An adjudicated label can be an approved training decision without being unquestionable ground truth. A model-generated label is a candidate until the required review establishes it; do not call a generated question family, a criterion assignment, or a formatting pass a gold-labelled dataset.

## Splits and contamination

Set the split boundary according to the unit of intended generalization: entity, source, conversation, time, or another relevant unit. Fit preprocessing, selection, and imputation only on the information permitted for that split. Check whether near-duplicates or shared sources create shortcuts across the boundary.

The boundary that matters most for training data is contamination with evaluation material. Use exact hashes for identical bytes or records and an appropriate similarity method for near-duplicates, and check training data against the evaluation set in both directions. Review borderline matches rather than treating a single similarity threshold as fact. Split before data-dependent augmentation, or retain source-group identity so descendants cannot cross the boundary. Overlap between training and evaluation inflates every later number and cannot be undone after the run.

A corpus that serves both evaluation and training keeps the split rules of both. On the evaluation side, evaluation-design's reference on eval cases and labels splits by the unit of generalization and keeps cases that tuned the system or its judge apart from cases that report the result. On the training side, nothing that reaches an evaluation split may be trained on. Draw the evaluation partition by the unit of generalization first, train only on what remains, and record each item's assignment so a later reuse of the corpus cannot cross the boundary.

## Target formatting

The training templates are part of the data, not a cosmetic detail. Verify that prompt and target formatting, loss masking, and special tokens match the recipe and the intended behavior; a formatting mismatch is a common silent failure that trains the model on the wrong signal while every structural check passes.

## Versions and review

Preserve stable identifiers and the reason for changed labels, exclusions, or transforms. Follow existing manifests and schema; add only the smallest missing documentation. A short source note can cover purpose, selection, annotation, split, permitted use, known limits, and version identity when those matter.

Verify both the loader's output and representative original records. Structural checks find missing fields or invalid values; semantic review establishes whether an item and label fit the task. Keep their conclusions distinct.

## Synthetic example

Synthetic example. A training set contains five paraphrases of each original query. Random row splitting puts related paraphrases in both the training portion and the held-out portion, and some paraphrases also near-match items in the capability benchmark. Partition by original query first, then check the training queries against the benchmark for exact and near-duplicate overlap. If the intended use is repeated variants of known queries, that is a different claim and must be trained and measured as such.
