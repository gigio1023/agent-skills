# PR 머지 전 셀프 체크리스트

문서 PR 을 머지하기 전 본인이 셀프 체크. 또는 리뷰어가 본 체크리스트로 코멘트.

---

## 빠른 점검 (10 항목)

작성한 / 수정한 모든 `*.md` 파일에 대해:

- [ ] **em-dash / middle-dot 0 회**: 본문에 `—`, `·`, `•` 가 한 번도 없다 (`grep -nE '[—·•]'` 0 매치). 치환은 `:` / `,` / 마침표.
- [ ] **출처 라벨 없음**: 본문에 `(Wiki §x.y)`, `(boilerplate 컨벤션)` 같은 라벨이 없다. 인라인 링크만.
- [ ] **bare path 없음**: 본문에 ``` `docs/spec/foo.md` ``` 나 raw URL 만 떨어뜨리지 않았다. 모든 cross-doc 참조가 `[설명 (어디)](경로)` descriptive link 거나 본문에서 빠졌다.
- [ ] **bullet shape 통일**: 모든 bullet 이 Form A (`**라벨**: 한 문장.`), Form B (완결된 한 문장), Form C (`**라벨**:` + nested 1 단) 중 하나다. **sub-fact 가 2 개 이상이면 Form C 강제** (inline comma 합치기 없음).
- [ ] **nested ≤ 1 단계**: 2 단계 이상 nested bullet 없다.
- [ ] **메타 섹션 없음**: 페이지 끝에 `## Notes`, `## More docs`, `## References`, `## 관련 문서`, `## 더 보기`, `## 참고` 가 없다.
- [ ] **도입문 ≤ 1 문장**: 섹션 시작이 단락이 아니라 한 문장 또는 곧장 코드 / 표.
- [ ] **정책 / 우선순위 / 미정 격리**: 본문에 박지 않고 `> [!NOTE]` 또는 별도 페이지.
- [ ] **분량 예산**: README ≤ 100 줄, docs/ 각 페이지 ≤ 250 줄. 초과 시 토픽 분할 검토 (코드 비중 높으면 예외 OK).
- [ ] **중복 없음**: 같은 표 / 리스트 / 정의가 두 페이지 이상에 동일 형태로 등장하지 않음.
- [ ] **코드 결과 인라인**: `#>` / `"""` / `<details>`. "다음을 실행하면 다음과 같이 출력됩니다" 줄글 없음.

---

## 분량 측정 (참고)

```bash
# 페이지별 줄 수 확인
find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" \
  | xargs wc -l | sort -rn | head -20

# README 분량
wc -l README.md
```

---

## 깊은 점검 (선택)

위 10 항목을 모두 통과했다면 다음을 추가로 점검:

### 11. Voice 일관성
- [ ] 헤딩 어투가 동사형 또는 명사형 한 가지로 통일되어 있다 (혼용 없음).
- [ ] 단서 약화 표현 (`-할 수도 있고`, `필요하다면`, `상황에 따라`) 의 절반 이상이 정말 조건부 정보를 전달한다 (장식이 아니다).
- [ ] 명령형 현재형. "할 수 있습니다" 가 대부분 "합니다" 로 표현되어 있다.

### 12. 한국어 / 영어 mix
- [ ] 기술 용어는 영어 그대로 (FastAPI, Bearer, Skill ID, conformance, ArtifactMetadata).
- [ ] 조사 / 연결어만 한국어. 무리한 한국어 직역 없음.
- [ ] 길어진 문장은 한국어로 풀어 써서 가독성 유지.

### 13. Code-first
- [ ] 토픽 페이지의 도입이 한 문장 + 코드 / 표. 도입 단락 (왜 / 무엇 / 어디 / 어떻게) 4 단 패턴 없음.
- [ ] 코드 블록 후 prose 가 1–3 문장 이내.
- [ ] 긴 출력은 `<details>` 로 접혀 있다.

### 14. Cross-page
- [ ] 첫 언급에만 reference 링크. 페이지 후반 같은 클래스명 / 함수명에 다시 링크 안 단다.
- [ ] 자기 영역 외 재설명 없음 (types 페이지에서 fields 다시 설명, README 에서 conformance 5 항목 다시 적기 등).

---

## 위반 발견 시 액션

체크 항목이 빨간불이면:

| 항목 | 액션 |
|---|---|
| em-dash / middle-dot / bullet char 1 회 이상 | `:` / `,` / 마침표로 치환. 절 부연이면 두 문장으로 분리 |
| 출처 라벨 본문 박힘 | 인라인 링크 한 번 또는 별도 `docs/spec-mapping.md` |
| bare path / raw URL 본문 등장 | descriptive link `[설명 (어디)](경로)` 으로 교체 또는 본문에서 제거 |
| bullet 안 sub-fact 2 개 이상 inline | Form C (`**라벨**:` + nested 1 단) 로 풀어쓰기 |
| nested 2+ 단계 | 섹션 쪼개기 또는 See 링크로 떠넘기기 |
| 메타 섹션 존재 | 일괄 삭제. 필요한 링크는 본문 인라인 |
| 도입 단락 ≥ 2 문장 | 한 문장 + 곧장 코드 / 표 |
| 정책 / 우선순위 본문 | `> [!NOTE]` 또는 별도 페이지 |
| 분량 초과 | 토픽 분할 (코드 비중 높으면 예외) |
| 중복 정보 | 한 곳에만 유지, 다른 곳은 한 줄 + 링크 |
| 줄글 출력 설명 | `#>` / `"""` / `<details>` 로 코드 안에 |

---

## 자주 놓치는 패턴

본 레포에서 반복적으로 등장한 위반:

- **`(옵션)` 단서 + em-dash + 출처 두 개** = 한 줄 4 메시지 패턴 (가장 흔함)
- **bullet 안 em-dash 부연** — bullet 자체가 Form A / B 가 아닌 변종
- **헤딩에 박힌 우선순위** (`(1 순위)`, `(후순위)`) — 라벨이 아니라 본문 또는 정책 페이지로
- **README 끝 3 메타 섹션** (Notes / More docs / References) — 셋 다 폐기
- **conformance 5 항목 세 곳 등장** (README / spec.md / conformance.md) — `docs/conformance.md` 단일 source

---

## 본 체크리스트 자동화 가능 항목

다음은 grep / lint 로 자동 체크 가능. (현재 본 레포는 자동 체크 미설정.)

- em-dash / middle-dot / bullet char (코드 블록 외 본문 0 회): `grep -nE '[—·•]' **/*.md`
- 출처 라벨 패턴: `grep -nE '\(Wiki §|\(boilerplate 컨벤션\)' **/*.md`
- bare path 인라인 (heuristic, 수동 확인): `grep -nE '\`(docs/|\.\./)[^\`]+\.md\`' **/*.md`
- 메타 섹션: `grep -nE '^## (Notes|More docs|References|관련 문서|더 보기|참고)$' **/*.md`
- 분량: `wc -l **/*.md | sort -rn | head -10`

장기적으로 langchain 의 Vale 룰 같은 lint 셋업을 검토할 만함.
