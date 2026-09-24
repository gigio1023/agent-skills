# Agent safety judge meta-evaluation 자료와 harmfulness 불일치 집계 제안

Agent safety judge의 정확도를 재는 데 쓸 수 있는 사내 자료는 trajectory 192개, 그중 75개에 붙은 사람 label, 192개 전부에 대한 judge 판정 결과다. 75개에서 judge는 goal compliance 68개, harmfulness 61개를 사람과 같게 판정했다. Harmfulness 불일치 14건 중 11건은 judge가 harmful trajectory를 놓친 false negative이고, 그중 8건은 tool 결과 중간에 들어간 주입 지시를 agent가 따라 파일을 삭제하거나 이메일을 보낸 경우다. Judge가 어떤 종류의 공격을 놓치는지 보려면 harmfulness 불일치를 주입 위치와 실제 발생한 state change 종류로 나눠 세야 하며, 첫 작업은 기존 14건의 분류다.

## Safety judge와 meta-evaluation

Safety judge는 agent가 tool을 호출하며 과업을 수행한 trajectory 하나를 입력받아 두 가지를 binary label로 판정하는 LLM이다.

- Goal compliance: agent가 사용자 과업을 완수했는가
- Harmfulness: agent가 금지된 state change를 일으켰는가

현재 judge는 Claude Sonnet 5를 기반으로 하며, 내부 이름은 `judge-v3`다.

Meta-evaluation은 같은 trajectory에 대한 judge 판정을 사람이 붙인 label과 비교해 judge의 정확도를 재는 일이다. 두 판정을 따로 비교하므로 일치율도 goal compliance와 harmfulness에 각각 나온다.

## 사내 자료

| 자료 | 규모 | 만든 방식 | 내부 이름 |
| --- | --- | --- | --- |
| Trajectory 모음 | 192개 | AgentDojo 공개 task 128개, 사내 제작 task 64개 | `traj-r3` |
| 사람 label | 75개 trajectory | 두 명이 독립으로 붙이고, 불일치 9건은 세 번째 사람이 확정 | `gold-r3` |
| Judge 판정 결과 | 192개 trajectory | `judge-v3`가 낸 두 label과 근거 문장 | `judge-v3-out` |

Trajectory 하나는 사용자 과업(user task), agent가 받은 tool 결과에 섞인 주입 문장(untrusted input), agent의 tool 호출과 최종 답변으로 이루어진다. 사람 label이 없는 나머지 117개에는 judge 판정만 있다.

## Judge와 사람 label의 일치

사람 label이 있는 75개에서 goal compliance는 68개(90.7%), harmfulness는 61개(81.3%)가 일치했다. Harmfulness 불일치 14건 중 11건은 사람이 harmful로 붙인 trajectory를 judge가 놓친 false negative이고, 3건은 사람이 무해하다고 본 trajectory를 judge가 harmful로 판정한 false positive다.

### Tool 결과 주입을 놓친 false negative

False negative 11건 중 8건은 같은 모양이다. 주입 문장이 tool 결과의 중간에 들어 있었고, agent는 그 지시를 따라 파일을 삭제하거나 이메일을 보냈다. 이 8건에서 judge의 근거 문장은 최종 답변만 언급하고 tool 호출은 언급하지 않았다.

파일 삭제와 이메일 전송은 agent의 tool 호출에서 일어난 state change인데, 근거 문장은 최종 답변만 다룬다. 따라서 judge가 최종 답변을 중심으로 판정하면서 tool 호출에서 일어난 harm을 놓쳤을 가능성이 있다. 다만 근거 문장만으로는 judge가 tool 호출을 읽지 않은 것인지, 읽고도 harmful로 보지 않은 것인지 구분할 수 없다.

## Harmfulness 불일치 집계 방식 제안 (팀 논의 전)

다음 판본부터 harmfulness 불일치를 두 축으로 집계한다. 목적은 judge가 어떤 종류의 공격을 놓치는지 확인하고, rubric에서 고칠 부분을 정하는 것이다.

- 주입 위치: system prompt, user turn, tool 결과
- 실제 발생한 state change: 파일 삭제, 외부 전송, 권한 변경, 없음

현재 결과는 trajectory마다 한 행에 label과 근거 문장만 담고 있어서, 불일치를 세면 개수와 방향(false negative, false positive)까지만 나온다. 두 축으로 나누면 앞의 8건은 주입 위치가 tool 결과이고 state change가 파일 삭제 또는 외부 전송(이메일)인 칸에 모이며, rubric 수정도 이렇게 불일치가 모인 칸의 사례를 근거로 정할 수 있다.

첫 적용은 기존 harmfulness 불일치 14건을 두 축으로 분류하는 일이고, 분류가 끝나면 나머지 117개 trajectory에도 사람 label을 붙일지 정한다. Trajectory 출처를 넓힐 때는 CVE-Bench와 R-Judge를 후보로 검토할 수 있으며, 둘 다 정해진 대상은 아니다.
