# Finding Unknowns 워크플로우 — 설계 기록

작성: 2026-07-11. 상태: Tier 0 배포 완료, `unknowns-pass` 스킬 제작 완료(이
레포 `skills/productivity/unknowns-pass/`). 이 문서는 Tariq Shihipar의
"Finding your unknowns" 글을 개인 워크플로우로 흡수하는 과정의 조사 결과,
결정, 근거를 남긴다. 다음 세션의 에이전트가 이 문서만 읽고 이어받을 수
있어야 한다.

## 1. 발단과 문제 정의

원문: [A field guide to Claude Fable 5: Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)
(Anthropic 공식 블로그, 2026-07-06, AI Engineer World's Fair 키노트 동반 게시).
map(프롬프트·스펙·멘털 모델)과 territory(실제 코드베이스·현실 제약)의 간극이
unknowns이고, 작업 품질은 모델이 아니라 사용자가 unknowns를 명확히 하는
능력에 병목이 걸린다는 주장. 3단계 8패턴:

- 착수 전: blind spot pass / brainstorm / prototype / interview / reference / implementation plan
- 작업 중: implementation notes (deviation 기록)
- 작업 후: pitch·explainer / quiz

(원문은 brainstorm과 prototype을 한 절로 묶지만 기능이 다르다. brainstorm은
발산적 옵션 탐색, prototype은 taste 확인. 이 기록에서는 분리해서 센다.)

**사용자의 pain**: 기법을 몰라서가 아니라 귀찮아서 매번 건너뛴다. 비용은
즉시(귀찮은 질문들), 보상은 나중에 확률적으로 오는 비대칭이라 의지로 못
이긴다. 결과: 토큰은 대량 소모하는데 산출물 품질이 낮다.

**진단**: 기법의 부재가 아니라 발동(initiation)의 부재. 조사 시점 기준 활성
환경은 완전 pull-only였다 — 설치 스킬 34개 전부 pull, 훅 7종은 전부 Orca
텔레메트리(컨텍스트 주입 없음), 글로벌 `~/.claude/CLAUDE.md` 부재,
`~/.codex/AGENTS.md`는 존재하되 0바이트.

## 2. 조사 결과 요약 (2026-07-11 기준)

### 외부 선례 — 이미 최소 5회 skill화됨

| 구현체 | 형태 | 스타 | 상태 |
| --- | --- | --- | --- |
| Neeeophytee/finding-unknowns-skills | 8스킬 팩 + 원파일 CLAUDE.md/AGENTS.md | 162 | 생성 6일차, 활발 |
| bozhouDev/finding-unknowns-skills | 단일 CLAUDE.md 행동 지침 | 48 | 생성일 이후 방치 |
| tankadoko/unknowns-field-guide-skill | 압축 단일 스킬 + CLAUDE.md 라우터 한 줄 | 9 | 방치 |
| GreatMark/fable-field-guide-skills | 플러그인 | 5 | 방치 |
| PH5h5W6d2L/fable-mode | Fable 작업 방식 지침 스킬 | 3 | 방치 |

머지 전 quiz 선례: dkamm/pr-quiz(207★, 원문보다 선행, 휴면), sphinx-ci(7★),
Gater(상용). 판정: 1:1 포팅은 선점됐고 니치는 붐비되 얕다(만들고 방치).
채택할 만큼 성숙한 것도 없다 → 만들 거라면 자체 제작, 단 차별점이 있어야 함.

### 로컬 harness 자산 (~/git/harness)

- **Superpowers** (252k★): 유일한 진짜 push 선례. SessionStart 훅이 매 세션에
  스킬 안내를 강제 주입, brainstorming 스킬은 "HARD-GATE"(해당 레포 자체
  용어; 승인 전 구현 금지, 예외 없음). 절차 최대주의라 이 사용자에게는
  부적합. push 패턴만 차용.
- **everything-claude-code `intent-driven-development`**: 엔지니어링 품질
  최상급. 정찰 우선, 리스크에 따른 깊이 조절, "기본적으로 구현을 막지 않음",
  구현 중 AC `[revised]` 프로토콜. 산출물이 acceptance criteria라 unknowns
  발견과는 직교 — 보완재. 리스크 큰 변경이 잦아지면 채택 후보.
- **mattpocock-skills**: `grilling`(12줄 초경량 인터뷰), `prototype`(taste
  탐침 최고 구현 — throwaway 위생, URL 파라미터 변형 전환, 평결 캡처).
  단 엔지니어링 형태라 비엔지니어링 도메인에는 안 맞음. 채택 보류.
- **flow-next**: `flow-next-interview` 등이 있으나 flowctl/.flow 프레임워크에
  락인. 부분 채택 불가.
- **전 레포 공통 공백**: blindspot 방향(에이전트가 사람의 unknown unknowns를
  가르침)은 어디에도 없음. deep-interview의 inverted interview는 방향이 반대
  (사람이 에이전트의 이해를 교정).

### 공식 스티어링 분업 (Anthropic, 2026-06-18)

CLAUDE.md = 항상 로드되는 사실/규범(200줄 이하 권장), 스킬 = 호출 시 로드되는
절차, `.claude/rules/` = compaction마다 재주입되는 하드 제약, 훅 = 결정적
자동화. → "짧은 라우터는 글로벌 파일에, 절차는 스킬에"가 공식 권장과 일치.

## 3. 사용자 프로필과 스코프 원칙

**도메인은 열린 집합이다.** 게임 개발, 연구성 프로젝트, 이직, 인생 설계,
돈 관리, 투자 전략·포트폴리오 관리 등은 전부 예시일 뿐이며, 이 목록으로
시스템의 범위를 한정하지 않는다. 새로운 도메인이 계속 추가된다는 전제로
설계한다.

유효한 분류 축은 두 가지다:

1. **엔지니어링 vs 비엔지니어링.** 본질적 차이는 도메인 정체성이 아니라
   **검증 방식**이다. 엔지니어링은 실행 가능한 검증(테스트·빌드·렌더)이 있고,
   비엔지니어링은 산출물을 직접 테스트할 수 없어 **사용자의 이해가 유일한
   승인 기준**이다(explainer+quiz가 요식이 아니라 품질 검증 그 자체가 되는
   이유).
2. **도메인 레인 분리.** 게임처럼 반복되는 도메인은 독립 레인(전용 스킬
   세트)으로 승격할 수 있다. 연구도 게임처럼 하나의 레인으로 분리 가능.

공통 작업 모드는 **novice-entry**: 전문성이 없는 도메인을 깊고 넓게 건드리며
아이디어를 내는 것. 원문 런치 비디오 일화의 루프가 이 모드의 범용 형태다 —
아는 것에서 출발 → 도메인 작동 원리 배우기 → 옵션 탐색 → 구체물에 반응 →
"good"을 모른다 싶으면 배우기로 전환 → 브리프로 발사.

## 4. 아키텍처: 3층 구조

```text
Layer 0  push 라인 (도메인 무관)          ← 배포 완료 (2026-07-11)
         발동 + 탐침 선택 + 분량 상한 + 레인 라우팅
Layer 1  unknowns-pass 스킬 (도메인 무관)  ← 제작 완료 (2026-07-11)
         탐침별 실행 지침 + launch brief 템플릿
Layer 2  도메인 레인 (열린 집합)           ← 반복 도메인만 승격
         game-*, (연구?), (투자?), ...
```

- **Layer 0 — push 라인**: 모든 harness의 글로벌 지시문. 스펙·플랜·레퍼런스
  없이 들어온 크거나/모호하거나/낯선 요청이면 실행 전에 가장 싼 탐침 하나를
  제안한다. 탐침 5종: blindspot brief / option map(발산 브레인스톰) /
  throwaway variants(taste) / mini-interview(≤7문항, 선택지+추천, 비가역
  우선) / reference request. 규칙: 발견 가능한 사실은 묻지 않기, 출발점
  1회 확인, 분량 상한(질문 ≤7, 변형 ≤3, 산출물 ≤1), 도메인 레인 우선
  라우팅, launch brief로 압축. 작업 중 deviation 로그(4필드), 작업 후 낯선
  도메인이면 explainer+quiz 제안. NOT: 작은 수정, 스펙 있는 작업,
  "just do it".
- **Layer 1 — unknowns-pass (제작 완료)**: push 라인이 발동을 담당하므로
  스킬은 실행 지침만 담당한다 — 지배적 unknown 분류표(탐침 선택), 탐침 5종
  각각을 잘 실행하는 방법, 검증 방식 분기(실행 검증 vs 이해 확인), launch
  brief 템플릿, 시나리오형 quiz 문항 구조. 위치:
  `skills/productivity/unknowns-pass/`.
- **Layer 2 — 도메인 레인**: 현존 레인은 게임(game-direction → production →
  review), 부분 레인은 투자(toss-portfolio-state + fable5-judgment),
  범용 심층 발견(deep-interview, 명시 호출 전용). **승격 규칙**: 어떤
  도메인이 (a) 반복되고 (b) 범용 탐침으로 품질이 부족하다는 게 관찰되면
  전용 레인으로 승격한다.
  발견 사항: `toss-portfolio-state`의 description이 미설치 스킬
  `investment-decision-support`를 참조함(dangling) — 투자 레인 승격 시 자연
  후보. 연구 레인(가칭 research-direction)도 승격 후보.

## 5. 배포된 것 (Tier 0 v2, 2026-07-11)

단일 정본 + 심링크/미러 구조:

```text
~/.agents/AGENTS.md            ← 정본 (여기만 수정)
├── ~/.claude/CLAUDE.md        → 심링크 (Claude Code)
├── ~/.codex/AGENTS.md         → 심링크 (Codex; 기존 빈 파일은 AGENTS.md.bak-empty로 백업)
└── Cursor User Rule           → 미러 (id 16793847; Cursor는 글로벌 rule을
                                  파일로 읽지 않아 cursor-app-control MCP의
                                  cursor_dialog로 등록. 정본 수정 후 재동기화 필요)
```

v1 → v2 변경(사용자 프로필 반영): 적용 범위를 코드에서 모든 실질 작업으로
확장, brainstorm(option map)을 taste 변형에서 분리해 탐침 4→5개, 우선순위에
"되돌리기 어려운 결정 먼저" 추가, 도메인 레인 라우팅 규칙 추가, 노트 파일을
`decision-log.md`(비코드)로 일반화, 작업 후 이해 확인(explainer+quiz) 추가.

알려진 리스크와 대응:

- **오발동** → 라인 내 NOT 절로 방어, 관찰하며 조정. 오발동이 잦으면 사용자가
  라인을 꺼버리는 게 최악 시나리오이므로 보수적으로 조인다.
- **긴 세션에서 준수 저하** → Claude Code는 `.claude/rules/`(compaction마다
  재주입)로 승격하는 에스컬레이션 경로 존재.

## 6. 만들지/채택하지 않기로 한 것

| 항목 | 이유 |
| --- | --- |
| 8스킬 1:1 팩 | 외부 구현 최소 4개 존재. 겹치는 스킬은 merge하라는 skill-builder 규율상 안티패턴. pull 스킬 8개는 건너뛸 대상 8개일 뿐 |
| quiz 단독 스킬 | 선례 다수. 원문 프롬프트를 맨몸으로 던져도 Fable이 잘함. 규율 문제는 push 라인 한 줄로 해결 |
| pitch/explainer 단독 스킬 | 병목 아님. engineering-docs + humanize-doc 조합으로 수동 대응 가능 |
| deviation ledger 단독 스킬 | push 라인에 4필드 지시로 내장하면 충분. flow-next plan-sync 선례 존재 |
| mattpocock grilling 채택 | 12줄이라 push 라인과 중복. deep-interview까지 있으면 인터뷰 스킬 3개가 되어 트리거 경계만 흐려짐 |
| mattpocock prototype 채택 | 품질은 최고지만 엔지니어링 형태 한정. 엔지니어링 비중이 커지면 재검토 |
| Superpowers 채택 | 승인 전 구현 금지 등 절차 최대주의. 이 사용자 성향과 정반대 |
| 외부 팩 채택 전반 | 성숙한 게 없음(§2). 인기 1위도 생성 일주일차 개인 레포 |

## 7. 결정 이력과 다음 행동

2026-07-11 인터뷰(deep-interview)로 확정된 결정:

- **관찰 대기 폐기, 즉시 제작**: 원래 계획은 "1–2주 관찰 후 제작 판단"이었으나
  미발동은 눈에 보이지 않아 수동 관찰로 잡히지 않는 자기모순이 있었다.
  사용자는 즉시 제작을 선택했다.
- **단일 스킬 + 검증 방식 분기**: 엔지니어링용/비엔지니어링용 2개로 쪼개면
  본문 대부분이 중복된다. 하나의 `unknowns-pass`가 Tariq의 생애주기(착수 전
  탐침 → 작업 중 노트 → 사후 확인)를 유지하고, 검증 방식(실행 가능 vs 이해
  확인)에 따라 플랜 순서·노트 파일·최종 확인만 갈린다. 비엔지니어링
  도메인(투자·연구·커리어·인생 설계·돈 관리)은 별도 레인이 아니라
  description의 트리거 어휘와 본문 분기로 흡수한다.
- **push 라인은 범용 유지**: 특정 스킬 이름을 지목하지 않는다(Cursor
  재동기화 부담과 결합도 회피). 스킬은 description 트리거로 발견된다.
- **배포 경로**: 이 레포에 제작 → main 병합 → install-skill-pack 절차로 설치.

남은 행동:

1. **도메인 레인 승격 판단**: 특정 도메인(연구, 투자, ...)이 반복되고 범용
   탐침이 부족하면 §4의 승격 규칙대로 전용 레인 검토.
2. **정본 수정 시 절차**: `~/.agents/AGENTS.md` 수정 → Cursor user rule
   재동기화(cursor_dialog update, id 16793847). 심링크 쪽은 자동.

## 8. 사용 시나리오 (예시 — 이 목록이 범위를 한정하지 않음)

- **레인 있는 도메인 (게임)**: "게임 만들고 싶은데 기획 경험 없음" → 라우팅
  규칙에 따라 game-direction이 받음(taste 인터뷰 + concept slate가 이미 특화
  구현). 범용 레이어는 레인이 안 덮는 하위 도메인에서만 발동("셰이더가 뭔지
  모름" → blindspot brief).
- **레인 없는 비엔지니어링 (투자 전략)**: toss-portfolio-state로 사실 확보 →
  blindspot brief(전문가라면 물을 질문, 지뢰) → option map(보수적~공격적
  후보) → 반응 → mini-interview(리스크 허용도 등 인간만 답할 결정, 비가역
  우선) → launch brief(사실상 투자 정책 문서) → 운용 중 decision-log →
  자금 투입 전 quiz(이 도메인에서 결과를 승인하는 실질 수단).
- **레인 없는 탐색 작업 (연구 아이디어)**: option map이 주 탐침 — 영역 탐색
  후 방향 5–10개 발산, 반응으로 스코프 확정 → launch brief로 새 세션 발사 →
  산출물 나오면 explainer+quiz로 이해 확인.
- **판단 무거운 작업 (이직/인생 설계)**: option map + blindspot brief로 진입
  → 깊이 필요 시 사용자가 deep-interview 명시 호출 → 최종 판단은
  fable5-judgment. 신규 제작 불필요, 진입만 push 라인이 담당.
- **negative (발동 금지)**: 오타 수정, 스펙 있는 구현, "그냥 해".

## 참고 링크

- 원문: https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns
- 스티어링 가이드: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- 외부 선례: https://github.com/Neeeophytee/finding-unknowns-skills ,
  https://github.com/bozhouDev/finding-unknowns-skills ,
  https://github.com/tankadoko/unknowns-field-guide-skill ,
  https://github.com/dkamm/pr-quiz
