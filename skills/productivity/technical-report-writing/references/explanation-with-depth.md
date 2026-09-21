# An Explanation With Optional Depth

Use for a technical introduction or long document whose readers have different backgrounds. The target is an explanation that works at the chosen depth. A shorter introduction is useful when it brings readers to the subject sooner; the mechanism may still need several paragraphs.

## Reader and supplied material

This independently synthetic case concerns a monitoring chart. The reader needs to understand why a moving average reacts later than the current sample and choose a window accordingly. The supplied teaching model is a trailing arithmetic mean over equally spaced samples, including the current sample. Samples are 12 before time 1 and 21 from time 1 onward; the window contains three samples. These are teaching inputs, not measured system results.

## Orientation that postpones the explanation

> This guide introduces moving averages from the fundamentals through practical selection. After reading it, you will understand the formula, explain response lag to a colleague, and choose a window. Read the conclusions first, then the derivation if you need the background. We use English terminology and explain the mathematical notation consistently. This guide does not cover every filter.

The passage spends its space describing the future reading experience. It has not yet explained what is averaged, why the output lags, or how the window affects the choice. A curriculum specification could need learning outcomes; this reader needs the explanation itself.

## A complete reader-facing passage

The following Korean sample keeps technical terms and defines them through use. Its HTML disclosure illustrates information placement; use the destination's actual supported blocks when producing the document.

### Moving average의 반응 지연

Moving average(이동평균)는 최근 여러 관측값을 평균한 값이다. 새 관측값이 들어와도 이전 값이 계산에 남기 때문에, 값이 갑자기 바뀌면 평균에는 그 변화가 점진적으로 반영된다.

예를 들어 관측값이 12에서 21로 바뀌었다고 하자. 최근 세 값을 평균하면 첫 결과는 `(12 + 12 + 21) / 3 = 15`다. 다음 관측값도 21이면 결과는 18이 되고, 세 번째 21이 들어온 뒤에야 평균도 21이 된다.

| 변화 후 관측 시점 | 새 관측값 | 평균에 들어가는 세 값 | Moving average |
| --- | ---: | --- | ---: |
| 1 | 21 | 12, 12, 21 | 15 |
| 2 | 21 | 12, 21, 21 | 18 |
| 3 | 21 | 21, 21, 21 | 21 |

표의 지연은 과거 값이 window(평균에 포함하는 구간)에서 빠져나가는 데 걸리는 시간에서 생긴다. 같은 간격으로 관측할 때 window를 늘리면 더 오래된 값도 평균에 남는다. 최근 변화에 빠르게 반응해야 하는 차트에서는 짧은 window를, 여러 관측값을 함께 보려는 차트에서는 긴 window를 검토할 수 있다. 적절한 길이는 관측 간격과 차트의 용도에 따라 정한다.

<details>
<summary>계산식: window와 가중치</summary>

위 계산은 현재 시점을 포함한 최근 N개 값을 같은 비중으로 평균한다. x_t는 시점 t의 관측값이고, m_t는 같은 시점의 moving average다.

$$
m_t = \frac{1}{N}\sum_{i=0}^{N-1}x_{t-i}
$$

N = 3이면 현재 값과 직전 두 값을 각각 1/3씩 반영한다. 새 값 하나가 평균 전체를 즉시 바꾸지 못하는 이유도 각 값의 가중치가 1/3이기 때문이다. 이 식은 관측 간격이 일정하고, 현재 값을 포함해 과거 N개를 사용하는 경우를 나타낸다.

</details>

## Why this passage works

- The heading names the phenomenon. The opening explains it immediately, using a definition because this reader needs one.
- The same numbers continue from prose into the table and formula. The table makes the changing window visible; the prose explains its consequence.
- The window choice follows from the demonstrated mechanism. It does not promise that one size is optimal or claim a measured reduction in noise.
- The main path explains the result without requiring summation notation. The disclosure preserves the calculation for a reader who wants the formal version. Its title is enough to choose whether to open it.
- The assumptions are next to the example and equation they qualify. English terms, Korean glosses, and mathematical symbols are used directly, without a separate statement of editorial policy.

## A shorter version that loses the explanation

> Moving average smooths values but causes lag. Choose the window for the task. See the formula for details.

This names an effect and a choice but gives the reader no way to connect them. The complete passage is longer because the numerical example and mechanism do necessary work. For an expert lookup, the formula and assumptions alone may suffice; for an introductory explanation, that reduction would lose the requested teaching.

## Transfer the operation

For another subject, choose an observation the reader can recognize, explain it through a stable example, and introduce concepts when the example needs them. Put optional depth where the reader encounters that need. Use a callout only when it supplies an otherwise missing scope or result; use a contents list when it aids navigation. The useful pattern is the advance in understanding, not this example's heading count, table, formula, or disclosure count.
