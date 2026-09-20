# Example Library

Use this library to find a public work close to the current reader task. The entries identify a passage and an original adaptation, not a prescribed template. Choose the relevant example, read its passage, and apply the technique to the actual project evidence. Read [writing patterns](writing-patterns.md) for finished synthetic examples and [source readings](source-readings.md) for the original technical foundations.

These are text and information-structure reading pointers. Inspect the actual figure or control before treating its visual meaning or behavior as evidence. Historical proposals, archived editions, and demos remain historical sources; current implementation claims require current documentation. Operational data-view examples are maintained in `insight-dashboard`.

## Contents

- [Design documents and exact references](#design-documents-and-exact-references)
- [Engineering reports and investigations](#engineering-reports-and-investigations)
- [Visual and data explanations](#visual-and-data-explanations)

## Design documents and exact references

- **[TigerBeetle Architecture (docs/ARCHITECTURE.md)](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/ARCHITECTURE.md)** — Read Design Decisions. Tie each design choice to the workload property that makes it useful. Give consequential decisions stable headings.

- **[FoundationDB Architecture (공식 문서)](https://apple.github.io/foundationdb/architecture.html)** — Read role descriptions. Explain component responsibilities in a consistent order, and trace the interaction that connects them.

- **[CockroachDB RFC: Distributing SQL queries (2016)](https://github.com/cockroachdb/cockroach/blob/master/docs/RFCS/20160421_distributed_sql.md)** — Read numbered examples and alternatives. Increase example complexity as the explanation needs it, then compare alternatives on the same constraints.

- **[SQLite Tokenizer Requirements (HLR 명세)](https://sqlite.org/draft/tokenreq.html)** — Read token requirements. For a testable specification, state the condition and required behavior precisely; use requirement IDs when traceability needs them.

- **[The Lemon Parser Generator (프로젝트 기술 문서)](https://www.sqlite.org/src/doc/trunk/doc/lemon.html)** — Read operation, syntax, and error processing. Introduce the operating model before syntax details, and place trust assumptions beside the input they constrain.

- **[React RFC 0188: Server Components](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md)** — Read basic example and component constraints. Show observable behavior before reference semantics, then explain adoption and compatibility for the affected callers.

- **[Svelte 5 소개 글 — Runes (공식 블로그)](https://svelte.dev/blog/runes)** — Read old and new code examples. Explain a changed programming model with corresponding code examples; preserve the proposal date and recheck current syntax.

- **[SQLite Release 3.45.0 Changelog](https://www.sqlite.org/releaselog/3_45_0.html)** — Read changed defaults and release identity. Put a changed default, its effect, and the relevant override together; link the exact release being described.

- **[Zig 언어 레퍼런스 (0.16.0)](https://ziglang.org/documentation/0.16.0/)** — Read alignment and reference navigation. State the concept in a complete sentence before its numeric boundary; make exact interfaces easy to locate.

- **[SRFI-1 List Library (Olin Shivers)](https://srfi.schemers.org/srfi-1/srfi-1.html)** — Read rationale and function specifications. Explain how existing implementations informed an interface, then keep exact function behavior available for lookup.

- **[PEP 683 — Immortal Objects, Using a Fixed Refcount](https://peps.python.org/pep-0683/)** — Read acceptance conditions and historical status. Keep conditional acceptance visible and distinguish a design record from the current implementation reference.

- **[LangGraph Overview (공식 문서)](https://docs.langchain.com/oss/python/langgraph/overview)** — Read overview and acknowledged influences. Explain the orchestration responsibilities and suitable use case. Use the overview for orientation, not promotional phrasing as a technical voice.

- **[KEP-4603: Tune CrashLoopBackoff (Kubernetes Enhancement Proposal)](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/4603-tune-crashloopbackoff/README.md)** — Read design details and current/proposed behavior. Connect a proposed policy to its changed behavior and relevant operational checks; adapt the questions to the project.

- **[ClickHouse MergeTree 테이블 엔진 문서](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree)** — Read physical organization and CREATE TABLE syntax. Connect storage structure to the interface the reader uses, then explain the parameters that change behavior.

- **[Pijul Manual — Theory 장 (웨이백 스냅샷)](https://web.archive.org/web/20210307215344/https://pijul.org/manual/theory.html)** — Read graph definitions and dependencies. Give formal objects concrete identities and explain the operations on them. Read the archived edition for historical rationale.

- **[draft-toomim-httpbis-braid-http-04 (Braid-HTTP Internet-Draft)](https://www.ietf.org/archive/id/draft-toomim-httpbis-braid-http-04.txt)** — Read independent protocol extensions. Explain each independently adoptable capability and its concrete use case before describing their combination; preserve draft status.

- **[KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/kafka/kip-500:+replace+zookeeper+with+a+self-managed+metadata+quorum)** — Read metadata as an event log. Explain the architectural constraint and the mechanism chosen to resolve it; keep a decision record connected to its discussion.

- **[SE-0393: Value and Type Parameter Packs (Swift Evolution)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0393-parameter-packs.md)** — Read motivation and detailed design. Derive the proposed abstraction from a concrete maintenance cost, and introduce dependent concepts in dependency order.

- **[Go 제네릭 구현 설계: Dictionaries + Gcshape Stenciling (Go 1.18)](https://go.googlesource.com/proposal/+/refs/heads/master/design/generics-implementation-dictionaries-go1.18.md)** — Read gcshapes and dictionary format. Define the equivalence conditions precisely and relate the concrete design to earlier proposals on the same subject.

- **[Rust RFC 131: Target Specification](https://rust-lang.github.io/rfcs/0131-target-specification.html)** — Read target settings and their combinations. State conditional configuration behavior so readers can predict the effect of combining options.

- **[SQLite Database File Format 명세](https://www.sqlite.org/fileformat.html)** — Read database header and record format. Present offsets, sizes, and meanings in a consistent lookup structure, with the version boundary that makes the format applicable.

- **[PyPA Binary Distribution Format (Wheel) 명세](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)** — Read filename rules and RECORD. Keep naming, integrity records, and installation-relevant behavior in the format specification where implementers can find them.

- **[PostgreSQL 18 Release Notes](https://www.postgresql.org/docs/current/release-18.html)** — Read migration and compatibility. Put upgrade consequences where operators will see them before acting, then describe new capabilities in their relevant groups.

- **[Django 5.1 Release Notes](https://docs.djangoproject.com/en/6.1/releases/5.1/)** — Read compatibility and paired code examples. Show the old and new use of an interface with comparable code, and keep supported-version information beside migration guidance.

- **[PostgreSQL Wiki: Don't Do This](https://wiki.postgresql.org/wiki/Don%27t_Do_This)** — Read rationale and appropriate exceptions. Pair a discouraged practice with the preferred alternative and the condition under which an exception is useful.

- **[RFC 9110: HTTP Semantics (표준)](https://www.rfc-editor.org/rfc/rfc9110.txt)** — Read method and status semantics. Preserve exact requirement levels and cross-reference definitions when writing a normative protocol specification.

- **[NEP 18: NumPy Array Function Protocol](https://numpy.org/neps/nep-0018-array-function-protocol.html)** — Read motivation and alternatives. Use concrete ecosystem needs to explain an interface extension, and state how experimental behavior will evolve.

- **[Git hash-function-transition 설계 문서 (Documentation/technical)](https://github.com/git/git/blob/master/Documentation/technical/hash-function-transition.adoc)** — Read goals and transition procedures. Explain compatibility during a staged format transition and show the ordered operations needed to preserve it.

- **[CPython Argument Clinic (Developer's Guide)](https://devguide.python.org/development-tools/clinic/)** — Read background, tutorial, reference, and how-to. Separate learning from exact lookup while keeping one current home for the documentation.

## Engineering reports and investigations

- **[Cloudflare outage on November 18, 2025](https://blog.cloudflare.com/18-november-2025-outage/)** — Read request processing and the outage. Connect recurring symptoms to the described configuration mechanism; derive event times from the source rather than an inferred chart timeline.

- **[Slack's Incident on 2-22-22](https://slack.engineering/slacks-incident-on-2-22-22/)** — Read mitigation and datastore load. Explain the immediate mitigation and its cost, then trace the conditions that caused the incident.

- **[Incident Report: Spotify Outage on April 16, 2025](https://engineering.atspotify.com/2025/5/incident-report-spotify-outage-on-april-16-2025/)** — Read impact and cause analysis. Separate affected populations in the prose and explain why their conditions differed; inspect the chart before asserting a visual encoding.

- **[Upgrading GitHub.com to MySQL 8.0](https://github.blog/engineering/infrastructure/upgrading-github-com-to-mysql-8-0/)** — Read upgrade plan, rollback, and challenges. Give migration stages concrete validation and recovery points, and explain gaps between test and production behavior.

- **[Partitioning GitHub's relational databases to handle scale](https://github.blog/engineering/infrastructure/partitioning-githubs-relational-databases-scale/)** — Read virtual partitions. Explain logical boundary enforcement before physical movement. Keep query rates distinct from the number of partitions.

- **[How GitHub uses eBPF to improve deployment safety](https://github.blog/engineering/how-github-uses-ebpf-to-improve-deployment-safety/)** — Read dependency types and filtering. Classify the actual failure modes before presenting the mechanism that addresses them.

- **[How Figma's multiplayer technology works](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)** — Read OT/CRDT influences and central authority. State the assumptions that permit a simpler custom design; this source describes CRDT-inspired structures, not adoption of OT.

- **[Rust in production at Figma](https://www.figma.com/blog/rust-in-production-at-figma/)** — Read performance and benefits/drawbacks. Relate a language choice to the service workload, its measured behavior, and the costs that remain.

- **[How Discord Scaled Elixir to 5,000,000 Concurrent Users](https://discord.com/blog/how-discord-scaled-elixir-to-5-000-000-concurrent-users)** — Read fanout, shared data, and concurrency. Organize the explanation around bottlenecks, showing how observations changed the attempted solution.

- **[The Data Canary: How Netflix Validates Catalog Metadata](https://netflixtechblog.com/the-data-canary-how-netflix-validates-catalog-metadata-18b699d58e36)** — Read controlled failure injection. Explain the validation system through its constraints, then describe a test that checks the validator itself.

- **[A Closer Look at the Christmas Eve Outage](https://netflixtechblog.com/a-closer-look-at-the-christmas-eve-outage-d7b409a529ee)** — Read dependency postmortem and service impact. Attribute the provider explanation separately from the impact observed in the dependent service.

- **[How we cut CDN metadata lookup latency by 91%](https://vercel.com/blog/how-we-cut-cdn-metadata-lookup-latency-by-91-percent)** — Read lookup stages and rollout trade-offs. Show how each change addresses a particular cost, including the evidence-based reason to stop optimizing.

- **[Reasons why bugs might feel "impossible"](https://jvns.ca/blog/2021/06/08/reasons-why-bugs-might-feel-impossible/)** — Read debugging difficulty categories. Turn a vague difficulty into a concrete information gap and the next useful way to investigate it.

- **[How web bloat impacts users with slow connections](https://danluu.com/web-bloat/)** — Read connection-speed comparison and tail behavior. Choose comparison dimensions that represent different user conditions, and preserve important variation beyond the average.

- **[Postgres Job Queues & Failure By MVCC](https://brandur.org/postgres-queues)** — Read test bench, lock time, and dead tuples. Descend from symptom to mechanism with an observation at each layer; keep the reproduction setup retrievable.

- **[AI Flame Graphs](https://www.brendangregg.com/blog/2024-10-29/ai-flame-graphs.html)** — Read profiling units and sample search. Explain what the visualization measures before interpreting its shapes, and state relevant collection overhead.

- **[A dynamic linker murder mystery](https://fasterthanli.me/articles/a-dynamic-linker-murder-mystery)** — Read investigation and counterexamples. Retain the observation that disproved a hypothesis; introduce background at the point the reader needs it.

- **[Jepsen: etcd 3.4.3](https://jepsen.io/analyses/etcd-3.4.3)** — Read consistency documentation, tests, and results. Translate a guarantee into observable behavior, then distinguish the test design from what the tests found.

- **[Problems with the heap](https://rachelbythebay.com/w/2025/03/26/atop/)** — Read reproduction blocks. Use a minimal observed failure to anchor an investigation; keep reproduction instructions separate from unsupported generalization.

- **[Stack Overflow: How We Do Monitoring - 2018 Edition](https://nickcraver.com/blog/2018/11/29/stack-overflow-how-we-do-monitoring/)** — Read data types and alerting. Organize a monitoring explanation by signals and operator tasks before listing the tools that implement them.

- **[Etsy's Debriefing Facilitation Guide for Blameless Postmortems](https://www.etsy.com/codeascraft/debriefing-facilitation-guide)** — Read debriefing questions and dialogue. Show questions that recover the information available at decision time, then connect that context to procedural improvement.

- **[How Uber Executed A JUnit Migration at Massive Scale](https://www.uber.com/blog/junit-migration/)** — Read migration prerequisites and recipe. Connect each automation stage to its concrete input, output, and check; use usage evidence to prioritize work.

- **[서버 증설 없이 처리하는 대규모 트래픽](https://toss.tech/article/monitoring-traffic)** — Read bottlenecks and improvement iterations. Connect each intervention to the observed bottleneck and its subsequent measurement; retain natural, complete Korean sentences.

- **[Feign 코드 분석과 서버 성능 개선](https://toss.tech/article/engineering-note-3)** — Read problem analysis and library behavior. Follow the observed symptom into the library mechanism before explaining why the change affects performance.

- **[BFF 서버에 SSE를 도입한 이유: 전시 서버의 통신 구조 재설계](https://techblog.woowahan.com/26507/)** — Read communication design and SSE choice. Explain the interface constraint, compare plausible transports, and describe the selected request flow.

- **[스마트스토어센터 Oracle에서 MySQL로의 무중단 전환기](https://d2.naver.com/helloworld/6512234)** — Read dual writes and consistency validation. Describe the migration mechanism and the checks needed to maintain consistent data during the transition.

- **[같은 장애를 두 번 겪지 않기 위해, 배포 전에 리뷰합니다 — KRIS 개발기](https://tech.kakao.com/posts/831)** — Read rule checks and model judgment. Explain which mechanism makes each decision and why the responsibilities are separated; use scope detail only where it affects the reader.

- **[개인화된 Airflow 테스트 환경 구축 및 운영 경험](https://tech.kakao.com/posts/829)** — Read environment design and lifecycle examples. Derive requirements from existing workflow friction, then show creation, use, and cleanup as concrete reader tasks.

- **[Profiling a simple performance issue in a JVM-based server](https://engineering.linecorp.com/en/blog/profiling-a-simple-performance-issue-in-a-jvm-based-server/)** — Read hotspot investigation and conclusion. Show the evidence behind continuing or stopping an optimization, with the interpretation limits of profiling samples.

- **[How adding Kubernetes label selectors caused an outage in Grafana Cloud Logs — and how we resolved it](https://grafana.com/blog/how-adding-kubernetes-label-selectors-caused-an-outage-in-grafana-cloud-logs-and-how-we-resolved-it/)** — Read investigation queries and label behavior. Connect the configuration change to traffic distribution and explain meaningful differences between affected and unaffected environments.

## Visual and data explanations

- **[GPS (interactive essay)](https://ciechanow.ski/gps/)** — Read simple positioning and time of flight. Begin with a small model, name the variable the reader changes, and add complexity when the earlier model reaches its limit.

- **[Sound (interactive essay)](https://ciechanow.ski/sound/)** — Read waves and oscillation. Let a concrete experiment introduce a parameter, then state the approximation conditions of the explanation.

- **[Curves and Surfaces (interactive essay)](https://ciechanow.ski/curves-and-surfaces/)** — Read splines and continuity. Show the failure of the initial construction, the improvement, and the next constraint that remains.

- **[Moon (interactive essay)](https://ciechanow.ski/moon/)** — Read brightness baseline and scene notation. Establish the comparison model and explain the simplifications that change how a diagram should be read.

- **[Hexagonal Grids (reference article)](https://www.redblobgames.com/grids/hexagons/)** — Read coordinate systems and conversions. Organize a reference by implementation task; keep linked representations consistent when a parameter changes.

- **[Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)** — Read paired search examples. Hold the input constant while changing one algorithmic condition, then explain the observed difference.

- **[Probability for RPG Damage](https://www.redblobgames.com/articles/probability/damage-rolls.html)** — Read distribution explanation. Explain unfamiliar encodings at first use and connect the distribution to the design choice it informs.

- **[2D Visibility algorithm](https://www.redblobgames.com/articles/visibility/)** — Read algorithm summary. Conclude a mechanism explanation with its usable ordered operations and a clear distinction between implemented and untried approaches.

- **[CO₂ and Greenhouse Gas Emissions landing page](https://ourworldindata.org/co2-and-greenhouse-gas-emissions)** — Read key insights and baseline. Make the supported finding prominent, with the baseline and uncertainty needed to interpret its evidence. Adapt headline wording to this skill's noun-phrase title default; state the finding in the nearby text.

- **[Air Pollution topic page](https://ourworldindata.org/air-pollution)** — Read metric definition and evidence. Define the measurement boundary before the result when that boundary is necessary for interpretation.

- **[Can an AI make a data-driven, visual story?](https://pudding.cool/2024/07/ai/)** — Read production stages and editorial feedback. Make tool output and reviewer judgment visibly distinct; retain representative failures as evidence in an adoption assessment.

- **[Why I changed my mind on dual-axis charts](https://datawrapper.de/blog/why-i-changed-my-mind-on-dual-axis-charts)** — Read alternative chart forms. Compare encodings using the same data and choose according to the reader question, preserving what each view makes harder to see.

- **[Plotting fall temperatures with range & value overlays (Weekly Chart)](https://datawrapper.de/blog/span-chart-range-value-overlays-in-column-charts)** — Read input columns, overlays, and annotations. Describe the input shape and transformation, then distinguish annotations that define the display from those that explain a finding.

- **[Up and Down the Ladder of Abstraction](https://worrydream.com/LadderOfAbstraction/)** — Read concrete, trajectory, and aggregate views. Move between individual behavior and aggregate structure, explaining what the reader is looking at after each change of level.

- **[Parable of the Polygons](https://ncase.me/polygons/)** — Read manual and automated simulations. Introduce the rule through a small manual example before moving to repeated aggregate behavior.

- **[How To Remember Anything Forever-ish](https://ncase.me/remember/)** — Read guided explanation and sources. Make the next learning action clear and keep supporting sources retrievable; retain a restrained register for technical work.

- **[Histogram (D3 notebook)](https://observablehq.com/@d3/histogram)** — Read input, transformation, and rendered result. Separate an analysis into reusable computational steps and preserve the rendered output for static readers.

- **[Blockchain Explained (Reuters visual guide)](https://www.reuters.com/graphics/TECHNOLOGY-BLOCKCHAIN/010070P11GN/index.html)** — Read components and transaction stages. Follow the same concrete record through the stages so the reader can connect the mechanism end to end.

- **[Feature Visualization (Distill)](https://distill.pub/2017/feature-visualization/)** — Read figure explanations and method questions. Give a technical figure enough local context to be interpreted, and organize unfamiliar methods around reader questions.

- **[Vital Signs: Global Temperature (NASA)](https://climate.nasa.gov/vital-signs/global-temperature/)** — Read takeaway, baseline, and measurement uncertainty. State the baseline beside the result and choose comparison language that matches the available uncertainty evidence.

- **[Climate change: global temperature (NOAA Climate.gov explainer)](https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature)** — Read definitions, captions, and archive notice. Define unfamiliar measurements where used, attribute the data behind a figure, and make an archived document recognizable.

- **[Attention in transformers, step-by-step (3Blue1Brown)](https://www.3blue1brown.com/lessons/attention)** — Read diagram notation and attention explanation. Explain what the diagram symbols and transformations mean before asking the reader to interpret them.

- **[[데이터로 보는 뉴스] 서울 아파트 전세값, 매매값의 70%](https://www.hani.co.kr/arti/economy/property/714189.html)** — Read aggregation method and sparse transactions. State the grouping rule and use a concrete small-sample case to explain why an apparent extreme needs care.

- **[퀀트 전략을 이용한 종목선정 (심화) — R 퀀트 쿡북](https://hyunyulhenry.github.io/quant_cookbook/%ED%80%80%ED%8A%B8-%EC%A0%84%EB%9E%B5%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%A2%85%EB%AA%A9%EC%84%A0%EC%A0%95-%EC%8B%AC%ED%99%94.html)** — Read problem, code, and explanation. Introduce the task before its code, then explain the transformation in natural Korean with a consistent register.

- **[Population structure and ageing (Eurostat Statistics Explained)](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Population_structure_and_ageing)** — Read highlights and extraction date. Pair a broad trend with important exceptions and distinguish data extraction time from the next planned update.

- **[An Intuitive Guide To Exponential Functions & e](https://betterexplained.com/articles/an-intuitive-guide-to-exponential-functions-e/)** — Read intuition and formal definition. Use a familiar structural relation to introduce a concept, then connect the intuition to its precise definition.
