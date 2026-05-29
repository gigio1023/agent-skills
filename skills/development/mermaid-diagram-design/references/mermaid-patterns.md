# Mermaid Reusable Patterns (v2)

## 1) Type Selection Matrix

- Workflow/funnel/branching: `flowchart`
- Interaction timeline: `sequenceDiagram`
- Layered architecture/context boundary: `flowchart + subgraph`, `architecture`, `block`
- State transition: `stateDiagram`

## 2) Frontmatter Presets

### 2-1) Baseline

```mermaid
---
config:
  look: classic
  layout: dagre
  flowchart:
    useMaxWidth: true
accTitle: Example diagram
accDescr: Example process flow from A to B
---
flowchart TD
  A --> B
```

### 2-2) Dense Graph (ELK)

```mermaid
---
config:
  layout: elk
  flowchart:
    useMaxWidth: true
---
flowchart LR
  A --> B --> C
```

### 2-3) Confluence Dense (Dagre + Spacing)

```mermaid
---
config:
  look: classic
  layout: dagre
  flowchart:
    useMaxWidth: true
    nodeSpacing: 45
    rankSpacing: 60
---
flowchart TD
  A[Input] --> B[Process]
  B --> C[Output]
```

### 2-4) Edge Visibility Baseline (Dark Edges)

```mermaid
---
config:
  look: classic
  layout: elk
  flowchart:
    useMaxWidth: true
---
flowchart TD
  linkStyle default stroke:#000000,stroke-width:1.8px;
  A[Start] --> B[Process]
  B -.drop.-> C[Terminal: business_drop]
  B -.error.-> D[Terminal: system_error]
```

### 2-5) Sequence with Numbers

```mermaid
---
config:
  sequence:
    showSequenceNumbers: true
---
sequenceDiagram
  participant A as API
  participant S as Service
  A->>S: request
  S-->>A: response
```

## 3) Professional Color Palette (기본)

Material Design 기반의 절제된 팔레트. 모든 다이어그램에서 이 classDef를 기본으로 사용한다.

### 3-1) Semantic (상태 표현)

```mermaid
flowchart LR
  OK["Success"]
  WARN["Warning"]
  ERR["Error"]
  NEU["Neutral"]

  classDef success fill:#e6f4ea,stroke:#34a853,color:#1e4620;
  classDef warning fill:#fef7e0,stroke:#f9ab00,color:#5f4b00;
  classDef error fill:#fce8e6,stroke:#ea4335,color:#7c1d13;
  classDef neutral fill:#f1f3f4,stroke:#5f6368,color:#3c4043;

  class OK success;
  class WARN warning;
  class ERR error;
  class NEU neutral;
```

### 3-2) Layer (아키텍처 레이어)

```mermaid
flowchart LR
  API["API"]
  DOM["Domain"]
  INF["Infrastructure"]
  TR["Transport"]

  classDef api fill:#e8f0fe,stroke:#1a73e8,color:#174ea6;
  classDef domain fill:#e6f4ea,stroke:#34a853,color:#1e4620;
  classDef infra fill:#fce8e6,stroke:#ea4335,color:#7c1d13;
  classDef transport fill:#f3e8fd,stroke:#9334e6,color:#4a1d8e;

  class API api;
  class DOM domain;
  class INF infra;
  class TR transport;
```

### 3-3) Pipeline (순서/단계 표현)

```mermaid
flowchart LR
  S1["Step 1"]
  S2["Step 2"]
  S3["Step 3"]
  S4["Step 4"]
  S1 --> S2 --> S3 --> S4

  classDef step1 fill:#e8f0fe,stroke:#1a73e8,color:#174ea6;
  classDef step2 fill:#f3e8fd,stroke:#9334e6,color:#4a1d8e;
  classDef step3 fill:#fef7e0,stroke:#f9ab00,color:#5f4b00;
  classDef step4 fill:#e6f4ea,stroke:#34a853,color:#1e4620;

  class S1 step1;
  class S2 step2;
  class S3 step3;
  class S4 step4;

  linkStyle default stroke:#455a64,stroke-width:1.8px;
```

### 3-4) 전체 classDef 복사용

```
  classDef success fill:#e6f4ea,stroke:#34a853,color:#1e4620;
  classDef warning fill:#fef7e0,stroke:#f9ab00,color:#5f4b00;
  classDef error fill:#fce8e6,stroke:#ea4335,color:#7c1d13;
  classDef neutral fill:#f1f3f4,stroke:#5f6368,color:#3c4043;
  classDef primary fill:#e8f0fe,stroke:#1a73e8,color:#174ea6;
  classDef purple fill:#f3e8fd,stroke:#9334e6,color:#4a1d8e;
  linkStyle default stroke:#455a64,stroke-width:1.8px;
```

### 색상 사용 규칙

- 색상만으로 의미를 전달하지 않는다. 라벨/선스타일(실선, 점선)도 같이 사용
- edge는 기본 회색이 아닌 `stroke:#455a64`(blue-grey 700)을 사용
- 노드 fill은 옅은 톤, stroke는 진한 톤, color(텍스트)는 가장 진한 톤
- 한 다이어그램에 4색 이하 권장. 색이 많으면 라벨로 구분

## 4) Core Patterns

### 4-1) Linear Pipeline

```mermaid
flowchart TD
  IN[Input]
  S1[Validate]
  S2[Transform]
  S3[Publish]
  OUT[Output]

  IN --> S1 --> S2 --> S3 --> OUT
```

### 4-2) Layered Architecture

```mermaid
graph TD
  subgraph API[API Layer]
    R[Routers]
  end

  subgraph DOMAIN[Domain Layer]
    A[Agents]
    P[Ports]
  end

  subgraph INFRA[Infrastructure Layer]
    AD[Adapters]
    OBS[Observability]
  end

  API --> DOMAIN
  DOMAIN --> INFRA
```

### 4-3) Before/After Comparison

```mermaid
graph LR
  subgraph BEFORE[Before]
    D1[Domain] --> X1[SDK]
  end

  subgraph AFTER[After]
    D2[Domain] --> P[Protocol]
    A[Adapter] -.->|implements| P
    A --> X2[SDK]
  end
```

### 4-4) Funnel + Terminal

```mermaid
flowchart TD
  ENTER[Enter]
  PROC[Process]
  DROP[business_drop]
  ERR[system_error]
  OK[success]

  ENTER --> PROC --> OK
  ENTER --> DROP
  ENTER --> ERR
```

### 4-5) Producer -> Transport -> Consumer

```mermaid
flowchart LR
  subgraph PROD[Producer]
    M[Metrics Emitter]
  end

  subgraph TRANS[Transport]
    VM[Victoria Metrics]
  end

  subgraph CONS[Consumer]
    G[Grafana]
    D[Demo/BFF]
  end

  M --> VM
  VM --> G
  VM --> D
```

### 4-6) Sequence Interaction

```mermaid
sequenceDiagram
  participant C as Client
  participant A as API
  participant O as Orchestrator
  C->>A: POST /v1/run
  A->>O: execute(request)
  O-->>A: result
  A-->>C: 200 response
```

### 4-7) State Transition

```mermaid
stateDiagram-v2
  [*] --> Received
  Received --> Validated
  Validated --> Processing
  Processing --> Success
  Processing --> Failed
  Success --> [*]
  Failed --> [*]
```

### 4-8) Compact Funnel (Shared Terminal)

```mermaid
flowchart TD
  S1[CADI enter]
  S2[AD Retrieval enter]
  S3[Answer Fusion enter]
  S4[QI enter]
  OK[terminal: success]
  DROP[terminal: business_drop]
  ERR[terminal: system_error]

  S1 -->|progress| S2 -->|progress| S3 -->|progress| S4 -->|pass| OK
  S1 -.blocking.-> DROP
  S2 -.empty_candidates.-> DROP
  S3 -.no_selected_ads.-> DROP
  S4 -.qi_rejected.-> DROP
  S1 -.exception.-> ERR
  S2 -.exception.-> ERR
  S3 -.exception.-> ERR
  S4 -.exception.-> ERR
```

### 4-9) Split Dense Diagram (Topology + Mapping)

```mermaid
flowchart TD
  SET[Singletons]
  A[Factory A]
  B[Factory B]
  SVC[Service]
  SET --> A --> SVC
  SET --> B --> SVC
```

```mermaid
flowchart LR
  A[Agent A LLM] --> EP1[Endpoint 1]
  B[Agent B LLM] --> EP2[Endpoint 2]
```

## 5) Preflight Checklist

- **노드/edge/subgraph 라벨에 `\n`이 없는가** (있으면 `<br/>`로 치환. `\n`은 줄바꿈이 아닌 리터럴 텍스트로 렌더됨)
- lower-case `end`가 라벨로 쓰여 파싱 오류를 유발하지 않는가
- `o-`/`x-`가 의도치 않은 edge 표현으로 해석되지 않는가
- 코멘트가 `%%` 규칙을 지키는가
- 외부 링크 때문에 `subgraph` direction이 무시되는 구조는 아닌가
- `sequenceDiagram`에서 participant를 명시했는가
- 탭 문자가 섞여 있지 않은가
- 노드 15개 이상이면 분할 또는 `elk` 전환을 검토했는가
- 접근성 메타데이터(`accTitle`, `accDescr`)가 필요한 문서인지 검토했는가

필수 검증 명령:

```bash
~/.agents/skills/mermaid-diagram-design/scripts/assess_mermaid_density.sh <markdown-file>
~/.agents/skills/mermaid-diagram-design/scripts/validate_mermaid_markdown.sh <markdown-file>
```

성공 기준:

- 출력이 `MERMAID_VALIDATE_OK ...`
- 밀도 점검에서 고위험 블록이 없거나, 고위험 블록에 대해 분할/축약 조치를 완료
- 실패 시 다이어그램 수정 후 재실행

## 6) Aesthetic Rules

- 다이어그램 단위 메시지 1개
- 순차 흐름은 `TD`, 비교는 `LR`를 기본
- 노드 수 6~12개 권장
- 긴 라벨은 `<br/>` 사용
- 장식용 노드/엣지 제거
- `LR`에서 겹침이 발생하면 먼저 `TD/TB`로 전환
- 구조 설명과 매핑 설명이 함께 있으면 다이어그램을 분리
