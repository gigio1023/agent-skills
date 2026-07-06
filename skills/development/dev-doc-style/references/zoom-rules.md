# 줌 레벨별 상세 룰

5 줌 레벨 (sentence / bullet / section / page / cross-page) 룰과 Bad/Good 예시.

근거 출처:
- langchain-ai/docs `AGENTS.md` (em-dash 룰, key-features 리스트 금지, sentence-case 헤딩, 명령형 현재형)
- pydantic/pydantic `docs/concepts/*.md` (admonition 분리, bullet shape, 도입문 ≤ 1 문장)

---

## 1. Sentence — 한 문장 = 한 사실

한 문장은 사실 한 개로 끝낸다. 단서 / 출처 / 예외가 추가로 붙어야 하면 다음 문장으로 쪼갠다.

### Rule

- em-dash 한 문장 1 개 이하. 2 개 이상이면 마침표로 끊는다.
- 본문에 출처 라벨 (`(Wiki §x.y)`, `(boilerplate 컨벤션)`, `— Wiki §7.1`) 박지 않는다.
- 단서 표현 ("옵션입니다", "가능합니다", "권장합니다", "할 수 있습니다") 의 절반은 빼도 의미 그대로다.
- 명령형 현재형 우선. "할 수 있습니다" → "합니다".

### Bad / Good

```markdown
# Bad — 한 줄에 사실 + 단서 + 출처 두 개 = 4 메시지
- **Bearer 인증** (옵션) — boilerplate 가 표준화, Wiki 는 일반 슬롯

# Good — 본문은 한 사실, 단서 / 출처는 admonition
- **Bearer 인증**: 환경 변수로 활성화합니다.

> [!NOTE]
> Wiki 스펙은 인증을 일반 슬롯으로 둡니다. 본 레포가 표준 형식을 정의합니다 — [spec mapping](spec-mapping.md).
```

```markdown
# Bad — em-dash 두 번 + 옵션 단서
이 어댑터는 — 환경 변수로 끄거나 — 직접 인스턴스를 주입하여, 로깅 동작을 바꿀 수도 있습니다.

# Good — 두 문장으로 쪼갬
환경 변수로 어댑터를 끕니다. 또는 인스턴스를 직접 주입해 동작을 바꿉니다.
```

---

## 2. Bullet — Form A / B / C

bullet 한 줄은 셋 중 하나로 통일.

### Rule

- **Form A**: `**라벨**: 한 문장.` (선택적 See 링크)
- **Form B**: 완결된 한 문장.
- **Form C**: `**라벨**:` + nested 1 단 list. 라벨 아래 동등 무게 항목이 4 개 이상이고 comma 합치기보다 풀어 쓰는 게 readable 할 때.
- 한 bullet 안에 메시지 ≥ 3 개면 잘못 쓴 것이다. 별도 단락 또는 admonition. 단, 라벨 아래 동등 무게 항목 묶음이면 Form C 로 풀어 쓰는 게 정답.
- nested bullet 1 단계 max. 2 단계가 필요하면 섹션을 쪼갠다.
- "Key features 7 개" hype 리스트 금지 (langchain-ai/docs `AGENTS.md:210` 명시).

### 선택 가이드

- 한 사실 + 한 정의: Form A
- 한 완결 사실: Form B
- 동등 무게 항목 4 개 이상 (예: "보일러플레이트가 자동 처리 / 직접 채울 영역" 같은 enumeration): Form C
- 항목 2–3 개고 한 줄에 자연스럽게 들어가면 comma 산문 OK

### Nested vs inline 판정 (핵심 휴리스틱)

라벨 뒤 정의를 인라인으로 두느냐 nested bullet 으로 풀어 쓰느냐의 기준.

| 라벨 뒤 sub-fact 수 | 권장 |
|---|---|
| 1 개 (한 줄 정의) | Form A 인라인 — `**라벨**: 정의.` |
| 2 개 이상 (구별되는 sub-fact) | Form C nested — `**라벨**:` + nested 1 단 |
| 4 개 이상 + 동등 무게 | Form C nested 강제 (comma 합치기 금지) |

판정 기준 한 줄: **"sub-fact 가 2 개 이상 = nest. 1 개면 inline."**

#### Bad — sub-fact 여러 개를 inline 에 우겨넣음

```markdown
- **운영 로그**: `audit_log.py` 의 `TaskAuditEntry` 스키마, 식별 필드 (task_id, context_id, skill), 메트릭 필드 (latency_ms, input_tokens, output_tokens), 어댑터는 `StdoutAuditLogAdapter` 가 기본
```

문제: 한 줄에 스키마 / 식별 / 메트릭 / 어댑터 4 개 sub-fact 가 comma 로 묶여 스캔 불가.

#### Good — Form A (sub-fact 1 개로 압축, 나머지는 See 링크)

```markdown
- **운영 로그**: `TaskAuditEntry` 스키마를 사용합니다. 필드 정의는 [audit_log](audit_log.md).
```

#### Good — Form C (sub-fact 모두 nested 로 풀기)

```markdown
- **운영 로그**:
    - 스키마: `TaskAuditEntry`
    - 기본 어댑터: `StdoutAuditLogAdapter`
    - 식별 / 메트릭 필드 정의: [audit_log](audit_log.md)
```

선택은 sub-fact 의 무게에 따라. 모두 page 자기 토픽이면 Form C, 보조 정보면 Form A + See 링크.

### Form A — 라벨 + 정의

```markdown
- **운영 로그**: `TaskAuditEntry` 스키마를 사용합니다. [audit_log](audit_log.md) 참조.
- **자체 trace span**: `telemetry.py` 가 OTel SDK 를 셋업합니다.
- **비즈니스 메트릭**: `telemetry.py` 가 Prometheus exposition 포트를 셋업합니다.
```

### Form B — 완결된 한 문장

```markdown
- 환경 변수 `OTEL_EXPORTER_ENDPOINT` 설정 시 OTel SDK 가 초기화됩니다.
- `OTEL_PROMETHEUS_PORT` (기본 9464) 의 `/metrics` 가 노출됩니다.
- LLM 호출 없는 step 은 `model_info` 가 null 이 됩니다.
```

### Form C — 라벨 + nested 1 단

라벨 아래 동등 무게 항목이 4 개 이상이고 comma 합치기보다 풀어 쓰는 게 가독성 우수할 때 사용.

```markdown
- **자동 처리**:
    - FastAPI + a2a-sdk `/a2a` mount
    - Agent Card `/.well-known/agent.json`, `/__health`
    - SemVer 와 Skill ID prefix 검증
    - OTel + Prometheus SDK 셋업
- **직접 채울 영역**:
    - `schema.py` 의 input / output 모델
    - `tools.py` 의 skill 함수 시그니처
    - `agent.py` 의 LLM instruction
```

Bad 패턴 (같은 정보를 comma 로 합치기):

```markdown
- **자동 처리**: FastAPI, Agent Card, /__health, SemVer 검증, OTel SDK 셋업.
```

### Bad

```markdown
# Bad — 라벨 + em-dash + 위치 + 구성 요소 + 동사 = 4 메시지
- **운영 로그** — `audit_log.py` 의 `TaskAuditEntry` 스키마와 어댑터 활용

# Bad — nested 2 단계 + 단서 분기 (2 단은 금지)
- **스키마** — `audit_log.py` 의 `TaskAuditEntry` (SOAP 조직 표준)
  - 식별: `task_id`, `context_id`, `skill`, `producer_version`, `status`
  - 메트릭: `quality_score`, `latency_ms`, `input_tokens`, `output_tokens`, `error`

# Good — Form A 적용 (nested 1 단으로 충분치 않으면 See 링크로 떠넘김)
- **스키마**: `TaskAuditEntry`. 식별 / 메트릭 필드 정의는 [audit_log](audit_log.md).
```

---

## 3. Section — 도입문 ≤ 1 문장

섹션 = 한 문장 컨텍스트 → 코드 / 표 / 스텝.

### Rule

- 도입 단락 1 개 이상 + 정책 인용구 + 우선순위 라벨링 + 외부 링크 4 단 패턴 금지.
- 메시지 유형별 표면 분리 (본문 / `> [!NOTE]` / `> [!WARNING]` / `> [!TIP]` / `<details>`).
- 정책 / 일정 / 우선순위는 본문에 두지 않는다 — 별도 페이지 (`docs/migration/schedule.md`) 한 곳.

### Bad

```markdown
## Observability (sub-agent 결정 영역)

Sub-agent 운영을 위한 로그 / 트레이스 / 메트릭은 sub-agent 가 자유롭게 결정합니다. 본 레포는 SDK 셋업과 어댑터 template 까지만 제공합니다.

> **5 월 중순까지는 로그가 어떤 형태로든 남기만 하면 됩니다.**

우선순위와 권장 사항: [docs/migration/schedule.md](docs/migration/schedule.md) 5.2 절.

### Logging (1 순위)
- ...
### Trace (후순위)
- ...
### Metrics (후순위)
- ...
```

문제:
- 도입문이 두 문장 (sub-agent 결정 / 본 레포 제공 범위)
- 정책 인용구 (`5 월 중순까지...`) 가 본문에
- 외부 링크 (`schedule.md 5.2 절`) 가 도입에
- 우선순위 라벨 (`(1 순위)`, `(후순위)`) 이 헤딩에 박힘

### Good

```markdown
## Observability

Sub-agent 가 결정합니다. 본 레포는 SDK 셋업과 어댑터 template 만 제공합니다.

### Logging
- **스키마**: `TaskAuditEntry`. [audit_log](docs/audit-log.md) 참조.
- **어댑터**: `StdoutAuditLogAdapter` 가 기본입니다.

### Trace
- `OTEL_EXPORTER_ENDPOINT` 설정 시 OTel SDK 가 초기화됩니다.

### Metrics
- `OTEL_PROMETHEUS_PORT` (기본 9464) 의 `/metrics` 가 노출됩니다.

> [!NOTE]
> 우선순위 / 마감은 [migration/schedule.md](docs/migration/schedule.md) 한 곳에서 관리합니다.
```

---

## 4. Page — 한 페이지 한 토픽

한 페이지에 두 토픽 섞지 않는다.

### Rule

- 한 페이지 = 한 토픽 (한 작업 가이드 / 한 개념 / 한 reference).
- 페이지 끝에 `## Notes`, `## More docs`, `## References`, `## 관련 문서`, `## 더 보기` 메타 섹션 만들지 않는다.
- 인덱스는 단일 `docs/index.md` 한 곳에서만.
- README 는 quick start + 인덱스 역할. 토픽 본문은 `docs/*.md`.

### 페이지 구조 템플릿

```markdown
---
frontmatter (필요 시)
---

[한 문장 컨텍스트 또는 한 문단 정의]

## [작업 섹션 1]
[한 문장] → 코드 / 표

## [작업 섹션 2]
...

(끝 — 메타 섹션 없음)
```

### Bad — 한 페이지에 quickstart + conformance + migration + observability + notes

본 레포 README (현재 206 줄) 가 그 예. quick start, build paths, conformance requirements 5 항목, migration 일정, observability 까지 다 담고 끝에 Notes / More docs / References 메타 섹션 3 개.

### Good — 한 페이지 한 토픽

```
README.md (~80 줄)
├── Quick start (skill 설치 → clone → 확인)
├── Build paths (ADK vs Raw A2A 표 + 링크)
└── Where to look next (단일 인덱스 링크)

docs/conformance.md  — 5 항목 단일 source
docs/migration/      — 일정 / 담당자 / 사전 작업
docs/observability.md — Logging / Trace / Metrics
```

---

## 4-bis. Cross-doc reference — bare path / URL 금지

다른 문서를 가리킬 때는 `[설명적 링크 텍스트](경로)` 한 단위로 적거나, 아예 적지 않는다.
독자는 bare path 를 클릭하지 않고 (그것이 뭔지 모르므로) 문서를 읽지 않는다.

### Rule

- **Bad (bare path)**: 본문 산문에 ``` `docs/spec/foo.md` ``` 만 떨어뜨려 두기. 자세한 정보가 거기 있다는 단서가 없다.
- **Bad (raw URL)**: `https://internal.example.com/spaces/...` 만 본문에 두기. 이 위키가 무엇인지 독자가 알 수 없다.
- **Good (descriptive link)**: `[SOAP 인터페이스 스펙 (Wiki)](https://internal.example.com/...)`, `[ArtifactMetadata 정의 (docs/spec/artifact-metadata.md)](docs/spec/artifact-metadata.md)`. 링크 텍스트가 내용을 알려준다.
- **Good (omit)**: 본문 흐름에서 출처가 결정적이지 않으면 그냥 빼고 본문 사실만 둔다. 출처는 문서 인덱스 (`docs/index.md`) 한 곳에 모은다.
- 한 문장 안에 링크 3 개 이상 = bullet 으로 풀어 쓰기 (Anti-pattern §7 참조).

### Bad / Good

```markdown
# Bad — bare path
본 레포의 의도는 docs/spec/foo.md 에 있습니다.

# Bad — raw URL
참고: https://internal.example.com/docs/example-spec

# Good — descriptive link
본 레포의 의도는 [SOAP 스펙 정합성 가이드 (docs/spec/foo.md)](docs/spec/foo.md) 에 있습니다.

# Good — omit (본문에 사실만)
본 레포는 SOAP 스펙 정합성을 강제합니다.
```

### 판정 기준

- 링크 텍스트가 "여기" / "링크" / 파일 경로 자체 / URL 자체이면 깬다.
- 링크 텍스트가 "무엇 (어디 / 어떤 종류)" 정보를 담으면 통과.
- 출처를 적을 가치가 있는지 헷갈리면, 본문에서 빼고 인덱스 (`docs/index.md`) 한 곳에만 둔다.

---

## 5. Cross-page — 같은 사실은 한 곳에만

self-containment 포기. 한 사실 = 한 페이지에만 둔다.

### Rule

- 같은 표 / 리스트 / 정의가 두 페이지에 있으면 한 곳을 링크로 바꾼다.
- 첫 언급에만 reference 링크. 페이지 후반 같은 클래스명에 다시 링크 안 단다.
- "이 문서만 보면 모름" 을 받아들인다.

### Bad

본 레포 conformance 5 항목이 세 곳에 거의 동일한 형태로 등장:
- `README.md` § Conformance requirements
- `docs/spec.md` § SOAP 인터페이스 층 — 다섯 가지 conformance requirements
- `docs/conformance.md` § PR 리뷰 체크리스트

### Good

```markdown
# README.md (요약 + 링크)
## Conformance requirements
5 가지 인터페이스 스펙을 지킵니다. 자세한 사항은 [docs/conformance.md](docs/conformance.md).

# docs/conformance.md (단일 source)
## 5 가지 인터페이스 스펙
1. Agent Card 노출
2. Skill ID 형식
3. DataPart 메타데이터 필드
4. SemVer 버전
5. 인증 / 헬스 / 메트릭

# docs/spec.md (필요 시 링크만)
[conformance requirements](conformance.md) 의 다섯 항목을 ...
```

---

## 6. Code — Code-first, prose-as-label

코드가 prose 보다 먼저 또는 동시. prose 는 한 문장 셋업 후 곧장 코드.

### Rule

- 한 문장 컨텍스트 → 코드 → 1–3 문장 주석.
- 도입 단락 (왜 / 무엇 / 어디 / 어떻게) 4 단 패턴 금지.
- 코드 결과는 `#>` / `"""` 로 인라인. "다음을 실행하면 다음과 같이 출력됩니다" 줄글 금지.
- 긴 출력 / 긴 예시는 `<details>` 로 접기.

### Bad

```markdown
# Bad — 코드 전 도입 단락 + 코드 후 줄글 설명
컨테이너 환경에서는 OTLP 프로토콜로 trace 를 export 하는 것이 일반적입니다. 본 레포는 OTel SDK 를 자동으로 셋업하므로 환경 변수 한 줄로 충분합니다. 다음 변수를 설정하면 됩니다.

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
```

위 명령을 실행하면 OTel SDK 가 자동 초기화되어 모든 span 이 collector 로 전송됩니다.
```

### Good

```markdown
환경 변수 한 줄로 trace export 를 활성화합니다.

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
```

OTel SDK 가 자동 초기화됩니다.
```

### 결과 인라인 패턴

````markdown
```python
print(repr(m.timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
```
````

여러 줄 결과:

````markdown
```python
print(m)
"""
id=1
name='Alice'
created_at=datetime.datetime(...)
"""
```
````

긴 출력:

```markdown
<details>
<summary>전체 출력</summary>

```
... (긴 출력) ...
```

</details>
```

---

## 7. Voice / 어투

### Rule

- 명령형 현재형. "Run the following command." → "다음 명령을 실행합니다."
- 헤딩은 동사형 또는 명사형 한 가지로 통일. 혼용 금지.
- 한국어 / 영어 mix:
  - 기술 용어 (FastAPI, Bearer, Skill ID) 는 영어.
  - 조사 / 연결어만 한국어. "Bearer 인증을 활성화합니다."
  - 문장이 길어지면 한국어로 풀어 쓴다.
- 단서 약화 표현 (`-할 수도 있고`, `-필요하다면`, `-상황에 따라`, `-옵션입니다`) 의 절반은 의미 손상 없이 삭제 가능.

### Bad / Good

```markdown
# Bad — 단서 약화 + 가능형
필요하다면 OTLP endpoint 를 설정할 수도 있습니다. 상황에 따라 환경 변수로 끌 수도 있고, 직접 인스턴스를 주입할 수도 있습니다.

# Good — 명령형 + 두 문장 분리
OTLP endpoint 를 설정합니다. 또는 환경 변수로 끄거나 인스턴스를 주입합니다.
```
