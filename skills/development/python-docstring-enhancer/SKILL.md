---
name: python-docstring-enhancer
version: 1.0.0
description: |
  AD-Agent 계열 Python 코드에 상세한 Docstring과 한국어 why 주석을 추가하여 코드의 가독성과 유지보수성을 높인다.
  트리거: "주석 보강", "문서화", "docstring 추가", "주석 달아줘" 등의 요청 시 사용.
  복잡한 메서드도 처음 보는 사람이 이해할 수 있도록 Step 기반 문서화, 의도 설명, 맥락 주석을 적용.
---

# Python Docstring Enhancer

## 목차
- [개요](#개요)
- [Quick Reference](#quick-reference)
- [기본 가이드라인](#기본-가이드라인)
- [복잡한 코드 문서화](#복잡한-코드-문서화)
- [메트릭 및 Observability 코드 구분](#메트릭-및-observability-코드-구분)
- [체크리스트](#체크리스트)

상세 예시는 [EXAMPLES.md](EXAMPLES.md) 참조.

---

## 개요

이 스킬은 프로젝트의 Python 소스 코드에 표준화된 Docstring 형식을 적용합니다.

**핵심 목표**: 복잡하거나 특이하게 구현된 코드라도 **처음 보는 사람이 흐름을 따라가며 이해할 수 있도록** 문서화합니다.

**적용 원칙**:
- 프로젝트 고유 용어 유지 (Answer Fusion, AD Retrieval 등)
- 개조식(Bullet) 문체로 간결하게 작성
- Type Hint 중복 제거 (코드에 이미 있으면 docstring에서 생략)

---

## Quick Reference

| 대상 | 핵심 포인트 |
|------|------------|
| **파일 헤더** | 목적 + 주요 워크플로우 개조식 요약 |
| **클래스** | 역할 + Usage 예시 |
| **Pydantic 모델** | 모델 역할/용도만 설명, 필드 설명은 Field(description=)에 위임 |
| **메서드 (짧음)** | Args, Returns만 간결하게 |
| **메서드 (길거나 복잡)** | `처리 단계:` 명시 + `# Step N:` 주석 |
| **변수 선언** | 의도와 사용처 설명 (특히 상태 추적 변수) |
| **조건문 (핵심!)** | 왜 이 조건을 체크하는지, 복합 조건의 각 조건 의미 설명 |
| **폴백/예외** | 동작 방식과 이유 설명 |
| **Metrics 코드** | `# [Metrics]` 접두어로 Prometheus 메트릭 코드 구분 |
| **Observability 코드** | `# [Observability]` 접두어로 Langfuse Trace/Span 코드 구분 |
| **Prompt Registry** | Langfuse Prompt는 Observability 아님, 별도 분류 불필요 |

---

## 기본 가이드라인

### 1. 용어 준수 (Terminology)
프로젝트 고유 명사는 번역하지 않고 그대로 사용:
- Answer Fusion, AD Retrieval, Quality Inspection, CADI, User Persona Synthesis 등

### 2. 작성 스타일
- **개조식 문체**: `-`, `*` 활용하여 간결하게
- **문장 종결**: "~함", "~임" 등 명사형 또는 간결한 서술형
- **Markdown 볼드 사용 금지**: 주석이나 docstring에 `**텍스트**` 형태의 볼드 표기 사용하지 않음
- **이모지 최소화**: 주석에 이모지 사용하지 않음 (README나 문서 파일은 허용)

### 3. 파일 헤더
```python
"""
AD Retrieval Agent

광고 후보 탐색을 위한 Agent.

주요 워크플로우:
- LLM을 통해 Next Intent 기반 광고 검색 질의 생성
- MCP를 통해 파워링크 광고 API 호출
- MCP 실패 시 Mock 광고로 fallback
"""
```

### 4. 클래스 Docstring
```python
class ADRetrievalAgent:
    """
    광고 검색 질의를 생성하고 후보를 탐색하는 Agent.

    역할:
    - QA Context 분석 후 Next Intent 기반 광고 질의 생성
    - MCP를 통해 실제 파워링크 광고 검색

    Usage:
        agent = ADRetrievalAgent(prompt_manager, llm_client)
        result = await agent.retrieve_async(question, answer)
    """
```

### 5. Pydantic 모델 Docstring

Pydantic 모델은 **모델의 역할/용도만** docstring에 작성하고, **개별 필드 설명은 `Field(description=...)`에 위임**합니다.

```python
class ADRetrievalRequest(BaseModel):
    """AD Retrieval Agent API 요청 모델."""

    question: str = Field(description="사용자 질문")
    answer: str = Field(description="원본 답변 텍스트")
    user_persona: str | None = Field(default=None, description="사용자 페르소나")
```

복잡한 모델은 역할과 사용 맥락을 추가:

```python
class ADRetrievalResult(BaseModel):
    """
    AD Retrieval Agent 실행 결과.

    용도:
    - Answer Fusion Agent 입력으로 전달
    - 광고 후보 목록과 검색 메타데이터 포함
    """

    ad_queries: list[AdQuery] = Field(description="생성된 광고 검색 질의 목록")
    ad_candidates: list[AdCandidate] = Field(description="탐색된 광고 후보 목록")
    empty_reason: str | None = Field(default=None, description="후보가 없는 경우 사유")
```

**주의**: docstring에 `필드:` 섹션으로 필드를 나열하지 않음 (Field description과 중복)

### 6. 메서드 Docstring (기본)
```python
def fuse_ads(self, question, answer, candidates):
    """
    Answer Fusion 로직 수행 및 광고 삽입 결과 반환.

    Args:
        question: 사용자 입력 질문
        answer: 원본 답변 텍스트
        candidates: AD Retrieval을 통해 확보된 광고 후보 리스트

    Returns:
        광고가 결합된 최종 답변 및 선택된 광고 정보 객체
    """
```

**주의**: Args에 타입 정보 기재하지 않음 (코드의 Type Hint와 중복 방지)

---

## 복잡한 코드 문서화

긴 메서드(50줄 이상)나 복잡한 분기 로직은 다음 패턴을 적용합니다.

### 패턴 1: Docstring에 처리 단계 명시

메서드가 여러 단계로 구성된 경우 `처리 단계:`를 docstring에 포함:

```python
async def retrieve_async(self, question: str, answer: str) -> Result:
    """
    광고 검색 질의를 생성하고 후보를 탐색.

    처리 단계:
    1. LLM으로 Next Intent 기반 광고 질의 생성
    2. MCP를 통해 광고 API 호출 (실패 시 Mock fallback)
    3. 최소 relevance score 이하 광고 필터링

    Args:
        question: 사용자 질문
        answer: 원본 답변 텍스트

    Returns:
        광고 검색 결과 객체:
        - ad_queries: 생성된 광고 검색 질의 목록
        - ad_candidates: 탐색된 광고 후보 목록
        - empty_reason: 후보가 없는 경우 사유
    """
```

### 패턴 2: Step 주석으로 코드 내비게이션

docstring의 처리 단계와 매칭되는 `# Step N:` 주석 삽입:

```python
# Step 1: 광고 질의 생성
rendered = self.prompt_manager.render(...)
parse_result = await self.llm_client.parse_buffered_async(...)

# Step 2: 광고 검색 (MCP 우선, 실패 시 Mock)
if self.mcp_client and self.mcp_client.enabled:
    ad_candidates, source, had_error = await self._search_ads_via_mcp(...)
else:
    ad_candidates = await self._search_ads_mock(...)

# Step 3: Relevance Score 기반 필터링
if min_relevance_score is not None and ad_candidates:
    ad_candidates = [c for c in ad_candidates if c.relevance_score >= min_relevance_score]
```

### 패턴 3: 변수 의도 설명

상태 추적 변수나 조건부 초기화에 의도 설명:

```python
# MCP 호출 성공 여부 추적 (fallback 결정 및 empty_reason 계산에 사용)
had_error: bool = False

# 최소 relevance score (config에서 동적 로드, None이면 필터링 안 함)
min_relevance_score: float | None = None
```

### 패턴 4: 조건문 의도 설명 (핵심)

**모든 조건문에 왜 이 조건을 체크하는지 설명합니다.** 특히:
- 복합 조건(`and`, `or`)의 각 조건이 왜 필요한지
- 조건이 참/거짓일 때 어떤 시나리오인지
- None 체크, 빈 리스트 체크 등 방어적 조건의 이유

```python
# min_relevance_score가 설정된 경우에만 필터링 수행
# ad_candidates가 비어있으면 필터링 불필요하므로 스킵
if min_relevance_score is not None and ad_candidates:
    before_filter_count: int = len(ad_candidates)
    ad_candidates = [
        c for c in ad_candidates
        if c.relevance_score >= min_relevance_score
    ]
```

```python
# empty_reason 결정: 필터링으로 인한 빈 결과와 원래 빈 결과를 구분
# empty_reason이 이미 설정된 경우(필터링으로 제거됨)는 덮어쓰지 않음
if not ad_candidates and empty_reason is None:
    empty_reason = (
        ADRetrievalEmptyReason.VECTOR_DB_ERROR
        if had_error  # MCP 호출 실패로 인한 빈 결과
        else ADRetrievalEmptyReason.NO_MATCHING_ADS  # 검색 결과 자체가 없음
    )
```

### 패턴 5: 폴백/예외 처리 설명

```python
if all_candidates:
    return all_candidates, "mcp", had_error

# MCP 검색 결과가 없는 경우 Mock으로 폴백
# - 프로덕션에서도 광고 없는 경우를 방지하기 위한 안전장치
logger.warning("MCP search returned no results, falling back to mock")
mock_candidates = await self._search_ads_mock(queries, categories)
return mock_candidates, "mock_fallback", had_error
```

---

## 메트릭 및 Observability 코드 구분

프로젝트에서 **메트릭 집계, 모니터링, LLM Observability**를 위한 코드는 비즈니스 로직과 명확히 구분합니다.

### 코드 분류 기준

| 분류 | 설명 | 주요 도구 | 주석 접두어 |
|------|------|----------|------------|
| **Metrics** | Victoria Metrics 집계용 `/metrics` API로 노출되는 지표 | Prometheus Counter, Histogram, Gauge 등 | `# [Metrics]` |
| **Observability** | LLM 호출 추적, Trace/Span 관리 | Langfuse Trace, Span, Generation | `# [Observability]` |
| **Prompt Registry** | 프롬프트 버전 관리 및 등록 | Langfuse Prompt | *(별도 분류 불필요)* |

> ⚠️ **주의**: Langfuse Prompt는 **Prompt Registry** 기능으로, Observability가 아닙니다.
> Prompt 버전 관리, A/B 테스트, 프롬프트 히스토리 추적 등의 목적으로 사용됩니다.

### 주석 패턴

#### 패턴 1: Metrics 코드 구분

Prometheus Counter, Histogram 등 메트릭 관련 코드에 `# [Metrics]` 접두어 사용:

```python
from prometheus_client import Counter, Histogram

# [Metrics] LLM 호출 횟수 추적
llm_call_counter = Counter(
    "adagent_llm_calls_total",
    "Total number of LLM API calls",
    ["agent", "model", "status"]
)

# [Metrics] LLM 응답 시간 분포 추적
llm_latency_histogram = Histogram(
    "adagent_llm_latency_seconds",
    "LLM API call latency in seconds",
    ["agent", "model"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
```

메서드 내 메트릭 기록 시에도 동일하게 적용:

```python
async def call_llm(self, prompt: str) -> str:
    start_time = time.time()
    try:
        result = await self._invoke_llm(prompt)
        # [Metrics] 성공 호출 카운트 증가
        llm_call_counter.labels(agent=self.name, model=self.model, status="success").inc()
        return result
    except Exception as e:
        # [Metrics] 실패 호출 카운트 증가
        llm_call_counter.labels(agent=self.name, model=self.model, status="error").inc()
        raise
    finally:
        # [Metrics] 응답 시간 기록
        llm_latency_histogram.labels(agent=self.name, model=self.model).observe(
            time.time() - start_time
        )
```

#### 패턴 2: Observability 코드 구분

Langfuse Trace, Span, Generation 등 LLM Observability 코드에 `# [Observability]` 접두어 사용:

```python
from langfuse import Langfuse

# [Observability] Langfuse 클라이언트 초기화
langfuse = Langfuse()

async def process_query(self, query: str) -> str:
    # [Observability] 새 Trace 시작 - 전체 요청 흐름 추적
    trace = langfuse.trace(
        name="ad_retrieval_flow",
        user_id=self.user_id,
        metadata={"query_length": len(query)}
    )

    # [Observability] LLM Generation Span 생성
    generation = trace.generation(
        name="generate_ad_query",
        model=self.model_name,
        input=query
    )

    result = await self.llm_client.generate(query)

    # [Observability] Generation 완료 기록
    generation.end(output=result)

    return result
```

#### 패턴 3: Prompt Registry 코드 (분류 불필요)

Langfuse Prompt는 Observability가 아닌 **Prompt Registry** 용도이므로 별도 분류 없이 일반 비즈니스 로직처럼 처리:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Langfuse에서 프롬프트 템플릿 로드 (Prompt Registry)
prompt = langfuse.get_prompt("ad_retrieval_system_prompt", version=2)
rendered = prompt.compile(context=user_context)
```

### 블록 단위 구분

메트릭/Observability 코드가 여러 줄에 걸쳐 있을 경우 블록 주석 사용:

```python
# [Metrics] --- 메트릭 정의 시작 ---
request_counter = Counter("adagent_requests_total", "Total requests", ["endpoint"])
error_counter = Counter("adagent_errors_total", "Total errors", ["endpoint", "error_type"])
processing_histogram = Histogram("adagent_processing_seconds", "Processing time")
# [Metrics] --- 메트릭 정의 끝 ---
```

```python
# [Observability] --- Trace 설정 시작 ---
trace = langfuse.trace(name="answer_fusion", user_id=user_id)
trace.update(metadata={"session_id": session_id, "ab_group": ab_group})
parent_span = trace.span(name="fusion_pipeline")
# [Observability] --- Trace 설정 끝 ---
```

### 이점

이 구분을 통해 달성하는 목표:

- **가독성**: 비즈니스 로직과 인프라 코드(메트릭/추적)를 시각적으로 명확히 분리
- **유지보수**: 메트릭 변경 시 `# [Metrics]` 검색으로 관련 코드 빠르게 탐색
- **리뷰 효율**: 코드 리뷰 시 비즈니스 로직과 Observability 변경을 구분하여 집중

---

## 체크리스트

문서화 작업 전 확인:

- [ ] 프로젝트 용어 그대로 사용 (번역 X)
- [ ] Type Hint 중복 제거
- [ ] 개조식 문체 적용

파일/클래스 레벨:

- [ ] 파일 헤더에 목적과 워크플로우 요약
- [ ] 클래스에 역할과 Usage 예시
- [ ] Pydantic 모델은 역할/용도만 docstring에 작성
- [ ] Pydantic 필드 설명은 Field(description=)에 작성 (docstring에 중복 X)

메서드 레벨:

- [ ] Args/Returns 작성 (타입 정보 제외)
- [ ] 긴 메서드는 `처리 단계:` 명시
- [ ] 코드 내 `# Step N:` 주석으로 내비게이션

인라인 주석:

- [ ] 상태 추적 변수에 의도 설명
- [ ] 분기 로직에 Why(이유) 설명
- [ ] 폴백/예외 처리에 동작 방식 설명

메트릭 및 Observability:

- [ ] Prometheus 메트릭 코드에 `# [Metrics]` 접두어 사용
- [ ] Langfuse Trace/Span/Generation 코드에 `# [Observability]` 접두어 사용
- [ ] Langfuse Prompt (Prompt Registry)는 별도 분류 없이 처리
- [ ] 여러 줄의 메트릭/Observability 코드는 블록 주석 사용
