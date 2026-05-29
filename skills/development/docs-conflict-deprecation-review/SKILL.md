---
name: docs-conflict-deprecation-review
version: 1.0.0
description: |
  구현 기준으로 프로젝트 문서를 전수 점검해 충돌 정보, 오래된 설명, deprecated 내용, 깨진 명령/경로를 찾아 즉시 수정한다.
  트리거: "문서 정합성 점검", "docs review", "deprecated 문서 업데이트", "구현 대비 문서 싱크" 요청 시.
  NOT for: 새 문서 작성(use dev-tech-spec-docs) 또는 문서 문체 정리(use dev-doc-style). 이 스킬은 기존 문서를 구현 기준으로 감사한다.
---

# Docs Conflict & Deprecation Review

구현(코드/스크립트/실행 커맨드)을 기준으로 문서를 검토하고, 충돌/폐기/노후 정보를 직접 수정한다.

## Goal

- 문서와 실제 구현의 불일치를 제거한다.
- deprecated/obsolete 안내를 최신 워크플로우로 교체한다.
- 문서 간 용어/명령/경로를 일관되게 맞춘다.

## Scope

기본 점검 대상 예시:

- 루트 문서: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`
- 제품 문서: `docs/**`, `packages/**/README.md`, `infra/**/README.md`
- 운영 문서: `checklist.md`, `agent-skills.md`, `plan.md` (존재 시)

## Non-Negotiable Rules

- 구현 사실을 우선한다. 문서가 코드와 다르면 문서를 수정한다.
- 단순 제안으로 끝내지 않고 가능한 항목은 즉시 패치한다.
- 의미 없는 대규모 리라이트를 피하고, 필요한 문맥만 최소 수정한다.

## Workflow

### 1) 문서 인벤토리 수집

```bash
rg --files -g '*.md' -g '*.mdx' -g '*.rst'
```

필요 시 우선순위 분류:

- Tier 1: 온보딩/실행 명령 (`README.md`, `CONTRIBUTING.md`)
- Tier 2: 아키텍처/운영 규칙 (`AGENTS.md`, `CLAUDE.md`, `docs/`)
- Tier 3: 도메인 상세 문서 (`packages/**/README.md`)

### 2) 구현 Truth 수집

문서와 비교할 근거를 코드에서 추출한다.

```bash
# 실행/검증 커맨드 근거
rg -n "pytest|ruff|docker compose|python -m" README.md CONTRIBUTING.md AGENTS.md docs scripts

# 구조/용어 근거: 실제 프로젝트 용어로 바꿔 실행한다.
rg -n "FastAPI|Celery|Prometheus|OpenAPI" app docs

# Deprecated 후보 탐지
rg -n "deprecated|deprecat|obsolete|legacy|TODO|TBD|WIP" docs README.md CONTRIBUTING.md AGENTS.md
```

### 3) 충돌/폐기 판정 기준

다음 중 하나면 수정 대상:

- 문서 명령이 현재 실행 불가 (파일 없음, 경로 변경, CLI 옵션 변경)
- 아키텍처/레이어 설명이 실제 디렉터리 구조와 불일치
- 용어가 공식 명칭과 불일치
- deprecated 항목이 남아 있고 대체 경로가 누락
- 두 문서가 동일 주제를 상반되게 설명

### 4) 문서 패치 원칙

- 최신 근거가 확인된 문장만 교체한다.
- 변경 이유가 불분명하면 보수적으로 유지하고 `Open Question`으로 남긴다.
- 반복되는 잘못된 용어/명령은 관련 문서 전체에서 일괄 정리한다.

### 5) 검증

문서 수정 후 최소 검증:

```bash
# 명령/경로 존재성 확인: 수정한 명령과 경로의 핵심 토큰으로 바꿔 실행한다.
rg -n "pytest|ruff|docker compose|scripts/" README.md CONTRIBUTING.md AGENTS.md docs
```

### 6) 프로젝트별 추가 검증

프로젝트에 따라 아래와 같은 추가 검증이 필요할 수 있다. 프로젝트의 가이드 문서(`AGENTS.md`, `CLAUDE.md` 등)를 먼저 읽고 해당 프로젝트의 검증 방법을 따른다.

예시 (Python/FastAPI 프로젝트):

```bash
# 린트/포맷
uv run ruff check --fix . && uv run ruff format .

# 테스트
uv run pytest tests/ -v
```

예시 (Node.js/Svelte 프로젝트):

```bash
pnpm check && pnpm lint
```

예시 (가이드 문서 동기화):

```bash
# AGENTS.md 변경 시 CLAUDE.md 동기화 (프로젝트 규칙인 경우)
cp AGENTS.md CLAUDE.md
```

## 결과 보고 포맷

1. **Updated files** — `path`: 무엇을 왜 바꿨는지 1줄
2. **Conflicts resolved** — 충돌 항목 -> 해결 방식
3. **Deprecated cleanup** — 제거/교체한 deprecated 안내
4. **Validation** — 실행한 검증 명령과 결과 (성공/실패)
5. **Open questions** — 근거 부족으로 보류한 항목

## Fast Checklist

- [ ] 문서 인벤토리 수집
- [ ] 구현 Truth 확보
- [ ] 충돌/폐기 항목 식별
- [ ] 문서 직접 패치
- [ ] 가이드 동기화 규칙 준수
- [ ] 관련 검증 실행
- [ ] 변경 요약 + 잔여 이슈 보고
