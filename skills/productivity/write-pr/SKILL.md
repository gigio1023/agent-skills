---
name: write-pr
description: |
  GitHub Pull Request 본문/제목을 작성하거나 기존 PR 본문을 갱신할 때 사용하는 스킬.
  존댓말, 20줄 이내, 왜(배경) + 결과(달라지는 것 + 영향) 중심으로 본문을 작성한다.
  파일/함수/라인 단위 디테일은 diff에 위임하고 본문에는 의도와 영향만 남긴다.
  검증/테스트 통과 여부는 본문에 적지 않는다 (CI 가 진실).
  Breaking Changes 는 별도 섹션 대신 결과 섹션 한 bullet 으로 통합한다.

  TRIGGER: "PR 작성", "pull request 만들어줘", "PR description 업데이트",
  "PR 본문 수정", "write a pull request", "open a PR", "draft PR", "gh pr".

  NOT for: GitHub Issue 작성(use write-issue), PR에 인라인 리뷰 코멘트 달기(use
  pr-review-comment), AI 생성 리뷰 검증(use validate-ai-review), PR 리뷰 수행
  자체(use code-review/review), 단순 커밋+푸시(use commit-push-sync).
version: 1.5.0
tags:
  - github
  - pull-request
  - korean
  - documentation
---

# Pull Request 작성 가이드

## Quick Start

```bash
# 1) 본문을 임시 파일에 먼저 쓴다 (heredoc + process substitution은 셸/gh 버전에 따라 본문이 누락됨)
cat > /tmp/pr-body.md <<'EOF'
Jira: https://jira.navercorp.com/browse/{이슈번호}

## 배경
{왜 이 작업이 필요한지 1-2문장, 존댓말}

## 변경 요약
- {핵심 변경 한 줄}
- {핵심 변경 한 줄}

## 결과
- {달라지는 동작/사용자 영향 한 줄}
- {Breaking 이 있으면 같은 섹션에 한 줄: "기존 X → 변경 Y. 운영 조치 한 줄"}
EOF

# 2) PR 생성 (GHE는 GH_HOST env var 필요. --hostname 플래그는 미지원 버전 있음)
GH_HOST=oss.navercorp.com gh pr create \
  --draft --base main --title "[ADAGENT-XXX] feat: 짧은 한 줄" \
  --body-file /tmp/pr-body.md --assignee @me
```

Jira 줄은 Jira 이슈가 명시적으로 제공된 경우만 둔다. 본문은 **20줄 이내가 기본**. 작은 PR 은 10줄 이하로 줄인다. 20줄을 넘으면 "분량 압축 순서"(`references/anti-patterns.md`) 대로 줄인다.

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| 간결성 우선 | 본문 전체 20줄 이내. 작은 PR은 10줄 이하. 리뷰어가 30초 안에 PR 의도와 영향을 파악할 수 있어야 함 |
| 존댓말 필수 | 모든 문장은 한국어 존댓말(`-습니다`, `-합니다`, `-됩니다`)로 마무리. bullet은 명사구 허용. 반말/명사 종결("했음", "수정") 금지 |
| 왜와 결과 우선 | 디테일한 구현 변경 나열보다 왜 했는지(배경)와 무엇이 달라지는지(결과)를 먼저 노출 |
| 디테일은 diff에 위임 | 변경 파일 목록, 함수 단위 변경, 라인 단위 설명은 본문에 적지 않음. diff와 커밋 메시지가 진실 |
| 검증/테스트는 본문에 적지 않음 | "pytest 통과", "lint 통과" 같은 문구 금지. CI 가 진실이고, 사람 리뷰어는 CI 결과를 직접 본다 |
| Breaking 은 결과에 통합 | 별도 섹션 만들지 않음. 결과 bullet 하나로 "기존 X → 변경 Y. 운영 조치 한 줄" 형태로 표현 |
| Jira 링크는 조건부 | Jira 이슈가 명시적으로 제공된 경우에만 본문 최상단에 전체 URL을 직접 기입. 이슈 키만 적은 형식(`Jira: ADAGENT-1`) 금지 |
| 처음 보는 사람 기준 | 이 레포를 처음 보는 동료도 본문만 읽고 "왜 이게 필요했고 머지하면 뭐가 달라지는지" 이해할 수 있어야 함. AI 세션 코드명("Workstream B", "round5", "fixture A"), 로컬 파일명, 작업자만 아는 약어 금지 |
| nested bullet 구조화 | 한 변경에 sub-aspect(왜/기존 vs 신규/영향 범위)가 2개 이상이면 nested bullet 1단으로 구조화. flat 나열보다 관계가 명확해진다. 단, 2단 이상 중첩은 PR을 쪼개는 신호 |
| PR 본문은 운영 문서가 아님 | 긴 postmortem, 측정 로그, 링크 모음, 체크박스형 Test Plan 을 본문에 복붙하지 않음. 필요한 상세는 별도 문서나 diff에 둔다 |
| 자동 생성 흔적 제거 | `Generated with Claude Code`, 작업 세션 요약, assistant 이름, 로컬 경로는 본문에 남기지 않음 |
| 이모지 금지 | 이모지 사용하지 않음 |
| AI slop 구두점 금지 | em dash(`—`), middle dot(`·`), bullet(`•`) 금지. 하이픈(`-`), 쉼표(`,`), 마침표(`.`)만 사용 |

## 분량 가이드

| 섹션 | 적정 분량 |
|------|----------|
| 배경 | 1-2문장. 왜 이 작업이 필요했는지만 |
| 변경 요약 | 2-4 bullet. 한 줄에 하나의 의미 단위 변경 |
| 결과 | 1-3 bullet. 사용자/시스템 관점에서 무엇이 달라지는지. Breaking 영향이 있으면 그 중 1-2 bullet 으로 흡수 |

전체 20줄 이내. 검증 섹션은 만들지 않는다. Breaking Changes 섹션도 만들지 않는다.

## Bad / Good 예시

### 구현 나열 대신 의도와 영향

Bad:
```markdown
- `src/answer_fusion/client.py` 에서 `chat.completions.create` 를 `parse` 로 변경
- `tests/test_response_schema.py` 추가
- pytest 82 passed
```

Good:
```markdown
## 배경
Answer Fusion SOAP 응답에서 광고 후보가 있는데도 빈 결과가 정상 응답처럼 반환되는 사례가 있었습니다.

## 변경 요약
- LLM 응답을 schema 강제 Structured Outputs로 받도록 변경합니다.
- 실패 또는 미배치 후보를 rejected_ads에 reason과 함께 채웁니다.

## 결과
- Caller가 후보 없음, LLM 실패, 모든 후보 미배치를 구분할 수 있습니다.
```

### nested bullet은 관계가 있을 때만

Bad:
```markdown
- outputSchema 수정
- runtime flag 수정
- default 수정
- drift test 추가
```

Good:
```markdown
- Agent Card와 runtime 동작을 같은 기준으로 맞춥니다.
    - 기존: outputSchema와 runtime default가 실제 실행과 어긋남
    - 변경: caller가 보낸 runtime flag가 graph 실행까지 전달됨
```

## 작성 프로세스

### Step 1: 상황 파악

```bash
git branch --show-current
gh pr view --json number 2>/dev/null && echo "PR 있음" || echo "PR 없음"
git log --oneline origin/main..HEAD
git diff --stat origin/main..HEAD
```

상황 분기:

| 현재 상태 | 행동 |
|----------|------|
| `main`/`master` 브랜치 | 새 브랜치 생성 → 푸시 → PR 생성 |
| 별도 브랜치, PR 없음 | 푸시 → PR 생성 |
| 별도 브랜치, PR 있음 | `gh pr edit {N} --body-file /tmp/pr-body.md` |

### Step 2: 본문 초안

Quick Start 템플릿 그대로. 20줄 검증:

```bash
wc -l /tmp/pr-body.md   # 20줄 넘으면 references/anti-patterns.md "분량 압축 순서" 적용
```

### Step 3: PR 생성/갱신

```bash
# 신규
GH_HOST=oss.navercorp.com gh pr create \
  --draft --base main --title "..." --body-file /tmp/pr-body.md --assignee @me

# 갱신
GH_HOST=oss.navercorp.com gh pr edit {PR번호} --body-file /tmp/pr-body.md
```

GHE 호스트는 `GH_HOST` 환경변수로 지정한다. 일부 `gh` 버전은 `--hostname` 플래그를 인식하지 못한다.

### Step 4: Jira 링크와 GitHub 이슈 닫기

- Jira 링크: `Jira: https://jira.navercorp.com/browse/{KEY}` 전체 URL 형식. 이슈 키만 적지 않음
- GitHub 이슈: `Closes #{N}`을 같이 적음. Jira 링크와 둘 다 적을 수 있음 (대체 관계 아님)

## Gotchas

- **존댓말 위반이 가장 흔한 미스**: 작성 직후 본문을 한 번 훑어 모든 평서문이 `-습니다`, `-합니다`, `-됩니다`로 끝나는지 확인. bullet은 명사구 허용이지만 본문 평서문은 반드시 존댓말.
- **검증 섹션을 만들고 싶은 충동**: pytest/lint 결과를 적고 싶어지지만 적지 않는다. CI 가 진실이고, 본문에 적힌 "통과" 문구는 시간이 지나면 거짓이 된다. 본문에는 결과 (사용자/시스템 영향) 만 남긴다.
- **Breaking 을 별도 섹션으로 빼고 싶은 충동**: 결과 섹션에 "기존 X → 변경 Y. 운영 조치 Z" 한 bullet 으로 흡수한다. 별도 섹션을 만들면 본문이 두 배로 길어지고 "결과" 와 "Breaking" 이 같은 사실을 두 번 말하게 된다.
- **heredoc + process substitution은 깨진다**: `--body-file <(cat <<EOF ...)` 패턴은 zsh/bash, `gh` 버전에 따라 본문 일부가 누락되거나 빈 본문으로 PR이 생성된다. 항상 `/tmp/pr-body.md` 같은 파일에 먼저 쓰고 `--body-file <path>`로 넘긴다.
- **GHE는 `--hostname` 안 먹을 수 있다**: 일부 `gh` 버전(특히 OSS GHE 호환 버전)에서 `gh --hostname X pr create`가 "unknown flag: --hostname" 에러로 도움말만 출력한다. `GH_HOST=oss.navercorp.com gh pr create ...`로 환경변수 사용.
- **PR 제목에 Jira 키 미포함이면 development panel 비활성**: OSS DVCS integration의 기본 Link Condition은 PR title이다. `Jira: https://...`만 본문에 적으면 사람은 클릭 가능하지만 Jira 개발 패널에서 PR을 못 찾는다. 제목에 `[ADAGENT-XXX]`를 포함시킨다.
- **20줄을 넘기면 리뷰어가 본문을 안 읽는다**: 디테일을 모두 적고 싶은 충동을 누른다. follow-up은 별도 이슈/코멘트로, 함수 단위 변경은 diff로 위임.
- **결과 섹션이 비면 PR 의도가 흐려진다**: "이 PR로 사용자/시스템에서 무엇이 달라지는지"가 비어 있으면 왜 머지해야 하는지 리뷰어가 판단할 수 없다. "변경 요약"과 "결과"는 다른 정보이다. 변경 요약은 우리가 한 일, 결과는 리뷰어가 받게 될 것.
- **현재 PR 본문을 commit message처럼 쓰는 실수**: commit message 는 변경 이력을 남기고, PR 본문은 리뷰어가 머지 판단을 하게 돕는다. commit message 의 bullet 을 그대로 복붙하면 파일/함수/측정 로그가 과다 노출된다.
- **Test Plan checkbox 복붙**: GitHub template 의 `Test plan` 과 checkbox 는 자동으로 남기지 않는다. 본문에는 테스트 수행 여부를 적지 않고, CI 결과와 리뷰 코멘트로 확인한다.
- **Claude footer 제거**: `Generated with Claude Code` 같은 footer 는 PR 본문에 남기지 않는다. co-author trailer 가 필요하면 commit message 에서만 다룬다.
- **내부 약어 과다 노출**: CADI, RADAR, MCP, A2A 처럼 팀 안에서는 익숙해도 리뷰어 범위가 넓으면 첫 등장에 짧게 풀어 쓴다. 제목에서 이미 분명하면 본문에서 반복 설명하지 않는다.
- **물결 표기는 GitHub/Jira에서 취소선이 된다**: `~10건~`, `1~6건` 같이 쓰면 취소선으로 렌더링된다. "약 10건", "1-6건"(하이픈)으로 작성한다.
- **Closes/Fixes 키워드는 본문 어디에 있어도 작동**: 단, 다른 PR이 같은 이슈에 대해 먼저 머지되면 자동으로 닫혀버리므로 의도된 이슈 번호인지 확인.
- **PR 본문이 작업자 개인 메모가 되는 경우**: 세션 중 합의한 코드명("round5", "Workstream B", "fixture A"), 로컬 파일 경로, 대화 중 약어를 그대로 박으면 처음 보는 리뷰어는 컨텍스트 없이 막힌다. 내부 식별자는 풀어서 설명하거나 생략한다.

## 본문 작성 규칙

- "배경"은 사실과 동기를 한 문단으로. 분석 수치 같은 디테일은 1-2줄로 압축
- "변경 요약"은 파일/함수 단위가 아니라 의미 단위로. "rules.py 수정" X, "알림을 error_type별로 분리" O
- "결과"가 비어 있으면 PR이 왜 필요한지 다시 자문할 것. 순수 리팩터처럼 사용자 노출 변화가 없을 때는 "내부 정합성/유지보수성 개선"도 결과로 인정하되 무엇이 구체적으로 쉬워지는지를 적는다 ("타입 시그니처 통일로 신규 어댑터 추가 시 보일러플레이트 1파일로 줄어듭니다")
- "결과"에 Breaking 영향이 있으면 한 bullet 으로 흡수: "기존 alert UID `X` → `Y`. silence 규칙 재설정 필요합니다"
- Breaking 영향이 1-2 bullet 으로 표현되지 않을 만큼 크면 PR 자체를 쪼갠다. 결과 섹션이 Breaking 으로만 채워지면 "변경 요약"과 구분이 사라진다
- Breaking 이 없는 PR 은 그냥 결과만 적는다. "Breaking 없음" 같은 의례적 문구는 적지 않는다
- 검증/테스트 섹션은 작성하지 않는다. CI 가 진실이고 사람 리뷰어는 CI 결과를 직접 본다
- 후속 작업/follow-up은 코멘트나 후속 이슈에서 다룸. PR 본문에 길게 적지 않음
- 현재 본문에 `Summary`, `Configuration`, `Test Plan`, `검증`, `추가`, `결정`, `머지 전 검토 필요` 같은 섹션이 많으면 대부분 압축 대상이다. `배경`, `변경 요약`, `결과` 세 섹션으로 다시 쓴다
- postmortem 문서 PR도 본문에 리포트 전체를 요약하지 않는다. 원인, 추가 문서, 리뷰어가 확인할 결과만 남긴다
- 변경사항은 카테고리 소제목 없이 flat 나열이 기본. 3개 이상 카테고리일 때만 H3 소제목 사용
- 한 bullet에 sub-aspect(기존 vs 신규, 영향 범위, 예외 조건)가 2개 이상이면 nested bullet 1단 사용. 예: `- retrieval_source 정규화` → 하위 bullet으로 `기존: MCP_ERROR → normalized → 알림 소실`, `변경: metric_source 필드로 raw 값 분리 보존`
- 모든 bullet을 nested로 만들지 않는다. sub-aspect 없이 한 줄로 표현 가능하면 flat이 맞다
- 참고사항은 lock 파일 diff 등 오해 소지가 있을 때만

## Reference Files

| File | When to read | Content |
|------|-------------|---------|
| `references/anti-patterns.md` | 본문 검토 시, 20줄 넘었을 때 | Bad/Good 표, 분량 압축 순서 |
| `references/examples.md` | 본문 톤이 감이 안 올 때 | 좋은 예시 2개 + 나쁜 예시 2개 |

## 체크리스트

PR 생성/갱신 직전에 본문에 대해 다음을 확인:

- [ ] 모든 평서문이 존댓말로 끝남
- [ ] 본문 전체 20줄 이내 (`wc -l /tmp/pr-body.md`)
- [ ] 배경(왜)과 결과(달라지는 것)가 모두 적혀 있음
- [ ] 검증/테스트 섹션 없음 (pytest/lint 통과 같은 문구 금지)
- [ ] Breaking 영향이 있다면 결과 섹션의 bullet 으로 흡수되어 있음 (별도 Breaking Changes 섹션 없음)
- [ ] 파일/라인 단위 디테일이 본문에 없음 (diff에 위임)
- [ ] Jira 이슈가 제공된 경우 상단에 `Jira: https://jira.navercorp.com/browse/{KEY}` 전체 URL 형식
- [ ] PR 제목에 `[ADAGENT-XXX]` 또는 `Closes #N`이 포함되어 DVCS 연동이 작동
- [ ] 이모지 미사용
- [ ] follow-up 줄줄이 나열 없음 (별도 이슈/코멘트로)
- [ ] 처음 보는 동료가 본문만 읽고 "왜 필요했고 머지하면 뭐가 달라지는지" 이해 가능한지 확인
- [ ] AI 세션 전용 참조 없음 (문서 섹션 번호, 작업공간 로컬 파일명, 대화 중 합의한 약어, "round5"/"Workstream B" 같은 세션 코드명)
- [ ] 자동 생성 footer 없음 (`Generated with Claude Code` 등)
- [ ] `Summary`/`Test Plan` template 를 그대로 남기지 않음
- [ ] 물결 표기 `~text~` 미사용
- [ ] AI slop 구두점 미사용 (`—`, `·`, `•` 금지)
