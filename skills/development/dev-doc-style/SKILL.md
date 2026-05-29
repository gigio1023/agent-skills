---
name: dev-doc-style
description: >
  개발 레포의 markdown 문서 (README, AGENTS.md, docs/*.md, *.mdx) 를 작성하거나 수정할 때
  적용하는 글쓰기 스타일 가이드. 한 문서가 사실 + 단서 + 출처 + 예외 + 옵션 + 링크를 줄줄이 같이 다는
  anti-pattern 을 끊고, 5 줌 레벨 (sentence / bullet / section / page / cross-page) 룰을 enforce.
  트리거: markdown 파일 작성/수정, "문서 정리해줘", "README 다듬어줘", "이 문서 장황해", "doc 가이드 적용",
  "writing style 적용", "dev-doc-style 적용", 새 docs/ 페이지 생성. 한국어 / 영어 / mix 모두 적용.
  NOT for: 기술 문서 신규 작성(use dev-tech-spec-docs), PR 본문(use write-pr), AI 티 제거(use im-not-ai).
  본 스킬은 doc 본문 구조와 zoom-level 정리에 집중.
version: 1.0.0
tags:
  - documentation
  - markdown
  - writing-style
  - korean
---

# dev-doc-style: 개발 문서 글쓰기 스타일

핵심 한 줄: **한 메시지 = 한 표면.** 본문에 사실만, 단서 / 출처 / 예외 / 정책은 별도 표면 (admonition / details / 다른 페이지) 으로 분리한다.

근거: langchain-ai/docs (`AGENTS.md` Vale 룰), pydantic/pydantic (`docs/concepts/*.md` 의 `!!! note` / `???` / `===` 분리).

## Quick rules

| Zoom | Rule | 빠른 판정 |
|---|---|---|
| Sentence | 한 문장 = 한 사실. em-dash `—` / middle-dot `·` / bullet `•` 본문 0 회 (im-not-ai J-0). 출처 라벨 (Wiki §x.y 등) 본문 금지 | 한 문장 안에 사실 + 단서 + 출처가 있으면 깬다. em-dash / middle-dot 가 한 번이라도 등장하면 깬다 |
| Bullet | Form A `**라벨**: 한 문장.` / Form B 완결된 한 문장 / Form C `**라벨**:` + nested 1 단 list. **sub-fact 2 개 이상이면 무조건 nest** (inline comma 합치기 금지). 4 개 이상 + 동등 무게면 Form C 강제 | bullet 안에 sub-fact 가 2 개 이상인데 inline 으로 우겨넣었으면 깬다. nested 2 단 이상이면 깬다 |
| Section | 도입문 ≤ 1 문장. 단순 anchor 보다는 WHY 한 문장이 가치 있다. 단서 / 정책 / 우선순위는 admonition 또는 다른 페이지 | 섹션 시작이 두 문장 이상 단락이면 깬다 |
| Page | 한 페이지 = 한 토픽. 메타 섹션 (`## Notes` `## More docs` `## References` `## 관련 문서`) 폐기 | 끝에 메타 섹션이 있으면 깬다 |
| Cross-doc ref | 다른 문서 가리킬 때는 **descriptive link** `[설명 (어디)](경로)` 한 단위 또는 omit. bare path / raw URL 본문 등장 금지 | bare path `` `docs/spec/foo.md` `` 가 본문에 떨어져 있으면 깬다 |
| Cross-page | 같은 사실 두 곳에 베끼기 금지. self-containment 포기 | 같은 표 / 리스트가 두 페이지에 있으면 깬다 |

## 적용 순서

문서 작성 / 수정 시 다음 순서로 점검합니다.

1. **트리거 확인**: 작업 대상이 markdown 문서 본문이면 본 스킬 적용. PR 본문 (`/tmp/pr-body.md` 등) 은 `write-pr` 스킬 사용.
2. **분량 예산 확인**: 페이지 길이 표 (아래) 와 비교. 예산 초과면 토픽 분할 신호.
3. **Quick rules 표** 5 개 룰을 한 번 훑어 위반 패턴 식별.
4. **상세 룰 / 변환 사례 필요 시** `references/zoom-rules.md` (줌 레벨별 Bad/Good), `references/anti-patterns.md` (Don't list + 변환 사례) 참조.
5. **PR 직전** `references/checklist.md` 의 체크리스트로 머지 전 확인.

## 페이지 분량 예산

| 페이지 종류 | 줄 수 |
|---|---|
| Stub / 인덱스 / redirect | 20–80 |
| 좁은 작업 가이드 | 80–150 |
| 개념 페이지 | 100–250 |
| 깊은 토픽 | 250–800 |
| 800 줄 초과 | 토픽이 너무 큼. 쪼갠다 |

README 는 100 줄 이하를 권장. quick start + 인덱스 역할만 두고, 토픽 본문은 `docs/*.md` 로 분리.

## 메시지 유형별 표면

본문에 사실만 두고, 다른 메시지 유형은 별도 표면으로 옮깁니다.

| 메시지 유형 | 표면 | 예 |
|---|---|---|
| 사실 / 절차 | 본문 | "Bearer 인증을 활성화합니다." |
| 보충 / 컨벤션 출처 | `> [!NOTE]` | "Wiki 는 일반 슬롯입니다. 본 레포가 표준 형식을 정의합니다." |
| 위험 / Breaking | `> [!WARNING]` | "Skill ID prefix 변경은 Orchestrator 재배포가 필요합니다." |
| 팁 / 바로가기 | `> [!TIP]` | "검증은 `uv run soap-conformance` 한 줄로 끝납니다." |
| 긴 부연 | `<details><summary>...</summary>...</details>` | 36 줄 코드, 풀 출력 예시 |
| API 진입점 링크 | 인라인 백틱 + 링크 | `` `record_task()` ([audit_log](audit_log.md)) `` |
| 운영 / 작업 추적 (Jira key, PR #, 담당자, 일정) | **스펙 / 가이드 문서 본문 금지**. 별도 surface 로 분리 | PR description, Jira issue body, runbook |

## 한국어 / 영어 mix 가이드

- 기술 용어 (FastAPI, Bearer, Skill ID, conformance, ArtifactMetadata) 는 영어 그대로.
- 조사 / 연결어 / 종결어만 한국어. 예: "Bearer 인증을 활성화합니다."
- 문장이 길어져 가독성이 떨어지면 한국어로 풀어 쓴다. 짧고 직설적이면 영어 비중 높여도 됨.
- 단서 약화 표현 (`-할 수도 있고`, `-할 수도 있습니다`, `필요하다면`, `상황에 따라`, `옵션입니다`) 의 절반은 의미 손상 없이 삭제 가능. 빼라.
- 명령형 현재형 우선. "할 수 있습니다" → "합니다".
- 슬랭 / 비공식 어휘 금지. 기술 문서 본문에는 정확한 동사 사용:
    - "박다" / "박음" / "박힘" / "박혀" → "추가" / "포함" / "기록" / "설정" / "전달" / "넣다"
    - "복붙" → "복사" 또는 "복제"
    - "짤방" → "캡처"
    - "직각" → "즉시"
    - "굴리다" → "실행"
    - "떡칠" → "남용"
- 풀이 비례 룰. 독자 컨텍스트별 풀이 정도 조절:
    - 내부 위키 / 팀 문서: 통용 도메인 약어 (`A2A`, `SOAP`, `orchestrator`, sub-agent 이름) 의 풀이 생략. 독자가 다 알고 있음
    - 외부 노출 / 신규 입사자 onboarding 문서: 첫 등장 시 한 줄 풀이
    - 트레이드오프 명시: response-style.md 의 self-containment 룰은 외부 / 신규 독자 컨텍스트용. 내부 팀 문서에 그대로 적용하면 통용 약어마다 괄호 풀이가 박혀 독자 노이즈 증가

## Top 6 patterns (즉시 적용)

1. **메타 섹션 폐기.** 페이지 끝의 `## Notes` `## More docs` `## References` `## 관련 문서` `## 더 보기` 일괄 삭제. 필요한 링크는 본문 인라인 또는 단일 `docs/index.md`.

2. **bullet shape 세 개.** 모든 bullet 을 (a) `**라벨**: 한 문장.`, (b) 완결된 한 문장, (c) `**라벨**:` + nested 1 단 list 중 하나로. **sub-fact 가 2 개 이상이면 nested (Form C) 강제**: comma 로 한 줄에 우겨넣지 않는다. **flat inline 은 sub-fact 1 개일 때만 default**. 항목이 4 개 이상이고 동등한 무게면 (c) 가 가독성 우수. nested 2 단계 이상은 금지.

3. **출처 라벨 본문 금지 + bare path 금지.** `(Wiki §x.y)` `(boilerplate 컨벤션)` 본문 박기 금지. 인용구 prefix (`권위 출처:`, `Source:`, `참고:`) 도 제거: 링크 자체가 자기 정체를 설명한다. 다른 문서를 가리킬 때는 **descriptive link** `[무엇 (어디)](경로)` 한 단위로 적거나 본문에서 빼라. bare path (` `docs/spec/foo.md` `) 나 raw URL 만 본문에 떨어뜨리면 독자는 클릭하지 않고 사실상 단서가 사라진다.

4. **Code-first.** 한 문장 컨텍스트 → 코드 → 1–3 문장 주석. 도입 단락 + 정책 인용 + 우선순위 라벨 + 외부 링크 4 단 패턴 금지. 코드 결과는 `#>` / `"""` 인라인.

5. **한 페이지 한 토픽 + self-containment 포기.** conformance 5 항목 같은 레포 단위 사실은 한 곳 (`docs/conformance.md`) 에만. 다른 페이지는 링크 한 줄.

6. **도입 직후 시각화.** 페이지 / 절 도입은 1 문장 + 즉시 코드 / mermaid / 표. 줄글로 결론 / 도입 단계 / 정책 풀어쓰면 묻힘. 줄글 단락이 두 개 이상 이어지면 핵심 정보 (도입 결정, 첫 코드, breaking change) 를 별도 시각화 surface 로 끌어올리기. 줄글은 시각화 사이의 transition 또는 1 ~ 3 문장 보조 주석으로만.

## Reference Files

| File | 언제 읽나 | 내용 |
|------|----------|------|
| `references/zoom-rules.md` | 룰 위반 패턴을 발견했을 때, 변환 방법이 헷갈릴 때 | 5 줌 레벨 (sentence / bullet / section / page / cross-page) 별 상세 룰 + Bad/Good 예시 |
| `references/anti-patterns.md` | "이건 어떻게 고치지" 가 떠오를 때, 진단서 anti-pattern 변환 시 | Don't list (즉시 제거 패턴) + 진단서 5 안티패턴 → 패턴 변환 사례 |
| `references/checklist.md` | 문서 PR 머지 전, 본인 셀프 리뷰 시 | 10 항목 체크리스트 |

## Gotchas

- **트리거 혼동.** 본 스킬은 doc 본문 구조 (zoom 레벨 룰). 어조 / AI 티 / 문장 윤문은 `im-not-ai` 스킬. PR 본문 형식 / 분량은 `write-pr` 스킬. 같은 PR 에서 셋이 같이 적용될 수 있음. 충돌 시 본 스킬이 본문 구조를 잡고 im-not-ai 가 어조를 잡도록 순서 분리.

- **self-containment 포기는 trade-off.** 한 페이지만 봐서는 모르는 상태가 됨. 사용자 / 팀 합의가 필요한 항목. 합의 안 된 레포에서는 적용 전에 한 번 확인. 진단서 `해결 방향성` 절 참고.

- **분량 예산은 신호이지 강제 아님.** 800 줄 넘는다고 무조건 쪼개는 게 아니라 "토픽이 너무 큰 거 아닌가" 의 trigger. langchain quickstart.mdx 는 1394 줄 (대부분 코드 변형). 코드 비중이 높으면 길어도 됨.

- **메시지 유형 표면 분리는 GitHub-flavored markdown 기반.** mkdocs-material 컴포넌트 (`!!! note`, `???`, `===`) 는 본 레포에 없으므로 GitHub `> [!NOTE]` / `<details>` 로 대체. 대상 플랫폼이 다르면 (예: mintlify, mkdocs) 표기는 그 플랫폼 컨벤션으로.

- **메타 섹션 일괄 삭제 시 외부 참조 깨짐 주의.** `## References` 등을 삭제할 때 내부 링크 (`#references`) 가 끊길 수 있음. grep 한 번 돌려 확인.

- **단서 약화 표현 무조건 삭제 X.** "필요하다면", "옵션입니다" 가 정말로 조건부 동작을 표현할 때는 유지. anti-pattern 은 "장식용 단서": 빼도 의미 그대로면 단서가 아니라 사족.

- **"한 사실 = 한 페이지" 의 conformance 5 항목 예외.** README 의 quick start 안에서 `soap-conformance` CLI 호출은 보여줘야 사용자가 그 자리서 검증 가능. 같은 사실의 "요약 1줄 + 링크" 는 중복으로 치지 않는다. "동일 5 항목 표가 세 페이지에 있는 것" 만 anti.

- **README 100 줄 이하는 권장 가이드라인.** 본 레포 README 가 현재 206 줄. 분할 시 quick start (50줄) + 인덱스 (30줄) 만 두고 build paths / conformance / migration / observability 모두 별도 페이지로. 합의 후 일괄 정리.

- **줄글 도입 단락은 묻힌다.** 페이지 / 절 시작에 줄글 두 문단 이상 이어지면 독자가 결론을 못 잡음. 핵심 정보 (도입 단계 결정, breaking change, 첫 코드) 는 즉시 코드 / mermaid / 표로 표시. 페이지 첫 화면이 줄글이면 거의 항상 시각화로 끌어올리기. 본 룰의 출처는 user 가 도입문 줄글 dump 패턴을 반복 지적한 케이스.

- **스펙 surface 와 운영 surface 혼동 금지.** 스펙 / 정책 / 가이드 문서에 PR / Jira / 담당자 / 일정 같은 작업 추적 정보 섞으면 독자가 무엇이 spec 인지 무엇이 진행 상황인지 분리 못 함. spec 은 spec 만. 작업 추적은 별도 surface (PR description, Jira issue body, runbook) 로 분리. 본 룰의 출처는 user 가 위키 페이지에서 운영 lane (Jira key / PR follow-up) 명시 제거 요청한 케이스.
