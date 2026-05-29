# Anti-patterns 와 변환 사례

본 레포에서 즉시 제거해야 하는 패턴 + 진단서 5 가지 anti-pattern 의 패턴 변환.

근거: `subagent-boilerplate/.local/docs-prose-diagnosis.md` 5 줌 레벨 진단.

---

## Don't list — 즉시 제거 패턴

### 본문에 박지 말 것

- **출처 라벨**: `(Wiki §x.y)`, `(boilerplate 컨벤션)`, `— Wiki §7.1`
- **redundant 출처 prefix**: 인용구 / bullet 안의 `권위 출처:`, `Source:`, `참고:`, `출처:` 같은 prefix. 링크 자체가 자기 정체를 설명합니다. `> [SOAP 명세서](https://...)` 한 줄이면 충분.
- **문서 거버넌스 어휘**: `단일 source`, `권위 문서`, `본문 정의 / 검증 항목은 [doc] 단일 source`, `이 문서가 다루는 범위`. 독자는 "어디 가서 보면 되나" 만 필요합니다. `[doc] 참고` 로 줄여 쓰십시오.
- **여러 링크의 mid-sentence comma merge**: `이식 준비는 [doc1], 일정 상세는 [doc2], 빌드 가이드는 [doc3]` 같은 한 문장 multi-link. 각 링크가 자기 bullet 을 가지는 게 readable. 특히 README / 인덱스 문서에서.
- **슬래시 나열**: `셋업 / 권장 span / 메트릭`, `Trace / Metrics`, `결정 / 일정 / 결과`. 세 개를 슬래시로 묶으면 항목 간 관계가 흐려지고 AI 가 적은 문서처럼 읽힙니다. 산문은 `, 와, 그리고` 로 분리하거나 bullet 으로 풀어 씁니다. 헤딩에서도 `Trace + Metrics` 류 합성보다 `Trace`, `Metrics` 별 헤딩.
- **도입 단락**: `이 섹션은 ~ 를 다룹니다`, `본 문서는 ~ 에 대해 설명합니다`, `다음 섹션에서는 ~ 를 살펴봅니다`
- **우선순위 라벨**: `(1 순위)`, `(후순위)`, `(미정)` 헤딩에 직접 박기
- **정책 인용구**: `> 5 월 중순까지는 ...` 토픽 페이지 안에 박기
- **메타 섹션**: `## Notes`, `## More docs`, `## References`, `## 관련 문서`, `## 더 보기`, `## 참고`
- **nested bullet 2 단계 이상** (1 단은 OK — Form C 참조)
- **한 bullet 에 라벨 + 부연 + 옵션 + 링크** (4 메시지). 단, 라벨 아래 동등 무게 항목 4 개 이상이면 Form C (`**라벨**:` + nested 1 단) 가 comma 합치기보다 readable.
- **"Key features" / "주요 특징" 7 개 hype 리스트**
- **같은 사실 두 페이지 이상에 동일 형태로 등장**

### 문장에 쓰지 말 것

- em-dash (`—`) 한 문장 2 개 이상
- 불필요한 단서: `~할 수도 있고`, `~할 수도 있습니다`, `필요하다면`, `상황에 따라`, `경우에 따라` (의미 손상 없이 빠지면 빼라)
- 가능형 약화: `~할 수 있습니다` (대부분 `~합니다` 로 바꿔도 의미 동일)
- 자기 영역 외 재설명: types 페이지에서 fields 다시 설명, README 에서 conformance 5 항목 다시 적기

---

## Anti-pattern → Pattern 변환 사례

진단서 5 가지 안티패턴의 구체 변환.

### 1. Sentence — 한 줄 4 메시지 → 본문 + admonition 분리

```markdown
# Anti
- **Bearer 인증** (옵션) — boilerplate 가 표준화, Wiki 는 일반 슬롯
```

분해:
- 사실: Bearer 인증 사용
- 단서: (옵션)
- 출처 1: boilerplate 가 표준화
- 출처 2: Wiki 는 일반 슬롯

```markdown
# Pattern
- **Bearer 인증**: 환경 변수로 활성화합니다.

> [!NOTE] 스펙 출처
> Wiki 는 인증을 일반 슬롯으로 둡니다. 본 레포가 표준 형식을 정의합니다.
> 자세한 매핑은 [spec mapping](spec-mapping.md).
```

핵심:
- 본문 bullet 한 줄 = 사실 한 개
- 출처 / 단서는 admonition 으로 격리
- 출처 라벨 (`Wiki §x.y`) 본문에서 제거, 인라인 링크로 한 번만

### 2. Bullet — 라벨 + 4 부분 → Form A

```markdown
# Anti
- **운영 로그** — `audit_log.py` 의 `TaskAuditEntry` 스키마와 어댑터 활용
```

분해:
- 핵심: 운영 로그
- 위치: `audit_log.py`
- 구성: `TaskAuditEntry`, 어댑터
- 동사: 활용

```markdown
# Pattern
- **운영 로그**: `TaskAuditEntry` 스키마를 사용합니다. [audit_log](audit_log.md) 참조.
```

핵심:
- bullet = `**라벨**: 한 문장.` (Form A)
- 위치 / 구성 / 동사 합쳐 한 문장
- 자세한 사항은 See 링크로 떠넘김

### 3. Section — 도입 + 정책 + 본문 + 후속 → 본문만

```markdown
# Anti — README "Observability" 섹션
## Observability (sub-agent 결정 영역)

Sub-agent 운영을 위한 로그 / 트레이스 / 메트릭은 sub-agent 가 자유롭게 결정합니다. 본 레포는 SDK 셋업과 어댑터 template 까지만 제공합니다.

> **5 월 중순까지는 로그가 어떤 형태로든 남기만 하면 됩니다.**

우선순위와 권장 사항: [docs/migration/schedule.md](docs/migration/schedule.md) 5.2 절.

### Logging (1 순위)
- **스키마** — `audit_log.py` 의 `TaskAuditEntry` (SOAP 조직 표준)
  - 식별: `task_id`, `context_id`, `skill`, `producer_version`, `status`
  - 메트릭: `quality_score`, `latency_ms`, `input_tokens`, `output_tokens`, `error`
- **기본 어댑터** — `StdoutAuditLogAdapter` (stdout JSON line)
- **AIDA push** — `AIDAAuditLogAdapter` template 을 채워 사용

### Trace (후순위)
- ...

### Metrics (후순위)
- ...
```

분해:
- 도입문 (두 문장): sub-agent 결정 / 본 레포 제공 범위
- 정책 인용구: `5 월 중순까지...`
- 외부 링크: `schedule.md 5.2 절`
- 우선순위 라벨: `(1 순위)`, `(후순위)`
- nested bullet 2 단계: 식별 / 메트릭 분기

```markdown
# Pattern
## Observability

Sub-agent 가 결정합니다. 본 레포는 SDK 셋업과 어댑터 template 만 제공합니다.

### Logging
- **스키마**: `TaskAuditEntry`. [audit_log](docs/audit-log.md) 참조.
- **어댑터**: `StdoutAuditLogAdapter` 가 기본입니다.
- **AIDA push**: `AIDAAuditLogAdapter` template 을 사용합니다.

### Trace
- `OTEL_EXPORTER_ENDPOINT` 설정 시 OTel SDK 가 초기화됩니다.

### Metrics
- `OTEL_PROMETHEUS_PORT` (기본 9464) 의 `/metrics` 가 노출됩니다.

> [!NOTE]
> 우선순위 / 마감은 [migration/schedule.md](docs/migration/schedule.md) 한 곳에서 관리합니다.
```

핵심:
- 도입문 한 문장
- 정책 / 우선순위는 admonition 또는 별도 페이지
- 헤딩에 우선순위 라벨 안 박음
- nested bullet 1 단계 max — 필드 정의는 See 링크로 떠넘김

### 4. Page — README 8 섹션 → README 3 섹션 + docs/ 분리

```markdown
# Anti — README.md (206 줄)
## Quick start
## Build paths
## Conformance requirements (5 항목 상세)
## Migration (일정 + 범위 + 더 보기)
## Observability (sub-agent 결정 영역) — Logging / Trace / Metrics
## Notes (PR 검증 / Orchestrator 동기화 / Wiki 미명시)
## More docs (인덱스)
## References (외부 링크)
```

문제:
- 한 페이지에 quick start + 5 토픽 본문 + 메타 3 섹션
- 메타 섹션 (Notes / More docs / References) 가 분량 30% 이상
- 같은 conformance 5 항목이 spec.md, conformance.md 와 중복

```markdown
# Pattern — README.md (~80 줄)
## Quick start (skill 설치 → clone → 확인)
## Build paths (ADK vs Raw A2A 표 + 링크)
## Where to look next (단일 인덱스 링크)

# 별도 페이지로 분리
docs/conformance.md  ← 5 항목 단일 source
docs/migration/      ← 일정 / 담당자 / 사전 작업
docs/observability.md ← Logging / Trace / Metrics
docs/index.md        ← 인덱스 단일 source
```

핵심:
- 한 페이지 한 토픽
- README = quick start + 인덱스 역할만
- 메타 섹션 (Notes / More docs / References) 일괄 폐기
- 본 PR 안에서 다 옮길 필요는 없음. 우선 메타 섹션만 비우고, 토픽 분리는 별도 PR.

### 5. Cross-page — 같은 정보 세 곳 → 한 곳 + 두 곳은 링크

```markdown
# Anti
README.md:
  ## Conformance requirements
    1. Agent Card 노출 — Wiki §7.1
    2. Skill ID 형식 — boilerplate 컨벤션
    3. DataPart 메타데이터 필드 — schema_urn, producer_version, ...
    4. SemVer 버전 — Wiki §7.1
    5. 인증 / 헬스 / 메트릭

docs/spec.md:
  ## SOAP 인터페이스 층 — 다섯 가지 conformance requirements
    (위와 거의 동일한 5 항목 다시 등장)

docs/conformance.md:
  ## PR 리뷰 체크리스트
    (위와 거의 동일한 5 항목 다시 등장)
```

```markdown
# Pattern
docs/conformance.md (단일 source):
  ## 5 가지 인터페이스 스펙
    1. Agent Card 노출
    2. Skill ID 형식
    3. DataPart 메타데이터 필드
    4. SemVer 버전
    5. 인증 / 헬스 / 메트릭

README.md:
  ## Conformance
  5 가지 인터페이스 스펙을 지킵니다. 자세한 사항은 [docs/conformance.md](docs/conformance.md).

docs/spec.md:
  SOAP 인터페이스 층은 [conformance requirements](conformance.md) 5 항목을 정의합니다.
```

핵심:
- 사실은 `docs/conformance.md` 한 곳에만
- 다른 페이지는 한 줄 요약 + 링크
- self-containment 포기 (사용자 합의 필요)

### 6. Bullet — comma 합치기 → nested 1 단 (Form C)

```markdown
# Anti — 동등 무게 4 항목을 comma 로 합쳐 한 bullet 에 박기
- **자동 처리**: FastAPI, Agent Card, /__health, SemVer 검증, OTel SDK 셋업.
```

문제:
- 항목이 5 개고 각각 동등한 무게인데 comma 로 묶음
- 각 항목이 자기 백틱 / 링크를 가지고 싶어도 갈 곳이 없음
- 스캔할 때 어디서 끊기는지 안 보임

```markdown
# Pattern — Form C (라벨 + nested 1 단)
- **자동 처리**:
    - FastAPI + a2a-sdk `/a2a` mount
    - Agent Card `/.well-known/agent.json`, `/__health`
    - SemVer 와 Skill ID prefix 검증
    - OTel + Prometheus SDK 셋업
```

핵심:
- 항목 ≥ 4 개 + 동등 무게면 comma 합치기보다 nested 1 단이 readable
- 라벨은 `**자동 처리**:` 한 줄 — 그 자체가 sub-list 의 컨텍스트
- nested 2 단계는 여전히 금지

### 7. Link — mid-sentence multi-link → bullet 분리

```markdown
# Anti — 한 문장에 링크 세 개 묶기
이식 준비는 [doc1], 일정 상세는 [doc2], 빌드 가이드는 [doc3].
```

문제:
- 각 링크의 라벨이 한 문장 안에 흩어져 클릭 표적이 작음
- 인덱스 역할이라면 한 줄 하나씩 보여주는 게 readable

```markdown
# Pattern — 각 링크가 자기 bullet
- 구현 참고: [doc3]
- 일정 상세: [doc2]
- 이식 준비: [doc1]
```

핵심:
- README / 인덱스 문서에서 특히 유효
- 산문 흐름 안에 링크 한두 개는 OK. 셋 이상이면 bullet 으로 풀어라.

### 8. Quote — redundant 출처 prefix 제거

```markdown
# Anti
> 권위 출처: [SOAP 명세서](https://wiki.navercorp.com/...)

# Pattern
> [SOAP 명세서](https://wiki.navercorp.com/...)
```

핵심:
- `권위 출처:`, `Source:`, `참고:`, `출처:` 같은 prefix 는 의미 없는 장식
- 링크 자체가 자기 정체를 설명한다
- 인용구 안의 한 줄짜리 출처라면 링크 하나로 충분

### 9. Section — anchor 도입문 → WHY 한 문장

```markdown
# Anti — 단순 anchor
## Migration

Migration 일정과 가이드입니다.

# Pattern — WHY 한 문장
## Migration

SOAP에서 의도하는 A2A 스펙의 Subagent가 완성되어서, 내부 구현이 미흡하더라도 올바른 프로토콜로 활용이 가능한 상태를 만들기 위한 migration.
```

핵심:
- 도입문 ≤ 1 문장 룰은 유지
- 그 한 문장이 단순 anchor (`~ 일정과 가이드입니다`) 보다 WHY 를 설명할 때 더 가치 있다
- 큰 섹션 안에 여러 토픽이 섞이면 sub-heading (`### 예제`, `### 1차 일정`, `### 그 외 문서`) 으로 분리. 매 표 / 리스트마다 라벨 단락을 쓰지 말고 sub-heading 이 그 역할.

---

## 코드 블록 변환

### "다음을 실행하면 다음과 같이 출력됩니다" 줄글 제거

```markdown
# Anti
컨테이너 환경에서는 OTLP 프로토콜로 trace 를 export 하는 것이 일반적입니다. 본 레포는 OTel SDK 를 자동으로 셋업하므로 환경 변수 한 줄로 충분합니다. 다음 변수를 설정하면 됩니다.

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
```

위 명령을 실행하면 OTel SDK 가 자동 초기화되어 모든 span 이 collector 로 전송됩니다.
```

```markdown
# Pattern
환경 변수 한 줄로 trace export 를 활성화합니다.

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
```

OTel SDK 가 자동 초기화됩니다.
```

### Python 출력 인라인

```python
# Anti
import datetime
m_timestamp = datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=datetime.UTC)
print(repr(m_timestamp))
# 이 코드는 다음과 같은 결과를 출력합니다:
# datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
```

```python
# Pattern
print(repr(m_timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
```

### 긴 출력 접기

```markdown
# Pattern — <details> 로 접기
$ uv run soap-conformance http://localhost:9000 --verbose

<details>
<summary>전체 출력 (40 줄)</summary>

```
PASS  agent_card_present
PASS  agent_card_legacy_404
PASS  health_endpoint
... (38 줄)
```

</details>
```

---

## 헤딩 어투 통일

### 동사형 vs 명사형 혼용 → 한 가지로

```markdown
# Anti — 혼용
## 에이전트 추가하기
## 도구를 정의합니다
## 검증

# Pattern A — 명사구 통일
## 에이전트 추가
## 도구 정의
## 검증

# Pattern B — 동사형 통일
## 에이전트를 추가합니다
## 도구를 정의합니다
## 검증합니다
```

본 레포는 명사구 통일 권장 (현재 컨벤션과 일치).

---

## 단서 약화 표현 정리

### 빼면 의미 그대로인 단서

```markdown
# Anti
필요하다면 OTLP endpoint 를 설정할 수도 있습니다.
상황에 따라 환경 변수로 끌 수도 있고, 직접 인스턴스를 주입할 수도 있습니다.
경우에 따라 `model_info` 가 null 이 될 수 있습니다.

# Pattern
OTLP endpoint 를 설정합니다.
환경 변수로 끄거나 인스턴스를 직접 주입합니다.
LLM 호출이 없는 step 은 `model_info` 가 null 입니다.
```

### 정말 조건부 동작은 유지

```markdown
# Keep — 조건이 진짜 정보일 때
LLM 호출 없는 step 은 `model_info` 가 null 입니다.
인증을 활성화한 경우 모든 요청에 `Authorization` 헤더가 필요합니다.
```

판정 기준: "이 단서를 빼면 사실관계가 틀려지는가?" 틀려지지 않으면 사족.
