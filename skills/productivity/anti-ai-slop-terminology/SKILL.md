---
name: anti-ai-slop-terminology
description: >
  Detect and replace AI-slop terminology in any user-written or AI-drafted text:
  docs, code comments, PR bodies, Jira tickets, wiki pages, Slack messages.
  Catches English LLM slop ("surface", "contract", "leverage", etc.) and Korean
  LLM slop ("봉투", "사양", "본 PR", etc.) by web-researching
  each suspect term against official docs, textbooks, papers, and community
  usage from the actual domain. Suggests replacements drawn from how
  practitioners in that domain actually write.
  TRIGGER: "리뷰해줘 ai slop 없는지", "이상한 용어 안 썼는지", "naturalize
  terminology", "term check", "anti-slop review", "industry-standard 표현으로
  바꿔줘", or whenever the user is writing/reviewing a document and wants
  industry-grade phrasing. Also trigger proactively after writing any doc /
  PR body / Jira ticket / wiki page if length > ~30 lines.
  NOT for: simple grammar / typo fixes (use spell-check), AI-tone removal
  on already-good terms (use im-not-ai), pure Korean polish (use im-not-ai
  for naturalness, this skill for term selection).
version: 1.0.0
tags:
  - writing
  - terminology
  - code-review
  - documentation
  - anti-slop
---

# Anti AI-Slop Terminology

LLM 들이 "전문 용어처럼 보이는" 단어 (surface, contract, canonical, envelope, 봉투, 사양 등) 를 분야 무관하게 멋대로 뿌리는 습관을 잡아내고, 실제 그 분야 (공식 문서, 개론서, 논문, 커뮤니티) 에서 쓰는 표현으로 교정한다.

핵심 가설: 어떤 단어가 적절한지 머릿속 직관만으로 판단하지 않는다. **그 분야의 1차 자료 (official docs, textbooks, papers, community discussion) 가 그 단어를 그 의미로 실제 쓰고 있는가** 를 web research 로 검증한다.

## Quick Start (80% case)

사용자가 "리뷰해줘", "ai slop 없는지", "이상한 용어 안 썼는지" 같은 요청을 했을 때:

1. **대상 텍스트 식별**. 어떤 파일 또는 어떤 글 범위인지 확인. 명시 안 됐으면 최근 작성 / 수정된 글 후보 제시.
2. **의심 단어 스캔**. `references/known-slop-terms.md` 의 알려진 리스트로 1 차 grep + 본문 도메인 (그 글의 분야: 메트릭, A2A, ML, frontend 등) 에 어울리지 않는 단어 후보 식별.
3. **각 의심 단어 web research** (`references/verification-procedure.md` 절차 따름). 그 분야의 공식 문서 + 개론서 / textbook + 학술 / 논문 + 커뮤니티 (Stack Overflow, GitHub issue, reddit, HN, 블로그) 가 그 단어를 그 의미로 쓰는가 확인.
4. **검증 결과로 판정**:
   - 그 분야에서 그 의미로 쓰임 → keep
   - 다른 분야에서만 쓰임 / 의미가 다름 → 교체 후보 제시
   - 어디서도 자연스럽지 않음 → 교체 후보 제시
5. **권장 교체안 제시**. `references/replacement-patterns.md` 의 매핑 + research 결과로. 사용자 confirm 후 patch.

## Detailed Workflow

### 1. 대상 텍스트와 도메인 식별

- 파일 1 개면 그 파일.
- 여러 파일 / 짧은 글이면 사용자에게 확인.
- **도메인 식별이 가장 중요**. 같은 단어도 분야 따라 OK / NG. 예시:
  - "contract" = OK in **smart contract (blockchain)**, **API contract testing (pact / consumer-driven)**, **법률**
  - "contract" = NG in **일반 microservice 호출 인터페이스 정의** (그냥 interface / schema / API 라고 부름)
  - "surface" = OK in **3D graphics / 수학 / 화학 (반응 표면)**
  - "surface" = NG in **soft engineering / metric scope / "적용 범위" 의미** (그냥 scope / area / range)
  - "envelope" = OK in **항공 (flight envelope)**, **SOAP envelope (legacy XML protocol)**
  - "envelope" = NG in **JSON / REST API response wrapping** (그냥 wrapper / response shape)

도메인 식별 못 하면 사용자에게 "이 글 어느 분야 글이에요?" 1 줄 물어봄.

### 2. 의심 단어 1차 스캔

```bash
# known-slop-terms.md 의 리스트로 grep
grep -niE 'surface|contract|canonical|envelope|leverage|robust|delve|...' <file>
```

`references/known-slop-terms.md` 에 카테고리별 리스트 있음:
- 영어 일반 LLM slop (delve, tapestry, multifaceted, robust, leverage 등)
- 영어 SW 엔지니어링 분야 LLM 오용 (surface, contract, canonical, envelope, semantic, paradigm, ecosystem 등)
- 한국어 LLM slop (봉투, 사양, 본 PR, 정합성 검증, 동일성을 담보 등)

1 차 grep 결과 + 본문 직접 read 로 의심 단어 후보 결정. **grep 결과만 보고 판정하지 말 것**. 문맥 따라 OK 일 수 있음.

### 3. Web research + 워크스페이스 grep 검증 (필수 단계)

각 의심 단어 / 후보에 대해 5 종 자료 (없는 자료는 명시). LLM 시대 web 글이 LLM 으로 오염되었으므로 가중치 다름:

| 자료 종류 | 도구 | 확인 사항 | 가중치 |
|---|---|---|---|
| 공식 spec / RFC / textbook | WebFetch on docs.* / *.dev / official spec | 그 분야 표준 문서가 그 단어를 그 의미로 쓰는가 | +1 |
| 사람 작성 GitHub issue / Stack Overflow / 논문 (arxiv) | WebSearch site:stackoverflow.com / arxiv.org / github.com issue | 실제 practitioner 가 그 단어를 어떻게 쓰는가 | +1 |
| **사용자 본인 워크스페이스 글** | `grep -rn <term> ~/git/<workspace>/` (예: `grep -rn "contract" /Users/user/git/ad-agent-metrics/`) | 작성자 본인 / 팀 글에 어떻게 쓰는가 (가장 가치 높음) | +2 |
| 공식 vendor docs (README, blog 본문) | WebFetch | conceptual term 정의는 신뢰, 본문 verb / adjective 는 별도 검증 | +0.5 |
| 2023 이후 blog / Medium / dev.to | WebSearch | LLM 오염 가능성 크므로 가중치 낮춤 | +0.3 |

**한국어 단어** 검증은 한국어 공식 문서 + 한국어 커뮤니티 (kldp, geeknews, okky 등) + 한국어 학술 자료 + 영문 원어를 한국어로 번역한 표준 용어집 (예: 한국정보통신기술협회 TTA 용어집). + 워크스페이스 본인 한국어 docs grep 동일하게.

판정 기준:
- 점수 합 4 이상 (워크스페이스 +2 포함 가능) → keep
- 점수 합 2 ~ 3 → Borderline. 대체안 있으면 권장 (강제 X)
- 점수 합 0 ~ 1 → 교체 권장
- 점수 합 -1 ~ 0 (워크스페이스 0 건 + 외부 자료 약함) → 강력 교체

### 4. 교체안 도출

`references/replacement-patterns.md` 의 자주 등장하는 mapping 확인:

| Slop | 분야 | 권장 대체 (영어) | 권장 대체 (한국어) |
|---|---|---|---|
| surface (적용 범위) | SW eng | scope, area, range | 범위, 영역 |
| contract (API) | SW eng | interface, schema, API | 인터페이스, 스키마 |
| canonical (the right one) | SW eng | standard, official, reference | 표준, 공식 |
| envelope (response wrap) | REST API | wrapper, response shape | 래퍼, 응답 구조 |
| leverage (use) | 일반 | use | 쓰다, 사용하다 |
| robust (works well) | 일반 | reliable, well-tested | 안정적인, 검증된 |
| 정합성 검증 (compare) | SW eng | comparison, diff check | 비교, diff 확인 |
| 동일성을 담보 (same) | 일반 | matches, identical to | 같음, 일치 |

매핑 없으면 research 결과의 실제 표현을 그대로 가져옴.

### 5. 사용자 confirm + patch

전체 표 형식으로 결과 제시:

| 줄 | 원문 | 의심 단어 | 검증 결과 (공식/textbook/논문/커뮤니티) | 교체안 | 비고 |
|---|---|---|---|---|---|

사용자 OK 후 Edit / Write 로 patch. patch 후 grep 으로 재확인.

## Reference Files

| 파일 | 언제 읽기 | 내용 |
|------|----------|------|
| `references/known-slop-terms.md` | 1 차 grep 전 항상 | 영어 일반 + 영어 SW + 한국어 알려진 slop 단어 리스트 |
| `references/verification-procedure.md` | web research 들어갈 때 | 5 종 자료 별 검색 명령 / 평가 기준 |
| `references/replacement-patterns.md` | 교체안 도출 시 | 자주 나오는 slop → 대체 매핑 + 분야별 예외 |

## Gotchas

### 공식 vendor docs 도 LLM slop 多

대형 vendor 의 공식 docs README 도 2024 ~ 2026 이후 LLM 으로 쓴 부분이 많음. vendor README 에 다음 LLM slop 단어가 다수 등장할 수 있음:

- "leverage LLM-driven dynamic routing"
- "Utilize pre-built tools"
- "scale seamlessly"
- "comprehensive documentation reference"
- "Rich Tool Ecosystem"

대응 룰:
- vendor docs 의 **conceptual term 정의** (예: ADK 의 `orchestrator`, `session`, `artifact`, `agent`, `tool`) 는 신뢰
- vendor docs 의 **본문 표현 (verb / adjective)** 은 별도 검증
- vendor docs 가 LLM 으로 쓰였다는 신호: marketing fluff ("rich", "seamless"), 동의어 반복, 글 길이 대비 정보 밀도 낮음

### 사용자 본인 워크스페이스 글이 best reference

사용자 본인 / 본인 팀이 작성한 docs (README, AGENTS.md, CLAUDE.md, 내부 wiki) 가 검증의 5 번째 자료. **공식 docs 보다 가치 높을 수 있음** (작성자 본인의 자연스러운 vocabulary 직접 반영).

procedure:
1. 의심 단어가 사용자 워크스페이스 안 다른 글에 등장하는지 grep
2. 등장하면 → 사용자 vocabulary 일부, keep
3. 안 등장하면 → LLM 이 새로 박은 표현, 의심 강화

예: `grep -rn "contract" /Users/user/git/ad-agent-metrics/` 결과로 팀 README 의 "I/O Contract" 발견 → contract 사용 OK

### 다중 도메인 글의 단어 검증

한 글이 여러 도메인 (metrics + observability + A2A + microservices 등) 걸칠 때 같은 단어가 도메인 따라 OK / NG. 단어 등장 위치마다 그 자리의 도메인 식별 후 검증.

예: "service boundary" 가 DDD 맥락 (OK) vs 일반 "scope" 대체 (NG) 같은 분리.

### LLM 시대 web 검색의 신뢰 함정

2023 ~ 2026 사이 blog / Medium / dev.to 글이 LLM 으로 쓰여 표현 패턴이 LLM slop 으로 오염됨. 검증 시 신뢰도 순서:

1. **공식 spec / RFC / textbook 출판물** (LLM 영향 적음)
2. **사람 작성 GitHub issue / Stack Overflow** (사람 의견 다수)
3. **사용자 본인 워크스페이스 글** (작성자 본인 vocabulary)
4. **공식 vendor docs README** (LLM 작성 가능성 있음, conceptual term 만 신뢰)
5. **2023 이후 blog / Medium** (LLM 오염 가능성 크므로 가중치 낮춤)

LLM 작성 글 판별 신호: "furthermore", "moreover", "it's important to note", "tapestry", "delve into" 다수 등장 + 글 전체가 동일 rhythm / 동일 길이 문장.

### 영어 단어 + 한국어 동사 mix slop

LLM 이 한국어 글에 영어 형용사 / 명사 단독 박고 한국어 동사로 연결하는 패턴이 자주 발생:

- "honest 채움" / "honest 하게 채우는" → "정직하게 채움" / "사실대로 채우는"
- "wired 상태" → "연결된 상태"
- "framing 작성" / "방어 framing" → "응답 문구 작성" / "방어 응답 문구"
- "단계 ramp" → "단계 도입" / "점진적 도입"

표준 IT 영어 hyphen 표현 (single-line JSON, request-scoped state, in-memory hold, caller-side observation) 은 한국어 글에 자연. 다만 **informal 영어 단어 + 한국어 동사 / 명사 mix** 는 LLM slop.

판정: 그 영어 단어가 IT 표준 hyphen 표현 또는 정식 type 명인가 vs 일반 informal 영어 단어인가.

### "본 X" 자기 지칭 패턴 종합 grep

"본 PR", "본 레포", "본 sub-agent", "본 시스템", "본 작업", "본 문서", "본 정책", "본 표", "본 작성자", "본 모듈", "본 스킬" 모두 같은 slop 패턴 (정부 보고서 / 격식 자기 지칭). 한 종류만 검사하면 다른 변형 놓침.

검증 grep:
```bash
grep -nE '본 (PR|레포|sub-agent|시스템|모듈|작업|문서|정책|스킬|skill|표|작성자|글)' file.md
```

### 도메인 무시 판정 금지

같은 단어가 분야에 따라 OK / NG. **도메인 식별 없이 grep 결과만 보고 "다 NG" 라고 단정하면 안 됨**. 예시:

- `contract` in **a smart contract codebase** → 100% OK
- `contract` in **a REST API document about envelope vs wrapper** → AI slop 의심 (그냥 interface / schema)
- `surface` in **3D graphics / GIS** → OK
- `surface` in **메트릭 정책 적용 범위** → AI slop (그냥 scope / 범위)

도메인 모르면 사용자에게 1 줄 묻기. 추측 금지.

### Web research 안 하고 직관 판정 금지

LLM 본인 head 속 "그 분야에서 그 단어 쓰는 거 같음" 같은 직관은 거짓일 가능성 큼. **반드시 WebFetch / WebSearch 로 1 차 자료 confirm**. 직관만으로 판정하지 말 것.

reverse 도 동일: "이건 분명 AI slop" 직관도 web research 로 confirm. 그 분야의 실제 표준 표현일 수도.

### 사용자 본인 글의 1 인칭 표현 검증 강도 다름

사용자가 본인 PR / 본인 Jira / 본인 Slack 본문 작성 중인 경우 → 자연스러움 우선 (의도 보존). 강제 교체 X, 후보 제시만.

사용자가 LLM 이 생성한 글 리뷰 의뢰한 경우 → 더 적극적인 교체 제안.

이 두 모드 구분은 사용자에게 1 줄 확인.

### 한국어 LLM slop 의 특수 패턴

한국어는 영어 mapping 1:1 안 됨. AI 가 영어 → 한국어 번역하면서 만들어내는 잘못된 표현이 많음:

- "envelope" → "봉투" (SOAP envelope 류 legacy 외에는 NG)
- "specification" → "사양" (자동차 / 하드웨어 spec 외에는 NG. SW 는 그냥 "스펙")
- "upstream" → "본가" (무협지 톤. 그냥 "원본 레포" 또는 "upstream")
- "본 PR / 본 레포 / 본 시스템" (정부 보고서 어투)
- "...하는 것이 ...의 목표입니다" (격식 술어)
- "X 사이클" / "정합성 검증" / "동일성을 담보" (추상 한자어 명사화 + 책임 회피 술어)

한국어 검증 시 본 사용자의 `~/.claude/rules/writing-style.md`, `pr-jira-tone.md`, `external-facing-strings.md` 의 어휘 룰 cross-check.

### Validation 후 grep 재확인 필수

patch 적용 후 다시 grep 으로 원래 의심 단어가 본문에 남아 있는지 확인. Edit 도중 일부만 치환되는 경우 자주 발생.

```bash
grep -niE '<slop terms>' <file>
```

### Surface / scope 등 단어 자체가 항상 slop 인 건 아님

- `surface` = OK in CSS (`surface color`), Material Design (`Material surface`), 3D graphics, geology
- `surface` = OK in `attack surface` (security 정식 표현)
- `surface` = NG in "정책 적용 surface", "검증 surface"

**판정은 도메인 + 의미 + practitioner 실사용** 3 가지로. 단어 자체로 black list 만들면 false positive 폭주.

### LLM 의 "이 단어 자연스러움" 자기 판정의 bias

LLM 은 본인이 자주 쓰는 단어를 "자연스럽다" 고 잘못 판정하는 경향. AI slop 단어가 LLM 한테는 정상으로 보임. 그래서 **web research 가 이 스킬의 핵심**. 직관 검증 단계 우회하면 스킬 의미 0.

## 적용 범위

- 사용자가 작성한 markdown 문서 (docs/, wiki/, README, AGENTS.md 등)
- 코드 안 docstring / 주석 (영어 / 한국어 둘 다)
- PR 본문, Jira ticket, GitHub Issue 본문
- Slack / Confluence 직장 글
- AI 가 생성한 finding / report / draft

NOT for: 코드 그 자체 (변수명, 함수명, 클래스명, enum 값 → 코드 컨벤션 별도), 외부 라이브러리 reference 안의 단어 (그건 그 라이브러리 표준)

## 관련 룰 / 스킬

- `~/.claude/rules/writing-style.md`: 한국어 punctuation / 어휘 / cross-doc reference 룰
- `~/.claude/rules/pr-jira-tone.md`: PR / Jira / Slack 본문 어투 룰
- `~/.claude/rules/response-style.md`: 사용자 답변 self-containment 룰
- `~/.claude/rules/external-facing-strings.md`: UI / 제품 노출 텍스트 룰
- skill `im-not-ai`: AI 티 (장황함) 제거. 이 스킬은 그것과 별개로 **단어 선택 정확성** 에 집중
- skill `dev-doc-style`: 문서 구조 5 줌 레벨. 이 스킬은 그 안의 단어 선택을 추가 검증
