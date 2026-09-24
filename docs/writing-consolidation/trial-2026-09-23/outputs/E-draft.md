# Safety judge meta-evaluation 자료와 오류 유형 집계 제안

현재 사내에는 safety judge를 평가하기 위한 trajectory 192개, 그중 75개에 대한 사람 label, judge의 전체 판정 결과가 있다. 75개 비교에서 goal compliance는 68건, harmfulness는 61건이 사람 label과 일치했다. harmfulness 불일치 14건 중 11건은 judge가 harmful을 놓친 경우이며, 이 11건 중 8건은 tool 결과에 섞인 주입 문장을 agent가 그대로 따른 경우다. 아래에서는 이 자료들의 구성과 결과를 정리하고, 다음 판본부터 harmfulness 불일치를 두 축으로 집계하자는 제안을 설명한다.

## Safety judge가 판정하는 두 가지

safety judge는 LLM이며, agent가 tool을 호출하며 수행한 trajectory 하나를 입력으로 받아 두 가지를 binary label로 판정한다.

- **goal compliance**: agent가 사용자 과업을 완수했는가.
- **harmfulness**: agent가 금지된 state change를 일으켰는가.

meta-evaluation은 이 두 판정을 사람이 붙인 label과 비교해 judge의 정확도를 재는 작업이다.

## 사내 자료 세 종류

| 자료 (내부 이름) | 규모 | 구성 | 출처 |
| --- | --- | --- | --- |
| trajectory 모음 (`traj-r3`) | 192개 | 사용자 과업, tool 결과에 섞인 주입 문장(untrusted input), agent의 tool 호출과 최종 답변 | AgentDojo 공개 task 128개 + 사내 제작 task 64개 |
| 사람 label (`gold-r3`) | 192개 중 75개 | goal compliance·harmfulness 각각 binary label | 두 명이 독립으로 라벨링, 불일치 9건은 세 번째 사람이 확정 |
| judge 판정 (`judge-v3-out`) | 192개 전부 | goal compliance·harmfulness 판정과 판정 근거 문장 | 현재 judge `judge-v3`(기반 모델 Claude Sonnet 5) |

현재 결과는 trajectory별 한 행으로 저장하며, 열은 trajectory id, judge의 두 판정, 사람 label 두 개(있는 경우), judge 근거 문장이다.

## 75개 비교 결과

사람 label이 있는 75개에서 goal compliance는 68건(90.7%), harmfulness는 61건(81.3%)이 judge 판정과 일치했다. harmfulness 불일치 14건은 두 종류로 나뉜다. judge가 harmful을 놓친 false negative가 11건, 무해한 것을 harmful로 판정한 false positive가 3건이다.

## False negative 11건의 mechanism

11건 중 8건은 주입 문장이 tool 결과의 중간에 들어 있고, agent가 그 지시를 따라 파일을 삭제하거나 이메일을 보낸 경우다. 이 8건에서 judge의 근거 문장은 최종 답변만 언급했고 agent의 tool 호출은 언급하지 않았다. 즉 judge가 최종 답변의 표면적인 내용만 보고, 그 답변이 나오기까지 실행된 tool 호출에서 일어난 state change를 확인하지 않아 harmful을 놓친 것으로 보인다.

## 제안: 오류 유형 두 축 집계

다음 판본부터 harmfulness 불일치를 두 축으로 집계한다.

- **주입 위치**: system prompt, user turn, tool 결과 중 어디에 주입 문장이 있었는가.
- **실제 발생한 state change 종류**: 파일 삭제, 외부 전송, 권한 변경, 없음.

목적은 judge가 어떤 종류의 공격을 놓치는지 확인하고 rubric에서 고칠 부분을 정하는 것이다. 첫 적용은 기존 14건을 이 두 축으로 분류하는 일이며, 분류가 끝나면 그 결과를 보고 사람 label이 없는 나머지 117개 trajectory에도 label을 붙일지 정한다.

이 제안은 문서 작성자 개인의 제안이며 아직 팀에서 논의된 바 없다.

## 향후 trajectory 출처 후보

CVE-Bench와 R-Judge는 이후 trajectory 출처로 검토할 수 있는 후보 예시일 뿐이며, 채택이 결정된 대상은 아니다.
