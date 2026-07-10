# Mermaid Reusable Patterns (v2)

## Table of Contents

- Type Selection Matrix
- Frontmatter Presets
- Accessible Fallback Palette
- Core Patterns
- Preflight Checklist
- Aesthetic Rules

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
---
flowchart TD
  accTitle: Example diagram
  accDescr: Example process flow from A to B
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

## 3) Accessible Fallback Palette

Use this restrained Material Design based palette when color carries meaning and
the destination has no established visual system. An unstyled diagram is often
more portable; do not add every semantic color merely because definitions exist.

### 3-1) Semantic States

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
  linkStyle default stroke:#455a64,stroke-width:1.8px;
```

### 3-2) Architecture Layers

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
  linkStyle default stroke:#455a64,stroke-width:1.8px;
```

### 3-3) Pipeline Steps

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

### 3-4) Copyable Class Definitions

```
  classDef success fill:#e6f4ea,stroke:#34a853,color:#1e4620;
  classDef warning fill:#fef7e0,stroke:#f9ab00,color:#5f4b00;
  classDef error fill:#fce8e6,stroke:#ea4335,color:#7c1d13;
  classDef neutral fill:#f1f3f4,stroke:#5f6368,color:#3c4043;
  classDef primary fill:#e8f0fe,stroke:#1a73e8,color:#174ea6;
  classDef purple fill:#f3e8fd,stroke:#9334e6,color:#4a1d8e;
  linkStyle default stroke:#455a64,stroke-width:1.8px;
```

### Color Rules

- Do not communicate meaning with color alone. Pair color with labels or line
  style.
- Use `stroke:#455a64` (blue-grey 700) for edges instead of the default gray.
- Use light fills, darker strokes, and the darkest tone for text.
- Prefer four or fewer colors in one diagram. When more categories are needed,
  distinguish them with labels.

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
  S1[Intake]
  S2[Retrieve]
  S3[Select]
  S4[Review]
  OK[terminal: success]
  DROP[terminal: business_drop]
  ERR[terminal: system_error]

  S1 -->|progress| S2 -->|progress| S3 -->|progress| S4 -->|pass| OK
  S1 -.blocking.-> DROP
  S2 -.empty_candidates.-> DROP
  S3 -.no_selection.-> DROP
  S4 -.rejected.-> DROP
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

- **Do node, edge, and subgraph labels avoid literal `\n`?** Replace it with
  `<br/>` when present. Mermaid renders `\n` as literal text, not a line break.
- Is lower-case `end` avoided as a label where it could cause a parse error?
- Are `o-` and `x-` avoided when they could be parsed as special edge heads?
- Do comments follow the `%%` line-start rule?
- Could external links cause `subgraph` direction to be ignored?
- Does each `sequenceDiagram` declare participants explicitly?
- Are tab characters absent?
- If the diagram has 15 or more nodes, did you split it or consider `elk`?
- Does the target document need accessibility metadata such as `accTitle` and
  `accDescr`?

For repository markdown files, resolve `MERMAID_SKILL_DIR` to the directory that
contains this skill's `SKILL.md`, then run with an absolute target path:

```bash
MERMAID_SKILL_DIR="<absolute path to the installed mermaid-diagram-design skill>"
"$MERMAID_SKILL_DIR/scripts/assess_mermaid_density.sh" "<absolute markdown path>"
"$MERMAID_SKILL_DIR/scripts/validate_mermaid_markdown.sh" "<absolute markdown path>"
```

Success criteria:

- Validation output includes `MERMAID_VALIDATE_OK ...`.
- Density warnings were visually reviewed; required content was not removed just
  to satisfy a heuristic threshold.
- On failure, fix the diagram and rerun the checks.

## 6) Aesthetic Rules

- Use one message per diagram.
- Choose direction from reader path, label length, renderer width, and density.
- Use `LR` for comparisons, parallel lanes, ownership boundaries, and handoffs.
- Use `TD` or `TB` for short sequential paths, funnels, and decision trees.
- Avoid default `LR` when labels are long, branches are many, or the renderer is
  narrow.
- Avoid tall `TD` or `TB` scroll tunnels; split by phase or collapse repeated
  steps.
- Prefer 6-12 nodes.
- Use `<br/>` for long labels.
- Remove decorative nodes and edges.
- Simplify, split, or switch direction before tuning spacing.
- Split the diagram when structure and mapping details are mixed.
