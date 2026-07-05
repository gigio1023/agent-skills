# Verification Procedure

의심 단어를 발견했을 때 5 종 1차 자료로 검증하는 절차. 이 스킬의 핵심.

## 핵심 원칙

LLM 본인 head 속 직관은 bias 가 큼. LLM 이 자주 쓰는 단어를 "자연스럽다" 고 잘못 판정. **반드시 외부 자료로 confirm**.

검증은 5 종 자료 (없는 자료는 명시). LLM 시대 web 글이 LLM 으로 오염되었으므로 자료 신뢰도 순서:

1. **공식 spec / RFC / textbook 출판물**: 가장 신뢰. LLM 영향 적음
2. **사람 작성 GitHub issue / Stack Overflow / 학술 논문 (arxiv)**: 사람 의견 다수
3. **사용자 또는 팀 워크스페이스 글**: 작성자 또는 팀 vocabulary (~/git/<workspace>/ 안 README / AGENTS.md / CLAUDE.md / docs/*.md, 예: /Users/user/git/ad-agent-metrics/)
4. **공식 vendor docs 본문 / README**: LLM 작성 가능성 있음. **conceptual term 정의만 신뢰**, 본문 verb / adjective 는 별도 검증
5. **2023 이후 blog / Medium / dev.to**: LLM 오염 가능성 크므로 가중치 낮춤

LLM 작성 글 판별 신호:
- "furthermore", "moreover", "it's important to note", "tapestry", "delve into" 다수 등장
- 글 전체가 동일 rhythm / 동일 길이 문장
- 동의어 반복 ("comprehensive, complete, full" 한 문장 안)
- marketing fluff ("rich", "seamless", "scale seamlessly")
- 글 길이 대비 정보 밀도 낮음

## 단계별 절차

### Step 1: 도메인 명확화

의심 단어가 발견된 글의 도메인 식별. 같은 단어도 도메인 따라 OK / NG.

도메인 예시:
- web infrastructure, microservices, observability, metrics
- machine learning, LLM, NLP
- frontend (React / Svelte / CSS), backend, database
- networking, distributed systems
- security, blockchain
- graphics, gamedev, 3D
- mobile (iOS / Android)

도메인 모르면 사용자에게 1 줄 물어보기. **추측 금지**.

### Step 2: 공식 문서 검증

해당 도메인의 spec / standard / official docs 에서 그 단어를 그 의미로 쓰는지 확인.

```bash
# WebFetch 사용. 도메인별 공식 문서 사이트:
# - W3C: https://www.w3.org/TR/
# - IETF RFC: https://datatracker.ietf.org/
# - OpenTelemetry: https://opentelemetry.io/docs/specs/
# - Kubernetes: https://kubernetes.io/docs/
# - Python PEP: https://peps.python.org/
# - MDN: https://developer.mozilla.org/
# - React: https://react.dev/
# - Vendor docs: https://docs.aws.amazon.com/ 등
```

또는 WebSearch 로 `<term> site:opentelemetry.io` 등 도메인 지정:

```bash
WebSearch "surface site:kubernetes.io"
WebSearch "envelope site:rest.api"
WebSearch "contract site:martinfowler.com"  # martinfowler.com 은 architecture 표준
```

평가:
- 그 의미로 쓰임 → +1 점
- 다른 의미로 쓰임 → 0 점 (의심 강화)
- 안 나옴 → 0 점

### Step 3: Textbook / 개론서 검증

해당 분야 표준 textbook 의 색인 / 본문 검색.

예시 textbook:
- **Algorithms**: CLRS (Cormen), SICP (Abelson)
- **OS**: Tanenbaum, Silberschatz
- **Networking**: Kurose & Ross, Tanenbaum
- **Database**: Database System Concepts (Silberschatz)
- **Distributed Systems**: DDIA (Designing Data-Intensive Applications, Kleppmann)
- **ML**: Bishop, Goodfellow Deep Learning, Murphy
- **NLP**: Jurafsky & Martin
- **Microservices**: Sam Newman "Building Microservices"
- **SRE**: Google SRE book / SRE Workbook

검색:
```bash
WebSearch "<term> kleppmann ddia"
WebSearch "<term> google sre book"
WebFetch https://www.oreilly.com/library/view/...  # textbook 본문 페이지
```

평가:
- textbook 의 색인 / 본문에 그 의미로 등장 → +1 점
- 등장하지만 다른 의미 → 0 점 (의심 강화)
- 안 나옴 → 0 점

### Step 4: 논문 / 학술 검증

arxiv, Google Scholar, ACM Digital Library, IEEE Xplore.

```bash
WebSearch "<term> site:arxiv.org"
WebSearch "<term> filetype:pdf"  # 논문 PDF
WebSearch "<term> google scholar"
```

평가:
- 학술 paper 다수 등장 + 그 의미 → +1 점
- 학술 등장하지만 의미 다름 → 0 점
- 거의 안 나옴 → 의심 강화

### Step 5: 커뮤니티 / practitioner 검증

실제 개발자가 쓰는지 확인. 본 단계에서 LLM 이 가장 잘 빠지는 함정: blog post 가 다 다른 LLM 이 쓴 글이면 검증 가치 0. **개인 블로그 + Stack Overflow / GitHub issue 의 사람 의견** 우선.

```bash
WebSearch "<term> site:stackoverflow.com"
WebSearch "<term> site:reddit.com/r/programming"
WebSearch "<term> site:news.ycombinator.com"
WebSearch "<term> site:github.com issues"
WebSearch "<term> site:martinfowler.com"  # 신뢰 블로그
WebSearch "<term> site:simonwillison.net"
WebSearch "<term> site:lwn.net"  # Linux community
```

평가:
- 실 사용자 토론에 빈도 높음 + 그 의미 → +1 점
- 등장하지만 의문 / 비판 → 0 점
- 거의 안 나옴 또는 LLM 글만 → 의심 강화

### Step 6: 사용자 또는 팀 워크스페이스 검색 (가장 가치 높음)

가장 신뢰성 있는 자료. 사용자가 본인 또는 본인 팀이 작성한 글이 어떤 단어를 어떤 의미로 쓰는지 확인.

```bash
# 워크스페이스 전수 grep
grep -rniE '<term>' ~/git/<workspace>/
# 예: grep -rniE 'contract' /Users/user/git/ad-agent-metrics/

# 더 좁혀서 README / docs 만
find ~/git/<workspace> -maxdepth 3 -type f \( -name "README.md" -o -name "AGENTS.md" -o -name "CLAUDE.md" \) -exec grep -niE '<term>' {} +

# 사용자 또는 팀 작성 docs/ 디렉토리
grep -rniE '<term>' ~/git/<workspace>/docs/
```

평가:
- 사용자 또는 팀 글에 등장 + 그 의미로 쓰임 → **+2 점** (가장 가중치 큼. 작성자 또는 팀 vocabulary 라 자연)
- 사용자 또는 팀 글에 등장하지만 다른 의미 → 0 점
- 사용자 또는 팀 글에 0 건 → LLM 이 새로 박은 표현, 의심 강화 → -1 점

사용자 또는 팀 워크스페이스 안에 비슷한 도메인 글이 여러 개 있으면 빈도까지 측정. 1 회만 등장하고 LLM 영향 가능성 있으면 가중치 절반.

## 점수 종합 판정

| 5 종 자료 점수 합 | 판정 |
|---|---|
| 4 ~ 6 (Step 6 가중치 +2 포함) | Keep. 그 단어는 그 도메인에서 표준 표현 |
| 2 ~ 3 | Borderline. 더 자연스러운 대체안 있으면 권장 (강제 X) |
| 0 ~ 1 | 교체 권장. AI slop 의심 |
| -1 ~ 0 (사용자 또는 팀 글 0 건 + 외부 자료 약함) | 강력 교체 |

## 한국어 단어 검증

한국어 단어 검증은 자료 종류 변경:

| 자료 종류 | 한국어 자료 |
|---|---|
| 공식 문서 | TTA 정보통신용어사전 (https://terms.tta.or.kr/), 한국 표준 (KS) |
| Textbook | 한국어 번역서 / 한국인 저자 textbook |
| 논문 | RISS, DBpia, 학술논문 DB |
| 커뮤니티 | OKKY, GeekNews (news.hada.io), KLDP, 한국 블로그 (Velog, Tistory), 한국어 GitHub README |

검색:
```bash
WebSearch "<term> site:news.hada.io"
WebSearch "<term> site:velog.io"
WebSearch "<term> site:okky.kr"
WebSearch "<term> 정보통신용어"  # TTA
```

한국어 LLM slop 은 영어 → 한국어 직역에서 발생. 영어 원어가 무엇인지 추정 + 한국어 표준 번역어가 무엇인지 별도 검색:

```bash
WebSearch "envelope 한국어 표준 번역"
WebSearch "specification 한국어 번역 IT"
```

## 가짜 검증 (안 됨)

다음은 검증으로 인정 X:

- LLM 본인 직관 ("그 단어 자주 봤음" 같은 자기 보고)
- 다른 LLM 의 글 (블로그 / 트윗 / Medium post 중 LLM 생성물)
- AI 가 쓴 docs (요즘 일부 docs 도 LLM 생성)
- 1 회성 검색 결과 (1 개 link 만 보고 판정)

판별 가이드:
- "Furthermore", "It's important to note", "In conclusion" 등 LLM 패턴 단어가 다수 등장하는 blog → 신뢰도 낮음
- 2023 ~ 2026 사이 생성된 글이 모두 같은 표현을 쓰는데 그 이전 글에 없는 경우 → LLM 영향 의심
- 명시적으로 "by GPT" / "AI-generated" 표기된 글 → 검증 자료로 0 점

## 검증 결과 기록 양식

리뷰 결과 사용자에게 보고 시 다음 표 사용:

| 줄 | 원문 | 의심 단어 | 도메인 | 공식 | textbook | 논문 | 커뮤니티 | 점수 | 판정 | 대체안 |
|---|---|---|---|---|---|---|---|---|---|---|

점수 컬럼은 0 ~ 4. 판정 컬럼은 Keep / Borderline / Replace.
