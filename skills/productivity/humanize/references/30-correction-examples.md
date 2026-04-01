# Correction Examples

유저가 승인한 교정 이력. humanize 실행 시 few-shot learning 용도로 참조.
새 교정이 승인될 때마다 해당 카테고리에 추가.

---

## 추상화 수준 교정 (Label → Observable)

- before: "협업 기반을 구축"
  after: "외부 레이어 변경 없이 agent 변경만 발생"
  문서: resume (2026-03-22)

- before: "품질 개선에 기여"
  after: "이전 버전 대비 5.6배 선호"
  문서: resume (2026-03-22)

## 구체성 교정 (Abstract → Specific)

- before: "agent 코어를 구현"
  after: "4개 agent 초기 버전을 직접 구현"
  문서: resume (2026-03-22)

- before: "외부 팀이 기여"
  after: "내부 모델러 조직이 agent 로직을 수정"
  문서: resume (2026-03-22)

## 포맷 교정 (AI Format → Domain Convention)

- before: "Langcon 2025 — Rethinking about Agents And Tools"
  after: "\"Rethinking about Agents And Tools\", Langcon 2025"
  문서: resume (2026-03-22)

## 자기선언 제거 (Self-Declaration → Show Don't Tell)

- before: "새로운 기술 영역을 빠르게 학습해 프로덕션 수준으로 구현하는 것이 강점."
  after: "광고·법률·챗봇 등 도메인을 전환하며 각 환경에서 시스템을 설계하고 프로덕션에 반영."
  문서: resume (2026-03-29)
  이유: "것이 강점"은 자기선언. 여러 도메인 전환 사실을 나열하면 읽는 사람이 판단.

- before: "LLM 인프라 인접 영역에서의 실무 경험."
  after: "Kubernetes multi-repo 배포 관리, VictoriaMetrics/Grafana observability 설계·구현, LiteLLM 도입·표준화, LLaMA-Factory 학습 환경 구성."
  문서: resume (2026-03-29)
  이유: "인접 영역에서의 실무 경험"은 자기 거리두기 + 추상 라벨. 한 것만 나열하면 충분.

## 불필요한 수식 제거

- before: "기본적인 메트릭 구축"
  after: "메트릭 구축"
  문서: resume (2026-03-22)
