---
name: commit-push-sync
version: 1.0.0
description: |
  변경사항을 논리적 단위로 분할 커밋하고 push까지 안정적으로 수행한다.
  이슈/PR 코멘트, 본문 수정, 제목 수정은 사용자가 명시적으로 요청한 경우에만 수행한다.
  트리거: "commit", "push", "git push", "커밋", "분할 커밋", "stage and commit", "push 해줘", "sync issue/PR updates", "commit to main", "direct commit"
---

# Smart Commit, Push, and Sync

변경사항을 논리적 단위로 분할해 커밋하고 push한다.

기본 원칙:
- 이 스킬의 기본 책임은 커밋 품질과 push 안정성에 집중하는 것임
- 이슈/PR 코멘트 추가, 본문 수정, 제목 수정은 기본 동작이 아님
- 사용자가 같은 턴에서 명시적으로 요청한 경우에만 이슈/PR 업데이트를 수행함
- 커밋 전 CI 전체 검증이 필요하면 `repo-ci-gate`, PR 본문 작성이 필요하면 `write-pr`를 사용함

## Process

1. **Check conventions**: `CONTRIBUTING.md` 확인 (없으면 conventional commits)
2. **Verify branch**: `git branch --show-current`로 현재 브랜치 확인
3. **Pull latest**: `git pull --rebase` (main 직접 커밋 시 필수)
4. **Analyze changes**: `git status` + `git diff`로 전체 변경 파악
5. **Group logically**: feature/layer/type 별로 분할
6. **Commit each group**: 파일별 staging -> 상세 커밋 메시지 -> 반복
7. **Push**: `git push`
8. **Optional sync**: 사용자가 명시적으로 요청한 경우에만 관련 이슈/PR 동기화

## Commit Message Format

### 기본 형식

```
<type>(<scope>): <subject>

<body>
```

- **type**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`, `style`
- **scope**: 모듈/컴포넌트/영역 (선택이지만 권장)
- **subject**: 최대 50자, 소문자, 명령형, 마침표 없음
- **body**: Why (동기) -> What (변경) -> Reference (이슈 #)
- **Language**: 영어 only
- **No author line** (시스템 git config 사용)

### 상세 형식 (복잡한 변경 시)

git log가 곧 문서 역할을 하는 경우(PR 없는 main 직접 커밋 등) 아래 형식 사용:

```
<type>(<scope>): <subject>

## Background
<이 변경이 왜 필요한가? 어떤 문제/요청/관찰이 트리거했나?>

## Intent
<이 변경의 목표는? 대안은 무엇이었고 왜 이 방식을 선택했나?>

## Implementation
<영역별 핵심 변경 설명. 사용한 패턴/라이브러리>
<비자명한 결정과 그 이유>

## Result
<관찰 가능한 결과. 검증 방법>
<알려진 제한, 후속 작업>

## Files Changed
<변경된 파일과 이유 요약>
```

## Grouping Rules

- **One commit = one logical unit** (독립적으로 revert 가능)
- **순서 중요**: 기반 변경 먼저, 의존 변경 나중
- **테스트는 구현과 함께**: 같은 커밋에 포함
- **설정은 분리**: 독립적으로 의미 있으면 별도 커밋

## Examples

### 논리적 분할 커밋

```bash
# Commit 1: 리팩토링
git add src/utils/validator.py src/controllers/user.py src/controllers/order.py
git commit -m "$(cat <<'EOF'
refactor: extract validation logic to separate module

Improve reusability by separating validation from controller.

Changes:
- Create ValidationHelper class
- Move input/output validation methods
- Update imports in existing controllers
EOF
)"

# Commit 2: 새 기능 (구현 + 테스트)
git add src/features/export.py src/types/export.py tests/test_export.py
git commit -m "$(cat <<'EOF'
feat: add user data export functionality

Enable users to export their data in CSV/JSON formats.

Changes:
- Add ExportService with CSV/JSON support
- Add ExportFormat type definitions
- Add unit tests for export logic

Related to: #45
EOF
)"

git push
```

### Main 직접 커밋 (상세 형식)

```bash
git add src/auth/oauth.py src/auth/tokens.py tests/test_oauth.py
git commit -m "$(cat <<'EOF'
feat(auth): add OAuth2 PKCE flow for mobile clients

## Background
Mobile apps were using the implicit grant flow which is deprecated
and insecure for public clients. Security audit flagged this as
high-priority. RFC 7636 recommends PKCE for all public clients.

## Intent
Replace implicit grant with Authorization Code + PKCE flow.
Chose PKCE over device flow because our mobile apps can handle
redirect URIs with better UX.

## Implementation
- Add PKCEAuthProvider class (S256 method)
- Add token exchange endpoint at /auth/token/pkce
- Store code_verifier in secure session storage with 10-min TTL
- Comprehensive test suite (happy path, expired verifier, replay attack)

## Result
Mobile clients now use PKCE flow. Implicit grant remains with
deprecation warning. Verified with iOS/Android test apps.
Token exchange ~200ms average.

## Files Changed
- src/auth/oauth.py: New PKCEAuthProvider class
- src/auth/tokens.py: PKCE token exchange logic
- tests/test_oauth.py: 12 new test cases
EOF
)"

git push origin main
```

## Optional Issue/PR Sync

Push 후 커밋 메시지에 언급된 이슈/PR(`#45`, `fixes #12` 등)을 업데이트할 수 있다.
이 섹션은 사용자가 같은 턴에서 명시적으로 요청한 경우에만 적용한다.
명시 요청이 없으면 이 단계는 건너뛴다.

```bash
# 이슈 업데이트 (Korean)
gh issue edit <number> --title "새 제목" --body-file /tmp/issue-body.md

# PR 업데이트 (Korean)
gh pr edit <number> --title "새 제목" --body-file /tmp/pr-body.md
```

### Issue/PR Content Guidelines

- **Language**: 제목/본문 **Korean**
- **Title**: 변경 요약
- **Body**: 변경 사항 요약, 구현 내용 상세, 테스트 방법, 관련 커밋 목록
- **--body-file 사용** (인라인 `--body` 금지 — escaped newline 방지)

## Key Rules

- 항상 `git pull --rebase` 후 커밋 (main 직접 커밋 시 필수)
- 린터/pre-commit 훅 실행 후 커밋
- 기본 동작은 커밋과 push까지만 수행
- 이슈/PR 코멘트, 본문, 제목 수정은 명시 요청이 있을 때만 수행
- 커밋: 영어 only / 이슈-PR: Korean only
- `Co-Authored-By` 라인은 명시 요청 시만 추가
