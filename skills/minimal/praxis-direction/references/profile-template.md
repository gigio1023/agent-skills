# Praxis profile template

Copy the field headings and fill the values for your organization. Keep the file within about forty lines. The example values below describe a synthetic company and are placeholders, not recommendations.

## Fields

| Field | Holds | Used by gate question |
| --- | --- | --- |
| Organizational outcomes | What the company must sell or prove this quarter, the deliverable forms that count, who decides | 1 |
| Evidence conventions | Internal evaluations and public benchmarks accepted as evidence, where results are recorded | 2 |
| Compute ladder | Always-on resources (accelerators, API limits), paid burst (provider, approval threshold, approver), what is written before a burst | 4 |
| In-house assets | Expert roles and how to reach them; internal datasets with size, supported use, and access rules | 5 |
| Horizon and kill rule | Default weeks per bet, review checkpoint, default kill condition | 6 |
| Records | Where a Goal block goes (plan format), where predictions and hindsight are kept | closing |
| Stances | Research stances the organization holds differently, stated in words; add the credo-taste tenet number only when that package is installed | all |

Question 3, the intervention and the question it answers, has no field: that reasoning does not depend on the organization.

## Example (synthetic)

````markdown
# Praxis profile

## Organizational outcomes
- Q4: close two pilots with mid-size accounting firms; the deliverable is a pilot pass on the prospect's own sample. Decided by the sales lead.
- Internal: replace the hosted extraction API with the in-house model by year end. Decided by the CTO.

## Evidence conventions
- The internal invoice evaluation (340 labeled invoices, 58 multi-page) is the accepted score; results go to the evaluation dashboard.
- Public benchmarks are context only; a prospect's sample outranks both.

## Compute ladder
| Tier | Resource | Approver |
| --- | --- | --- |
| always-on | one 24 GB GPU, hosted API within the monthly quota | none |
| one-day | the same GPU for up to 24 hours | team lead |
| paid burst | cloud provider, above 300 USD per run | CTO, after a written prediction |

## In-house assets
- Expert: former auditor (document-review lead); ask in the weekly review or by direct message.
- Data: invoice set, 340 labeled, supports evaluation and few-shot; a training seed only with augmentation. Access: internal only, no customer samples leave the workspace.

## Horizon and kill rule
- Three weeks per bet, checkpoint at the end of week one, kill when the first test contradicts the prediction.

## Records
- Goal blocks go to `.plans/<name>.md`; predictions and hindsight are appended to the same plan.

## Stances
- Run several projects and expect to finish about one in five (credo-taste T8): not held; one bet at a time.
- Go to lengths a reasonable person would not (credo-taste T9): held only within the tier already approved.
````
