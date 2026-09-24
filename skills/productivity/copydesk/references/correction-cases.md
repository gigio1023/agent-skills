# 교정 사례

이 사례들은 사용자가 한국어 기술 문서에서 반복해서 고친 문장 유형을 실제 교정 기록에서 뽑아 합성으로 다시 쓴 것이며, 사용자 발화 인용만 원문이다. 한국어 기술 문서를 쓰거나 고치기 전에 읽는다. 수정한 뒤에는 직전 판본과의 diff에 이 모양이 새로 생기지 않았는지 확인한다.

### 삭제된 읽기 안내의 재생

**계기**: 사용자가 읽는 길과 학습 목표를 직접 지운 뒤 "기초 이론은 Collapse하고, 펴서 볼 수 있도록 가이드"를 요청했다.

**실패한 문장**: "기초 읽기: vector projection이 낯설면 기초 1부터, Transformer 구조가 궁금하면 기초 2~4를 펼쳐 본다." toggle 제목은 "처음 읽는다면 여기부터".

**고친 문장**: toggle 제목 "Residual stream에 쓰는 행렬". 첫 문장: "Attention과 FFN의 출력은 `o_proj`와 `down_proj`를 거쳐 residual stream에 더해지므로, refusal direction을 지우려면 이 두 행렬의 weight를 편집한다."

**판정**: 접힌 절의 제목과 첫 문장이 내용을 말하게 하고, 언제 펼칠지 안내하는 문장은 어느 자리에도 다시 쓰지 않는다.

### 지시문의 본문 이식

**계기**: "최신인게 가장 위에", "pr 항상 as-is, to-be를 명확하게".

**실패한 문장**: "Source artifact의 기록 날짜 기준 최신순이다." "이 PR은 as-is와 to-be를 명확히 구분해 설명한다."

**고친 문장**: 표를 날짜 내림차순으로 둔다. PR 본문: "As-is: judge 호출이 실패하면 그 row를 건너뛴다. To-be: 실패한 row를 `unscorable`로 기록하고 집계에서 따로 센다."

**판정**: 사용자 지시는 문서를 바꾸는 작업으로 실행하고, 지시 내용을 설명하는 문장은 만들지 않는다.

### 검토 단서의 본문 유입

**계기**: subagent 검토의 표본 수 단서가 3분 뒤 본문 callout이 됐고, 사용자는 "이런류의 문장은 아예 쓰지말고 제거"라고 했다.

**실패한 문장**: "Stored result row를 independent sample이나 verified label로 세지 않는다."

**고친 문장**: "Result row 96개는 target LLM answer 8건을 judge configuration 12개로 각각 채점한 결과다."

**판정**: 검토 단서는 수치를 점검할 이유로만 쓰고, 본문에는 그 수치가 무엇과 무엇의 곱인지 쓴다.

### 부정형 정의로 대신한 설명

**계기**: "설명한 척"이라는 지적 뒤 추가된 문단을 두고 "하나도 영양가 없어".

**실패한 문장**: "평가 대상은 response를 생성한 model이 아니라 그 response를 채점하는 judge다. Label 자체에 대한 독립 검토는 남아 있다."

**고친 문장**: "Judge meta-evaluation은 같은 target LLM answer를 여러 judge configuration에 채점시키고, 각 judge prediction을 reference label과 비교한다. 결과는 configuration별 agreement와, label이 `harmful`인데 prediction이 `safe`인 사례 목록이다."

**판정**: 대상이 무엇을 입력받아 무엇을 하고 무엇을 내놓는지 쓰고, 부정형 정의와 남은 검토 목록은 지운다.

### 생산자 없는 명칭

**계기**: "뭐에 대한 response인데? llm의 단건 응답? 최종 응답? 혹은 tool calling 한번?", "대체 뭐에 대한 judge이고 뭐에 대한 rubric".

**실패한 문장**: "실제 response와 기존 judge output을 비교한다. v3 자료로 rubric v3를 검증한다."

**고친 문장**: "Target LLM의 single-turn answer마다 붙은 reference label을 harmfulness judge의 prediction과 비교한다. 판정 기준은 harmfulness judge rubric이며 내부 revision `rev-b`는 조회용으로 병기한다."

**판정**: 명칭에 평가 단위, 생산자, 역할을 넣고 version은 뒤에 붙는 조회용 식별자로 둔다.

### 예시의 확정 대상 승격

**계기**: "CVEBench와 AgentDojo는 예시야. 마치 이거 두개를 타겟하는것처럼 하지말아줘".

**실패한 문장**: 절 제목 "시작할 benchmark", 본문 "CVE-Bench와 AgentDojo를 먼저 실행하며 evaluation harness를 구축한다."

**고친 문장**: "Official runner와 scorer가 공개된 public benchmark 두세 개를 먼저 실행해 harness의 task adapter와 scorer 연결을 검증한다. 후보로는 취약점 공격 실행을 채점하는 CVE-Bench와 prompt injection 저항을 채점하는 AgentDojo가 있다."

**판정**: 선정 기준을 먼저 쓰고 이름은 후보로 표시하며, 절 제목과 그림 label도 같은 지위로 맞춘다.

### 개인 제안의 논의 중 변환

**계기**: 사용자가 자기 제안이라고 밝힌 문서에서 작성자 표현을 지우라고 했다.

**실패한 문장**: 첫 판 "1부. 내가 제안하는 평가", 다음 판 "평가 방향은 팀 내에서 논의 중이며 아직 확정되지 않았다."

**고친 문장**: 절 제목 "Agent safety 평가 설계 제안". 본문: "첫 비교는 agent scaffold를 고정하고 model만 바꾼다. 같은 task set에서 task 성공률과 호출 비용을 기록한다."

**판정**: 제안 지위는 제목이나 metadata에서 한 번 밝히고, 본문은 제안 내용을 평서문으로 쓰며 없는 논의를 만들지 않는다.

### 축약 요청 뒤 mechanism 삭제

**계기**: "이론 설명은 좋긴한데 너무 길어" 뒤 figure와 수식의 대부분이 사라졌고, 사용자는 "상세한 figure나 이론 설명들이 너무 많이 덜어진거 같은데 이런것들은 유지"라고 했다.

**실패한 문장**: "Refusal direction은 harmful prompt와 harmless prompt의 activation 차이다. 이 방향을 weight에서 제거하면 거부가 줄어든다."

**고친 문장**: "Layer $l$에서 harmful prompt의 평균 activation $\mu^{+}$에서 harmless prompt의 평균 $\mu^{-}$를 빼고 정규화해 $\hat r$을 얻는다. Residual stream에 쓰는 행렬마다 $W \leftarrow W - \hat r \hat r^{\top} W$를 적용하면 어떤 입력에서도 그 행렬의 출력에 $\hat r$ 성분이 남지 않는다."

**판정**: 축약 요청에는 읽기 안내, 반복, 과정 서술, 망라 목록을 지우고 mechanism, 수식, 주제 그림, 확정된 예시는 남긴 뒤 직전 판본과 diff해 확인한다.

### 주제와 무관한 첫 그림

**계기**: "너무 기초라서 사실 refusal research와는 좀 관련없어보여".

**실패한 문장**: "그림 1. Transformer block의 attention, FFN, residual 연결"

**고친 문장**: "그림 1. Refusal direction의 추출, 제거, 평가. Harmful과 harmless prompt의 activation 차이로 방향을 구하고, write 행렬에서 그 성분을 지운 뒤, refusal rate와 일반 benchmark 점수를 원본 model과 비교한다."

**판정**: 첫 그림에는 문서 주제의 관계를 그리고, 선행 지식 그림은 그것이 필요한 절의 접힌 영역으로 옮긴다.

### 면피 문구로 채운 상태 열

**계기**: "자산 규모와 상태 테이블에서 상태는 필요없어. 이것보단 규모만 정확하게".

**실패한 문장**: 상태 열의 "Label review 필요", "기록 있음; acceptance criterion 없음".

**고친 문장**: 규모 열만 남긴다: "Target LLM answer 120건, harmfulness label 120개", "Agent task 40개, state-based verifier 36개".

**판정**: 상태 열은 값이 독자의 다음 행동을 바꿀 때만 두고, 규모는 단위가 붙은 개수로 쓴다.

### 수량의 수식화와 checkbox

**계기**: "억지로 만든 수식(v3에 대한 n 설명)은 제거해줘 너무 이상해".

**실패한 문장**: display 수식 "$$n_{\mathrm{rev\text{-}b}} = 150$$", 완료 조건 "- [ ] 모든 run에 model, prompt, environment, scorer revision이 기록돼 있다."

**고친 문장**: "Reference label set(내부 revision `rev-b`)은 150건이다. 완료 기준: 모든 run이 model, prompt, environment, scorer revision을 같은 run ID로 남긴다."

**판정**: 수식은 계산이나 관계를 보일 때, checkbox는 독자가 실제로 체크할 때만 쓰고, 수량과 기준은 평서문으로 쓴다.

### 보이는 배열을 읊는 문장

**계기**: "어차피 테이블에서 암묵적으로 이런게 표현되어 있고", "이런게 '불필요하게 작성된 문장'이라고".

**실패한 문장**: "아래 표는 사건 경과를 시간순으로 정리한 것이다. 마지막 열이 핵심이다."

**고친 문장**: "탈취된 CI token으로 14:05에 package가 게시됐고, 14:40에 token을 폐기하기까지 35분 동안 악성 version 두 개가 배포됐다."

**판정**: 표 위 문장에는 표에서 바로 읽히지 않는 결론을 쓰고, 표의 배열과 열을 설명하는 문장은 지운다.
