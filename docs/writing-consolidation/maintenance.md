# 통합 writer의 유지 규칙

2026년 9월 24일. [adjudication.md](adjudication.md)의 통합이 설치된 뒤 하루 안에 드러난 구멍 하나와, 통합 스킬이 다시 비대해지는 것을 막는 규칙 셋을 적는다.

## 두 층

| 층 | 내용 | 들어오는 방식 |
|---|---|---|
| 취향(writing-profile.md, 40줄 안) | 저자의 상시 선호: 첫 화면, 본문 형태, 남기는 것과 지우는 것, 문장부호와 영어 경계, PR과 issue | 매 세션 컨텍스트에 본문이 들어간다. Claude Code는 `~/.claude/CLAUDE.md`의 `@` import, Codex는 `~/.codex/AGENTS.md` 안의 복사본(`scripts/sync_profile.py`로 갱신). 두 파일의 원본은 [docs/global-instructions](../global-instructions/README.md) |
| craft(SKILL.md 12KB 안과 참조) | 어느 저자에게나 적용되는 문서 기술 | 문서 작업에서 스킬이 호출될 때 |

취향을 참조 파일에만 두면 스킬이 로드될 때만 작동한다. 설치 다음 날의 첫 실제 문서 작업(2026-09-23 20:28, README 전문 재작성 한 턴)에서 CLAUDE.md의 "스킬과 profile을 먼저 읽어라" 지시가 있었음에도 스킬 본문과 profile은 한 번도 컨텍스트에 들어오지 않았다. 취향은 호출과 무관하게 작동해야 하므로 지시 파일에 본문으로 들어간다. 원본은 스킬 안의 파일 하나이고, 지시 파일의 복사본은 원본에서만 갱신한다.

진단의 전체 요약은 [findings.md](findings.md), 규칙을 넣거나 뺄 때 돌리는 비교 시험은 [harness/](harness/README.md)에 있다.

## 규칙 셋

1. **상한.** SKILL.md는 12,288바이트, writing-profile.md는 40줄. 새 규칙은 기존 규칙 하나를 빼야 들어간다.
2. **근거.** 규칙은 비교 시험이나 실제 교정 기록에서 측정된 실패에만 넣는다. 한 번 눈에 띈 문장 하나로는 넣지 않고, 후보로 [correction-cases.md](../../skills/productivity/copydesk/references/correction-cases.md)에 먼저 적는다.
3. **교체.** 분기마다 correction-cases 12건을 최근 실제 교정으로 갈아 끼우고, 더 이상 나오지 않는 유형은 지운다.

## 2026-09-24의 변경

- 스킬 이름을 technical-report-writing에서 copydesk로 바꿨다. 글 전반을 맡는 스킬이 된 뒤에도 이름이 보고서 하나를 가리켰기 때문이다. 설치 경로는 `~/.agents/skills/copydesk`, CLAUDE.md import 경로도 함께 바뀌었다. 이 폴더의 제안서와 인벤토리는 당시 이름을 그대로 둔다.

- 규칙 2의 첫 적용: 비교 시험에서 측정된 실패 (d) 원문 밖 발명에 대해 규칙 문장이 아니라 절차를 넣었다. `references/source-tracing.md`와 `scripts/trace_check.py`. 블록마다 출처 marker를 달아 쓴 뒤 스크립트로 벗겨 낸다. SKILL.md에는 조건 한 문장과 routing 한 줄만 들어갔고, 그만큼 세 문장을 뺐다(표 대신 목록을 쓰라는 규칙, 권한 없는 시스템 변경 금지의 중복, 단일 행 문단 규칙).

- share-internal-doc(gigio-pack)을 `references/sharing-and-delivery.md`로 흡수. 문서 없이 전달만 하는 요청이 없고, SKILL.md 7절과 규칙이 겹쳤다. 사용자 정책인 sharing pass(2026-09 두 차례 검토, 보고서 아홉 편)는 문장 그대로 옮겼다.
- profile에 본문 형태 기본값 한 항목 추가: 구조가 내용을 담고, 산문은 연결어가 필요한 mechanism, 원인, trade-off에만. 근거는 2026-09-20 사용자 피드백(긴 산문 없는 구조화 문서)과 Notion 수기 편집 네 페이지.
- 비교 시험이 남긴 약점은 "원문에 없는 것을 말하지 마라"이고, 이는 규칙이 아니라 형태로 줄인다. 다음 지렛대는 원문 대조 판본과 수정마다 `protected_diff` 결과 첨부이며, 몇 주 실제 문서의 교정 횟수를 본 뒤 기본값으로 올릴지 정한다.
