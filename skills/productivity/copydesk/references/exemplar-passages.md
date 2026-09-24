# Exemplar Passages

These are short quotations from public Korean technical writing, each chosen for the writing operation it performs rather than for its topic. Read them when drafting Korean technical prose, to hear how a sentence names the actor, states a result with its limit, or gives a decision with its reason. They are not templates: borrow the operation, never the outline, the topic, or the blog's register.

## Mechanism: from code fact to symptom

> `KeepAliveCache kac` 변수에 `static` 키워드가 붙어있기 때문에 `HttpClient` 클래스의 모든 인스턴스가 단 하나의 `KeepAliveCache kac`를 공유해서 사용하게 된 거였어요. `KeepAliveCache kac`는 공유자원인데 여러 스레드가 동시에 `synchronized put` 메서드를 수행하려고 하니 동시성 문제가 발생한 거예요.

김성두 (토스페이먼츠), "Feign 코드 분석과 서버 성능 개선", 2023. https://toss.tech/article/engineering-note-3

Every subject is a real identifier, and the cause runs from one keyword to shared state to contention in two sentences. Borrow the chain; the 해요체 ending belongs to the blog.

## Incident: miss, cause, fix, recheck

> 한 케이스에서 운영 설정 파일에 비운영 환경 호스트가 들어간 변경이 있었습니다. (…) 비운영 환경을 식별하는 마커 목록에 `-dev`, `-beta`, `-cbt`, `-sandbox`만 있었고, 해당 케이스에서 쓰인 `canary` 표기가 목록에 없었던 것입니다. 곧바로 `canary`, `stage`, `staging`, `alpha`, `test` 계열 마커를 추가했고, 이후 같은 케이스에서 정상적으로 검출됐습니다.

diana.jung (카카오), "같은 장애를 두 번 겪지 않기 위해, 배포 전에 리뷰합니다 — KRIS 개발기", 2026. https://tech.kakao.com/posts/831

The cause is the exact missing value, and the fix is verified on the same case. Borrow the order and the concrete values instead of "some markers were missing".

## Result, then what it does not cover

> SSE 도입 이후에는 서브카테고리처럼 가벼운 구좌의 응답이 약 15ms 만에 먼저 나갑니다. 물론 지면의 핵심인 가게 리스트는 여전히 약 300ms에 도착합니다. 데이터가 모두 도착하는 시점이 빨라진 것이 아니라, 첫 반응까지의 시간이 달라졌습니다.

정시윤, 정진솔 (우아한형제들), "BFF 서버에 SSE를 도입한 이유: 전시 서버의 통신 구조 재설계", 2026. https://techblog.woowahan.com/26507/

The gain comes with its number, then the number that did not move, then the one metric that changed. Borrow the second and third sentences: state the limit before the reader asks.

## Table: rows are cases, columns are conditions

> 클라이언트가 기록한 이벤트별 도착 시각입니다(3회 중앙값).
>
> | 이벤트 크기 (송출 시점) | 프록시 없음 | nginx 버퍼링 ON | nginx 버퍼링 OFF |
> | --- | --- | --- | --- |
> | 200B (0ms) | 5ms | 5ms | 5ms |
> | 20KB (100ms) | 108ms | 109ms | 108ms |
> | 280KB (300ms) | 313ms | 310ms | 313ms |
>
> (…) nginx 버퍼링 ON은 프록시가 없을 때와 구분되지 않았습니다.

Same article; three of the table's five rows shown.

The caption names who measured and the statistic, the row key carries the send time, the control column comes first, and one sentence gives the reading. Borrow all four.

## Decision with its reason

> Oracle 쿼리 수행에 영향을 주지 않는 가장 확실한 방법은 트랜잭션 도중 수행되는 쿼리를 모아두었다가 커밋 후 한꺼번에 MySQL에서 수행하는 것입니다. (…) 트랜잭션이 롤백되더라도 MySQL에서는 수행된 쿼리가 없으므로 신경 쓰지 않아도 됩니다. Oracle 커넥션을 점유하는 시간이 늘어나지도 않고 예외 처리 및 추적도 용이합니다.

스마트스토어 회원 파트 (NAVER D2), "스마트스토어센터 Oracle에서 MySQL로의 무중단 전환기", 2026. https://d2.naver.com/helloworld/6512234

The decision is one direct claim that carries its constraint, and each consequence is one checkable fact. Borrow claim, constraint, consequences, with no "we believe" frame.

## Finding, then its mechanism

> 판정보다 판정 근거를 먼저 쓰게 한 것이 실제로 효과가 있었습니다. 결론부터 뽑게 하면 근거가 결론에 맞춰 사후 작성되는데, 순서를 뒤집으면 근거가 빈약한 케이스에서 LLM이 등급을 낮춰 잡습니다.

diana.jung (카카오), KRIS 개발기, 2026. https://tech.kakao.com/posts/831

One sentence of finding, then one sentence holding both orderings and what each produces. Borrow the contrast inside a single sentence, so the condition travels with the claim.
