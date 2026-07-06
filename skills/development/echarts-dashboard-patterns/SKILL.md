---
name: echarts-dashboard-patterns
description: |
  ECharts 대시보드 차트 구성 시 반복되는 실수를 방지하는 패턴 가이드.
  x축 라벨 겹침, legend-chart 영역 충돌, dual y-axis 여백, 시계열 갭 처리,
  series 이름 매핑, 공통 config 추출 등 실전에서 검증된 규칙 모음.
  TRIGGER: ECharts 차트를 생성/수정하거나, "x축 라벨 겹침", "legend 충돌",
  "dual y-axis 여백", "connectNulls", "splitNumber" 같은 차트 가독성 문제를 수정할 때.
version: 1.0.0
---

# ECharts Dashboard Patterns

ECharts 기반 대시보드 차트를 만들 때 반복적으로 발생하는 문제와 해결 패턴.
실시간 대시보드 구현 과정에서 반복적으로 검증된 내용을 일반화했다.

## When to Apply

- ECharts `option` 객체를 생성하거나 수정할 때
- 차트 가독성 이슈(라벨 겹침, legend 충돌, 여백 부족)를 수정할 때
- 시계열 차트에서 의도적 갭(NaN)을 다룰 때
- 여러 차트가 공통 구조를 공유할 때

---

## 1. x축 라벨 겹침 방지

**문제**: 시간 범위가 길어지면(6h, 12h, 24h) x축 틱이 촘촘해져 `14:00`, `15:00` 등이 겹쳐 읽을 수 없다.

**해결**:

```typescript
xAxis: {
  type: 'time',
  splitNumber: 5,                          // 틱 수를 5~6개로 제한
  axisLabel: { formatter: '{HH}:{mm}', hideOverlap: true }  // 겹치면 자동 숨김
}
```

**규칙**:
- `splitNumber`는 차트 너비 기준 5~7이 적정. 노트북(~700px)에서는 5.
- `hideOverlap: true`는 ECharts 5.x 기본 내장. 반드시 켜둔다.
- 24시간 이상 범위에서는 `{MM}/{dd}\n{HH}:{mm}` 포맷으로 날짜를 함께 표시.

---

## 2. Legend와 차트 영역 겹침 방지

**문제**: `legend: { bottom: 0 }` + `grid: { bottom: 40 }` 조합에서 legend 항목이 많으면 차트 하단과 겹친다. 특히 노트북 화면에서 심하다.

**해결**:

```typescript
legend: { data: names, bottom: 0, type: 'scroll' },  // 많으면 스크롤
grid: { top: 24, right: 16, bottom: 56, left: 56 },  // bottom 여백 충분히 확보
```

**규칙**:
- `grid.bottom`은 legend 높이를 고려해 최소 56px.
- legend 항목이 4개 이상이면 `type: 'scroll'`을 기본으로 적용.
- legend `bottom`과 grid `bottom` 사이 최소 16px 간격 유지.

---

## 3. Dual y-axis 차트 여백

**문제**: 오른쪽 y축 라벨(`/s`, `req/s`)이 차트 영역 밖으로 잘린다.

**해결**:

```typescript
grid: { top: 24, right: 56, bottom: 56, left: 56 },  // right도 56
yAxis: [
  { type: 'value', position: 'left', axisLabel: { formatter: '{value}s' } },
  { type: 'value', position: 'right', axisLabel: { formatter: '{value}/s' }, splitLine: { show: false } }
],
```

**규칙**:
- dual y-axis 시 `grid.right`를 56px로 확보.
- 오른쪽 축은 `splitLine: { show: false }`로 격자 중복 방지.
- 배경 bar + 전경 line 조합 시 bar를 먼저 렌더(`series` 배열에서 bar를 앞에).

---

## 4. 시계열 갭(NaN) 처리

**문제**: 저트래픽 구간에서 histogram_quantile이 의미 없는 값을 반환. PromQL에서 NaN으로 만들었는데 차트가 이전 값으로 이어 그린다.

**해결**:

```typescript
series: [{
  connectNulls: false,  // NaN 구간을 자연스러운 갭으로 렌더
  // ...
}]
```

**규칙**:
- 의도적 NaN(min-sample guard 등)이 있는 시계열은 반드시 `connectNulls: false`.
- 갭이 발생하는 이유를 UI에 안내 텍스트로 표시 (hover tooltip만으로는 부족).
- 갭과 트래픽의 상관관계를 보여주려면 배경 bar(request count)를 dual y-axis로 추가.

---

## 5. Series 이름 매핑

**문제**: Prometheus 결과의 raw label(`cache_hit`, `retrieval`, `ranking`)이 차트 legend에 그대로 노출.

**해결**:

```typescript
const SERIES_LABELS: Record<string, string> = {
  cache_hit: 'Cache Hit',
  retrieval: 'Retrieval',
  ranking: 'Ranking',
  quality_check: 'Quality Check'
};

// toNamedSeries에 labelFormatter 전달
toNamedSeries(result, 'source', (value) => SERIES_LABELS[value] || value)
```

**규칙**:
- raw metric label을 UI에 직접 노출하지 않는다.
- 프로젝트별 서버 계층이 있으면 label -> display name 매핑은 BFF/server endpoint에서 수행. 클라이언트에 raw label이 도달하면 안 된다.
- `labelFormatter`가 `labelKey` 유무와 관계없이 항상 적용되도록 구현 (fallback `'value'` 버그 방지).

---

## 6. 공통 차트 config 추출

**문제**: 여러 차트가 tooltip, legend, grid, xAxis를 각각 중복 정의.

**해결**:

```typescript
function baseChartConfig(names: string[]) {
  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: { data: names, bottom: 0, type: 'scroll' },
    grid: { top: 24, right: 16, bottom: 56, left: 56 },
    xAxis: { type: 'time', splitNumber: 5, axisLabel: { formatter: '{HH}:{mm}', hideOverlap: true } }
  };
}

// 일반 차트
function buildChartOption(series, unit) {
  return { ...baseChartConfig(series.map(s => s.name)), yAxis: { ... }, series: [...] };
}

// dual y-axis 차트는 grid.right만 override
function buildLatencyChartOption(latency, traffic) {
  return { ...baseChartConfig(allNames), grid: { ...base.grid, right: 56 }, yAxis: [...], series: [...] };
}
```

**규칙**:
- base config를 추출하고 차트별로 `yAxis`와 `series`만 다르게 구성.
- spread (`...`) 후 개별 속성 override로 차이점만 명시.
- `toEchartsData()` 같은 data 변환 헬퍼도 공유.

---

## 7. 반응형 고려사항

**문제**: 데스크톱에서는 괜찮지만 노트북(1366px 이하)에서 차트가 찌그러진다.

**체크리스트**:
- `splitNumber`를 고정값이 아닌 차트 너비 비례로 설정하는 것도 고려 (단, 대부분 5~6 고정으로 충분).
- legend `type: 'scroll'`은 노트북에서 4+ 항목이 한 줄에 안 들어갈 때 필수.
- `grid.bottom` 56px 이상 확보 — 노트북에서 legend가 x축 라벨과 겹치는 주요 원인.
- 차트 높이는 `280px` 이상 유지. 그 이하로 줄이면 y축 라벨이 겹친다.

---

## Quick Checklist (차트 생성 시)

```
[ ] splitNumber: 5~6, hideOverlap: true
[ ] grid.bottom >= 56px (legend 공간)
[ ] dual y-axis 시 grid.right >= 56px
[ ] legend type: 'scroll' (항목 4개 이상)
[ ] connectNulls: false (의도적 갭이 있는 시계열)
[ ] raw metric label → human-readable name 매핑
[ ] 공통 config는 baseChartConfig()로 추출
[ ] 차트 높이 280px 이상
```
