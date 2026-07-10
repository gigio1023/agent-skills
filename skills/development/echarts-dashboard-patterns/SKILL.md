---
name: echarts-dashboard-patterns
description: >
  Use when creating, modifying, or reviewing Apache ECharts dashboard charts,
  especially time-series density, overlapping axis labels, legend/grid
  collisions, multiple y-axes, missing-data gaps, series naming, responsive
  resizing, or shared option builders. Trigger for "x축 라벨 겹침", "legend
  충돌", "dual y-axis", "connectNulls", and "splitNumber". NOT for general
  dashboard art direction without an ECharts implementation.
---

# ECharts Dashboard Patterns

ECharts 옵션을 고정 숫자 모음으로 만들지 않는다. 실제 컨테이너 크기,
데이터 밀도, 라벨 길이, 범례 위치와 누락 데이터의 의미에 맞추고 렌더 결과로
확인한다.

먼저 요청 모드를 구분한다. 리뷰·진단 요청이면 차트와 렌더 결과를 읽고 근거가
있는 발견사항만 보고하며, 파일 수정이나 주변 차트 리팩터링은 하지 않는다.
생성·수정 요청일 때만 아래 패턴을 실제 구현에 적용한다.

## Quick Start

1. 설치된 ECharts 버전과 기존 옵션 빌더, 테마, 렌더러를 확인한다.
2. 차트가 답해야 할 질문과 반드시 보여야 하는 series를 한 문장으로 정한다.
3. 대표 데이터뿐 아니라 긴 라벨, 최대 series 수, 누락 구간을 준비한다.
4. 아래 패턴 중 현재 문제에 필요한 것만 선택한다. 리뷰 모드에서는 진단 기준으로
   사용하고, 생성·수정 모드에서만 코드에 적용한다.
5. 목표 너비와 가장 좁은 지원 너비에서 실제 차트를 렌더한다. 생성·수정 모드라면
   확인된 문제를 범위 안에서 수정한다.
6. 변경이 있었다면 범위에 맞는 테스트·빌드와 resize 동작을 확인한다.

## Core Patterns

### Time-axis density

`splitNumber`는 정확한 tick 개수가 아니라 힌트다. 차트 너비와 시간 범위에
맞춰 3-8 정도의 읽을 수 있는 목표값을 정하고 `hideOverlap`을 안전망으로 쓴다.

```ts
xAxis: {
  type: 'time',
  splitNumber: targetTickCount,
  axisLabel: {
    hideOverlap: true,
    formatter: rangeIncludesMultipleDays ? '{MM}/{dd}\n{HH}:{mm}' : '{HH}:{mm}',
  },
}
```

라벨을 모두 노출하려고 글자를 지나치게 줄이지 않는다. 실제 시간 범위와
타임존이 맞는지 먼저 확인하고, 좁은 화면에서는 tick 수를 줄이거나 포맷을
단순화한다.

### Legend and grid ownership

축 라벨에는 `grid.containLabel: true`를 사용한다. 범례는 grid 밖의 별도 영역이므로
항목 수가 아니라 실제 폭과 줄바꿈 여부를 보고 공간을 확보한다.

```ts
legend: { type: legendMayOverflow ? 'scroll' : 'plain', bottom: 0 },
grid: {
  containLabel: true,
  top: 24,
  right: 16,
  bottom: legendHeight + 16,
  left: 16,
},
```

`56px`, `4개 이상` 같은 값은 시작점일 뿐 계약이 아니다. 번역된 라벨,
글꼴, 아이콘, 컨테이너 폭이 바뀌면 다시 렌더해 결정한다.

### Multiple y-axes

각 축이 다른 단위와 series를 명확히 소유하게 한다. 오른쪽 축의 여백은 가장 긴
포맷 라벨로 검증하고, 같은 쪽에 축이 둘 이상이면 `offset`을 사용한다. 격자선은
주축 하나에만 두는 편이 읽기 쉽다.

```ts
yAxis: [
  { type: 'value', name: latencyUnit },
  {
    type: 'value',
    name: trafficUnit,
    position: 'right',
    splitLine: { show: false },
  },
]
```

서로 다른 스케일을 같은 축에 억지로 넣거나, 시각적으로 강한 bar가 핵심 line을
가리지 않게 series 순서, 투명도, `z`를 실제 렌더에서 확인한다.

### Intentional gaps

의미 없는 값을 0으로 채우거나 앞 값으로 이어 붙이지 않는다. API 결과의 `NaN`,
빈 문자열 같은 값을 ECharts가 누락 데이터로 문서화한 `'-'` sentinel로
정규화하고 연결 여부를 명시한다.

```ts
const toMetricValue = (value: unknown) => {
  if (value === null || value === undefined || value === '') return '-'
  const numeric = Number(value)
  return Number.isFinite(numeric) ? numeric : '-'
}

series: [{
  type: 'line',
  connectNulls: false,
  data: points.map(([time, value]) => [time, toMetricValue(value)]),
}]
```

누락이 샘플 부족이나 수집 중단을 뜻한다면 범례·보조 문구·tooltip 중 적절한
위치에서 설명한다. 원인이 다른 gap을 하나의 시각 규칙으로 숨기지 않는다.

### Human-readable series names

raw metric label은 표시 직전에 안정된 display name으로 매핑한다. 기존 BFF나
서버 표현 계층이 있으면 그 경계를 따르되, 이 문제만 해결하려고 새 서버 계층을
만들지는 않는다. 알 수 없는 값은 원문을 유지해 series가 사라지지 않게 한다.

```ts
const SERIES_LABELS: Record<string, string> = {
  cache_hit: 'Cache Hit',
  retrieval: 'Retrieval',
  ranking: 'Ranking',
}

const displayName = SERIES_LABELS[rawName] ?? rawName
```

### Shared option builders

두 차트 이상에서 같은 tooltip, grid, axis 정책이 실제로 반복될 때만 공통 빌더를
추출한다. 새 추상화를 만들기 전에 기존 헬퍼를 확장할 수 있는지 확인한다.

얕은 spread는 `grid`, `axisLabel`, `tooltip` 같은 중첩 객체 전체를 덮어쓸 수 있다.
공통 빌더가 새 객체를 반환하게 하고 차트별 차이는 명시적으로 합친다. 한 차트만
바꾸는 요청에서 주변 차트까지 리팩터링하지 않는다.

## Responsive Behavior

- 컨테이너의 CSS 크기가 명확해야 하며 높이 0 상태에서 초기화하지 않는다.
- 레이아웃 변화에는 window resize만 가정하지 말고 기존 프로젝트 패턴에 맞춰
  `ResizeObserver` 또는 동등한 수단으로 `chart.resize()`를 호출한다.
- 숨겨진 탭에서 처음 렌더한 차트는 표시된 뒤 resize가 필요할 수 있다.
- 작은 화면에서 정보를 무조건 삭제하지 않는다. tick, legend, grid, tooltip의
  우선순위를 정하고 핵심 series가 남는지 확인한다.

## Verification Loop

최소한 다음 상태를 실제 렌더로 확인한다.

- 목표 너비와 가장 좁은 지원 너비
- 가장 긴 축·범례 라벨과 최대 series 수
- 정상값, 빈 결과, missing-data gap, 극단값
- legend scroll, tooltip, hover/emphasis, 컨테이너 resize
- 축 단위 잘림, legend-grid 충돌, 수평 overflow, 0 높이 canvas 부재

가능하면 기존 Storybook, 대시보드 route, visual test를 사용한다. 렌더 환경이
없으면 옵션 검사만으로 완료를 주장하지 말고 확인하지 못한 viewport와 상태를
명시한다.

## Output Contract

리뷰라면 중요한 발견사항부터 말하고 파일을 바꾸지 않았음을 명시한다. 생성·수정
요청이라면 변경 결과를 먼저 말한다. 이어서 실제로 렌더한 viewport·데이터 상태와
실행한 테스트만 짧게 적는다. 시각 확인을 못 했다면 그 사실과 남은 위험을
명시한다.

## Gotchas

- `splitNumber`는 보장값이 아니며 `hideOverlap`만으로 좋은 축이 되지는 않는다.
- `containLabel`은 축 라벨을 돕지만 외부 legend 공간까지 계산하지 않는다.
- `connectNulls: false`는 입력이 실제 missing 값으로 정규화되어야 의미가 있다.
- dual-axis는 상관관계를 암시하기 쉽다. 단위와 series 소유권을 분명히 한다.
- 테스트 fixture가 짧은 영문 라벨뿐이면 실제 충돌을 놓친다.
- 요청받지 않은 BFF, 디자인 시스템, 차트 라이브러리 교체로 범위를 넓히지 않는다.
