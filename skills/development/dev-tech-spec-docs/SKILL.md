---
name: dev-tech-spec-docs
version: 1.0.0
description: |
  개발 스페이스 전용 개발/기술/스펙 문서 작성 스킬.
  트리거: "README 작성", "CONTRIBUTING 작성", "API 문서 작성", "아키텍처 문서", "스펙 작성", "기술 가이드 작성" 요청 시.
  코드베이스 기반 기술 문서를 간결성, 명료성, 구조화 원칙으로 작성/개선.
  NOT for: 문서 문체/구조 리라이팅(use dev-doc-style), AI 티 제거(use im-not-ai), PR 본문(use write-pr), Issue 작성(use write-issue), Python docstring(use python-docstring-enhancer).
  일반 홍보/마케팅/비개발 문서는 대상에서 제외.
---

# 개발 스페이스용 개발/기술/스펙 문서 작성

## 적용 범위 (필수)

- 이 스킬은 개발 스페이스의 엔지니어링 문서 전용
  - 대상: README, CONTRIBUTING, How-to, API Reference, Architecture, Spec
  - 대상 문서의 목적: 구현/운영/설계 의사결정 전달
- 비대상: 일반 안내문, 홍보/마케팅 문서, 비개발 조직 공지

## 빠른 사용법

1. 문서 타입 결정
   - README / How-to / Reference / Architecture
2. 템플릿 적용
   - [TEMPLATES.md](TEMPLATES.md)
3. Anti-pattern 점검
   - [PATTERNS.md](PATTERNS.md)
4. 최종 품질 점검
   - [CHECKLIST.md](CHECKLIST.md)

## 기본 규칙 (기본값)

- 이모지 사용 최소화
- 한국어 문서
  - 개조식 작성
  - 표/리스트 우선
- 작업 시간/소요 시간
  - 사용자가 요청한 경우만 포함
- 장애 대응/담당자 호출
  - Runbook, Incident Response 등 목적 문서에서만 포함

## 핵심 원칙

### Progressive Disclosure
- 정보를 단계적으로 노출
- Quick Start → 상세 가이드 → 참조 문서 → 설계 문서 순서
- 사용자가 필요한 정보만 빠르게 접근

### Single Responsibility
- 하나의 문서는 하나의 목적
- 목적이 다르면 문서를 분리
- 명확한 문서명으로 내용 예측 가능

### Clarity over Completeness
- 완벽한 설명보다 명확한 이해 우선
- 핵심 정보만 포함, 부차적 내용 제거
- 모호한 표현 금지, 구체적 예시 필수

### DRY (Don't Repeat Yourself)
- 중복 제거, 참조 링크 활용
- 단일 정보 출처 (Single Source of Truth)
- 변경 시 한 곳만 수정

---

## 정보 아키텍처

### Tier 1: 진입점
**목적**: 프로젝트 이해 및 빠른 시작

- README.md: 프로젝트 개요, Quick Start, 주요 링크
- Getting Started: 환경 설정, 첫 실행

**특징**:
- 최소한의 정보만 포함
- 상세 내용은 다른 문서로 링크
- 신규 사용자 기준 작성

### Tier 2: 실무 가이드
**목적**: 특정 작업 수행 방법

- API 사용법
- CLI 도구 가이드
- 튜토리얼

**특징**:
- 단계별 명령어/코드
- 실행 가능한 예시
- Troubleshooting 섹션

### Tier 3: 참조 문서
**목적**: 옵션, 파라미터, 스펙 조회

- API 명세
- 설정 파일 옵션
- 용어집

**특징**:
- 표 형식 활용
- 완전성 (모든 옵션 포함)
- 알파벳/카테고리 정렬

### Tier 4: 설명 문서
**목적**: 내부 동작, 설계 의도 이해

- 아키텍처 문서
- 설계 결정 (ADR)
- 배경 및 컨텍스트

**특징**:
- 다이어그램 활용
- 의사결정 근거 명시
- 트레이드오프 설명

---

## 작성 스타일 가이드

### 한국어 문서
**개조식 작성**:
- 서술형 문장 지양
- 명사형 종결 또는 동사원형 사용
- 불필요한 조사 제거

**예시**:
```markdown
# Bad
이 기능을 사용하려면 먼저 환경 변수를 설정해야 합니다.
설정이 완료되면 서버를 실행할 수 있습니다.

# Good
환경 변수 설정:
- `.env.sample` 복사 → `.env`
- 필수 값 입력: `API_KEY`, `DATABASE_URL`

서버 실행:
- `uv run uvicorn app.main:app --reload`
```

### 영어 문서
**명령형/현재형 사용**:
- Use imperative mood for instructions
- Present tense for descriptions
- Active voice preferred

### 공통 규칙
**간결성**:
- 한 문장 = 한 개념
- 불필요한 수식어 제거
- 중복 표현 삭제

**구체성**:
- 추상적 표현 대신 구체적 예시
- "적절히", "가능하면" 같은 모호한 표현 금지
- 명령어/코드는 복사 가능하게

**일관성**:
- 용어 통일 (동의어 사용 금지)
- 형식 통일 (헤딩, 코드블록, 리스트)
- 구조 통일 (같은 타입 문서는 같은 구조)

### 이모지 사용
**최소화 원칙**:
- 과도한 이모지는 가독성 저하
- 필요한 경우만 사용 (예: 섹션 구분, 중요도 표시)
- 일관된 의미로 사용 (같은 이모지 = 같은 의미)

**허용 사례**:
- 문서 타입 표시: 책, 공구, 차트 등
- 상태 표시: 체크, 경고, 오류
- 강조: 중요, 주의사항

**금지 사례**:
- 장식용 이모지
- 문장마다 이모지 추가
- 의미 없는 이모지 남용

---

## 문서 타입별 가이드라인

### README.md
**목적**: 프로젝트 첫인상, 핵심 정보 전달

**구조**:
```markdown
# Project Name
[1문장 요약]

## Quick Start
[3단계 이내 실행 방법]

## Documentation
[주요 문서 링크]

## Contributing
[기여 방법 링크]

## License
```

**체크리스트**:
- [ ] 프로젝트가 무엇인지 1문장으로 설명
- [ ] 설치/실행이 3단계 이내
- [ ] 상세 내용은 별도 문서로 링크
- [ ] 50줄 이내 권장

### CONTRIBUTING.md
**목적**: 개발자 온보딩, 개발 규칙 안내

**구조**:
```markdown
# Contributing

## 개발 환경 설정
[의존성 설치, 환경 변수]

## 코드 스타일
[린터, 포매터, 규칙]

## 테스트
[실행 방법, 작성 규칙]

## PR 프로세스
[브랜치 전략, 리뷰 규칙]
```

**체크리스트**:
- [ ] 환경 설정이 재현 가능
- [ ] 명령어가 복사 가능
- [ ] 규칙이 구체적 (모호한 표현 없음)
- [ ] 예시 코드 포함

### How-to Guide
**목적**: 특정 작업 수행 방법 안내

**구조**:
```markdown
# How to [Task]

## Prerequisites
[필요 조건]

## Steps
### 1. [First Step]
[명령어/코드]

### 2. [Second Step]
[명령어/코드]

## Verification
[성공 확인 방법]

## Troubleshooting
[자주 발생하는 문제와 해결]
```

**체크리스트**:
- [ ] 각 단계가 실행 가능
- [ ] 예상 출력 포함
- [ ] 에러 대응 방법 명시
- [ ] 순서대로 따라하면 성공

### Architecture Document
**목적**: 설계 의도 및 내부 동작 설명

**구조**:
```markdown
# [Component] Architecture

## Context
[배경 및 문제 정의]

## Decision
[선택한 설계]

## Alternatives
[고려했던 다른 방안]

## Consequences
[장점, 단점, 트레이드오프]

## Implementation
[핵심 구현 포인트]
```

**체크리스트**:
- [ ] 의사결정 근거 명확
- [ ] 다이어그램 포함
- [ ] 트레이드오프 명시
- [ ] 변경 이력 관리

### API Reference
**목적**: 엔드포인트/함수 스펙 조회

**구조**:
```markdown
# API Reference

## Endpoint/Function Name

**Request/Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| ... | ... | ... | ... |

**Response**:
[스키마 또는 예시]

**Example**:
[실행 가능한 코드/curl]

**Errors**:
[가능한 에러와 의미]
```

**체크리스트**:
- [ ] 모든 파라미터 문서화
- [ ] 타입 정보 명확
- [ ] 예시 코드 실행 가능
- [ ] 에러 케이스 포함

---

## Anti-patterns

### 장황한 배경 설명
**Bad**:
> 현재 시스템은 2019년에 시작되었으며, 당시 A 방식을 사용했으나 2021년 B로 변경하였고...

**Good**:
> **현재**: B 방식 사용
> 
> 이전 방식 및 변경 이유: [ADR-001](docs/adr/001-migration-to-b.md)

### 모호한 표현
**Bad**:
> 적절한 값으로 설정하세요.
> 필요하면 옵션을 추가할 수 있습니다.

**Good**:
> 권장값: `timeout=30`
> 선택 옵션: `--verbose` (상세 로그 출력)

### 중복 정보
**Bad**:
```markdown
# README.md
테스트 실행: `uv run pytest`

# CONTRIBUTING.md  
테스트 실행: `uv run pytest`
```

**Good**:
```markdown
# README.md
개발 가이드: [CONTRIBUTING.md](CONTRIBUTING.md)

# CONTRIBUTING.md
테스트 실행: `uv run pytest`
```

### 전제 조건 누락
**Bad**:
```bash
$ curl http://localhost:8080/api
```

**Good**:
```bash
# Prerequisites: 서버가 실행 중이어야 함
$ uv run uvicorn app.main:app --reload

# 다른 터미널에서
$ curl http://localhost:8080/api
```

### 작업 시간 명시
**Bad**:
> Quick Start (5분 소요)
> 전체 설정 완료까지 약 30분

**Good**:
> Quick Start
> 전체 설정

**예외**: 사용자가 특별히 요청하거나 작업 계획 문서인 경우만 포함

### 장애 대응 절차
**원칙**:
- 일반 문서: Troubleshooting만 포함
- 별도 Runbook: 장애 대응 절차 상세 기술

**예외**:
- Runbook, Incident Response 등 목적 문서

---

## Best Practices

### 결론 우선
**구조**:
1. 결론/요약
2. 상세 설명
3. 배경/컨텍스트

**예시**:
```markdown
# Bad
과거에는 A 방식을 사용했으나, 여러 문제가 있었습니다.
따라서 B 방식으로 변경하기로 결정했습니다.

# Good
**현재 방식**: B

**변경 이유**:
- A 방식의 문제: X, Y
- B 방식의 장점: P, Q
```

### 구체적 예시
**추상 개념을 코드/명령어로**:
```markdown
# Bad
환경 변수를 올바르게 설정하세요.

# Good
환경 변수 설정:
```bash
export DATABASE_URL="postgresql://localhost/mydb"
export API_KEY="your-api-key-here"
```
```

### 시각화
**복잡한 관계는 다이어그램**:
- 아키텍처: 컴포넌트 다이어그램
- 플로우: 시퀀스 다이어그램
- 계층: 레이어 다이어그램

**도구**: Mermaid, PlantUML, ASCII art

### 검증 가능성
**예시 코드는 실행 가능해야 함**:
- 복사-붙여넣기로 동작
- 예상 출력 명시
- 에러 케이스 포함

---

## 품질 체크리스트

- [CHECKLIST.md](CHECKLIST.md) 참조

---

## 사용 가이드

### 새 문서 작성
1. 문서 타입 결정 (README, Guide, Reference, Architecture)
2. [TEMPLATES.md](TEMPLATES.md)에서 해당 템플릿 선택
3. 핵심 원칙 적용하여 작성
4. [CHECKLIST.md](CHECKLIST.md)로 검증

### 기존 문서 개선
1. [PATTERNS.md](PATTERNS.md)의 Anti-patterns 탐지
2. 중복 정보 제거, 참조 링크 활용
3. 장황한 설명 간결화 (개조식)
4. [CHECKLIST.md](CHECKLIST.md)로 검증

### 문서 구조 설계
1. 정보 아키텍처 (Tier 1~4) 설계
2. 각 Tier에 맞는 문서 배치
3. README.md에서 주요 문서 링크
4. 진입점 → 상세 문서 흐름 확인
