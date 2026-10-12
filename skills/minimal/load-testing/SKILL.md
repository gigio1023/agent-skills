---
name: load-testing
description: >
  Design, run, and interpret load, stress, and capacity tests of a service or model-serving endpoint: a workload model drawn from representative traffic, stepped concurrency or arrival-rate ramps, latency percentiles and errors per step, the saturation point, and the operating point that meets a latency budget. Use for "load test", "stress test", "how many RPS can it handle", "p95 under load", "capacity", "QPS", "부하 시험", "부하 테스트", "동시 요청 몇 개까지", or "몇 QPS까지 버텨". Sends load only on request, and only to systems the user owns or operates. NOT for finding why something got slower (bug-diagnosis), comparing serving configurations for model quality or choosing a pinned-revision serving setup without load (ml-experiment), or evaluation runs (evaluation-design, evaluation-operations).
---

# Load Testing

Measure how a service behaves as offered load rises, in one named environment: where latency or errors bend upward, the highest load that still meets the latency budget, and what the numbers do not cover. The work ends with a short result record that another person can rerun and compare, or with a test plan when only a design was requested. A load test answers a capacity question; beyond checking that responses are valid, it says nothing about output quality.

## Evaluation numbers are not performance evidence

Throughput and latency logged by an evaluation run are not capacity evidence. An evaluation harness sends requests at a pace of its own choosing, usually one at a time or at a small fixed concurrency, with inputs chosen to cover behaviors rather than to match traffic, and often with settings that differ from serving. It is unloaded by design and measures model quality. When a document, plan, or decision needs capacity or latency under load, cite a load test or say that none exists. The reverse also holds: a load test establishes capacity, not quality, so quality claims stay with the evaluation.

## Route other questions elsewhere

- Why the service got slower, why latency jumps at some load, or what causes a bottleneck: `bug-diagnosis`. This skill locates where the limit appears; finding its cause is a diagnosis.
- Which model, quantization, mode, or serving configuration gives better outputs, or pinning a serving setup at fixed revisions before a campaign, with no load involved: `ml-experiment`.
- What an evaluation measures, or running an evaluation campaign: `evaluation-design` or `evaluation-operations`.

Comparing serving configurations for latency and throughput under load stays here: run the same workload and step plan against each configuration and change one setting at a time.

## Authority and early questions

Send load only to systems the user owns or operates. Shared environments and production need explicit authorization from whoever runs them, with agreed limits: maximum rate or concurrency, duration, time window, abort conditions such as an error-rate or latency ceiling, and who to notify. A third-party API the user calls but does not operate is not a load-test target; loading it also spends money and runs into its terms and rate limits.

A design or interpretation request returns findings. Sending load needs the user's request; within an environment already granted, a short smoke run at a low rate can check the setup before the full plan.

Inspect facts before asking: serving configuration, hardware, engine and model versions, existing load scripts, dashboards, and logs. Ask the consequential questions together and early, usually three: which environment and what limits are authorized; what latency budget at which percentile, and what decision the result feeds; and whether representative traffic exists and may be used. A quantity nobody knows yet, such as real arrival burstiness, becomes something to measure or an assumption stated in the record, not a question.

## Model the workload first

Build the request mix from real or representative traffic before choosing any rate:

- input length distribution, in tokens for model serving, because prefill cost grows with input length; output length for generative endpoints;
- request types or endpoints and their shares;
- arrival pattern: steady, bursty, or a daily peak, and whether clients are independent callers or a fixed pool;
- source: sampled request logs used under their data-handling rules, a published traffic profile, or stated assumptions when nothing else exists.

Short and long inputs often saturate at very different rates. Run each as its own workload as well as the mix: a mixed result hides a long-input cliff and shifts whenever the share of long inputs changes.

Do not replay one request, or a small set, in a loop. Response caches, the prefix caches of model-serving engines, and warm data paths turn repetition into unrealistically good latency. Vary inputs as traffic does, and reproduce real shared prefixes, such as a common system prompt, at their real share when the engine caches them.

State what the workload does not represent, for example an auth gateway it bypasses, client retries, cold starts, autoscaling, or a seasonal mix the sample missed.

## Open or closed load

A closed-loop generator keeps a fixed number of virtual users, each waiting for its response before sending again. When the server slows, the generator sends less, so the server is spared exactly when it struggles and latency under overload looks better than real traffic would see. An open-loop generator sends on a schedule, such as Poisson arrivals at a target rate, regardless of responses, so queues build when the server falls behind, as they do under many independent clients. Match the real clients: a fixed worker pool or connection pool is closed; independent users or upstream services are open. Report which one ran.

Coordinated omission is the error where a generator blocked by a slow response delays its next send and never records the wait that delayed request would have seen. Closed-loop tools and naive send-wait-send scripts have it by construction. Measure latency from the intended send time, compare the achieved send rate with the target at every step, and treat a step where the generator fell behind its schedule as invalid rather than as a lower result.

Translate between the two framings with Little's law: requests in flight equal arrival rate times mean time in the system. At 200 requests per second and a 50 ms mean latency, about 10 requests are in flight. Answer "how many concurrent requests" and "how many RPS" questions in both units.

## Ramp in steps and find the bend

Raise the arrival rate (open) or concurrency (closed) in steps, coarse first and then finer around the bend. Hold each step until latency and queue depth are stable, and long enough that the high percentiles rest on many samples: a step with 200 completed requests has only two above its p99. Discard warm-up at the start of the run and the transition at the start of each step; model servers compile kernels, capture graphs, and fill caches on their first requests.

The saturation point is where latency percentiles or errors bend upward while successful throughput stops rising. Beyond it, queues grow, throughput flattens or falls, and timeouts appear. Push past saturation (a stress test) only when the question concerns overload behavior such as load shedding and recovery, and only within the authorized limits. Hold the operating point for hours (a soak) when the question involves memory growth, leaks, or drift.

## Measure each step

Report every step, never averages alone:

- offered load (target rate or concurrency) and the achieved send rate;
- successful throughput in requests per second and, for generative serving, output tokens per second;
- latency p50, p95, p99, and max over successful responses; for streaming, time to first token and time per output token as well as end-to-end latency;
- error rate by type: timeouts, 429 and 5xx responses, invalid or empty outputs;
- resource use: accelerator utilization and memory, KV cache use where it applies, CPU, queue depth, and batch size.

Count only valid, successful responses as throughput; a fast 429, 503, or empty body lowers latency and raises apparent throughput. Set the client timeout above the latency range of interest, report it, and count timeouts as errors: a 1 s timeout hides every slower request, and percentiles over successes alone understate the tail once timeouts appear. Disable client retries or count them, since a retry adds load the plan did not offer.

Percentiles do not average across steps, runs, or instances; merge raw samples or histograms instead. Keep raw per-request records (intended send time, actual send time, end time, status, input and output length) so the table can be recomputed.

State the latency budget before reading results: a percentile, a threshold, and an error ceiling, such as p95 at most 150 ms with errors below 0.1%. The operating point is the highest tested load that meets it. Recommend planning below it, because real traffic bursts above its mean rate.

## Locate the limit before concluding about the server

A flat throughput curve can come from the load generator or the path to the server. Before attributing the limit to the service, check:

- the generator: its CPU, event loop, connection and file-descriptor limits, and achieved versus target rate; when in doubt, split the load across a second generator host and see whether the limit moves;
- the network and anything in front of the service: bandwidth, round-trip time, proxies, load balancers, and rate limiters, since a gateway limiter that returns 429 measures the limiter, not the service;
- the server: utilization, queue depth, and batch size should show saturation at the same step where latency bends.

Record the environment with the result: hardware (accelerator model and count, CPU, memory), serving engine and version, model and exact revision, quantization, batch and concurrency settings, replica count, the service's code revision, and the load generator's tool, version, and host.

When the limit needs a cause, such as why p99 jumps at one step or why a configuration leaves the accelerator underused, hand off to `bug-diagnosis` with the step table and the step that reproduces the symptom. Measurement ends at where the limit appears.

## Results bind to their environment

A result describes one environment: production or production-like versus staging, dedicated versus shared hardware, a replica count, an autoscaling state. A number from a different accelerator, engine version, quantization, or batch setting is a different measurement. Never reuse a number in another environment without saying so beside the number. On shared hardware, record what else was running; when the decision sits near the budget, repeat the decisive steps and report the run-to-run spread.

## Tools

Use the load generator the project already has. Otherwise the options include k6, Locust, vegeta, wrk2, a serving engine's own benchmark client, or a small async client script; none is required. Read [load generators](references/load-generators.md) when choosing one, setting up open or closed load in it, or checking whether it measures from the intended send time. Installing a tool follows the project's dependency rules and the user's authorization; when nothing is available, a short async client script in the project's language covers an HTTP endpoint.

A load script is a measurement instrument. Keep it with the result record so the run can be repeated; it does not join the project's test suite unless the user asks.

## Result record

Write a short record where the project keeps such results:

- question, the decision it feeds, and the latency budget;
- environment, as listed above, including dedicated or shared and production-like or staging;
- workload model: source, length distribution, mix, arrival process, and what it does not represent;
- method: generator and version, open or closed, step plan, hold time, warm-up discarded, timeout and retry settings;
- step table;
- saturation point, and the operating point that meets the budget with the recommended planning figure;
- generator and network checks, and where the limit appeared;
- limits of the claim and the next test that would extend it;
- artifacts: script, command, and raw per-request results.

Read [worked example](references/worked-example.md) when writing a first record or when the shape of the step table and its conclusion is unclear. Read [sources](references/sources.md) when maintaining this package.
