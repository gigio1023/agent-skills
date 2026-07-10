# 문서 작성 패턴

## Contents

- Anti-patterns
- Best Practices
- 정보 계층 예시
- 문서 유형별 예시

## Anti-patterns (피해야 할 것)

### 1. 장황한 역사 서술

**Bad**:
> 이 프로젝트는 2019년 3월에 시작되었습니다. 당시에는 Python 2.7을 사용했으나, 2020년 1월 Python 2.7 지원 종료로 인해 Python 3.8로 마이그레이션했습니다. 2021년에는 FastAPI 프레임워크를 도입하면서 Flask에서 전환했고, 이 과정에서 많은 리팩토링이 있었습니다. 현재는 FastAPI 0.100을 사용하고 있습니다.

**Good**:
> **현재 기술 스택**:
> - Python 3.11
> - FastAPI 0.100
> 
> 변경 이력: 프로젝트의 `CHANGELOG.md` 참조

---

### 2. 모호한 지시어

**Bad**:
- "적절한 값을 설정하세요"
- "필요에 따라 조정하세요"
- "상황에 맞게 사용하세요"
- "적당히 대기하세요"

**Good**:
- 권장값: `timeout=30` (범위: 10-60초)
- 선택사항: `--verbose` (디버그 시 사용)
- 필수값: `API_KEY` (환경변수 설정 필요)
- 대기시간: 최소 5초 (서버 재시작 시)

---

### 3. 전제 조건 생략

**Bad**:
```bash
$ curl http://localhost:8080/api/health
```

**Good**:
```bash
# Prerequisites: 서버 실행 중이어야 함
$ uv run uvicorn app.main:app --reload

# 다른 터미널에서 실행
$ curl http://localhost:8080/api/health
```

---

### 4. 실행 불가능한 예시

**Bad**:
```python
# 사용자 생성
user = create_user(...)
```

**Good**:
```python
# 사용자 생성
user = create_user(
    name="John Doe",
    email="john@example.com",
    role="admin"
)
```

---

### 5. 중복 정보

**Bad**:
```markdown
# README.md
## 환경 설정
`.env` 파일에 다음 변수를 설정:
- DATABASE_URL
- API_KEY

# CONTRIBUTING.md
## 환경 설정
`.env` 파일에 다음 변수를 설정:
- DATABASE_URL
- API_KEY
```

**Good**:
```markdown
# README.md
## 환경 설정
[CONTRIBUTING.md](CONTRIBUTING.md#환경-설정) 참조

# CONTRIBUTING.md
## 환경 설정
`.env` 파일에 다음 변수를 설정:
- DATABASE_URL
- API_KEY
```

---

### 6. 예상 결과 누락

**Bad**:
```bash
$ pytest tests/
```

**Good**:
```bash
$ pytest tests/

# Expected output:
# ===== 85 passed in 20.00s =====
```

---

### 7. 오류 처리 방법 없음

**Bad**:
```bash
$ docker-compose up
```

**Good**:
```bash
$ docker-compose up

# 오류 발생 시:
# Error: port 5432 already in use
# 
# 해결 방법:
$ docker-compose down
$ docker-compose up
```

---

### 8. 시간 추정 남발

**Bad**:
> Quick Start (5분)
> 환경 설정 (30분)
> 전체 튜토리얼 (2시간)

**Good**:
> Quick Start
> 환경 설정
> 전체 튜토리얼

**허용**:
사용자가 명시적으로 요청하거나, 작업 계획 문서(task.md)인 경우만 포함

---

### 9. 장애 대응 절차 혼입

**Bad** (일반 문서에 포함):
- 장애 대응 절차, 연락 체계, 롤백 기준 포함

**Good**:
- 일반 문서: Troubleshooting만 포함
- 별도 Runbook: 장애 대응 절차 작성

---

### 10. 이모지/아이콘 남발

**Bad**:
- 문장/항목마다 이모지/아이콘 추가
- 의미 없는 장식 목적 사용

**Good**:
- 필요할 때만 제한적으로 사용
- 같은 기호는 같은 의미로 사용
- 한국어 문서도 독자 작업에 맞춰 prose, 목록, 표를 선택

---

## Best Practices (권장 사항)

### 1. 결론 우선 (Conclusion First)

**Structure**:
```
1. 결론/핵심
2. 상세 설명
3. 배경/컨텍스트
```

**Example**:
```markdown
# Bad
과거에는 A 방식을 사용했으나 성능 문제가 있었고,
여러 대안을 검토한 결과 B 방식이 적합하다고 판단했습니다.

# Good
**현재**: B 방식 사용

**이유**:
- A 방식의 문제: 성능 저하
- B 방식의 장점: 30% 성능 향상

**배경**: [ADR-001](docs/adr/001-migration.md)
```

---

### 2. 계층적 정보 제공

**Tier 1 (README.md)**:
````markdown
## Quick Start
```bash
uv sync
uv run uvicorn app.main:app
```

상세: [Getting Started](docs/getting-started.md)
````

**Tier 2 (docs/getting-started.md)**:
````markdown
## Quick Start

1. 의존성 설치
```bash
uv sync --group dev
```

2. 환경 변수 설정
```bash
cp .env.sample .env
# API_KEY, DATABASE_URL 설정 필요
```

3. 서버 실행
```bash
uv run uvicorn app.main:app --reload
```
````

---

### 3. 구체적 예시 우선

**Bad**:
> API 엔드포인트에 적절한 헤더와 바디를 포함하여 요청하세요.

**Good**:
```bash
curl -X POST "http://localhost:8080/api/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{"name": "John", "email": "john@example.com"}'
```

---

### 4. 시각화 활용

**복잡한 구조는 다이어그램으로**:

````markdown
# Bad (텍스트로만 설명)
오케스트레이터가 AD Retrieval, Answer Fusion, Quality Inspection을
순차적으로 호출합니다. 각 에이전트는 LLM Client를 통해 OpenAI와
통신하며, 결과를 Langfuse에 기록합니다.

# Good (다이어그램 + 간단한 설명)
```
Orchestrator
  ├── AD Retrieval → LLM Client → OpenAI
  ├── Answer Fusion → LLM Client → OpenAI
  └── Quality Inspection → LLM Client → OpenAI
                                    ↓
                                 Langfuse
```

**설명**:
- Orchestrator: 에이전트 순차 실행
- LLM Client: OpenAI API 호출 및 Langfuse 기록
````

---

### 5. 검증 가능한 예시

**실행 가능하다고 제시하는 코드 예시는 검증 가능해야 함**:

````markdown
# Bad
```python
result = process_data(data)
```

# Good
```python
# Prerequisites: data.json 파일 존재
from app.processor import process_data

with open("data.json") as f:
    data = json.load(f)

result = process_data(data)
print(result)  # Expected: {"status": "success", ...}
```
````

---

### 6. 명확한 에러 처리

```markdown
**Common Errors**:

1. `ModuleNotFoundError: No module named 'app'`
   - 원인: PYTHONPATH 미설정
   - 해결: `export PYTHONPATH=$(pwd)`

2. `Connection refused`
   - 원인: 서버 미실행
   - 해결: `uv run uvicorn app.main:app --reload`
```

---

### 7. 단계별 검증

````markdown
## Steps

### 1. 환경 변수 설정
```bash
export DATABASE_URL="postgresql://localhost/db"
```

**Verification**:
```bash
echo $DATABASE_URL
# Expected: postgresql://localhost/db
```

### 2. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

**Verification**:
```bash
alembic current
# Expected: [current version hash]
```
````

---

### 8. 일관된 용어 사용

**Bad** (동의어 혼용):
- "광고 검색", "AD 탐색", "광고 조회"
- "품질 검사", "QI", "Quality Check"

**Good** (프로젝트 용어 통일):
- AD Retrieval (일관되게 사용)
- Quality Inspection (일관되게 사용)

**용어집 제공**:
```markdown
## Glossary

- **AD Retrieval**: 광고 후보 검색 에이전트
- **Answer Fusion**: 광고 삽입 에이전트
- **Quality Inspection**: 품질 검증 에이전트
```

---

### 9. 절차를 스캔 가능하게 만들기 (한국어)

**Bad**:
> 이 기능을 사용하려면 먼저 환경 변수를 설정해야 합니다.
> 설정이 완료되면 서버를 실행할 수 있습니다.
> 서버가 정상적으로 실행되면 API를 호출할 수 있습니다.

**Good**:
> 환경 변수 설정:
> - `.env.sample` → `.env` 복사
> - 필수값 입력: `API_KEY`, `DATABASE_URL`
> 
> 서버 실행:
> - `uv run uvicorn app.main:app --reload`
> 
> API 호출:
> - `curl http://localhost:8080/health`

---

### 10. 링크 활용

**Bad** (같은 정보 반복):
```markdown
# README.md
## 환경 설정
1. Python 3.11 설치
2. uv 설치
3. 의존성 설치

# CONTRIBUTING.md
## 환경 설정
1. Python 3.11 설치
2. uv 설치
3. 의존성 설치
```

**Good** (참조 링크):
```markdown
# README.md
## Quick Start
환경 설정: [CONTRIBUTING.md](CONTRIBUTING.md#환경-설정)

# CONTRIBUTING.md
## 환경 설정
1. Python 3.11 설치
2. uv 설치
3. 의존성 설치
```
