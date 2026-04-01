# Scoring Rubric

Score each dimension from `0` to `3`.

## 1) Evidence Depth

- `0`: no direct evidence
- `1`: one weak or partial source
- `2`: multiple relevant sources with clear provenance
- `3`: primary source plus independent corroboration

## 2) Coverage and Triangulation

- `0`: single viewpoint or single domain
- `1`: multiple pages but same viewpoint/family
- `2`: cross-family corroboration with minor gaps
- `3`: explicit triangulation including contradiction handling

## 3) Recency and Consistency

- `0`: timing unknown or clearly stale
- `1`: mixed recency with unresolved mismatch
- `2`: dates checked and mostly consistent
- `3`: dates checked, latest updates verified, inconsistencies resolved

## 4) Uncertainty Handling

- `0`: overconfident despite weak evidence
- `1`: vague caveats without claim-level impact
- `2`: claim-level uncertainty explicitly marked
- `3`: uncertainty propagated to dependent conclusions and next checks defined

## Release Rule

Confident finalization is allowed only when relevant dimensions are all `>= 2`.

If any key dimension is below `2`, continue investigation or output a limited-confidence answer.
