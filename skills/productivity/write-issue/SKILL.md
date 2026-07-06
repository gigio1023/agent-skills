---
name: write-issue
version: 1.0.0
description: |
  GitHub Issue 작성/정비 스킬.
  트리거: "이슈 만들어줘", "이슈 작성", "issue 생성", "이슈 내용 정리", "이슈 문구 수정" 요청 시.
  깨진 Markdown(escaped newline)과 영문-only 본문을 방지하고, 한국어 중심의 실행 가능한 이슈 본문 및 이슈 코멘트를 작성/수정한다.
  NOT for: PR 본문 작성/수정(use write-pr), Jira 이슈(use a Jira-specific issue skill).
---

# write-issue

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| 간결 | 1줄로 쓸 수 있으면 1줄로 |
| 명료 | 읽는 사람이 "뭘 하면 되지?"를 즉시 파악 |
| 정확 | 모호한 표현 금지, 구체적 작업 제시 |
| 이모지 최소화 | 이모지 사용하지 않음 |

## 작성 규칙

- 한국어 중심 (영어-only 금지, 필요한 용어만 영어 혼용)
- 개조식
- 문서/파일 언급 시 Markdown 링크 사용 (짧게)
- 작업은 반드시 체크리스트로
- Assignee는 `@me`
- 제목/본문/코멘트 모두 Markdown 렌더링 기준으로 작성

## 원문 Markdown 노출 금지 규칙 (추가)

- PR 본문/코멘트, Issue 본문/코멘트에 **기존 원문(raw) Markdown을 그대로 재게시하지 않는다**.
- 기존 본문을 인용해야 하면 원문 dump 대신 **요약/재작성**해서 게시한다.
- 다음 패턴은 금지:
  - `Original body:` 이후 원문 전체 붙여넣기
  - 원문을 코드블록(````md ... ````)으로 통째로 복붙
  - escaped newline(`\\n`)이 보이는 문자열을 그대로 게시

## AI 세션 맥락 노출 금지

AI와의 대화에서만 통용되는 참조를 이슈/PR 본문에 그대로 쓰지 않는다.
읽는 사람은 AI 세션에 참여하지 않았으므로, 세션 내부 참조만으로는 의미를 알 수 없다.

금지 패턴:
- 내부 문서 섹션 번호만 단독 사용: "§6.7", "SSOT 항목 3번"
- 작업공간 로컬 파일명: "METRICS_TRUTH.md", "plan.md", "handoff.md"
- AI 대화에서 합의한 약어를 정의 없이 사용

교정 방법:
- 섹션 번호 → 그 섹션이 뜻하는 내용을 직접 쓰기
- 로컬 파일 → 대상 레포에서 확인 가능한 경로나 설명으로 대체
- 약어 → 처음 등장 시 풀어서 쓰기

판단 기준: **이 URL만 받은 동료가 30초 안에 이해할 수 있는가?**

## 필수 품질 게이트

- literal escaped newline 금지: 본문/코멘트에 `\\n`, `\\r\\n`, `\\t` 문자열이 그대로 들어가면 안 됨
- 본문/코멘트 언어 규칙: 한글 문장 최소 1개 이상 포함
- 생성/수정/코멘트 모두 `--body-file` 사용 (`--body` inline 문자열 금지)

## 기존 이슈 정비 워크플로우

1. 스캔
   - `python3 scripts/audit_issue_bodies.py --repo <owner/repo> --author <login> --state open`
2. 수정 대상 확정
   - `escaped_newline=true` 또는 `english_heavy=true`면 수정 대상
3. 본문 재작성
   - 임시 `.md` 파일에 한국어 중심 템플릿으로 재작성
4. 이슈 업데이트
   - `gh issue edit <번호> --title "<제목>" --body-file <파일>`

## 이슈 본문 템플릿

```md
## 배경
- (왜 필요한지 1~2줄)

## 목표
- (완료 시 달라지는 것)

## 범위
| 포함 | 제외 |
|------|------|
| ... | ... |

## 작업 목록
- [ ] ...
- [ ] ...

## 완료 기준
- ...
```

### 선택 섹션 (필요 시에만)

```md
## 레퍼런스
- [README](README.md)
```

## gh cli 명령어

```bash
gh issue create --title "feat: ..." --body-file <(cat <<'EOF'
(본문)
EOF
) --assignee @me
```

수정 시:

```bash
gh issue edit <번호> --title "..." --body-file <(cat <<'EOF'
(수정 본문)
EOF
)
```

이슈 코멘트:

```bash
gh issue comment <번호> --body-file <(cat <<'EOF'
(재작성된 코멘트 본문)
EOF
)
```

PR 본문 수정:

```bash
gh pr edit <번호> --body-file <(cat <<'EOF'
(재작성된 PR 본문)
EOF
)
```

PR 코멘트:

```bash
gh pr comment <번호> --body-file <(cat <<'EOF'
(재작성된 코멘트 본문)
EOF
)
```

## 안티패턴

| Bad | Good |
|-----|------|
| 장황한 배경 설명 | 핵심만 1~2줄 |
| "여러 파일 수정 예정" | 구체적 파일/모듈 명시 |
| 이모지 남발 | 이모지 미사용 |
| 모호한 완료 기준 | 측정 가능한 기준 |
| `\\n` 문자열이 보이는 본문 | 실제 줄바꿈이 있는 Markdown 본문 |
| 영어-only 본문 | 한국어 중심 + 필요한 용어만 영어 혼용 |
| 원문 Markdown 통복붙 | 요약/재작성 후 게시 |
| AI 세션 맥락 노출 ("§6.7", "SSOT 항목 3번") | 내용을 직접 풀어쓰기 ("기존 stage 체계") |
| 물결 표기 `~text~` 사용 (취소선으로 렌더링됨) | 약, 대략 등 한국어 표현 또는 하이픈 범위 `1-6건` |
