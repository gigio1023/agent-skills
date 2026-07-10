# Good and Bad PR Body Examples

## Table of Contents

- 좋은 예시 1: 짧고 왜/결과 중심 (Breaking 포함)
- 좋은 예시 2: 작은 버그 수정
- 나쁜 예시 1: 디테일 나열 + 반말 + 검증 섹션
- 나쁜 예시 2: Breaking 을 별도 섹션으로 빼서 결과와 중복
- 나쁜 예시 3: 배경/결과 누락

## 좋은 예시 1: 짧고 왜/결과 중심 (Breaking 포함)

```md
Jira: https://issues.example.com/browse/PROJ-109

## 배경
LLM Dependency Error Burst 알림이 baseline 에 묻혀 하루 약 5시간 firing 상태였습니다.
원인은 `parse_error`(자체 파서 실패)가 전체 에러의 88%를 차지하면서 LLM endpoint
장애 알림에 합산되고 있었기 때문입니다.

## 변경 요약
- 알림을 error_type 별로 분리하고 critical 은 LLM endpoint 측 문제로 한정합니다
- 운영 알림을 절대 카운트가 아닌 호출 총량 대비 비율로 전환합니다

## 결과
- critical 알림은 실제 LLM endpoint 또는 자체 코드 문제일 때만 발화합니다
- 기존 alert UID `pipeline-llm-dep-error-high` → `pipeline-llm-endpoint-error-rate-high`/`pipeline-llm-parse-error-burst` 로 분리됩니다. 기존 silence 규칙은 새 UID 로 재설정 필요합니다.
```

이 예시가 좋은 이유:
- 본문 약 15줄, 20줄 이내
- 배경(왜) → 변경 요약(무엇) → 결과(달라지는 것) 3섹션
- 모든 문장이 존댓말로 마무리
- 검증 섹션 없음 (CI 가 진실)
- Breaking 영향이 결과 섹션 한 bullet 으로 흡수됨 (`기존 X → 변경 Y. 운영 조치 Z`)
- 파일명/함수명/라인 단위 디테일 없음

## 좋은 예시 2: 작은 버그 수정

```md
Closes #432

## 배경
production 에서 retry 카운터가 0부터 기록되어 Grafana 1회차 retry 비율이 항상 0% 로 표시되었습니다.

## 변경 요약
- retry attempt 라벨 인덱스를 0-based 에서 1-based 로 정정합니다

## 결과
- Grafana retry 패널이 1회차 retry 비율을 정상 표시합니다
```

본문 약 9줄. 작은 변경에는 더 짧게.

## 나쁜 예시 1: 디테일 나열 + 반말 + 검증 섹션

```md
## 변경사항
- `rules.py`의 `_llm_dependency_error_rule` 제거
- `_llm_endpoint_error_rate_rule` 신설
- `_llm_parse_error_burst_rule` 신설
- `contacts.py`의 `_EMAIL_SUBJECT_TEMPLATE` 단순화
- `contacts.py`의 `_EMAIL_MESSAGE_TEMPLATE` 단순화
- `test_alerting.py` 테스트 2개 추가

## 검증
- 테스트 다 돌렸음
- 빌드 OK
```

문제점:
- 함수/파일 단위 나열로 본문이 길어짐
- "왜"와 "결과"가 없음
- 반말/명사 종결
- 검증 섹션을 작성함 (CI 가 진실인데 본문에 적음). 신정책에서는 섹션 자체가 금지

## 나쁜 예시 2: Breaking 을 별도 섹션으로 빼서 결과와 중복

```md
## 배경
alert UID 체계를 error_type 별로 분리합니다.

## 변경 요약
- LLM dependency alert 를 endpoint/parse 두 룰로 분리합니다

## 결과
- critical 알림이 LLM endpoint 문제일 때만 발화합니다
- alert UID 체계가 error_type 별로 분리됩니다

## Breaking Changes
- 기존: `pipeline-llm-dep-error-high`
- 변경: `pipeline-llm-endpoint-error-rate-high`, `pipeline-llm-parse-error-burst`. silence 규칙 재설정 필요합니다.
```

문제점:
- "alert UID 체계가 분리됩니다"(결과)와 Breaking Changes 섹션이 같은 사실을 두 번 말함
- 본문이 불필요하게 길어짐
- 신정책에서는 별도 섹션 금지

수정 방향: 결과 섹션의 마지막 bullet 을 한 줄로 묶습니다.

```md
## 결과
- critical 알림이 LLM endpoint 문제일 때만 발화합니다
- 기존 alert UID `pipeline-llm-dep-error-high` → `pipeline-llm-endpoint-error-rate-high`/`pipeline-llm-parse-error-burst` 로 분리됩니다. 기존 silence 규칙은 새 UID 로 재설정 필요합니다.
```

## 나쁜 예시 3: 배경/결과 누락

```md
## 변경사항
- alert rule 3개로 분리
- email template 정리
```

문제점:
- 왜 했는지 설명 없음
- 무엇이 달라지는지 없음
- 리뷰어가 PR 의도를 파악하려면 diff 를 직접 읽어야 함
