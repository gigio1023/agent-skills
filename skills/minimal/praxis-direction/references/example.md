# Worked example: from agenda to bet

Synthetic organization: a twelve-person company selling a document-extraction model to accounting firms. Its profile names one always-on GPU, a paid burst provider with approval above a stated amount, one domain expert (a former auditor), and an internal set of 340 labeled invoices, 58 of them multi-page. Every number below is invented for the example.

Agenda as stated: "we need better table extraction".

| Gate question | Answer that emerged |
| --- | --- |
| Outcome | Two prospects declined a pilot because line items on multi-page invoices were merged. The sales lead decides on pilots; the deliverable is a pilot pass on the prospects' own samples. |
| Operational definition | Line-item recall on multi-page invoices, scored by the internal evaluation the team already runs. Today 0.71 on the 58 multi-page invoices. Success is 0.90 on those 58 plus the prospects' 20 samples. |
| Intervention | The candidates answer different questions. A page-boundary fix in post-processing asks "is the model already reading rows correctly and losing them at the join"; fine-tuning on more multi-page invoices asks "can the model learn the join". The cheapest separating test scores the model per page and compares with the joined result: if per-page recall is already near 0.9, the join is the problem and no training is needed. |
| Compute ladder | Always-on: the per-page scoring, one afternoon. One GPU-day: fine-tune on the 58 with augmented splits if the join test fails. Paid burst: only if a larger backbone is tried; the profile's threshold applies and a prediction is written first. |
| In-house assets | The expert question: which line-item fields matter for the audit trail, so the metric weights them. The 340 invoices support evaluation and a few-shot pool; as a training seed, 58 multi-page examples are too few without augmentation, which the plan records. |
| Deliverable and kill | A pilot run on the prospects' 20 samples in three weeks. Kill if per-page recall is also below 0.75: then the reading model itself is the problem and the bet becomes a model-selection question. |

Prediction written by the user: "Per-page recall will be above 0.88 and the join fix will reach 0.90 without training."

The Goal block named the per-page scoring as the first action and left fine-tuning conditional on its result. The paid burst never entered the plan because no tier below it had been exhausted.
