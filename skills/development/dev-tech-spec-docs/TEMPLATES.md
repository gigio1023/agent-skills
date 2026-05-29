# 문서 타입별 템플릿

## README.md

```markdown
# Project Name

[프로젝트를 한 문장으로 설명]

## Quick Start

**Prerequisites**:
- [필수 도구 목록]

**Installation**:
```bash
# 의존성 설치
[설치 명령어]

# 환경 설정
[설정 명령어]
```

**Run**:
```bash
[실행 명령어]
```

**Verification**:
- [성공 확인 방법]

## Documentation

- [주요 가이드 문서 링크]
- [API 문서 링크]
- [아키텍처 문서 링크]

## Contributing

[CONTRIBUTING.md 링크]

## License

[라이선스 정보]
```

---

## CONTRIBUTING.md

```markdown
# Contributing

## 개발 환경 설정

**Requirements**:
- [필수 도구 및 버전]

**Setup**:
```bash
# 1. 저장소 클론
git clone [repository-url]

# 2. 의존성 설치
[설치 명령어]

# 3. 환경 변수 설정
cp .env.sample .env
# .env 파일 수정 필요
```

## 코드 스타일

**Linter**:
- 도구: [린터 이름]
- 실행: `[lint 명령어]`

**Formatter**:
- 도구: [포매터 이름]
- 실행: `[format 명령어]`

**Conventions**:
- [코딩 컨벤션 항목들]

## 테스트

**실행**:
```bash
# 전체 테스트
[테스트 명령어]

# 특정 파일
[특정 파일 테스트 명령어]
```

**작성 규칙**:
- [테스트 작성 가이드라인]

## PR 프로세스

1. Feature 브랜치 생성: `git checkout -b feature/your-feature`
2. 변경사항 커밋: `git commit -m "type: description"`
3. 테스트 통과 확인
4. PR 생성
5. 리뷰 반영
6. 머지

**커밋 메시지 규칙**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
```

---

## How-to Guide

```markdown
# How to [Task Name]

## Prerequisites

- [필요한 환경/도구]
- [선행 작업]

## Steps

### 1. [First Step Title]

```bash
[명령어 또는 코드]
```

**Expected Output**:
```
[예상 출력]
```

### 2. [Second Step Title]

```bash
[명령어 또는 코드]
```

### 3. [Third Step Title]

[설명 및 코드]

## Verification

성공 확인 방법:
- [ ] [확인 항목 1]
- [ ] [확인 항목 2]

## Troubleshooting

### Problem: [문제 설명]
**Symptom**:
[증상]

**Solution**:
[해결 방법]

### Problem: [다른 문제]
**Symptom**:
[증상]

**Solution**:
[해결 방법]
```

---

## Architecture Document

```markdown
# [Component Name] Architecture

## Context

**Problem**:
[해결하려는 문제]

**Requirements**:
- [요구사항 1]
- [요구사항 2]

## Decision

**Chosen Approach**: [선택한 방식]

**Rationale**:
- [이유 1]
- [이유 2]

## Alternatives Considered

### Alternative 1: [방식 이름]
- 장점: [pros]
- 단점: [cons]
- 선택하지 않은 이유: [reason]

### Alternative 2: [방식 이름]
- 장점: [pros]
- 단점: [cons]
- 선택하지 않은 이유: [reason]

## Design

**Components**:
[컴포넌트 다이어그램 또는 설명]

**Data Flow**:
[데이터 흐름 다이어그램]

**Key Interactions**:
1. [상호작용 1]
2. [상호작용 2]

## Consequences

**Pros**:
- [장점 1]
- [장점 2]

**Cons**:
- [단점 1]
- [단점 2]

**Trade-offs**:
- [트레이드오프 설명]

## Implementation

**Key Files**:
- `[파일 경로]`: [역할]
- `[파일 경로]`: [역할]

**Critical Sections**:
```[language]
[핵심 코드 스니펫]
```

## Migration Plan

(기존 시스템 변경 시)

**Steps**:
1. [단계 1]
2. [단계 2]

**Rollback Strategy**:
[롤백 방법]
```

---

## API Reference

```markdown
# API Reference

## [Endpoint/Function Name]

**Description**:
[간단한 설명]

**Request**:

```http
POST /api/v1/resource
Content-Type: application/json
```

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `param1` | `string` | Yes | - | [설명] |
| `param2` | `number` | No | `10` | [설명] |

**Request Body**:

```json
{
  "param1": "value",
  "param2": 123
}
```

**Response**:

**Success (200)**:
```json
{
  "result": "success",
  "data": {...}
}
```

**Errors**:

| Code | Description |
|------|-------------|
| `400` | Invalid parameters |
| `404` | Resource not found |
| `500` | Internal server error |

**Example**:

```bash
curl -X POST "http://localhost:8080/api/v1/resource" \
  -H "Content-Type: application/json" \
  -d '{"param1": "value", "param2": 123}'
```

**Response**:
```json
{
  "result": "success",
  "data": {...}
}
```
```

---

## Troubleshooting Guide

```markdown
# Troubleshooting Guide

## Category 1: [문제 카테고리]

### [Problem Name]

**Symptoms**:
- [증상 1]
- [증상 2]

**Possible Causes**:
1. [원인 1]
2. [원인 2]

**Solutions**:

#### Solution 1: [해결 방법 제목]
```bash
[해결 명령어]
```

**Verification**:
[해결 확인 방법]

#### Solution 2: [해결 방법 제목]
[해결 절차]

---

## Category 2: [다른 카테고리]

### [Problem Name]

[위와 동일한 구조]
```

---

## ADR (Architecture Decision Record)

```markdown
# ADR-[번호]: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Deciders**: [의사결정자 목록]

## Context

[의사결정이 필요한 배경 및 상황]

## Decision

[내린 결정]

## Rationale

[결정의 근거]
- [이유 1]
- [이유 2]

## Alternatives

### Alternative 1
- 설명: [...]
- 장점: [...]
- 단점: [...]

### Alternative 2
- 설명: [...]
- 장점: [...]
- 단점: [...]

## Consequences

**Positive**:
- [긍정적 영향]

**Negative**:
- [부정적 영향]

**Risks**:
- [위험 요소]

## References

- [관련 문서/이슈 링크]
```

---

## Changelog

```markdown
# Changelog

## [Unreleased]

### Added
- [새 기능]

### Changed
- [변경사항]

### Deprecated
- [폐기 예정]

### Removed
- [제거됨]

### Fixed
- [버그 수정]

### Security
- [보안 패치]

## [1.0.0] - YYYY-MM-DD

### Added
- [새 기능]

### Changed
- [변경사항]
```
