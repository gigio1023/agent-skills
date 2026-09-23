# 규칙 판정표

[inventory-writer.md](inventory-writer.md)와 [inventory-siblings.md](inventory-siblings.md)의 행을 근거로, 통합 SKILL.md에 무엇을 어떤 형태로 남기는지 정한다. 판정은 다섯 가지다. 유지(SKILL.md 본문), 참조(작업별로 여는 파일), profile(저자 취향 층 `writing-profile.md`), 삭제, 해소(충돌을 조건으로 푼다). 근거는 Notion 수기 편집 분석과 교정 세션 분석([REVIEW-2026-09-23.md](../../../../../../aim-intelligence/research/2026-09-22-writing-review-learning/REVIEW-2026-09-23.md))이다.

## 1. writer 내부 긴장 T1~T14

| 번호 | 충돌 | 판정 | 근거 |
|---|---|---|---|
| T1 | 접힌 절에 "언제 펼칠지" 짧은 안내 허용(ID:23) 대 어디에도 다시 쓰지 않음(CC:13) | 해소: 접힌 절의 제목과 첫 문장이 내용을 말한다. 별도 안내 문장은 쓰지 않는다. ID:23의 허용 구절 삭제 | 사용자가 "펼치는 기준" 블록을 두 차례 지웠고 toggle 제목 안내도 지웠다 |
| T2 | 범위 callout 허용(SK:30) 대 scope notice 금지(PF) | 해소: 범위는 제목과 첫 줄의 주어가 진다. 별도 범위 문장은 문서 묶음에서 이 문서가 다루지 않는 자매 문서를 가리킬 때 한 줄만 | 사용자가 "…은 별도 문서에서 다룬다"를 지웠고, 자기 메모 "refusal suppression 위주로"는 독자용 문장이 아니었다 |
| T3 | 관찰을 한정하는 날짜 유지(SK:48) 대 as-of 문장 금지(PF) | 해소: 날짜는 그것이 한정하는 표나 수치 옆에 둔다. 문서 머리의 기준일 문장은 쓰지 않는다 | 평가 설계 페이지의 표 아래 "2026년 9월 19일 집계"는 남았고, 머리말의 "9월 19일 기록, 9월 20일 확인 기준"은 지워졌다 |
| T4 | 실제 경로 선택이 있으면 읽기 안내 허용(RV:26) 대 금지(PF, CC) | 해소: 한 문서 안의 읽기 안내는 쓰지 않는다. 여러 페이지 묶음에서 어느 페이지를 열지 고르는 개요 표는 허용 | 사용자는 문서 안 읽기 안내를 매번 지웠고, 여러 페이지에 결과가 묻혔을 때는 개요를 요청했다(C13) |
| T5 | 부정형 정의 절대 금지(SK:56) 대 독자가 X로 오해할 때 허용(MW:29) | 해소: 조건부로 통일. 독자가 X를 가정할 근거가 있을 때만 "X가 아니라 Y". SKILL.md의 "no definition by negation or added qualification"을 조건형으로 고침 | Astra 리뷰가 절대 표현을 지적. 사용자가 남긴 "대신하지 못함"이 반례 |
| T6 | 제안 지위를 한 번만(CC:73) 대 제목, 요약, 모든 그림 label에(PF) | 해소: 제목과 첫 화면 요약에서 한 번 밝히고, 본문과 그림 label과 절 제목은 그와 어긋나지 않게 쓴다("시작할 benchmark" 금지) | 사용자 교정은 지위 표시의 반복이 아니라 어긋남("시작할 benchmark", "논의 중")을 지적했다 |
| T7 | 그림 개수 의무 없음(SK:40) 대 PR 동작 변경마다 표와 그림(PF) | 유지, 범위 명시: 문서 일반에는 개수 의무 없음. PR 동작 변경은 사용자의 명시적 상시 규칙 | 9월 22일 사용자 발화 "항상" |
| T8 | 기본값을 반복하는 별도 style 층 금지(CO:17) 대 writing-profile | 해소: composition의 문장을 "별도 style 스킬을 만들지 않는다. 저자 취향은 writer 안의 profile 파일 하나에 둔다"로 고침. profile은 SKILL.md 규칙을 반복하지 않고 취향만 담는다 | Astra 리뷰: house-style 스킬 불필요, profile 파일과 지시 파일 참조로 충분 |
| T9 | caption에 측정 조건과 결론(MF:35, SK:24) 대 표본 수와 단서를 그림 밖 prose로(PF) | 해소: 그림 캔버스 안에는 이름과 mechanism. 조건, 표본 수, 시각은 caption이나 인접 prose. caption은 그림 밖이다 | 사용자 피드백 "figure는 dashboard처럼 압축"은 SVG 안을 말했다 |
| T10 | 확인하지 않은 것에 대한 문장 삭제(PF) 대 독자가 실행됐다고 가정할 한계는 밝힘(WE:307, EP:27) | 해소: 독자가 그 확인이 됐다고 가정하고 행동할 때는 한 문장으로 밝힌다. 저자의 성실함을 기록하는 문장(범위 고지, 미확인 나열, 다음 계획)은 지운다 | 사용자가 "비교 근거는 없음"은 남기고 "serving 모델은 확인하지 않았다", "다음 비교는…"은 지웠다 |
| T11 | 가운뎃점과 dash 금지 범위가 한국어 산문(MW:31) 대 모든 본문(PF) | 해소: profile이 범위를 정한다(이 저자의 모든 본문). multilingual의 Korean 절은 profile을 가리키기만 한다 | 사용자 발화 "middel dot, dash 쓰지마"는 언어 조건이 없었다 |
| T12 | 요약 블록은 명사구 항목(PF) 대 관련 bullet에는 연결 문장 필요(ID:19) | 유지, 범위 명시: 요약 블록은 병렬 항목, 본문은 연결 문장 | 사용자는 요약을 bullet로 되돌리고 본문 산문은 두었다 |
| T13 | 교정 밖은 byte 유지(SK:54) 대 좁은 규칙을 범위 안 비슷한 구절에 적용(AR:21) | 해소: 교정이 "이런류의 문장은 다 빼"처럼 유형을 지목하면 같은 유형 전체가 범위다. 한 문장을 지목하면 그 문장만 고치고 같은 유형의 다른 위치는 보고한다 | 사용자 교정에 두 형태가 다 있다(1462행 유형 지목, 2928행 문단 지목) |
| T14 | PR 언어를 먼저 묻기(PF) 대 가능한 입력으로 먼저 쓰고 중대한 공백만 묻기(SK:16) | 유지, 범위 명시: PR 언어는 저장소당 한 번 묻는 draft-pr 규칙. 문서 일반은 SKILL.md 규칙 | 9월 17일 사용자 결정 |

## 2. user-pref 행의 profile 이동

profile에 없어서 추가하는 것: 1인칭과 저자 도입부 제거(SK:48, VF:17), 건조한 서술 기본(SR:5, EL:167). SKILL.md에 procedure로 남기는 것: Markdown source 줄바꿈 금지(SK:97, 저장소 관행), Typst 우선(DP:18, 제작 절차). SKILL.md 본문의 user-pref 행(SK:14, 24, 36)은 craft 문장에서 취향 부분을 profile로 옮기고 본문에는 "profile을 적용한다"만 남긴다.

경계 사례 W-051, W-053, W-071, W-165, W-171(과정 서술 삭제, 읽기 안내 금지, 지시문 본문화 금지, 부정형 정의 삭제, 상태 열 조건)은 craft로 SKILL.md에 남긴다. 사용자 교정에서 나왔지만 어느 독자에게도 맞는 규칙이다.

## 3. 열리지 않은 참조의 규칙

source-readings(0회), example-library(0회), writing-patterns(1회), worked-examples(1회)의 행 가운데 SKILL.md에 없는 것은 39행이다. 옮기는 것: CC BY-NC-ND 자료는 링크만(SR), teaching example의 이름과 수치를 실제 문서에 복제하지 않음(SR), 독자가 실행됐다고 가정할 한계 유지(WE, T10 해소에 필요), 넓은 약속은 관측 가능한 검사로 바꾼 뒤 결과를 씀(WP). 나머지는 SKILL.md 원칙의 사례형 변주라 옮기지 않는다. source-readings와 example-library는 docs/writing-sources.md로 이동하고 스킬에서 제거한다. worked-examples와 writing-patterns은 합성 예시 파일 하나로 합친다.

## 4. 통합 SKILL.md 절과 각 절이 흡수하는 행

| 절 | 흡수 | 상한 |
|---|---|---|
| 1 작업 종류와 기준 판본 | SK 도입, AR 표 "Choose the work", 사용자 편집본 기준(AR:21~23) | 8문장 |
| 2 의미와 수정 범위 보존 | SK Revision discipline(PR #71), AR "Check the requested result", T13 해소 문장, share-internal-doc의 최신 공유본 회수 | 12문장 |
| 3 저자 취향 | profile 참조 한 문장과 "항상 읽는다" | 2문장 |
| 4 정보 선택과 구조 | SK Document structure, Content and evidence 압축, reader-value의 판단 기준 | 14문장 |
| 5 표와 그림 | SK Tables and visuals, ID 요약, 첫 도식, MF의 조건 규칙 | 10문장 |
| 6 설명과 언어 | SK Explanation and language, korean-clarity 핵심, korean-tells 근거 항목 요약, T5 조건형 | 12문장 |
| 7 공유와 전달 | share-internal-doc 중 수신자와 출처 접근과 전달 확인 | 6문장 |
| 8 검사 | SK Reader and delivery checks, scripts 두 개 실행 | 8문장 |

## 5. 자매 스킬 판정

[inventory-siblings.md](inventory-siblings.md) 활성 369행 기준이다.

| 스킬 | 판정 | 내용 |
|---|---|---|
| slop-aware-writing | writer로 흡수 | SKILL.md의 진단 절차와 references의 revision, voice-preservation, source-grounding 핵심은 authoring-and-revision.md와 voice-and-facts.md로. korean-tells의 근거 있는 항목은 korean-writing.md로. legacy core-rules.md는 옮기지 않음. MIT 출처 표기는 유지 |
| korean-clarity | writer로 흡수 | SKILL.md 규칙과 meaning-examples를 korean-writing.md로. 채팅 답변에도 적용한다는 K-004는 SKILL.md 도입에 한 문장으로 |
| share-internal-doc | 유지 → 2026-09-24 writer로 흡수 | 처음에는 수신자, 출처 접근, 최신 공유본 회수, 게시 후 확인만 남겨 유지했으나, 문서 없이 전달만 하는 요청이 없고 SKILL.md 7절과 규칙이 겹쳐 references/sharing-and-delivery.md로 옮겼다. 사유와 유지 규칙은 [maintenance.md](maintenance.md) |
| use-terminology, curate-terminology | 유지 | 문서 밖에도 적용되고 서로 짝. writer는 용어 절에서 참조만 |
| draft-pr, write-issue | 유지 | 장르 규칙 소유. 편집 판단은 writer 참조 |

충돌 후보 12개 중 실제 충돌은 둘이다. 구두점 기본값은 profile에 두고 범위는 모든 본문으로 확정한다(T11). PR as-is/to-be는 자매 인벤토리가 "표와 그림까지는 사용자 발화가 지지하지 않는다"고 봤으나, 원문은 "pr 항상 as-is, to-be를 명확하게 표와 technical-diagram로 표현하도록 해줘"이므로 표와 그림 모두 사용자 단어다. profile 유지. 나머지는 legacy 파일과의 충돌이거나 범위를 적으면 사라진다.

writer에 대응 규칙이 없어 잃기 쉬운 행은 옮긴다. S-062(change narration이 필요한 장르 예외), S-080(일괄 수정에서 목소리 수렴 금지), S-107(고친 결과에 새 tell이 생겼는지 점검), S-177(명령형 caption 금지), S-191(governance-speak), K-004와 K-026(채팅 답변 적용), K-028(사용자 오타와 속어 모방 금지). korean-tells에서는 [AI]와 [self] 태그와 한계, A-2, A-16, I-1의 오탐 경고, C-8 keep test와 "측정 근거는 논설과 블로그" 단서, "pattern count나 change ratio로 채점하지 않는다"를 함께 옮긴다.

## 6. 파일 배치

| 결과 | 출처 |
|---|---|
| SKILL.md (11KB 이하) | 현재 SKILL.md 압축 + slop SKILL 진단 절차 + korean-clarity 핵심 문장 + 4절 판정 |
| references/writing-profile.md | 신규, 항상 읽음 |
| references/korean-writing.md | 신규: korean-clarity + korean-tells 근거 항목 + multilingual Korean 절 |
| references/multilingual-writing.md | Korean 절은 korean-writing 포인터로, 나머지 언어 유지 |
| references/authoring-and-revision.md, voice-and-facts.md | slop revision, voice-preservation, source-grounding, gates의 잃기 쉬운 행 흡수 |
| references/synthetic-examples.md | worked-examples + writing-patterns 병합 후 축약 |
| docs/writing-sources.md | source-readings + example-library 이동. 스킬에서 제외 |
| 유지 | correction-cases, exemplar-passages, finished-examples, explanation-with-depth, information-design, measurements-and-figures, document-forms, document-production, reader-value, composition(T8 수정) |
| scripts/ | check_draft.py, protected_diff.py |
