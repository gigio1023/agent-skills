# Load Generators

Each note says which load model a tool produces, how it measures latency, and what to check in its output. Option names change between versions; confirm them in the documentation of the installed version before a run.

## Choose by load model

- Open loop at a target rate: k6 arrival-rate executors, vegeta, wrk2, or an async script that schedules sends by timestamp.
- Closed loop with a fixed pool of clients: k6 virtual-user executors, Locust, or an async script with a fixed worker count.
- Token-level latency for a streaming model-serving endpoint: the serving engine's benchmark client, or an async script that records the arrival time of the first and each later chunk.

## k6

k6 runs JavaScript scenarios through executors. `constant-vus` and `ramping-vus` are closed: each virtual user loops, waiting for its response. `constant-arrival-rate` and `ramping-arrival-rate` are open: k6 starts iterations at the configured rate and takes virtual users from a pool sized by `preAllocatedVUs` and `maxVUs`. When the pool runs out, k6 skips iterations and counts them in the `dropped_iterations` metric; a nonzero count at a step means the planned load was not offered. The end-of-test summary stops at p(95) by default, so add p(99) to the summary trend statistics or export raw results. Thresholds can encode the latency budget and error ceiling.

## Locust

Locust describes simulated users in Python. Each user sends a request, waits for the response, then waits for its `wait_time`, so the load is closed per user even with throughput-paced wait times: a user whose response is slow cannot keep its pace. It fits multi-step user sessions and teams that write Python. For a target arrival rate that does not depend on responses, prefer an open-loop tool. One Locust process is limited by one CPU core, so use distributed mode when the generator's CPU becomes the limit.

## vegeta

vegeta is a Go command-line tool and library that sends HTTP requests at a constant rate (`-rate`) for a duration (`-duration`), reading targets from a file or standard input, which makes it open loop. When responses slow down it adds workers to hold the rate, up to `-max-workers`; once that cap is reached the achieved rate falls. In `vegeta report`, compare the request rate with the target, and the throughput (successful responses per second) with the rate. Keep the binary results file so percentiles can be recomputed or plotted.

## wrk2

wrk2 is a variant of wrk that holds a constant throughput set by `-R` and measures each request's latency from its intended send time, which corrects for coordinated omission; its README explains the problem. Requests can vary through Lua scripts. Connections are fixed by `-c`, so too few connections cap the achievable rate: by Little's law a target of 500 requests per second at 200 ms latency needs at least 100 connections.

## Serving engine benchmark clients

Many inference servers ship a client that sends a dataset at a request rate and reports time to first token, time per output token, and throughput. Check three things before trusting it: its arrival process, since some default to sending every request at once; its dataset, which should be replaced by the workload model rather than left at a default synthetic or public chat set; and whether repeated or templated prompts hit the engine's prefix cache.

## Async client script

When no tool fits, for example a custom protocol, token-level timing, or replaying logged inputs with their real lengths, write a short client:

- precompute intended send times from the arrival process, with exponential gaps for Poisson arrivals;
- start each request at its intended time without waiting for earlier ones;
- cap requests in flight high enough that the cap is never the limit, and log when it is reached;
- measure latency from the intended send time;
- write one record per request: intended send time, actual send time, end time, status, input and output length.

Run it on a host other than the server and watch its CPU. A single event loop that parses JSON or handles TLS can saturate before the service does; split the load across processes or hosts when it does.

## Checks for any tool

- Achieved send rate matches the target at every open-loop step; otherwise the step is invalid.
- Generator CPU, memory, and connection limits stay below saturation.
- Latency is measured from the intended send time, or the closed load model is stated in the record.
- Timeout and retry settings are recorded, and timeouts count as errors.
- Raw per-request results are saved beside the summary.
