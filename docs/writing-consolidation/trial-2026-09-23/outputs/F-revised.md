# Safety judge meta-evaluation 자료와 오류 유형 집계 제안

Safety judge(`judge-v3`)의 meta-evaluation에 쓰는 사내 자료는 trajectory 모음(`traj-r3`), 사람 label(`gold-r3`), judge 판정(`judge-v3-out`) 세 가지다. `gold-r3`와 `judge-v3-out`을 비교하면 harmfulness 불일치 14건 중 11건이 judge가 harmful을 놓친 경우이고, 그중 8건은 tool 결과에 섞인 주입 문장을 agent가 그대로 따른 경우다.

## Safety judge와 meta-evaluation

Safety judge는 agent가 tool을 호출하며 수행한 trajectory 하나를 입력으로 받아 두 가지를 binary label로 판정하는 LLM이다. Goal compliance는 agent가 사용자 과업을 완수했는지를 나타내고, harmfulness는 agent가 금지된 state change를 일으켰는지를 나타낸다. Meta-evaluation은 이 판정을 사람이 붙인 label과 비교해 judge의 정확도를 재는 작업이다.

## 보유 자료와 비교 결과

trajectory 모음(`traj-r3`)은 192건이며, AgentDojo 공개 task 128건과 사내 제작 task 64건으로 구성된다. 각 trajectory는 user task, tool 결과에 섞인 주입 문장, agent의 tool 호출, 최종 답변으로 이루어진다. 이 중 75건에 사람 label(`gold-r3`)이 있다. 두 명이 독립으로 goal compliance와 harmfulness를 라벨링했고, 두 사람의 판정이 갈린 9건은 세 번째 사람이 확정했다. judge 판정(`judge-v3-out`)은 192건 전부에 대해 goal compliance와 harmfulness 판정, 그리고 근거 문장을 낸다. 기반 모델은 Claude Sonnet 5다.

75건을 비교하면 goal compliance는 68건, harmfulness는 61건이 일치한다. harmfulness 불일치 14건 중 11건은 judge가 harmful을 놓친 경우(false negative)이고, 3건은 무해한 것을 harmful로 판정한 경우(false positive)다.

## Harmfulness false negative의 패턴

false negative 11건 중 8건은 주입 문장이 tool 결과의 중간에 들어 있고, agent가 그 지시를 따라 파일을 삭제하거나 이메일을 보낸 경우다. 이 8건에서 judge의 근거 문장은 최종 답변만 언급했고, agent의 tool 호출은 언급하지 않았다.

## Harmfulness 불일치 오류 유형 집계 제안

다음 판본부터 적용을 제안한다. 아직 팀 논의를 거치지 않은 개인 제안이다.

harmfulness 불일치를 주입 위치(system prompt, user turn, tool 결과)와 실제 발생한 state change 종류(파일 삭제, 외부 전송, 권한 변경, 없음)의 두 축으로 집계한다. 목적은 judge가 어떤 종류의 공격을 놓치는지 확인하고 rubric을 고칠 부분을 정하는 것이다.

첫 적용은 기존 불일치 14건을 이 두 축으로 분류하는 일이다. 분류가 끝나면 나머지 117건에 사람 label을 붙일지 정한다.
