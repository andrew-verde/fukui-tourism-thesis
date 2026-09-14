# ADR 0038: Keep frozen FTAS history and select only new responses

Date: 2026-09-14
Status: accepted 2026-09-14 by Andrew before any Arm 2 result was computed

## Context

ADR 0037 replaced an impossible byte-prefix condition with exact row-identity
reconciliation. The guarded production entry point then established that the
current upstream merge has revised or removed at least one committed June
row. It stopped before `analyze_guarded` ran, produced no result artifact, and
printed no outcome value. P1 and P2 were not computed.

The current upstream file cannot validate the historical population because
that population has changed. It can still supply new responses whose dates
fall strictly after the frozen boundary. The committed file remains the sole
authority for the seen population.

## Decision

The gateway will construct the 2026 FTAS analysis wave from two disjoint
sources:

1. the checksum-pinned committed file for all seen rows through 2026-06-29;
2. rows from the checksum-pinned current upstream file whose response dates
   are later than 2026-06-30.

The gateway ignores all current-file rows on or before 2026-06-30. It requires
the current file to retain the expected schema, requires every response date
to parse, requires at least one post-boundary row, and rejects exact duplicate
post-boundary rows. The 2026-06-30 seam remains excluded, as specified in the
original gateway. The raw current file remains unchanged in quarantine with
its source checksum.

S1 and S3 remain exploratory secondary checks under ADR 0037 because their
assembly protocol changed after ADR 0020 was accepted. P1 and P2 remained
confirmatory under this decision, but ADR 0039 later demoted them to
exploratory after a missing mobile cell required a new rule. The failed
guarded attempt did not call their computation and revealed no result. S2
remains descriptive under ADR 0036.

## Rejected alternatives

- Use the current pre-July rows. That would replace the frozen seen population
  with revised history.
- Require current history to reconcile with the frozen file. The first guarded
  attempt established that this condition is unsatisfied.
- Drop the current FTAS file entirely. That would make the planned post-June
  secondary checks unavailable even though their new-response population is
  identifiable by the frozen date boundary.
