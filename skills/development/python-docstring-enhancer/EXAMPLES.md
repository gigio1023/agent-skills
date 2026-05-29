# Docstring 작성 예시

이 문서는 [SKILL.md](SKILL.md)의 가이드라인을 따른 상세 예시를 제공합니다.

## 목차
- [Before/After 비교](#beforeafter-비교)
- [완전한 예시: 긴 메서드](#완전한-예시-긴-메서드)
- [안티 패턴](#안티-패턴)

---

## Before/After 비교

### 예시 1: 간단한 메서드

**Before** (문서화 없음):
```python
def search_ads(self, queries, categories):
    results = []
    for q in queries:
        ads = self.client.search(q)
        results.extend(ads)
    return results
```

**After** (기본 docstring):
```python
def search_ads(self, queries, categories):
    """
    주어진 질의로 광고 검색 수행.

    Args:
        queries: 검색 질의 목록
        categories: 필터링할 광고 카테고리

    Returns:
        검색된 광고 목록 (중복 포함 가능)
    """
    results = []
    for q in queries:
        ads = self.client.search(q)
        results.extend(ads)
    return results
```

---

### 예시 2: 복잡한 분기 로직

**Before** (이해하기 어려움):
```python
def get_empty_reason(self, candidates, had_error, filtered_out):
    if candidates:
        return None
    if filtered_out:
        return EmptyReason.THRESHOLD_NOT_MET
    if had_error:
        return EmptyReason.API_ERROR
    return EmptyReason.NO_RESULTS
```

**After** (맥락 설명 포함):
```python
def get_empty_reason(self, candidates, had_error, filtered_out):
    """
    광고 후보가 없는 이유 결정.

    우선순위:
    1. 후보가 있으면 None
    2. 필터링으로 제거된 경우 → THRESHOLD_NOT_MET
    3. API 오류가 있었던 경우 → API_ERROR
    4. 기본값 → NO_RESULTS

    Args:
        candidates: 현재 남은 광고 후보
        had_error: API 호출 중 오류 발생 여부
        filtered_out: relevance score 필터링으로 제거된 후보 존재 여부

    Returns:
        EmptyReason enum 또는 None
    """
    # 후보가 있으면 empty_reason 불필요
    if candidates:
        return None
    
    # 필터링으로 인한 빈 결과 (원래는 후보가 있었음)
    if filtered_out:
        return EmptyReason.THRESHOLD_NOT_MET
    
    # API 오류로 인한 빈 결과
    if had_error:
        return EmptyReason.API_ERROR
    
    # 검색 결과 자체가 없음
    return EmptyReason.NO_RESULTS
```

---

## 완전한 예시: 긴 메서드

실제 프로젝트의 `retrieve_async` 메서드를 예시로 합니다.

```python
async def retrieve_async(
    self,
    question: str,
    answer: str,
    ad_categories: list[AdType] | None = None,
    user_persona: str | None = None,
    trace_id: str | None = None,
) -> ADRetrievalResult:
    """
    광고 검색 질의를 생성하고 후보를 탐색.

    처리 단계:
    1. LLM으로 Next Intent 기반 광고 질의 생성
    2. MCP를 통해 광고 API 호출 (실패 시 Mock fallback)
    3. 최소 relevance score 이하 광고 필터링

    Args:
        question: 사용자 질문
        answer: 원본 답변 텍스트
        ad_categories: 광고 카테고리 목록 (우선순위 순, 미지정 시 전체)
        user_persona: User Persona Synthesis 결과 텍스트 (개인화 적용 시)
        trace_id: Langfuse trace ID (외부 trace에 연결 시 사용)

    Returns:
        광고 검색 결과 객체:
        - ad_queries: 생성된 광고 검색 질의 목록
        - ad_candidates: 탐색된 광고 후보 목록
        - retrieval_strategy: 검색 전략 (contextual/personalized)
        - empty_reason: 후보가 없는 경우 사유
    """
    async with observe_agent_async(AgentName.AD_RETRIEVAL):
        langfuse: Langfuse = self.langfuse or get_client()

        # 외부 trace 연결용 context 설정
        trace_context: dict[str, str] | None = (
            {"trace_id": trace_id} if trace_id else None
        )

        with langfuse.start_as_current_observation(
            as_type="span",
            name="ad-retrieval",
            trace_context=trace_context,
        ) as span:
            span.update(input={...})

            # 기본 광고 카테고리 설정
            if ad_categories is None:
                ad_categories = list(AdType)

            # Step 1: 광고 질의 생성
            persona_text: str = user_persona or ""
            interests: str = ""

            rendered = self.prompt_manager.render(
                self.config.prompt_name,
                question=question,
                answer=answer,
                ad_categories=[c.value for c in ad_categories],
                persona_text=persona_text,
                interests=interests,
            )

            messages: list[ChatMessage] = [
                ChatMessage(role=MessageRole.USER, content=rendered.text)
            ]

            parse_result = await self.llm_client.parse_buffered_async(
                messages=messages,
                response_format=AdQueryListResult,
                model=self.config.get_llm_model(),
                langfuse_prompt=rendered.langfuse_prompt,
                agent=AgentName.AD_RETRIEVAL,
                **self.config.get_llm_kwargs(),
            )
            query_result: AdQueryListResult | None = parse_result.result

            if query_result is None:
                logger.error("LLM parsing failed")
                raise ValueError("Failed to parse LLM response")

            # Step 2: 광고 검색 (MCP 우선, 실패 시 Mock)
            queries: list[str] = [q.query_text for q in query_result.ad_queries]
            
            # 검색 결과 및 상태 추적 변수
            ad_candidates: list[AdCandidate]
            retrieval_source: str
            had_error: bool = False  # MCP 오류 발생 여부 (empty_reason 결정에 사용)

            if self.mcp_client and self.mcp_client.enabled:
                (
                    ad_candidates,
                    retrieval_source,
                    had_error,
                ) = await self._search_ads_via_mcp(
                    queries=queries,
                    categories=ad_categories,
                    langfuse=langfuse,
                )
            else:
                # MCP 비활성화 시 Mock으로 직접 폴백
                ad_candidates = await self._search_ads_mock(
                    queries=queries,
                    categories=ad_categories,
                )
                retrieval_source = "mock"
                had_error = False

            # Step 3: Relevance Score 기반 필터링
            empty_reason: ADRetrievalEmptyReason | None = None
            
            # config에서 min_relevance_score 동적 로드 (None이면 필터링 안 함)
            min_relevance_score_raw = self.config.options.get("min_relevance_score")
            min_relevance_score: float | None = None
            if min_relevance_score_raw is not None:
                min_relevance_score = float(min_relevance_score_raw)

            # min_relevance_score가 설정된 경우에만 필터링 수행
            # ad_candidates가 비어있으면 필터링 불필요하므로 스킵
            if min_relevance_score is not None and ad_candidates:
                before_filter_count: int = len(ad_candidates)
                ad_candidates = [
                    c for c in ad_candidates
                    if c.relevance_score >= min_relevance_score
                ]
                # 필터링 전에는 후보가 있었지만 모두 제거된 경우
                # → 검색은 성공했으나 품질 기준 미달
                if before_filter_count > 0 and not ad_candidates:
                    empty_reason = ADRetrievalEmptyReason.RELEVANCE_THRESHOLD_NOT_MET

            # empty_reason 결정: 위에서 설정되지 않은 케이스 처리
            # empty_reason이 이미 설정된 경우(필터링으로 제거됨)는 덮어쓰지 않음
            if not ad_candidates and empty_reason is None:
                empty_reason = (
                    ADRetrievalEmptyReason.VECTOR_DB_ERROR
                    if had_error  # MCP 호출 실패로 인한 빈 결과
                    else ADRetrievalEmptyReason.NO_MATCHING_ADS  # 검색 결과 자체가 없음
                )

            # 검색 전략 결정 및 메트릭 기록
            retrieval_strategy: str = (
                "personalized" if user_persona else "contextual"
            )
            metric_ad_type = (
                MetricAdType.PERSONALIZED if user_persona else MetricAdType.GENERAL
            )
            record_ad_retrieval_candidates(metric_ad_type, len(ad_candidates))
            record_ad_retrieval_source(retrieval_source)

            result = ADRetrievalResult(
                ad_queries=query_result.ad_queries,
                ad_candidates=ad_candidates,
                retrieval_strategy=retrieval_strategy,
                empty_reason=empty_reason,
            )

            span.update(output={...})
            return result
```

---

## 안티 패턴

### ❌ Pydantic 필드 설명 중복

```python
# 나쁜 예: docstring에 필드 설명 중복
class ADQAGenRequest(BaseModel):
    """
    광고 통합 QA 생성 요청.

    필드:
    - question: 사용자 질문
    - answer: 원본 답변 텍스트
    - use_personalization: 개인화 파이프라인 사용 여부
    """

    question: str = Field(description="사용자 질문")
    answer: str = Field(description="원본 답변 텍스트")
    use_personalization: bool = Field(default=False, description="개인화 파이프라인 사용 여부")
```

```python
# 좋은 예: 모델 역할만 docstring에, 필드 설명은 Field에 위임
class ADQAGenRequest(BaseModel):
    """광고 통합 QA 생성 요청."""

    question: str = Field(description="사용자 질문")
    answer: str = Field(description="원본 답변 텍스트")
    use_personalization: bool = Field(default=False, description="개인화 파이프라인 사용 여부")
```

```python
# 좋은 예: 복잡한 모델은 용도/맥락 추가
class ADRetrievalResult(BaseModel):
    """
    AD Retrieval Agent 실행 결과.

    용도:
    - Answer Fusion Agent 입력으로 전달
    - Orchestrator에서 파이프라인 결과 추적에 활용
    """

    ad_queries: list[AdQuery] = Field(description="생성된 광고 검색 질의 목록")
    ad_candidates: list[AdCandidate] = Field(description="탐색된 광고 후보 목록")
    empty_reason: str | None = Field(default=None, description="후보가 없는 경우 사유")
```

### ❌ Type Hint 중복

```python
# 나쁜 예: 타입 정보 중복
def search(self, query: str, limit: int) -> list[Ad]:
    """
    Args:
        query (str): 검색어
        limit (int): 최대 결과 수
    
    Returns:
        list[Ad]: 검색된 광고 목록
    """
```

```python
# 좋은 예: 의미만 설명
def search(self, query: str, limit: int) -> list[Ad]:
    """
    Args:
        query: 검색어
        limit: 최대 결과 수
    
    Returns:
        검색된 광고 목록
    """
```

### ❌ 장황한 서술

```python
# 나쁜 예: 불필요하게 장황함
"""
이 메서드는 사용자가 입력한 질문과 시스템이 생성한 답변을 분석하여
광고 검색에 적합한 질의를 생성하는 역할을 수행합니다.
생성된 질의를 통해 MCP 서버에 연결하여 파워링크 광고를 검색하며,
만약 MCP 서버 연결에 실패하거나 결과가 없는 경우에는 Mock 데이터로
대체하여 반환합니다.
"""
```

```python
# 좋은 예: 개조식으로 간결하게
"""
광고 검색 질의를 생성하고 후보를 탐색.

처리 단계:
1. LLM으로 광고 질의 생성
2. MCP로 광고 검색 (실패 시 Mock fallback)
3. Relevance score 필터링
"""
```

### ❌ 무의미한 주석

```python
# 나쁜 예: 코드를 그대로 반복
# candidates 리스트를 순회한다
for candidate in candidates:
    # ad_id를 가져온다
    ad_id = candidate.ad_id
```

```python
# 좋은 예: Why(이유)를 설명
# 중복 광고 제거를 위해 ad_id 기준으로 필터링
for candidate in candidates:
    ad_id = candidate.ad_id
    if ad_id in seen_ids:
        continue
    seen_ids.add(ad_id)
```
