# Replacement Patterns

자주 등장하는 AI slop → 표준 표현 매핑. 이 매핑은 1 차 출발점일 뿐이며, 실제 도메인 + 검증 결과로 최종 결정한다.

## Contents

- 영어 SW 엔지니어링 분야
- 영어 일반 표현
- 영어와 한국어 혼용
- 한국어 표현
- Cross-domain 단어
- 적용 시 주의

## 영어 SW 엔지니어링 분야

### 메트릭 / observability / 인프라

| Slop | 권장 |
|---|---|
| "metric surface" / "instrumentation surface" | 공개된 metric names, labels, query/API entry points의 구체적 집합을 정의했다면 유지 가능. OpenTelemetry의 telemetry source grouping이면 `instrumentation scope`; 방출·검토 대상이면 metrics, metric set, coverage |
| "the surface of X" | 외부에서 관찰·호출·설정할 수 있는 요소의 집합이면 유지. 단순 적용 범위면 the scope of X, the area covered |
| "applied surface" | applied scope, where X applies |
| "blind spot surface" | 기하·모델링 의미가 없다면 blind spots, gaps in coverage |
| "attack surface" | (그대로 OK, security 정식 표현) |
| "API surface" / "public API surface area" | (공개된 operations, types, flags, configuration, observable behavior의 집합이나 상대적 범위를 뜻하면 그대로 OK) |
| "configuration surface" / "public surface" | 실제 options나 touchpoints를 가리키면 유지. 막연한 범위면 configuration options, public API, user-facing features |
| "API contract" | 호환성 약속, versioning, consumer expectation을 뜻하면 유지. 단순 구조만 뜻하면 API, interface, schema, request/response shape |
| "data contract" | producer/consumer 사이 schema, 품질, versioning 의무를 뜻하면 유지. 단순 파일 형식이면 schema, data shape, format |
| "Pact contract" / "consumer-driven contract" | (그대로 OK, contract testing 정식 용어) |
| "smart contract" (blockchain) | (그대로 OK) |
| "implementation brief is the contract" | 실제 승인·의무·호환성 기준이면 유지. 아니면 requirements, specification, agreed plan |
| "quality gate" / "release gate" | 명시된 조건 실패가 다음 단계나 배포를 차단하면 유지. 아니면 check, review criterion, prerequisite |
| "knowledge gate" / "context gate" | 보통 prerequisite, required context, decision point; 실제 pass/fail 차단 규칙이 있으면 예외 |
| "vertical slice" | 게임의 주요 시스템·아트가 반영된 작은 playable section 또는 여러 계층을 관통하는 end-to-end 구현이면 유지 |
| "documentation slice" / "review slice" | section, subset, sample, review scope |
| "JWT claim" / "OIDC claim" | (governing specification의 정의된 name/value 의미이므로 유지) |
| "research claim" / "argument claim" | 근거로 지지하거나 반박할 수 있는 명제이면 유지 |
| "readiness claim" / "done claim" | 완료·준비 상태를 누군가 주장하고 검증하는 문맥이면 유지. 확인된 상태면 readiness status, completion status 또는 직접 서술 |
| 모든 발언·요구사항·관찰을 `claim`으로 부름 | statement, requirement, observation, finding, report 중 실제 역할을 쓰거나 직접 서술 |
| "canonical form" (math, DB) | (그대로 OK) |
| "canonical implementation" (the right one 의미) | reference implementation, standard implementation |
| "canonical version" | standard version, official version |
| "SOAP envelope" (legacy XML) | (그대로 OK) |
| "response envelope" (REST) | response wrapper, response shape |
| "envelope encryption" (cloud KMS) | (그대로 OK) |
| "service boundary" (DDD / microservice 정식 용어) | (그대로 OK) |
| "trust boundary" (security 정식) | (그대로 OK) |
| "scope boundary" (의미 모호) | scope, area |
| "RED / USE boundary" (위 두 method 의 책임 분리) | (그대로 OK) |

### 일반 코드 / 시스템

| Slop | 권장 |
|---|---|
| "leverage X" | use X |
| "utilize X" | use X |
| "facilitate" | help, enable, support |
| "orchestrate" (overused) | coordinate, run, schedule |
| "harness" (when "use") | use |
| "robust system" | reliable system, well-tested system |
| "comprehensive solution" | complete solution, full coverage |
| "holistic approach" | overall approach, whole-system view |
| "first-class citizen" (정식 PL 용어) | (그대로 OK) |
| "first-class support" (overused for "important") | core support, full support |
| "production-grade" (release 의미 명확하면 OK) | stable, release-ready |
| "battle-tested" | well-tested, mature |
| "enterprise-grade" | scaled, large-deployment-ready |
| "cutting-edge" | new, recent |
| "state-of-the-art" | current best (학술 정식 표현 OK), recent |
| "next-generation" | new, next, replacement |
| "single source of truth" (SSOT 약어 OK) | (그대로 OK 약어로) |
| "single pane of glass" | unified view, one dashboard |

### Architecture / 디자인

| Slop | 권장 |
|---|---|
| "paradigm" (overused) | approach, way, model |
| "paradigm shift" | change, new approach |
| "ecosystem" (overused) | tooling, set of tools |
| "framework" (when "approach") | approach, way |
| "abstraction" (overused) | (그대로 OK if real abstraction) |
| "layer" (overused) | (그대로 OK if real layer) |
| "concern" (overused) | responsibility, task |
| "primitive" (overused) | basic unit, building block |
| "modal" (when not UI modal) | (의미 모호. context 확인) |
| "idiomatic" (정식 PL 용어 OK) | (그대로 OK in language context) |
| "opinionated" (framework 정식 OK) | (그대로 OK in framework context) |

## 영어 일반 LLM slop

### 부사 / 형용사 (drop 권장)

대부분 그냥 drop. 글에서 빼도 의미 동일.

| Slop | 권장 |
|---|---|
| nuanced | (drop) or subtle, complex |
| intricate / intricately | complex, detailed |
| multifaceted | complex, many-sided |
| pivotal | important, key |
| crucial (overused) | key, important |
| profound | deep, significant |
| seamless | smooth, simple |
| meticulous | careful, detailed |
| bespoke | custom, tailored |
| myriad | many |
| plethora of | many |
| groundbreaking | new, novel |

### 동사 (rewrite)

| Slop | 권장 |
|---|---|
| delve into | look at, examine, explore |
| delve | drop, replace with concrete verb |
| traverse (when "go through") | go through |
| elucidate | explain, clarify |
| delineate | describe, define |
| transcend | go beyond, exceed |
| unpack (when "explain") | explain |

### 명사 / 클리셰

| Slop | 권장 |
|---|---|
| tapestry (of X) | (drop) or set, mix, collection |
| realm (of X) | area, field, domain |
| landscape (of X) | field, area, state of |
| journey | process, path |
| cornerstone | core, key |
| bedrock | foundation, base |
| nexus | connection, intersection |
| juncture | point |
| testament to | (drop), or shows |

### 구문

| Slop | 권장 |
|---|---|
| furthermore | also |
| moreover | also |
| notwithstanding | despite |
| subsequently (when "then") | then, after |
| in essence | (drop) or basically |
| in light of | given, because of |
| in conjunction with | with, together with |
| at the end of the day | (drop) |
| it is worth noting | (drop): just state the fact |
| it should be noted | (drop) |
| needless to say | (drop) |
| paradigm shift | change |
| game-changer | big change |
| low-hanging fruit | easy win, simple fix |
| move the needle | make a difference |
| boil down to | come down to, mainly about |

## 영어 + 한국어 mix slop

LLM 이 한국어 글 안에 informal 영어 단어를 박고 한국어 동사 / 명사로 mix 한 패턴. 표준 IT hyphen 표현과 구분.

| Slop (mix) | 권장 | 비고 |
|---|---|---|
| honest 채움 / honest 하게 | 정직하게 / 사실대로 / 정확히 | 영어 "honest" 형용사가 한국어 동사 mix 로 등장하면 slop |
| wired 상태 / wired up | 연결된 상태 / 설정된 상태 / 적재되는 상태 | informal 영어 |
| 방어 framing / framing | 응답 문구 / 응답 논리 | "framing" 자체 적합한 한국어 풀이 |
| 단계 ramp / ramp 없음 | 단계 도입 / 점진적 도입 | "ramp" 단어 자체 OK 하지만 "단계 ramp" 같은 mix 는 slop |
| seamless 하게 | 부드럽게 / 매끄럽게 / drop | LLM slop 형용사 |
| robust 하게 | 안정적으로 / 검증된 / 잘 동작하는 | LLM slop |
| holistic 하게 | 전체적으로 / 시스템 전체로 | LLM slop |
| nuanced 하게 | 세밀하게 / 미묘하게 | LLM slop |

**Keep (표준 IT hyphen 표현)**: 한국어 글에 자연:
- `single-line JSON`, `request-scoped state`, `in-memory hold`, `caller-side observation`
- `graceful degradation`, `blind spot`, `cardinality`, `livesum`, `multiprocess mode`
- `staging dry run`, `local E2E`, `cross-check`, `consumer-driven contract`
- `ArtifactMetadata`, `DataPart`, `AgentCard`, `Skill`, `Task`, `Artifact` (A2A 정식 type 명)
- `RED method`, `USE method`, `Golden Signals` (SRE 정식)

## 한국어 LLM slop

### 자기 지칭 (가장 흔함, "본 X" 다양한 변형)

| Slop | 권장 |
|---|---|
| 본 PR | 이번 PR / drop |
| 본 레포 | 이 레포 |
| 본 sub-agent | 이 sub-agent / drop |
| 본 시스템 | 이 시스템 / drop |
| 본 작업 | 이번 작업 / drop |
| 본 문서 | 이 문서 |
| 본 정책 | 이 정책 |
| 본 표 | 이 표 |
| 본 작성자 | 이 작성자 / 작성자 (1 명) / drop |
| 본 모듈 | 이 모듈 |
| 본 스킬 / 본 skill | 이 스킬 |
| 본 글 | 이 글 |
| 본 정합성 검증 | drop entire phrase |

검증 grep (모든 변형 한 번에):

```bash
grep -nE '본 (PR|레포|sub-agent|시스템|모듈|작업|문서|정책|스킬|skill|표|작성자|글)' file.md
```

### 격식 술어

| Slop | 권장 |
|---|---|
| ...하는 것이 ...의 목표입니다 | ...해야 합니다 / ...입니다 |
| ...하는 것이 본 작업의 의도입니다 | ...하려는 작업입니다 |
| ...라는 점을 보장합니다 | ...합니다 (단정형) |
| ...를 담보합니다 | ...합니다 |
| ...점을 담보 / 보장 합니다 | ...합니다 |
| ...의 결정적 요소입니다 | ...에 큰 영향을 줍니다 |
| ...의 핵심 의의입니다 | ...의 핵심입니다 / drop |
| ...의 핵심 근거입니다 | ...의 근거입니다 |

### 한자어 추상 명사

| Slop | 권장 |
|---|---|
| 봉투 | (영어 그대로 OR 풀어쓰기) |
| 사양 (SW) | 스펙 |
| 본가 | 원본 레포, upstream |
| 계약 (API/data 의미) | 호환성·schema·producer/consumer 의무가 실제 개념이면 유지. 단순 interface면 스펙, 인터페이스 |
| 정합성 | DB/복제/캐시/데이터 consistency 속성이면 유지. 단순 결과 비교면 일치, 같음 |
| 정합성 검증 | consistency 속성을 검증하면 유지. 파일·문서 비교면 비교, diff 확인 |
| 정합성 회복 | 분산 상태의 consistency 복구면 유지. 단순 동기화 결과면 다시 일치시킴 |
| 동일성 | 같음 |
| 동일성을 담보 | 같습니다 / 일치합니다 |
| 동등성 | 같음 |
| 단일성 | 하나임 |
| 일관성 확보 | 일관됩니다 |
| 책임 영역 | 담당 영역, 책임 |
| X 사이클 | X 작업, X 시점, X 중에 |
| X 라운드 | X 차, X 번째 |
| X 프로세스 (overused) | X 작업, X 단계 |

### 명사화 (-화 / -성 / -적)

LLM 은 "-화" / "-성" / "-적" 접미사 남발. 대부분 동사형이 자연.

| Slop | 권장 |
|---|---|
| 메트릭화 (메트릭으로 만듦) | 메트릭으로 만들다 / 메트릭으로 export |
| 추상화 (overused) | 추상적으로 만들다 / drop |
| 모듈화 (overused) | 모듈로 분리 |
| 자동화 (overused) | 자동으로 만들다 / 자동 |
| 적극적 | 적극적으로 / 강하게 |
| 능동적 | 능동적으로 |
| 인지적 | 인지의 |

## Cross-domain 단어 (도메인 따라 OK / NG)

다음 단어들은 도메인 확인 필수:

| 단어 | OK 도메인 | NG 도메인 |
|---|---|---|
| surface | physical/math/modeling / rendering and UI / security / concrete API, public, or configuration touchpoints | 포함 집합·상대·결과가 없는 즉석 `scope`, `set`, `aspect` 대용어 |
| contract | blockchain / Pact / 법률 / SLA / API·service compatibility / producer-consumer data contract | 구체적 의무 없이 단순 interface를 추상적으로 부를 때 |
| gate | digital logic / CI quality gate / release or governance gate with blocking criteria | 차단 효과 없는 질문, 문서, 검토 |
| slice | array/string operations / game vertical slice / end-to-end software slice / scheduler time slice | 단순 문서 부분, 주제, 작업 범위 |
| claim | JWT/OIDC / patent / insurance / academic argument / disputed assertion | 확인된 사실, 관찰, 상태, 요구사항을 일괄 재분류할 때 |
| canonical | math / DB normalization / URL canonical (SEO) | 일반 SW (그 standard 의미) |
| envelope | SOAP / aerospace / cloud KMS encryption | REST API wrapping |
| artifact | build / git / Maven / A2A spec | 일반 산출물 |
| boundary | service boundary (DDD) / trust boundary | 일반 scope 의미 |
| paradigm | OOP / FP / Kuhnian | 일반 approach 의미 |
| holistic | medicine / system thinking | 일반 overall 의미 |
| primitive | crypto / PL type | 일반 basic 의미 |
| concern | aspect / separation of concerns | 일반 issue 의미 |

이 표 단어가 본문에 등장하면 먼저 문맥과 governing source를 확인한다.
판정이 중요하거나 불확실한 경우에만 위험도에 맞춰 외부 근거를
확인한다.

## 적용 시 주의

1. **사용자 의도 보존**. 의미가 바뀌는 교체 금지
2. **분야 정통 표현으로 교체**. 다른 분야 표현으로 가는 거 금지 (예: 머신러닝 글에 갑자기 networking 표현)
3. **자연스러운 한국어 / 영어 흐름 유지**. 단어 1 개 바꿔서 문장 어색해지면 문장 전체 재작성
4. **약어는 그대로** (PR, API, JSON, URL, CSS, HTML 등)
5. **코드 식별자 / 변수명 / 함수명 / 외부 라이브러리 명칭은 교체 X**
