# Known AI-Slop Terms

알려진 LLM 과용 / 오용 표현 리스트. **black list 아님**. 각 항목은
문맥을 다시 읽기 위한 검색 후보일 뿐이다. 도메인, 의미, 독자, 프로젝트
용례로 먼저 판정하고, 결정이 중요하거나 불확실할 때만 외부 자료를
검증한다.

## Contents

- Category 1: 일반 영어 표현
- Category 2: SW 엔지니어링 용어
- Contextual technical-term checks
- Category 3/3b: 한국어 표현과 영어 혼용
- Category 4: 단어 밖의 메타 패턴
- 검증 원칙

## Category 1: 영어 일반 LLM slop (분야 무관)

LLM 이 "지적이고 격식 있는 글" 만들려고 본인 직관으로 뿌리는 단어. 학술 / 업계 글에서는 빈도 낮음.

### Verb / 동사

- `delve` / `delves into` / `delving into`: LLM 의 가장 대표적 마커. 실제로는 "look at", "examine", "explore" 또는 그냥 동사 없이 직접 본론
- `leverage`: `use` 로 충분
- `utilize`: `use`
- `facilitate`: `help`, `enable`
- `elucidate` / `elucidating`: `explain`, `clarify`
- `delineate`: `describe`, `define`
- `transcend`: `go beyond`, `exceed`
- `traverse` (when meaning "go through"): `go through`, `walk`
- `orchestrate` (when overused for "coordinate"): `coordinate`, `run`
- `harness` (when meaning "use"): `use`
- `unpack` (when meaning "explain"): `explain`
- `dive into`: `look at`, `start`

### Noun / 명사

- `tapestry` (of X): LLM 클리셰. 그냥 단어 빼거나 "set", "mix", "collection"
- `realm` (of X): `area`, `field`, `domain`
- `landscape` (of X): `field`, `area`, `state of`
- `journey` (of X): `process`, `path`
- `cornerstone`: `core`, `key`
- `paradigm` (when not strict Kuhnian paradigm): `approach`, `way`, `model`
- `ecosystem` (when overused): `set`, `group`, `tooling`
- `framework` (when overused for "approach"): `approach`, `way`
- `nexus`: `connection`, `intersection`
- `juncture`: `point`
- `testament to`: drop entirely, or `shows`
- `paragon of`: `example of`
- `bedrock`: `foundation`, `base`

### Adjective / 형용사

- `nuanced` (overused): `subtle`, `complex`, or drop
- `intricate` / `intricately`: `complex`, `detailed`
- `multifaceted`: `complex`, `many-sided`
- `robust` (overused for "works well"): `reliable`, `stable`, `well-tested`
- `comprehensive` (overused): `complete`, `full`
- `pivotal`: `important`, `key`
- `crucial` (overused): `key`, `important`
- `profound` / `profoundly`: `deep`, `significant`
- `groundbreaking`: `new`, `novel`
- `cutting-edge`: `new`, `recent`
- `state-of-the-art`: `current best`, `recent`
- `bespoke` (overused): `custom`, `tailored`
- `seamless`: `smooth`, `simple`
- `myriad`: `many`
- `plethora of`: `many`
- `meticulous`: `careful`, `detailed`
- `holistic` (overused): `overall`, `whole-system`

### Phrase / 구문

- `furthermore` / `moreover`: `also`
- `notwithstanding`: `despite`
- `subsequently` (when meaning "then"): `then`, `after`
- `in essence`: drop, or `basically`
- `at the end of the day`: drop
- `it is worth noting`: drop, just state the fact
- `it should be noted`: drop
- `needless to say`: drop
- `in light of`: `given`, `because of`
- `in conjunction with`: `with`, `together with`
- `paradigm shift`: `change`, `new approach`
- `game-changer`: `big change`
- `low-hanging fruit`: `easy win`, `simple fix`
- `move the needle`: `make a difference`
- `boil down to`: `come down to`, `mainly about`

## Category 2: 영어 SW 엔지니어링 LLM 오용

도메인 따라 OK / NG. **확인 없이 black list 처리 금지**.

| 단어 | OK 분야 | NG 분야 (LLM 오용) |
|---|---|---|
| `surface` | 3D graphics, GIS, geology, `attack surface` (security), API surface, `Material surface` (Material Design), CSS `surface color` | 노출되거나 상호작용할 수 있는 면이 아니라 단순 "적용 범위", "메트릭 범위", "검증 범위"를 뜻할 때. `scope`, `area`, `range` 검토 |
| `contract` | smart contract, 법률/SLA, API or service compatibility contract, consumer-driven contract, data contract with producer/consumer obligations | 구체적 호환성·스키마·의무 없이 단순 interface를 거창하게 부를 때. 그 경우 `interface`, `schema`, `API`, `spec` |
| `gate` | logic gate, quality/release gate with pass-fail criteria that blocks promotion, stage-gate governance | 실패해도 아무것도 차단하지 않는 질문·문서·검토를 비유적으로 부를 때. `check`, `criterion`, `prerequisite`, `decision point` 검토 |
| `slice` | array/string slice, game vertical slice, end-to-end vertical slice, time slice | 단순한 문서 부분·작업 범위·샘플을 축이나 계층 의미 없이 부를 때. `section`, `subset`, `sample`, `scope` 검토 |
| `claim` | JWT/OIDC claim, patent or insurance claim, academic/argumentative claim that can be supported or contested | 사실·상태·요구사항·사용자 발언을 검증 가능한 주장이라는 구분 없이 일괄적으로 부를 때. `statement`, `finding`, `requirement`, `report`, 또는 직접 서술 검토 |
| `canonical` | math (canonical form), DB (canonical form / normalization), URL canonicalization (SEO), Linux distro 회사명 | "the right one", "the standard one" 의미. 그냥 `standard`, `official`, `reference` |
| `envelope` | SOAP envelope (legacy XML), flight envelope (aerospace), TCP / IP envelope (deprecated usage), 한국어 "envelope encryption" | REST API response wrapping, A2A response 구조. 그냥 `wrapper`, `response shape`, `outer object` |
| `semantic` | semantic web, semantic versioning, semantic HTML, NLP | "의미 있는" 의 일반적 의미로 형용사 남발. 그냥 `meaningful`, drop |
| `artifact` | build artifact (Maven / Gradle / GitHub Actions), git artifact, Jenkins artifact, A2A protocol Artifact (정의된 spec 용어), archaeology | 일반 "산출물" 의미로 남발. 그냥 `output`, `result`, `deliverable` |
| `boundary` | service boundary, trust boundary, security boundary (정의된 용어) | "scope" 와 혼용. 그냥 `scope` |
| `ecosystem` | software ecosystem (예: npm ecosystem) | 단순 "여러 도구" 의미. 그냥 `tooling`, `set of tools` |
| `paradigm` | programming paradigm (OOP / FP / logic), Kuhnian paradigm | 단순 "방법" 의미. 그냥 `approach`, `way`, `model` |
| `holistic` | medicine, system thinking | 단순 "전체적인". 그냥 `overall`, `whole-system` |
| `first-class` | first-class function / citizen (정의된 PL 용어) | 단순 "중요한". 그냥 `important`, `core` |
| `opinionated` | framework design 맥락 (Rails / Django) | 단순 "특정 방식 강요". 그냥 `prescriptive`, `restrictive` |
| `idiomatic` | 언어별 표준 표현 맥락 | 단순 "좋은 방식". 그냥 `standard`, `conventional` |
| `production-grade` / `production-ready` | release 상태 명시 시 | 단순 "잘 만든". 그냥 `stable`, `well-tested` |
| `enterprise-grade` | B2B SaaS / B2B 제품 맥락 | 일반 코드 품질 의미. drop |
| `battle-tested` | 오래 운영된 시스템 맥락 | 새 라이브러리에 남발 시. drop |
| `out of the box` | 즉시 사용 의미 | 일반적 OK 표현. 남발 시만 의심 |
| `under the hood` | 내부 구현 설명 시 | 일반적 OK. 남발 시만 |
| `single source of truth` (SSOT) | 데이터 정합성 맥락 | 약어 SSOT 는 OK. 풀어쓴 영문 본문에 자주 남발 |
| `single pane of glass` | observability 마케팅 buzzword | NG. 그냥 `unified dashboard` |

### Contextual technical-term checks

전문 용어가 등장했다는 사실보다 그 용어의 **성립 조건**이 문맥에 있는지
확인한다. 주변 문단이나 프로젝트에서 이미 조건을 분명히 했다면 매 문장에
되풀이할 필요는 없다.

| 용어 | 성립 조건을 확인하는 질문 | 장식적 사용 신호 |
|---|---|---|
| `contract` | 당사자는 누구이며 어떤 기대·호환성·의무를 검증하거나 집행하는가? | 단순 문서, 타입, 계획을 권위 있어 보이게 부름 |
| `gate` | 명시된 통과 조건은 무엇이며 실패하면 어떤 진행·병합·배포가 멈추는가? | 차단 효과 없는 체크리스트나 질문에 붙임 |
| `slice` | 무엇을 어떤 축으로 자르며, vertical이면 어떤 계층을 end-to-end로 관통하는가? | 단순 부분, 주제, 검토 범위에 붙임 |
| `claim` | 누가 무엇을 주장하며 무엇이 이를 지지·반박·검증할 수 있는가? 또는 governing spec의 정의된 필드인가? | 확인된 사실, 관찰, 요구사항까지 모두 `claim`으로 재분류함 |
| `boundary` | 경계 양쪽에서 책임, 신뢰, 정책, 소유권 중 무엇이 달라지는가? | `scope`의 시작과 끝을 추상적으로 다시 이름 붙임 |
| `artifact` | 어떤 도구나 절차가 무엇을 생성하며 저장·전달·추적하는가? | 모든 메모와 문서를 산출 과정과 무관하게 부름 |

빠른 대체 테스트: `requirement`, `check`, `section`, `statement`, `result`처럼
평범하고 구체적인 단어로 바꿔도 기술적 구분이 하나도 사라지지 않는다면
원래 용어는 장식일 가능성이 높다. 이 테스트만으로 자동 교체하지 말고,
governing source와 실제 문맥으로 최종 판정한다.

## Category 3: 한국어 LLM slop

영어 → 한국어 번역에서 자주 발생하는 잘못된 표현. 한국어 공식 자료 / 커뮤니티 사용 빈도 낮음.

### 명사 / 형용사

| 한국어 slop | 원어 / 추정 출처 | 권장 |
|---|---|---|
| 봉투 | envelope | SOAP envelope 류 legacy 외 NG. 그냥 영어 단어 사용 (예: "wrapper", "응답 구조") |
| 사양 | specification / spec | 자동차 / 하드웨어 spec 외 SW 에서는 NG. 그냥 "스펙" |
| 본가 | upstream | 무협지 톤. "원본 레포", "upstream" |
| 계약 | contract | API/data contract처럼 호환성·스키마·생산자/소비자 의무가 실제 개념이면 유지. 단순 interface를 추상적으로 부를 때만 "스펙", "인터페이스" 검토 |
| 정합성 | consistency / parity | DB read consistency, 데이터 integrity, 복제·캐시·스키마 consistency처럼 구분이 실제로 중요하면 유지. 단순 비교 결과면 "일치", "diff 없음"이 더 구체적인지 검토 |
| 동일성 | identity / sameness | 한자어 추상화. 그냥 "같음" |
| 추상화 (남발 시) | abstraction | 진짜 추상화 개념 아니면 drop |
| 단일성 | singleness | 그냥 "하나임" |
| 가용성 (남발 시) | availability | SLA 맥락 외 drop |

### 술어

| 한국어 slop | 권장 |
|---|---|
| ...하는 것이 ...의 목표입니다 | ...해야 합니다 / ...입니다 |
| ...하는 것이 본 작업의 의도입니다 | ...하려는 작업입니다 |
| ...라는 점을 보장합니다 | ...합니다 (단정형) |
| ...를 담보합니다 | ...합니다 |
| ...점을 담보 / 보장 합니다 | ...합니다 |
| ...의 결정적 요소입니다 | ...에 큰 영향을 줍니다 |
| ...의 핵심 의의입니다 | ...의 핵심입니다 / 그냥 drop |
| ...의 핵심 근거입니다 | ...의 근거입니다 |

### 자기 지칭 ("본 X" 패턴, 다양한 변형 다 잡아야 함)

| 한국어 slop | 권장 |
|---|---|
| 본 PR | 이번 PR / 그냥 drop |
| 본 레포 | 이 레포 / 이번 레포 |
| 본 sub-agent | 이 sub-agent / 그냥 drop |
| 본 시스템 | 이 시스템 / 그냥 drop |
| 본 작업 | 이번 작업 / 그냥 drop |
| 본 문서 | 이 문서 |
| 본 정책 | 이 정책 |
| 본 표 | 이 표 |
| 본 작성자 | 이 작성자 / 작성자 (1 명) / drop |
| 본 모듈 | 이 모듈 |
| 본 스킬 / 본 skill | 이 스킬 |
| 본 글 | 이 글 |
| 본 정합성 검증 | drop (전체 문구 slop) |

검증 grep (모든 변형 한 번에):

```bash
grep -nE '본 (PR|레포|sub-agent|시스템|모듈|작업|문서|정책|스킬|skill|표|작성자|글)' file.md
```

### 추상 명사화 (영어 → 한국어 직역)

| 한국어 slop | 권장 |
|---|---|
| X 사이클 (예: 정합성 검증 사이클) | "X 작업", "X 시점", "X 중에" |
| X 프로세스 (남발 시) | "X 작업", "X 단계" |
| X 라운드 | "X 차", "X 번째" |
| 정합성 검증 사이클 | "비교 작업", "diff 확인" |

### Punctuation (프로젝트 글쓰기 가이드가 있으면 cross-reference)

- em-dash `—`
- middle-dot `·`
- bullet char `•`
- 슬래시 `/` 로 명사 2 개 이상 묶음 (코드 식별자 안 슬래시 / URL / MIME type 예외)
- bullet item 끝에 ` - ` 종속절

## Category 3b: 영어 informal 단어 + 한국어 동사 mix slop

LLM 이 한국어 글 안에 informal 영어 형용사 / 명사를 박고 한국어 동사로 연결하는 패턴. 표준 IT hyphen 표현 (예: single-line JSON, request-scoped state, in-memory hold, caller-side, graceful degradation, blind spot, cardinality) 과 구분되어야 함.

| Slop (mix) | 권장 (자연 한국어) |
|---|---|
| honest 하게 / honest 채움 | 정직하게 / 사실대로 / 정확히 |
| wired 상태 / wired up | 연결된 상태 / 설정된 상태 / 적재되는 상태 |
| framing / 방어 framing | 응답 문구 / 응답 논리 |
| 단계 ramp / ramp 없음 | 단계 도입 / 점진적 도입 |
| 격하게 push 함 | 강하게 push 함 / 강하게 밀어붙임 |
| seamless 하게 | 부드럽게 / 매끄럽게 / drop |
| robust 하게 | 안정적으로 / 검증된 |
| holistic 하게 | 전체적으로 |
| nuanced 하게 | 세밀하게 / 미묘하게 |

판정 원칙:

1. 그 영어 단어가 **IT 표준 hyphen 표현** 또는 **정식 type 명** 인가 → keep (예: `single-line JSON`, `caller-side`, `request-scoped`, `ArtifactMetadata`)
2. 그 영어 단어가 **일반 informal 영어 형용사 / 동사** 인가 → 한국어로 풀어쓰기 (예: honest, wired, robust, seamless, holistic)
3. 그 영어 단어가 **conceptual term 표준** 인가 (CADI / RADAR / A2A / RED / USE / OTel 등) → keep

## Category 4: AI slop 의 메타 패턴

단어가 아닌 패턴:

- 표 / bullet / 산문 한 섹션에 다 들어있음 (산문이 3 문장 이상)
- 같은 결론을 TL;DR / 본문 / 결론 3 번 반복
- "X 라는 점에서 Y 한 측면에서 Z 라는 것은 ..." 식 종속절 3 단 이상
- 모든 문장이 동일 길이 (LLM 의 rhythm)
- 한 섹션이 200 자 이상 산문 + 표 + bullet 다 들어간 케이스

이건 단어 검증과 별개로 프로젝트 간결성 가이드나 humanization skill 로.

## 검증 원칙

- 위 리스트는 **black list 아닌 watch list**. 도메인, 의미, 독자,
  governing source, 실제 용례를 필요한 만큼 확인한다.
- 직관만으로 전문 용어를 단정하지 않는다. 정의된 이름, 논쟁적 표현,
  최신 용례처럼 외부 근거가 결론을 바꿀 때 web research를 사용한다.
- 분야가 문서와 레포에서 분명하면 그 근거로 진행한다. 불확실성이
  교체 의미를 바꿀 때만 사용자에게 확인한다.
