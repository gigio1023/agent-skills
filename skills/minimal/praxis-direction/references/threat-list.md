# Failure-mode list for a new system

Ten failure modes to check against every new system, used by the failure-mode pass in praxis-direction. Fill one row per item:

| Item | Applies? | Why (interface, access, data flow) | Most realistic variant and rough cost | Known prior work | Worth a look? |

Ten failure modes: Items 1 to 4 are the four Carlini named in the [Latent Space interview](https://www.latent.space/p/carlini); 5 to 10 extend the list to systems that read untrusted content and take actions. Terms follow common usage in the adversarial machine learning literature (see NIST AI 100-2 for definitions); state the objective, the technique, and the assumed access separately when you fill a row.

| # | Failure mode | Objective (what fails) | Typical access needed | First question to ask |
| --- | --- | --- | --- | --- |
| 1 | Evasion at inference time | The model gives the attacker's chosen wrong output on a crafted input | Query access; gradients help but are not required | Which inputs are attacker-controlled, and what does a wrong output cost? |
| 2 | Data poisoning (including web-scale and continual training) | Training or fine-tuning data is altered so the resulting model misbehaves | Ability to place content where the pipeline collects it | Where does training data come from, who can write there, and is provenance checked? |
| 3 | Model extraction | A functional or exact copy of the model, or of a layer, is recovered from queries | Query access; richer outputs (logits, probabilities, logit bias) make it cheaper | What does the API return beyond the top answer, and how many queries are cheap? |
| 4 | Training-data extraction and membership inference | Verbatim or near-verbatim training records, or membership of a record, is recovered | Query access; generation endpoints are most exposed | Was the model trained on data anyone would mind leaking, and can it be made to regurgitate? |
| 5 | Prompt injection, direct and indirect | Instructions in attacker-supplied content override the operator's intent | The system reads attacker-influenced text: user input, documents, web pages, tool results | Which text reaches the model from sources the operator does not control? |
| 6 | Jailbreaking | Safety or refusal behavior is bypassed for a restricted request | Query access | What is the model supposed to refuse, and what would a bypass enable downstream? |
| 7 | Information disclosure and exfiltration | System prompt, hidden context, retrieved private documents, or user data leaves its boundary | Query access; an output channel (links, tool calls, markdown images) for exfiltration | What is in context that the user should not see, and can output reach a third party? |
| 8 | Unsafe actions through tools or agents | The system performs an action the operator did not intend: writes, sends, deletes, purchases | Influence over any input the agent reads | What can the system do besides answer, and what confirms an action before it runs? |
| 9 | Backdoors and supply chain | A model, dataset, or dependency carries a hidden trigger or malicious component | Control over an artifact the victim downloads or fine-tunes from | Where do weights, datasets, and packages come from, and are they verified? |
| 10 | Denial of service and resource abuse | Availability or cost is degraded: pathological inputs, quota exhaustion, runaway agent loops | Query access | What input makes the system slow or expensive, and who pays? |

Keep the list fixed between passes; edit it only with a dated note here so results stay comparable across systems.
