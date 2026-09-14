# ADR 0039: Impute one missing Arm 2 mobile cell

Date: 2026-09-14
Status: accepted 2026-09-14 by Andrew before any Arm 2 estimate was computed

## Context

The guarded Arm 2 run stopped before it returned, printed, or saved an
estimate. The 2026 mobile vintage lacks municipality 06366 for March 2026.
That municipality has positive frozen weight in 58 treated or placebo
models. The frozen gap computation therefore cannot use the complete
January through August window without a missing-data rule.

## Decision

The guarded loader will preserve the quarantined source files and derive one
value for municipality 06366 in March 2026. It will use the geometric mean
of that municipality's February and April counts. This is linear
interpolation on the log scale used by the synthetic-control gap calculation.
The loader requires the target to be absent and both neighboring values to
be positive and finite. It rejects the vintage if those conditions change.

P1 and P2 are exploratory because this rule changes their accepted protocol
after the unseen vintage was loaded. Their frozen thresholds and mechanical
classification labels remain unchanged, but neither classification supports
a confirmatory claim. The result artifact must record the imputation, label
P1 and P2 exploratory, and state that a confirmatory claim is not permitted.

## Rejected alternatives

- Waiting for another vintage preserves the original confirmatory protocol,
  but it does not answer the thesis-feasibility question now and may not
  restore the missing cell.
- Dropping March changes the complete contiguous window for every model.
- Removing municipality 06366 and renormalizing weights changes all eight
  months for 58 frozen models.
- Treating the missing value as zero violates the positive-outcome condition
  required by the log-scale model.
