# GPT-6 Astra Routing Policy

Use GPT-6 Astra for GPT work by default. GPT-6.1 Sol is an exception for very easy, deterministic bulk collection, transformation, or status-command execution that requires no semantic judgment. Ambiguous tasks stay on Astra.

This is the owner's operating policy, not a claim that Sol cannot perform more complex work. It applies to GPT workers under any lead, at every permitted delegation depth, and inside missions launched through `codex-delegate`. Anthropic choices remain with the [Fable routing policy](../fable/policy.md).

## Routing Decision

Use Sol only when every condition holds:

1. The packet fixes the inputs, procedure, and output format.
2. No step requires choosing a source, interpreting meaning, diagnosing a cause, ranking importance, or deciding the next action.
3. A count, hash, schema, source comparison, or other explicit mechanical criterion checks the result.
4. An unexpected result returns to Astra with the raw evidence and completed actions.

| Work | Route |
| --- | --- |
| Fetch specified URLs or collect results for fixed queries | Sol 6.1 or a script |
| Deduplicate by a supplied key or run an approved deterministic transform | Sol 6.1 or a script |
| Run named status commands and return their raw output | Sol 6.1 or a script |
| Choose sources, summarize papers, compare conflicting evidence | Astra |
| Diagnose failures or choose recovery actions | Astra |
| Design, implement, debug, critique, review, write, or edit prose | Astra |
| Mixed or uncertain task | Astra |

Read-only work and large volume do not establish simplicity. Extracting important limitations from many papers requires judgment. Running `nvidia-smi` can be mechanical; explaining a GPU failure requires Astra. A bounded implementation still requires judgment and stays on Astra.

Prefer a direct script or tool call when it already performs the mechanical operation. A Sol worker is useful only when it adds execution capacity within the same fixed contract. When a bounded executor prompt is needed and `small-model-handoff` is installed, it may write that packet. Otherwise write the packet directly: the fixed inputs, the exact commands or transforms, the output format, the mechanical acceptance check from condition 3, and an instruction to stop and return the raw evidence and completed actions to Astra on any unexpected result. Do not apply these restrictive execution rules to ordinary Astra work.

## Delegation And Effort

An explicit user instruction about delegation, model, effort, or budget governs. Within that grant and the current harness contract, the lead or `orchestrate-subagents` decides whether delegation helps. This policy authorizes selecting model and effort for an already justified GPT delegation; it does not require spawning or changing installed configuration.

Astra workers may research, implement, write, review, or recommend within their assigned scope. The lead owns integration, conflict resolution, and the final user response. When a worker may delegate further, its packet carries this GPT routing rule and the same authority and resource limits.

Preserve the user's selected effort or the effective session effort when supported and appropriate to the task. Do not lower frontier effort merely because the model is a worker. When no effort has been chosen, the shipped roles use `xhigh` as this pack's default for both Astra and Sol 6.1. Name model and effort together; a model-only override may use a catalog default. Runtime-specific modes such as `ultra` need their own compatibility and delegation checks.

Keep the user's actual cost, time, concurrency, and token limits. Do not invent a frontier consultation cap or require a cheap-model trial before Astra. After a failure, inspect the evidence and choose the next action within the grant; retry count alone does not identify the cause.

## Worker Roles

| Role | Responsibility | Shipped model and effort |
| --- | --- | --- |
| `astra-scout` | Source selection, exploration, evidence interpretation, summaries | `gpt-6-astra`, `xhigh` |
| `astra-builder` | Design, implementation, debugging, writing | `gpt-6-astra`, `xhigh` |
| `astra-judge` | Independent review of a specification and artifact | `gpt-6-astra`, `xhigh` |
| `sol-clerk` | Fixed collection, transformation, or command execution | `gpt-6.1-sol`, `xhigh` |
| Unnamed worker | General work within its packet | `gpt-6-astra`, `xhigh` |

The role defines the task; it does not reduce the task's authority or expand it. A review packet returns findings, while a packet that authorizes fixes may include them. Astra is not restricted to advisory consultations.

Read [harness adapters](harness-adapters.md) before the first spawn in an unfamiliar harness. Use only fields, models, and effort levels the active surface supports. If the harness cannot select Astra for judgment-bearing GPT work, keep that work with an eligible lead or report the affected limitation. Do not silently replace it with Sol.

Before a spawn, state the task, role, selected model and effort, configuration source, and confirmation state. For example:

```text
Implementation | astra-builder | gpt-6-astra | xhigh | spawn arguments | runtime unverified
```

Requested settings and observed runtime settings are separate evidence. A role file or accepted request establishes configuration, not proof of what the child ran.

## Worker Evidence

Astra workers return the result, decisive sources or changed files, relevant checks, unresolved conflicts, and material limits. The lead inspects the evidence and integrates the result while continuing independent work.

Sol workers return the requested raw or mechanically transformed output, source locations, command exit statuses, counts or hashes when requested, and failed or missing items. Do not ask them to select decisive facts, summarize implications, assess confidence, propose recovery, or choose follow-up queries. Escalate those decisions to Astra.

## Installation

The [Codex assets](../../assets/gpt/codex/config.snippet.toml) provide worker defaults and role files. Install or update them only when the user requests configuration changes. Reuse that authorization without another confirmation. Merge with the existing configuration, preserve unrelated settings, and verify the installed paths and model availability. Editing or installing the skill alone does not activate its roles.

Record runtime checks in the task's artifact or installation report. Change packaged [source notes](source-notes.md) only when maintaining this policy, not during ordinary use.

## Verification

Check that every judgment-bearing GPT packet resolves to Astra and that each Sol packet satisfies all four mechanical conditions. Check role references, selected effort, and the actual harness contract. Report material substitutions and unobserved runtime settings. Package checks establish consistency; they do not demonstrate a quality or cost gain.
