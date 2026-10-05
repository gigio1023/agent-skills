# Copydesk 유지 기준

Copydesk는 독자의 이해와 의미 보존을 개선하는 지침을 유지한다. 명시적인 사용자 선호, 실제 작업에서 확인한 문제, 유용한 작성 방법을 근거로 내용을 갱신하며 크기나 교정 횟수만으로 규칙을 넣고 빼지 않는다.

## 원본과 적용 범위

| 원본 | 책임 | 적용 |
| --- | --- | --- |
| [Writing profile](../../skills/productivity/copydesk/references/writing-profile.md) | 저자의 문체와 표현 선호 | 지시 파일의 import 또는 동기화된 복사본 |
| [SKILL.md](../../skills/productivity/copydesk/SKILL.md)와 참조 | 독자, 수정 범위, 의미 보존, 구조, 검토 방법 | 현재 작업에 필요한 지침과 참조 |

Profile은 한 원본에서 관리한다. 배포용 지시 파일과 갱신 방법은 [global instructions](../global-instructions/README.md)에 있다. 저장소의 원본과 복사본을 고치는 일과 실제 전역 설치는 별도 범위다. 현재 요청과 문서의 필수 template이 profile보다 우선하며 다른 저자의 글은 요청된 범위 안에서 고친다.

## 현행 유지 기준

- **기능과 근거:** 지침이 바꾸는 판단이나 결과를 설명한다. 명시적인 선호나 충분히 이해한 실제 사례 하나도 근거가 될 수 있다. 반복 실패, source 충돌, 검증 결과가 있으면 함께 사용하되 비교 시험을 모든 변경의 진입 조건으로 삼지 않는다.
- **내용과 배치:** 필요한 의미와 절차는 보존하고 중복, 불필요한 금지, 사용되지 않는 우회 규칙은 줄인다. Profile 행 수, SKILL.md 바이트 수, one-in-one-out을 제한으로 두지 않는다. 길어지면 언제 읽어야 하는지를 기준으로 참조를 나눈다.
- **사례와 이력:** [교정 사례](../../skills/productivity/copydesk/references/correction-cases.md)는 해당 실패를 설명할 때 갱신한다. 유효한 옛 사례는 유지하며 주기나 사례 수를 맞추려고 교체하지 않는다. 새 사실이 필요한 예시는 함께 제공된 근거를 명시한다.
- **검증:** 변경된 package의 링크와 형식을 확인한다. Script나 template이 바뀌면 관련된 실제 입력 또는 고정 입력으로 동작을 확인한다. 글쓰기 품질은 의미, 조건, 설명의 연결을 읽어 판단한다. Model 비교는 요청된 경우 실행하며 정적 검사나 checker의 finding 수를 행동 개선의 증거로 쓰지 않는다.

[Findings](findings.md)와 [비교 시험 harness](harness/README.md)는 통합 당시의 진단과 선택적 비교 방법을 보존한다. 그 기록의 규칙 수나 과거 판정은 현행 skill을 덮어쓰지 않는다.

## 2026-10-06의 변경

- 새 작성, 부분 교정, 전체 개정의 수정 범위를 구분했다. 전체 개정은 의미와 명시적으로 보호된 원문을 보존하면서 구조와 표현을 바꿀 수 있다.
- 문장 길이, 연결어미 수, 문단 길이, 명사 수 제한과 80% STE 정책을 제거했다. 영어 명료성 지침은 용어 구별, 행위자와 조건, modality 보존을 통합했다.
- 표, 그림, 문단을 독자의 질문에 따라 선택한다. 완성 예시와 의미 보존을 표면적인 패턴보다 우선한다.
- 한국어 통계 자료와 source tracing, draft checker, protected diff를 필요한 작업에서만 사용한다. 공유 점검은 기존 권한과 독자 정보를 재사용하며 실제 공개 범위 문제가 있을 때 확인한다.

## 2026-10-03의 변경: 문장과 형식 제한 폐기

이 절은 당시 결정의 기록이다. STE 적용 비율, 문장 수치 제한, figure 우선 규칙은 2026-10-06에 폐기했다.

- 문장 규칙으로 ASD-STE100 Issue 9(2025-01-15)의 문장과 문단 규칙을 약 80% 강도로 들였다. 승인 어휘 사전은 들이지 않았다. 근거는 소유자 요청이다. profile은 "남기는 것" 두 줄을 한 줄로 합치고 그 자리에 문장 규칙 한 줄을 넣어 37줄을 유지했다. 당시 규칙과 예시는 `references/voice-and-facts.md`의 Controlled sentences 절에 있었다. 현재 지침과 의미를 보존한 예시는 [Clear sentences](../../skills/productivity/copydesk/references/voice-and-facts.md#clear-sentences)에 있다.
- 독자가 mechanism, 구조, 비교를 이해해야 하면 산문보다 figure나 interactive page를 먼저 고른다. 현재 [Medium for understanding](../../skills/productivity/copydesk/references/information-design.md#medium-for-understanding)은 독자의 질문에 따라 산문, 표, 그림을 선택한다.
- 늘어난 바이트는 다른 파일과 겹치는 문장을 지워 갚았다. 패키지 전체는 112바이트 줄었다.

## 2026-09-29의 변경: 크기와 교체 제한 폐기

이 절의 크기 목표, 2% 허용치, 하나를 넣으면 하나를 빼는 규칙은 2026-10-06의 현행 유지 기준으로 대체했다.

- 규칙 1의 상한을 목표치로 바꿨다. 12,288바이트를 지키느라 #87에서 3바이트, #89 뒤 163바이트를 다투는 것은 유지 비용만 들고 비대화를 막지 못한다. 소유자 결정: 2%까지 넘는 것은 괜찮다. 비대화를 막는 장치는 규칙 교체(하나 넣으면 하나 빼기)이고, 당시에는 이를 유지했다. 같은 취지로 skill-builder와 cross-harness-skills의 크기 문장도 "목표치, 2% 여유"로 맞췄다.

## 2026-09-24의 변경: 통합 기록

이름 변경과 통합은 유지한다. 아래의 의무적 trace, 산문 제한, 매 수정의 diff 첨부 제안은 현재 작업별 선택 기준으로 대체했다.

- 스킬 이름을 technical-report-writing에서 copydesk로 바꿨다. 글 전반을 맡는 스킬이 된 뒤에도 이름이 보고서 하나를 가리켰기 때문이다. 설치 경로는 `~/.agents/skills/copydesk`, CLAUDE.md import 경로도 함께 바뀌었다. 이 폴더의 제안서와 인벤토리는 당시 이름을 그대로 둔다.

- 규칙 2의 첫 적용: 비교 시험에서 측정된 실패 (d) 원문 밖 발명에 대해 규칙 문장이 아니라 절차를 넣었다. `references/source-tracing.md`와 `scripts/trace_check.py`. 블록마다 출처 marker를 달아 쓴 뒤 스크립트로 벗겨 낸다. SKILL.md에는 조건 한 문장과 routing 한 줄만 들어갔고, 그만큼 세 문장을 뺐다(표 대신 목록을 쓰라는 규칙, 권한 없는 시스템 변경 금지의 중복, 단일 행 문단 규칙).

- share-internal-doc(gigio-pack)을 `references/sharing-and-delivery.md`로 흡수. 문서 없이 전달만 하는 요청이 없고, SKILL.md 7절과 규칙이 겹쳤다. 사용자 정책인 sharing pass(2026-09 두 차례 검토, 보고서 아홉 편)는 문장 그대로 옮겼다.
- profile에 본문 형태 기본값 한 항목 추가: 구조가 내용을 담고, 산문은 연결어가 필요한 mechanism, 원인, trade-off에만. 근거는 2026-09-20 사용자 피드백(긴 산문 없는 구조화 문서)과 Notion 수기 편집 네 페이지.
- 비교 시험이 남긴 약점은 "원문에 없는 것을 말하지 마라"이고, 이는 규칙이 아니라 형태로 줄인다. 다음 지렛대는 원문 대조 판본과 수정마다 `protected_diff` 결과 첨부이며, 몇 주 실제 문서의 교정 횟수를 본 뒤 기본값으로 올릴지 정한다.
