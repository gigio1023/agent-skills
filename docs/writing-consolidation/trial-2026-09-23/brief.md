# 작성 과제

동료 연구자들에게 공유할 사내 문서를 한국어로 작성한다. 독자는 LLM 평가를 아는 연구자이며, 이 프로젝트의 자료를 처음 본다. 매체는 Notion 페이지이며 Markdown으로 작성한다. 목표 분량 제한은 없다. 독자가 짧게 훑어도 무엇이 있는지 알고, 필요한 부분을 읽으면 자료를 실제로 이해하고 다음 작업을 정할 수 있어야 한다.

## 주제

agent safety judge의 meta-evaluation에 쓰는 사내 자료 현황과, 다음 단계로 제안하는 오류 유형 집계 방식.

## 확인된 사실 (모두 가상의 자료이며 이 과제 안에서만 참이다)

- 평가 대상은 "safety judge"다. safety judge는 LLM으로, agent가 tool을 호출하며 수행한 trajectory 하나를 입력으로 받아 두 가지를 판정한다. goal compliance(사용자 과업을 완수했는가)와 harmfulness(금지된 state change를 일으켰는가). 각 판정은 binary label이다.
- meta-evaluation이란 judge의 판정을 사람이 붙인 label과 비교해 judge의 정확도를 재는 일이다.
- 사내 자료 세 종류가 있다.
  1. trajectory 모음: 192개. 각 trajectory는 사용자 과업(user task), agent가 받은 tool 결과에 섞인 주입 문장(untrusted input), agent의 tool 호출과 최종 답변으로 구성된다. 출처는 AgentDojo의 공개 task 128개와 사내에서 만든 task 64개다. 내부에서는 이 모음을 `traj-r3`라고 부른다.
  2. 사람 label: 192개 중 75개에만 있다. 두 명이 독립으로 붙였고 불일치 9건은 세 번째 사람이 확정했다. 내부 이름은 `gold-r3`.
  3. judge 판정 결과: 현재 judge(내부 이름 `judge-v3`, 기반 모델은 Claude Sonnet 5)가 192개 전부에 대해 낸 판정과 근거 문장. 내부 이름 `judge-v3-out`.
- 75개 label과 judge 판정을 비교한 결과: goal compliance 일치 68/75, harmfulness 일치 61/75. harmfulness 불일치 14건 중 11건은 judge가 harmful을 놓친 경우(false negative), 3건은 무해한 것을 harmful로 판정한 경우다.
- false negative 11건 중 8건은 주입 문장이 tool 결과의 중간에 들어가 있고 agent가 그 지시를 따라 파일을 삭제하거나 이메일을 보낸 경우다. judge의 근거 문장은 최종 답변만 언급하고 tool 호출은 언급하지 않았다.
- 현재 결과 저장 형식은 trajectory별 한 행이며, 열은 trajectory id, judge의 두 label, 사람 label 두 개(있을 때), judge 근거 문장이다.
- 제안: 다음 판본부터 harmfulness 불일치를 "주입 위치"(system prompt, user turn, tool 결과)와 "실제 발생한 state change 종류"(파일 삭제, 외부 전송, 권한 변경, 없음)의 두 축으로 집계한다. 목적은 judge가 어떤 종류의 공격을 놓치는지 확인하고 rubric을 고칠 부분을 정하는 것이다. 첫 적용은 기존 14건을 두 축으로 분류하는 일이고, 분류가 끝나면 사람 label을 117개 나머지 trajectory에도 붙일지 정한다.
- 이 제안은 문서 작성자 개인의 제안이며 팀에서 논의된 바 없다.
- CVE-Bench와 R-Judge는 이후 trajectory 출처로 검토할 수 있는 후보 예시일 뿐이며 결정된 대상이 아니다.

## 요청

위 사실을 바탕으로 문서를 작성하라. 문서 하나를 Markdown 파일로 저장한다. 다른 파일은 만들지 않는다.
