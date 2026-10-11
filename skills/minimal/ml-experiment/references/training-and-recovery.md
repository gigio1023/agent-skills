# Training and Recovery

Use the project's runner, scheduler, configuration system, and checkpoint conventions. Do not replace them with a new orchestration service.

## Establish readiness

Inspect actual model and tokenizer revisions, the data transform and split, objective and loss masking, trainable parameters, batch semantics, optimizer and schedule, precision, and checkpoint policy where they affect the experiment. For fine-tuning, verify that the intended parameters receive updates and that prompt/target formatting matches the task.

A small authorized run can reveal invalid batches, non-finite loss, absent gradients, or an evaluation path that reads the wrong checkpoint. Overfitting a tiny sample can be a diagnostic when appropriate; it is not a universal requirement or a model-quality result.

Estimate duration and resource demand from representative throughput when available. State the uncertainty that changes whether to launch. A run that spends beyond the always-on tier or the stated budget, or a material expansion, needs the presentation in SKILL.md unless already authorized; duration alone does not decide.

## Preserve and recover

Identify the live job and its owned output before resuming. A model checkpoint alone may lack optimizer, scheduler, scaler, RNG, or data-progress state. Establish what the saved state actually supports; label a restart or approximate continuation accurately.

Do not overwrite another run's outputs, silently switch revisions, or restart because a session lost its handle. Preserve the project's checkpoint retention and privacy rules. Store credentials in their configured mechanism, not experiment records.

When infrastructure fails, diagnose the failure and decide whether retrying the same intended comparison is useful. Do not count a failed attempt as a negative scientific result, or omit its impact on consumed resources and available observations.

## Finish

A completed process, saved checkpoint, evaluated result, and supported scientific claim are different accomplishments. Report the one actually established. Keep detailed configuration and output identity in the experiment records; select only reader-relevant details for a report.
