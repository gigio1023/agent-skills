# Model routing skill composition

GPT work defaults to Astra. Sol 6.1 is reserved for very easy deterministic collection, transformation, or command execution with fixed inputs, procedure, output, and mechanical acceptance. Source selection, interpretation, diagnosis, implementation, review, and writing require Astra. Uncertain assignments stay on Astra.

| Skill | Responsibility |
| --- | --- |
| `gpt6-astra-model-routing` | GPT model and effort selection, worker roles, and nested GPT delegation |
| `fable5-model-routing` | Anthropic model and effort choices under a Fable lead |
| `orchestrate-subagents` | Decomposition, ownership, coordination, and synthesis |
| `small-model-handoff` | Fixed execution contracts for a selected mechanical or weaker executor |
| `codex-delegate` | External Codex mission launch, authority, runtime, and evidence |

GPT routing applies inside delegated missions and under non-GPT leads whenever the worker is a GPT model. Fable routing keeps its Anthropic choices separate. The two routing packages no longer mirror a common model table. The [terminology index](../terminology.md) records shared orchestration vocabulary.

## Collection And Judgment

| Packet | GPT route |
| --- | --- |
| Download specified URLs and return file hashes | Sol 6.1 or script |
| Run fixed status commands and return raw output | Sol 6.1 or script |
| Select sources or summarize a paper's limitations | Astra |
| Diagnose a service failure | Astra |
| Implement or review a scoped change | Astra |

Sol output contains raw or mechanically transformed results, source locations, execution status, and missing items. Astra interprets that evidence and chooses the next action. Read-only status, high volume, and a compact output do not make a task mechanical.

## Effort And Authority

Preserve an explicit user choice and the effective session effort where supported. Do not lower frontier effort merely because the model is a worker. The Codex assets default to Astra at `xhigh` for named and unnamed general workers, and Sol 6.1 at `xhigh` for `sol-clerk`. Fable assets preserve selected session effort; Sonnet and Opus retain their separate `xhigh` defaults.

Actual user budgets, concurrency limits, and scope remain binding at every delegation depth. The skills do not impose an arbitrary frontier consultation count. Each dispatch states task, role, model, effort, configuration source, and whether the runtime was observed. Selecting a role or accepting a request does not prove which settings ran.

## Adoption

Editing or installing a routing skill does not activate its role assets. Apply configuration changes only under the user's installation grant and preserve unrelated settings. Current harness schemas control role fields, override support, and fork modes. Sol 6.1 and legacy Sol have different API contracts; verify the exact model and active catalog before installation.

For existing installations, replace `sol-scout` with `astra-scout`, `sol-builder` with `astra-builder`, and `fable-lean-builder` with `fable-builder`. Update references and retire the old roles within the same installation grant. The repository assets and an installed runtime are separate verification targets.
