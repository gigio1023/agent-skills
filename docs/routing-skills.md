# Model routing skill composition

Two skills assign a model and a reasoning effort to each subagent a lead spawns. They are keyed to the lead model, not to a harness: `fable5-model-routing` applies when Claude Fable 5 or 5.1 leads, `gpt6-astra-model-routing` when GPT-6 Astra leads. Claude Code and Codex are the worked examples in their adapter references; Hermes, Cursor, and OpenCode appear there too, and a generic procedure covers any other harness with subagents.

| Capability | Responsibility |
| --- | --- |
| `fable5-model-routing` | Tier each delegated task under a Fable lead, apply the effort policy, install subagent definitions where the harness needs them, and state each subagent's resolved settings before spawning |
| `gpt6-astra-model-routing` | The same under an Astra lead, with worker defaults and role files that keep workers on GPT-5.6 models and reserve Astra for judgment |
| `orchestrate-subagents` | Decide whether and how to decompose, write the packets, coordinate, and synthesize |
| `small-model-handoff` | Write the bounded prompt when a pack skill dispatches to a weaker executor |
| `codex-delegate` | Launch and own a whole Codex mission from another host; routing inside that mission belongs to the Astra skill only when Astra leads it |

The two routing skills share a core section word for word: three signals that place a task in one of four tiers, an effort policy by model class, eleven decision rules, and a dispatch statement. Their `references/source-notes.md` files carry a mirror note; change the core in both or in neither. The vocabulary they use (subagent, subagent definition, task, dispatch, route, tier) is recorded in the repository's [terminology index](../terminology.md).

## Effort policy

Frontier lead models vary effort by task shape. Every model below the frontier runs at `xhigh` by default, and `xhigh` is the floor; a route is lowered only by editing its subagent definition or spawn arguments with a recorded reason. Models without an effort control stay out of the default routes. The cost lever under this policy is which model does the work, not how hard the cheaper model thinks.

## Adoption

Installing a routing skill does not change any configuration. Each skill ships its subagent definitions as assets and proposes their installation; the user approves before anything is copied into a harness's agent directory or configuration file. Model facts such as prices, effort ladders, and catalog defaults are read from the harness at install time and dated in the skill's source notes rather than hard-coded in instructions.
