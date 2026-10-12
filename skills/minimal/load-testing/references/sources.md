# Sources and Scope

Written 2026-10-12. The works below are cited for established concepts and were not fetched while this version was written; recheck a definition or tool option against the current source before quoting it in detail.

- Bianca Schroeder, Adam Wierman, and Mor Harchol-Balter, "Open Versus Closed: A Cautionary Tale," USENIX NSDI 2006. Source of the distinction between open and closed load generation and of the finding that the two behave differently at the same load; used for the open or closed rule.
- Gil Tene's account of coordinated omission, in his talk "How NOT to Measure Latency" and in the [wrk2 README](https://github.com/giltene/wrk2). Used for measuring latency from the intended send time and for treating a generator that falls behind its schedule as an invalid step.
- John D. C. Little, "A Proof for the Queuing Formula: L = λW," Operations Research 9(3), 1961. Little's law, used to translate between requests in flight, arrival rate, and latency.
- Tool repositories: [k6](https://github.com/grafana/k6), [Locust](https://github.com/locustio/locust), [vegeta](https://github.com/tsenart/vegeta), and [wrk2](https://github.com/giltene/wrk2). Used only for each tool's load model and the option names in [load generators](load-generators.md).

The rule against using evaluation-run numbers as performance evidence, the workload-first rule, the step plan, the per-step measurements, the environment binding, and the worked example are independently authored. The example is synthetic. These sources do not establish any capacity figure, and package validation does not show that a particular load test is sound.
