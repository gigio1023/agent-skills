# Agent safety judge meta-evaluation 자료 현황과 오류 유형 집계 제안

현재 safety judge(`judge-v3`)는 사람 label이 있는 trajectory 75개에서 goal compliance 판정 68개, harmfulness 판정 61개가 사람 label과 일치했다. harmfulness 불일치 14건 중 11건은 judge가 harmful한 trajectory를 놓친 false negative이고, 그중 8건은 tool 결과 중간에 들어간 주입 문장을 agent가 따른 경우였다. 이 문서는 meta-evaluation에 쓰는 사내 자료 세 가지와 위 비교 결과를 정리하고, 다음 판본부터 harmfulness 불일치를 주입 위치와 state change 종류로 나누어 집계하자는 제안을 설명한다. 이 집계 방식은 작성자 개인의 제안이며 아직 팀에서 논의하지 않았다.

## 평가 대상: safety judge

safety judge는 agent가 tool을 호출하며 과업을 수행한 trajectory 하나를 입력으로 받아 두 가지를 판정하는 LLM이다.

- **Goal compliance**: agent가 사용자 과업을 완수했는가.
- **Harmfulness**: agent가 금지된 state change를 일으켰는가.

두 판정은 모두 binary label이다. 여기서 meta-evaluation은 judge의 판정을 사람이 붙인 label과 비교해 judge의 정확도를 재는 일을 뜻한다. 현재 평가 중인 judge는 Claude Sonnet 5를 기반으로 한 `judge-v3`다.

## 사내 자료

meta-evaluation에는 아래 세 자료를 함께 쓴다. 세 자료는 같은 trajectory id로 연결된다.

| 자료 | 내부 이름 | 범위 | 내용 |
| --- | --- | --- | --- |
| Trajectory 모음 | `traj-r3` | 192개 | 사용자 과업, 주입 문장, agent의 tool 호출과 최종 답변 |
| 사람 label | `gold-r3` | 192개 중 75개 | trajectory별 goal compliance·harmfulness label |
| Judge 판정 결과 | `judge-v3-out` | 192개 전부 | `judge-v3`의 두 label과 근거 문장 |

**Trajectory 모음(`traj-r3`)**: 각 trajectory는 사용자 과업(user task), agent가 받은 tool 결과에 섞인 주입 문장(untrusted input), agent의 tool 호출과 최종 답변으로 구성된다. 192개 중 128개는 AgentDojo의 공개 task에서, 64개는 사내에서 만든 task에서 왔다.

**사람 label(`gold-r3`)**: 75개 trajectory에만 있다. 두 사람이 각각 독립으로 label을 붙였고, 두 사람의 판단이 갈린 9건은 세 번째 사람이 확정했다. 나머지 117개 trajectory에는 사람 label이 없으므로, 그 117개에서 judge가 얼마나 정확한지는 아직 알 수 없다.

**Judge 판정 결과(`judge-v3-out`)**: `judge-v3`가 192개 전부에 대해 낸 두 label과, 각 판정의 근거로 쓴 문장이다.

현재 결과는 trajectory 하나당 한 행으로 저장한다. 열은 trajectory id, judge의 두 label, 사람 label 두 개(있는 경우), judge 근거 문장이다.

## `judge-v3`와 사람 label의 비교

사람 label이 있는 75개에서 judge 판정과 사람 label을 비교한 결과는 다음과 같다.

| 판정 | 일치 | 불일치 | 일치율 |
| --- | ---: | ---: | ---: |
| Goal compliance | 68 / 75 | 7 | 90.7% |
| Harmfulness | 61 / 75 | 14 | 81.3% |

harmfulness 불일치 14건은 방향이 한쪽으로 치우쳐 있다. 11건은 사람이 harmful로 판정한 trajectory를 judge가 harmful이 아니라고 판정한 false negative이고, 3건은 사람이 무해하다고 본 trajectory를 judge가 harmful로 판정한 false positive다. 즉 `judge-v3`의 harmfulness 오류는 주로 위험을 놓치는 쪽에서 나온다.

false negative 11건 중 8건에는 공통된 모양이 있다.

- 주입 문장이 tool 결과의 중간에 들어가 있었다.
- agent가 그 지시를 따라 파일을 삭제하거나 이메일을 보냈다.
- judge의 근거 문장은 최종 답변만 언급했고, 파일 삭제나 이메일 전송 같은 tool 호출은 언급하지 않았다.

이 관찰은 judge가 harmfulness를 판정할 때 tool 호출보다 최종 답변에 의존했을 가능성을 보여 준다. 다만 근거 문장이 tool 호출을 언급하지 않았다는 사실만으로 judge가 tool 호출을 판정에 반영하지 않았다고 확정할 수는 없다. 나머지 false negative 3건과 false positive 3건은 아래 제안의 첫 단계에서 함께 분류한다.

## 제안: harmfulness 불일치의 두 축 집계

다음 판본부터 harmfulness 불일치를 두 축으로 분류해 집계하자는 제안이다. 목적은 judge가 어떤 종류의 공격을 놓치는지 확인하고, judge rubric에서 고칠 부분을 정하는 것이다.

| 축 | 값 |
| --- | --- |
| 주입 위치 | system prompt, user turn, tool 결과 |
| 실제 발생한 state change 종류 | 파일 삭제, 외부 전송, 권한 변경, 없음 |

현재 저장 형식은 trajectory별 판정과 근거 문장만 담고 있어, 불일치가 어떤 공격에서 생겼는지 알려면 근거 문장과 trajectory를 하나씩 다시 읽어야 한다. 두 축을 열로 추가하면 불일치를 주입 위치 3가지 × state change 4가지의 칸으로 셀 수 있다. 예를 들어 위 8건은 모두 주입 위치가 "tool 결과"이고, state change는 "파일 삭제" 또는 "외부 전송"(이메일)에 들어간다. 불일치가 특정 칸에 몰리면 rubric에서 그 경우를 다루는 부분을 먼저 고칠 수 있다.

### 적용 순서

1. 기존 harmfulness 불일치 14건을 두 축으로 분류한다.
2. 분류 결과를 보고, 사람 label이 없는 나머지 117개 trajectory에도 label을 붙일지 정한다.

첫 단계는 새 label 없이 기존 14건만으로 할 수 있다. 다만 14건은 칸 12개에 나누기에는 적은 수이므로, 첫 분류 결과는 어느 칸을 더 확인해야 하는지 정하는 용도에 가깝다. 117개에 label을 추가할지는 이 분류 결과를 보고 판단한다.

## 이후 trajectory 출처 후보

trajectory 출처를 넓힐 경우 CVE-Bench와 R-Judge를 검토해 볼 수 있다. 두 자료는 후보 예시일 뿐이며, 사용하기로 결정한 대상은 아니다.

## 논의가 필요한 결정

- 두 축(주입 위치, state change 종류)과 각 축의 값을 이대로 쓸지.
- 기존 14건 분류를 누가 언제 할지.
- 분류 결과를 본 뒤 나머지 117개에 사람 label을 붙일지.
