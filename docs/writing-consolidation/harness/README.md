# 행동 비교 harness

writer 스킬의 판본 두 개 이상을 같은 과제로 실행하고, 초안과 교정 세 차례의 결과를 익명 채점으로 비교한다. 규칙을 넣거나 빼기 전에 돌리고, 결과는 [results](results-2026-09-23.md)처럼 회차별 파일로 남긴다. 스킬을 고칠 때 이 폴더의 packet과 채점 기준을 그대로 다시 쓴다.

| 파일 | 내용 |
|---|---|
| [comparison-plan.md](comparison-plan.md) | arm 구성, 과제 둘, 측정 세 층, 판정 조건 |
| [packet-template.md](packet-template.md) | 실행자에게 주는 packet. `__SKILLS__`에 arm의 스킬 경로만 바꾼다 |
| [rubric.md](rubric.md) | 채점 항목. 초안용 a~j와 교정 추적용 a~h |
| [results-2026-09-23.md](results-2026-09-23.md) | 첫 회차 결과와 읽는 법 |
| [scorer-packet.md](scorer-packet.md) | 익명 채점자(subagent)에게 주는 packet |
| `make_arm.py` | packet의 placeholder를 채우고 arm workspace(packet.md, source-report.md, pr.diff, out/)를 만든다 |
| `auto_measures.py` | arm workspace들의 out/에 check_draft와 protected_diff를 돌려 자동 표시 행을 출력한다 |

## 절차

1. 원자료를 고른다. 예시 제작에 쓰지 않은 실제 문서 하나(20~30KB)와 실제 diff 하나. 원자료는 공개 저장소에 두지 않고 로컬 workspace에 `source-report.md`, `pr.diff`로 놓는다.
2. arm마다 `make_arm.py`로 workspace를 만든다. `--skills`만 다르게 하고 나머지 인자는 같게 둔다. 비교하려는 차이(스킬 판본, 함께 로드하는 자매 스킬 유무)만 다르게 한다.
3. 모델은 실제 사용 환경 둘 이상(예: Codex GPT-6 Astra xhigh, Claude Opus). 실행자는 packet 밖 자료를 읽지 않는다.
4. 자동 표시: `auto_measures.py <workspace>...`가 초안 표시 건수, r1 유지율, r2와 r3의 요청 밖 변경 수를 한 표로 낸다. `--allow`에 교정이 이름 붙인 절을 준다.
5. 익명 채점: 출력물을 `arms/<중립 라벨>/`로 복사하고 `scorer-packet.md`와 rubric, 원자료, 교정 문장을 함께 준다. 한 채점자(subagent)가 모든 arm을 같은 기준으로 센다. 채점자가 바뀌면 회차 간 수치를 직접 비교하지 않는다.
6. 판정 조건에 하나라도 어긋나면 그 과제만 반복해 원인을 보고 스킬을 고친 뒤 다시 실행한다. arm당 표본이 하나면 크기는 방향만 읽는다.

## 한계

- arm당 문서 하나라 차이의 크기는 신뢰할 수 없다. 방향이 두 모델에서 같을 때만 결론으로 쓴다.
- 채점 기준 (b)는 관측과 추론을 구분하는 정당한 단서까지 감점할 수 있다. (c)와 (d)가 그 편향을 상쇄한다.
- 교정 세 차례는 실제 세션보다 짧다. 세션에서 관찰된 drift(교정마다 전체 재작성)는 이 길이에서 약하게만 재현된다.
