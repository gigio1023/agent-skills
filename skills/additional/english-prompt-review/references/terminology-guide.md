# Technical English Terminology Guide

Use this as a judgment guide, not a replacement table. A term earns a recommendation only when it captures the user's intended technical distinction more clearly than the original wording.

## How to Teach a Term

Keep the term, alternatives, and examples in English. Use Korean for the narrow semantic explanation, then return immediately to an English contrast or reuse example. Do not finish with a Korean-only definition.

```text
`identify the root cause`: 실패 지점을 찾는 데서 끝나지 않고 원인을 특정한다는 뜻이다. `locate the failure` describes where; `identify the root cause` explains why.
```

If two terms imply different work, present both English choices and explain the decision boundary in Korean. Do not recommend the more technical-sounding term until the prompt provides enough evidence to support it.

## Software Engineering

| Intent | Natural technical wording | Use when |
| --- | --- | --- |
| Find why a failure happens | `identify the root cause` | The request is diagnostic, not merely descriptive. |
| Make a failure happen again | `reproduce the issue` | There is a specific bug or failure to verify. |
| Avoid breaking existing behavior | `avoid regressions` or `preserve backward compatibility` | The first is broad; the second concerns existing interfaces or consumers. |
| Check that a change works | `verify the change` | State the test, observable behavior, or acceptance criterion when known. |
| Make a small safe change | `make the smallest viable patch` | The user wants constrained scope, not an arbitrary refactor. |
| Check resource use | `profile` or `benchmark` | `Profile` locates cost; `benchmark` compares measured performance. |
| Limit the work | `keep the change scoped to ...` | The boundary matters to implementation and review. |

Prefer concrete verbs such as `trace`, `isolate`, `validate`, `instrument`, `refactor`, `ship`, and `roll out` when the request supports them. Do not use `robust`, `seamless`, `leverage`, or `ensure` as vague substitutes for an observable requirement.

## AI and Machine Learning

| Intent | Natural technical wording | Distinction to preserve |
| --- | --- | --- |
| Test model quality | `evaluate the model` | Name the task, metric, or held-out data when available. |
| Compare a changed component | `run an ablation` | Use only when isolating the contribution of a component or choice. |
| Use a model to produce results | `run inference` | This is execution, not training or evaluation. |
| Improve data quality | `curate the dataset` or `clean the data` | `Curate` is deliberate selection; `clean` usually removes or fixes defects. |
| Check if results generalize | `evaluate generalization` | Do not use it as a synonym for any improvement. |
| Tie answers to supplied sources | `ground the response in ...` | This refers to evidence use, not generic accuracy. |

Avoid treating `hallucination`, `alignment`, `agentic`, `reasoning`, and `grounded` as catch-all praise or diagnosis. Ask for the observed behavior, failure mode, or metric instead when the wording is not specific enough.

## Game Development

| Intent | Natural technical wording | Use when |
| --- | --- | --- |
| Improve response and feedback | `improve game feel` | It is a valid industry term; specify input, animation, audio, or feedback if possible. |
| Investigate inconsistent smoothness | `investigate frame-time spikes` | The issue is uneven frame pacing, not necessarily low average FPS. |
| Find a performance bottleneck | `profile the bottleneck` | Measurement is needed before optimization. |
| Define recurring player actions | `gameplay loop` | The request concerns the repeatable player experience. |
| Improve game-agent behavior | `AI behavior` or `behavior tree` | Use `behavior tree` only when that architecture is actually intended. |
| Change rendering stages | `render pipeline` | The request is about rendering flow, not a visual style alone. |

`Lag` is often too broad. Prefer `input latency`, `network latency`, `frame-time spike`, `stutter`, or `low frame rate` when the prompt provides enough evidence to distinguish them.

## Rewrite Patterns

These are shapes for whole-prompt paraphrases, not mandatory templates.

```text
Investigate <observed failure>, identify the root cause, and make the smallest viable fix. Preserve <constraint> and verify the result with <evidence>.

Review <target> for <goal>. Keep the scope to <boundary>, call out uncertainties, and do not change files unless I explicitly ask.

Profile <system> under <scenario>, identify the main bottleneck, and recommend the next experiment before making an optimization.
```

Prefer the user's own concise wording when it already states the task clearly.
