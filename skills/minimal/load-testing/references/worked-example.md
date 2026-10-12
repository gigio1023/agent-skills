# Worked Example: Text-Classification Service

The service, numbers, and environment below are synthetic. They show the shape of a result record and which conclusions its step table supports.

## Question

An HTTP service assigns each incoming document to one of 40 categories before the document is indexed for retrieval. The team needs the replica count for an expected peak of 520 requests per second. Budget: p95 end-to-end latency at the service of at most 150 ms, with errors below 0.1%.

An earlier evaluation run logged 38 requests per second for the same classifier on the same hardware. That harness sent requests at a fixed concurrency of 4 to score accuracy, so the figure is not a capacity measurement and the record does not use it.

## Record

- **Environment:** staging cluster; one replica on one dedicated 24 GB GPU, 8 vCPU, 32 GB RAM; inference server 2.4.1 with dynamic batching (max batch 32, max queue delay 5 ms); 350M-parameter encoder classifier in FP16 at model revision `a1b2c3d`; service revision `4e5f6a7`; no response cache.
- **Workload:** 120,000 inputs sampled without repetition from one week of request logs, used under the service's data-handling rules. Input length median 180 tokens, p90 900 tokens, truncated at 2,048; 12% of inputs exceed 512 tokens. Open-loop Poisson arrivals, because callers are independent upstream services.
- **Not represented:** the API gateway and its authentication (requests went to the internal endpoint), client retries, cold starts, autoscaling, more than one replica, and the year-end mix, in which long documents are about twice as common.
- **Method:** k6 `constant-arrival-rate` executor, one scenario per step, from a separate host in the same zone. Steps of 50 to 300 requests per second, plus 225 added around the bend. Each step held 5 minutes with the first 60 seconds discarded. Client timeout 5 s, retries off.

## Step table (logged mix)

| Offered (req/s) | Successful (req/s) | p50 (ms) | p95 (ms) | p99 (ms) | Errors | GPU util | Queue depth p95 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 | 50.0 | 21 | 48 | 71 | 0.00% | 18% | 1 |
| 100 | 99.9 | 23 | 55 | 84 | 0.00% | 35% | 2 |
| 150 | 149.8 | 27 | 68 | 105 | 0.00% | 54% | 4 |
| 200 | 199.7 | 34 | 96 | 148 | 0.01% | 72% | 9 |
| 225 | 224.6 | 41 | 138 | 260 | 0.02% | 81% | 17 |
| 250 | 247.1 | 61 | 212 | 410 | 0.05% | 91% | 38 |
| 300 | 266.2 | 840 | 2,900 | 4,700 | 2.30% | 97% | 220 |

At 300 requests per second the errors are timeouts and the percentiles cover successful responses only, so the real tail at that step is worse than the table shows.

Generator checks: `dropped_iterations` was 0 at every step, generator CPU peaked at 22%, and the round trip to the service was 0.4 ms. The limit therefore sits on the server side, where GPU utilization and queue depth climb at the same steps as latency.

## Input length split

The same step plan was repeated with two single-length workloads drawn from the same logs.

| Workload | Highest rate meeting budget (req/s) | Saturation begins (req/s) |
|---|---:|---:|
| Short only, up to 256 tokens | 400 | 400 to 450 |
| Logged mix, 12% above 512 tokens | 225 | 225 to 250 |
| Long only, 1,024 to 2,048 tokens | 60 | 60 to 80 |

## Conclusion

One replica in this staging environment meets p95 at most 150 ms with errors below 0.1% up to 225 requests per second of the logged mix. Latency bends between 225 and 250 requests per second while the generator and network stay well below their limits. Planning at 200 requests per second per replica leaves room for bursts above the mean rate, so a 520 requests per second peak needs three replicas, provided replicas scale linearly behind the load balancer.

The result does not show that linear scaling, latency through the gateway, or capacity under the year-end mix. The split runs show that long inputs cost several times more than short ones, so a mix with twice the long share needs its own run rather than an estimate from this table.

## Next tests

- Three replicas behind the load balancer, stepping from 450 to 700 requests per second with the same workload.
- The year-end mix, built from last year's logs for that period.
- A comparison of max batch 32 and 64 under this workload, changing nothing else, if the team wants more per-replica headroom.

Why p99 grows faster than p95 from 200 requests per second onward is a diagnosis question for `bug-diagnosis`, which receives this table and the 225 step as the reproducing condition.

## Artifacts

The run directory holds the k6 script, the exact command line for each step, the per-request results, and the server metrics export for the same time window.
