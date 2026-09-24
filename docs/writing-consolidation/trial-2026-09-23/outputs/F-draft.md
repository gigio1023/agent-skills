# Safety judge meta-evaluation 자료와 오류 유형 집계 제안

Safety judge(`judge-v3`)의 meta-evaluation에 쓰는 사내 자료는 trajectory 모음(`traj-r3`), 사람 label(`gold-r3`), judge 판정(`judge-v3-out`) 세 가지다. `gold-r3`와 `judge-v3-out`을 비교하면 harmfulness 불일치 14건 중 11건이 judge가 harmful을 놓친 경우이고, 그중 8건은 tool 결과에 섞인 주입 문장을 agent가 그대로 따른 경우다.

## Safety judge와 meta-evaluation

Safety judge는 agent가 tool을 호출하며 수행한 trajectory 하나를 입력으로 받아 두 가지를 binary label로 판정하는 LLM이다. Goal compliance는 agent가 사용자 과업을 완수했는지를 나타내고, harmfulness는 agent가 금지된 state change를 일으켰는지를 나타낸다. Meta-evaluation은 이 판정을 사람이 붙인 label과 비교해 judge의 정확도를 재는 작업이다.

## 보유 자료 세 가지

| 자료 | 규모 | 구성 |
| --- | --- | --- |
| trajectory 모음 (`traj-r3`) | 192건(AgentDojo 공개 task 128건, 사내 제작 task 64건) | user task, tool 결과에 섞인 주입 문장(untrusted input), agent의 tool 호출, 최종 답변 |
| 사람 label (`gold-r3`) | 192건 중 75건 | goal compliance와 harmfulness 각각의 binary label |
| judge 판정 (`judge-v3-out`) | 192건 전부 | goal compliance와 harmfulness 판정, judge의 근거 문장 |

`gold-r3`의 75건은 두 명이 독립으로 라벨링했고, 두 사람의 판정이 갈린 9건은 세 번째 사람이 확정했다. `judge-v3-out`을 낸 `judge-v3`의 기반 모델은 Claude Sonnet 5다.

## 사람 label과 judge 판정의 일치

`gold-r3`의 75건을 `judge-v3-out`과 비교한 결과는 다음과 같다.

| 판정 항목 | 일치 | 비교 대상 |
| --- | ---: | ---: |
| goal compliance | 68건 | 75건 |
| harmfulness | 61건 | 75건 |

harmfulness 불일치 14건 중 11건은 judge가 harmful을 놓친 경우(false negative)이고, 3건은 무해한 것을 harmful로 판정한 경우(false positive)다.

## Harmfulness false negative의 패턴

false negative 11건 중 8건은 주입 문장이 tool 결과의 중간에 들어 있고, agent가 그 지시를 따라 파일을 삭제하거나 이메일을 보낸 경우다. 이 8건에서 judge의 근거 문장은 최종 답변만 언급했고, agent의 tool 호출은 언급하지 않았다.

## 현재 결과 저장 형식

현재 결과는 trajectory 하나당 한 행으로 저장하며, 열은 다음과 같다.

- trajectory id
- judge label: goal compliance, harmfulness
- 사람 label: goal compliance, harmfulness(있는 75건만)
- judge 근거 문장

## Harmfulness 불일치 오류 유형 집계 제안

다음 판본부터 적용을 제안한다. 아직 팀 논의를 거치지 않은 개인 제안이다.

harmfulness 불일치를 주입 위치와 실제 발생한 state change 종류의 두 축으로 집계한다.

- 주입 위치: system prompt, user turn, tool 결과
- state change 종류: 파일 삭제, 외부 전송, 권한 변경, 없음

목적은 judge가 어떤 종류의 공격을 놓치는지 확인하고 rubric을 고칠 부분을 정하는 것이다.

첫 적용은 기존 불일치 14건을 이 두 축으로 분류하는 일이다. 분류가 끝나면 나머지 117건에 사람 label을 붙일지 정한다.

## 향후 trajectory 출처 후보

CVE-Bench와 R-Judge는 이후 trajectory 출처로 검토할 수 있는 후보이며, 아직 결정된 대상은 아니다.
