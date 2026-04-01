---
name: humanize
description: Detect and fix AI-sounding expressions, invented terminology, and unnatural phrasing in any document. Use when asked to humanize, de-AI, or make text sound natural.
---

# Humanize

## When to use

- "자연스럽게 다듬어줘" / "AI스러운 거 고쳐줘" → review and fix AI patterns
- "이 문서 검토해줘" → quality check for human-sounding prose
- When other skills (resume-write, slidev-portfolio, etc.) reference this skill's rules while writing

## Inputs

- Target file(s) or text to review
- Language: KO, EN, or both (auto-detect if not specified)

## Workflow

### Correction mode (직접 호출)
1. Read the target document
2. **문서 유형 판단** — 경로와 내용에서 유형을 파악하고 탐지 강도를 조절 (아래 Document Type Calibration 참조)
3. **추상화 수준 탐지** — Abstraction Level Framework로 문장별 판단 (아래 참조)
4. Load language-specific anti-patterns from `references/`
5. Load correction examples from `references/30-correction-examples.md`
6. Identify AI-sounding patterns with exact quotes
7. Present before/after pairs for each finding
8. Apply fixes after user confirms (or all at once if user says "다 고쳐")
9. 교정한 before/after를 `references/30-correction-examples.md`에 추가 (유저가 승인한 교정만)

### Guide mode (다른 스킬에서 참조)
Other skills should load `references/10-ko-anti-patterns.md` or `references/20-en-anti-patterns.md` and apply the rules while writing. Do not repeat the patterns here — the references are the source of truth.

## Abstraction Level Framework

Claude 글의 가장 근본적인 문제: **추상화 수준이 높다.** 단어를 바꿔도 추상화 수준이 그대로면 여전히 AI스럽다.

| Level | 이름 | 예시 |
|---|---|---|
| Level 3 | Label (선언) | "협업 기반을 구축" |
| Level 2 | Mechanism (구조) | "외부 팀이 agent 로직에만 기여하는 구조" |
| Level 1 | Observable (관찰 가능) | "외부 레이어 변경 없이 agent 변경만 발생" |

**탐지 순서** (모든 markdown 문서에 적용):

1. **Self-awarded label 탐지**: "구축", "마련", "확보", "달성", "도모", "실현", "established", "built a foundation", "achieved" — 이 동사가 문장의 핵심 성취로 쓰이면 Level 3일 가능성 높음. 실제로 뭐가 달라졌는지(Level 1-2)로 바꿀 수 있는지 판단.

2. **Placeholder entity 탐지**: "외부 팀", "관련 부서", "다양한 분야", "여러 방면", "various teams", "multiple stakeholders" — 실제 이름/수량으로 바꿀 수 있으면 교체. 정보가 없으면 유지하되 플래그.

3. **AI 포맷 패턴 탐지**: em-dash 나열("X — Y"), 기계적 병렬 구조(3개 이상 동일 패턴 반복), 접속사 체인("이를 통해", "이를 기반으로", "이에 따라").

4. **불필요한 수식 탐지**: 축소("기본적인", "간단한") — 의도적 scope 한정인지 확인. 과장("혁신적", "획기적") — evidence 있는지 확인. 의도 없으면 삭제.

## Document Type Calibration

문서 유형에 따라 탐지 강도를 조절한다. 별도 config 없이 Claude가 문서를 보고 판단.

| 문서 유형 | 엄격 적용 | 완화 |
|---|---|---|
| Resume/Portfolio | 탐지 1-4 전부 | — |
| Career decision doc | 탐지 1 (label), 2 (placeholder) | 탐지 3 (포맷), 4 (수식) |
| Research note | 탐지 2 (placeholder) | 나머지 |
| 이메일/메신저 | Medium-Aware Tone 규칙 우선 | 탐지 1-4는 가볍게 |
| 일반 markdown | 탐지 1 (label vs observable) | 나머지 |

## References (progressive disclosure)

- `references/10-ko-anti-patterns.md` — 한국어 AI 패턴 + before→after 예시
- `references/20-en-anti-patterns.md` — English AI patterns + before→after examples
- `references/30-correction-examples.md` — 유저 승인 교정 이력 (few-shot learning용)

## Gotchas

These are the patterns Claude produces most frequently. Not obvious rules — these are **Claude's actual blind spots** found from scanning this repo:

### 1. 없는 용어 만들기
Claude가 전문적으로 들리는 복합어를 만들어서 반복 사용. 해당 업계에서 실제로 쓰지 않는 표현.
- "metric contract" → metric spec, metric definition
- "주 포지션 가설 / 보조 포지션 / 도전 포지션" → best-fit / backup / stretch
- "dashboard consistency" → dashboard accuracy

**체크**: 전문 용어를 쓸 때 "이 단어를 구글에 검색하면 해당 맥락에서 실제로 나오는가?"

### 2. 다른 분야 프레임워크 남용
소프트웨어/비즈니스 용어를 개인 계획이나 비-SW 문서에 강제 적용.
- 개인 이주 계획에 "ROI", "pipeline warming", "abort criteria", "hard gate"
- 커리어 메모에 "vertical slice", "data point", "strategic optionality"
- 개인 결정에 "A/B test", "north star"

**체크**: "이 용어를 빼고 일상어로 바꿔도 의미가 전달되면, 빼라."

### 3. 과도한 단정 + 코칭 톤
Claude가 사용자에게 코치/컨설턴트처럼 말하는 패턴. 개인 메모인데 남이 단정하는 어조.
- "이대로 가면 된다." / "비협상" / "어떤 시나리오든 실패"
- "솔직한 답:" (사용자가 묻지 않은 질문을 자체 설정)
- "이것만. 이것조차 안 하면..." (동기부여 코치 스타일)

**체크**: "이 문장의 주어가 누구인가? 자기 자신의 메모에서 자기에게 명령하는 톤이면 부자연스럽다."

### 4. 기계적 대칭 구조
모든 섹션이 동일한 틀로 반복. 사람은 이렇게 정리하지 않음.
- 10개 시나리오가 전부 Assessment table + Root Causes + Early Warning Signs + Contingency Plan + Decision Trigger
- 낙관/중립/비관 3단 시나리오 표
- 정확히 3-tier 분류 (강한 증거 / 약한 증거 / 증거 아닌 것)

**체크**: "상위 3-4개만 상세히, 나머지는 한 줄이면 충분한가?"

### 5. 사람이 자기 자신을 "사용자"라고 부르지 않음
AI가 분석 모드에서 문서 주인을 "사용자"로 지칭. 자기 메모에서 자신을 3인칭으로 부르는 사람은 없음.

### 6. 완곡한 재포장 (euphemistic rephrasing)
AI가 부정적 상황을 격식적/임상적 표현으로 바꿈.
- "going home" → "strategic regrouping"
- "both hit at once" → "activate simultaneously"
- "looked for work" → "conducted targeted job search"

**체크**: "혼잣말로 이 상황을 설명한다면 이 단어를 쓸까?"

### 7. 화행(Speech Act) 오인
AI가 상황의 의사소통 목적을 잘못 읽는다. 허락을 구해야 하는 상황에서 일방적으로 공유/선언하고, 제안해야 하는 상황에서 단정 짓고, 질문해야 하는 상황에서 결론을 내린다. 글의 형식(정중한 어미, 불릿 정리)은 맞는데 화행 자체가 틀린 것.
- "먼저 공유드립니다" (선언) → "진행해도 괜찮을지 의견 여쭤보고자 합니다" (요청)
- "이렇게 진행하겠습니다" (통보) → "이렇게 진행해도 될까요?" (허락 구하기)
- 커리어 메모에서 결론 단정 → 실제로는 고민 중인 사안

**체크**: "이 글을 받는 사람이 해야 하는 행동이 무엇인가? 승인? 검토? 정보 수령? 그 행동에 맞는 화행인가?"

### 8. 부정 나열 과잉 (면책 조항 증후군)
AI가 "하지 않는 것"을 길게 나열해서 안심시키려 한다. 실제로는 많이 나열할수록 불안해 보이고, 뭔가 숨기는 것처럼 읽힌다.
- "사업 전략, 조직 구조, 인사, 사내 수치, 기타 민감 주제는 일절 다루지 않습니다" → "AI 프로젝트 방향이나 조직 관련 내용은 다루지 않습니다"
- 보안 면책 3줄 → 핵심 1줄

**체크**: "부정문이 2개 이상 연속이면 가장 중요한 1개만 남겨도 의미가 전달되는가?"

### 9. 간접화법 누락 (voice flattening)
AI가 남의 말이나 외부 정보를 자기 주장처럼 1인칭 평서문으로 쓴다. 한국어에서는 "~한다고 합니다", "~라고 합니다"로 출처를 신호해야 하는 경우가 많다.
- "개인 커리어 경험 범위에서만 진행합니다" → "개인 커리어 경험 범위에서만 진행한다고 합니다" (웍스피어 측 설명 전달)
- 리서치 문서에서 "X는 Y이다" → "Z에 따르면 X는 Y이다"

**체크**: "이 정보의 출처가 나인가, 남인가? 남이면 간접화법 표지가 있는가?"

### 10. 마무리를 선언으로 닫음
AI는 글의 끝을 조건부 선언("~하겠습니다")으로 닫는다. 사람은 대화를 여는 질문으로 닫는 경우가 많다. 특히 승인/피드백을 기다리는 맥락에서 선언으로 끝나면 "네 의견은 필요 없다"는 느낌을 준다.
- "괜찮으시면 올리겠습니다!" → "진행해도 될지 궁금합니다"
- "정리 완료했습니다." → "이 방향으로 괜찮을까요?"

**체크**: "이 글 뒤에 상대방이 답할 공간이 있는가? 없으면 대화가 아니라 통보."

### 11. 도메인 용어 회피
AI가 해당 조직/분야에서 실제로 쓰는 용어 대신 안전한 일반 동사를 쓴다. 결과적으로 그 조직에 속하지 않은 사람이 쓴 글처럼 읽힌다.
- "올리다" → "상신하다" (사내 결재 맥락)
- "보내다" → "배포하다" (릴리스 맥락)
- "만들다" → "기안하다" (공문서 맥락)

**체크**: "이 조직에서 이 행위를 부를 때 실제로 쓰는 동사는 무엇인가?"

## Medium-Aware Tone (매체별 톤 분기)

같은 내용이라도 매체에 따라 허용되는 구조화 수준이 다르다. 대상 텍스트의 매체를 먼저 파악하고 그에 맞는 톤을 적용한다.

| 매체 | 구조화 수준 | 특징 |
|------|-----------|------|
| 문서 (markdown, 보고서) | 높음 | 헤더, 테이블, 넘버링 허용 |
| 이메일 | 중간 | 간단한 인사/마무리, 불릿 위주, 볼드 최소 |
| 메신저/DM | 최소 | 불릿만, 한 문장 오프닝, 별도 클로징 없음, 볼드 헤더 금지 |

메신저 메시지를 문서처럼 포맷팅하는 것은 가장 흔한 AI 실수 중 하나다. 리더에게 보내는 업무 DM에 볼드 넘버링과 별도 요약 문단이 들어가면 즉시 AI가 쓴 것으로 느껴진다.

### AI가 잘 못하는 것: 실용적 다음 스텝 제안

AI는 정보를 정리하고 요약하는 데 강하지만, "줌으로 간단하게 의견 주셔도 좋을 것 같습니다" 같은 실용적이고 구체적인 다음 행동 제안은 잘 하지 못한다. 이런 한 줄이 메시지를 자연스럽게 만든다. 메신저/이메일 톤에서는 정보 나열 후 구체적 액션을 제안하는 패턴을 의식적으로 적용한다.

## Corrections Log

교정한 before/after를 `references/30-correction-examples.md`에 축적한다.
- 유저가 승인한 교정만 기록 (자동 제안 중 거부된 것은 기록하지 않음)
- 다음 humanize 실행 시 이 파일을 읽고 유사 패턴을 참고 (few-shot learning)
- 시간이 지나면 이 파일 자체가 유저 맞춤 wording guide가 됨

## Safety

- 사실 관계는 절대 변경하지 않음. 표현만 수정.
- 전문 용어가 해당 맥락에서 정확히 맞으면 유지 (DDD, Hexagonal, LLM-as-Judge 등은 업계 표준).
- 메타포가 의도적이고 효과적이면 유지 — 모든 비유를 제거하는 것이 목적이 아님.
- 교정 시 원래 의미와 뉘앙스를 보존.

## Outputs

### Correction mode
- Before/after 쌍 목록 (카테고리별 그룹)
- 수정된 문서

### Guide mode
- 다른 스킬이 참조할 규칙 (references/ 파일)

## Eval Criteria

1. SKILL.md 체크리스트 실행 후 flagged 패턴 0개
2. 원문 사실/데이터 보존

## 완료 전 자체 검증

Eval Criteria의 각 항목을 확인하고, 미충족 항목이 있으면 사용자에게 보고한 뒤 수정.
