# ADR 0035: Arm 3 battery size — "24 specifications" is loose; the frozen artifact records 12 specifications across two targets

Date: 2026-07-30
Status: accepted 2026-07-30 (corrects wording in ADR 0031 and `docs/arm3_implementation_report.md`; changes no result, no verdict, and no analysis)

## Context

ADR 0031 describes Arm 3's battery three times as a "24-specification
battery" (`:21`, `:29`, `:80`, after the correction note this ADR adds). The frozen artifact
`output/arm3_kanazawa/causal_robustness/metrics.json` records
`design.specification_count: 12`. The 12 specifications are run against
two targets — Ishikawa (treated) and Toyama (negative control) — giving
**24 target-by-specification rows**.

The discrepancy was found while deepening `docs/thesis/defense_memo.md`
and was flagged rather than repaired, because ADR 0031 is accepted and
correcting an accepted ADR's wording is a human decision
(`docs/arm3_implementation_report.md` §"Battery size"). The memo already
states the correct form and says so explicitly (`defense_memo.md:441-446`).

This is a counting-vocabulary error, not a numerical one. Every quantity
in the verdict — V1a p = 0.181818, V2a p = 0.212121, the strict-pool
p = 0.210526, the RMSPE values, the placebo floor — is unaffected, and
the p-value scan behind the verdict ("no run reaches p ≤ 0.05 on V1a")
holds identically whether the denominator is described as 12
specifications or 24 rows, because the scan covers every row either way.

## Decision

**1. The correct form is: 12 specifications, run against two targets, for
24 target-by-specification rows.** That is what every document says from
now on. "24 specifications" is not used again.

**2. ADR 0031's body is not rewritten.** The ADR log is append-only
(ADR 0033). A correction note is added under its Status line pointing
here, in the same style as the inline `Corrected same day by ADR 0032`
note ADR 0031 already carries. Its three "24-specification battery"
occurrences are read through that note.

**3. `docs/arm3_implementation_report.md` is corrected in place.** It is
an implementation report, not an ADR, and its "discrepancy flagged, not
repaired" paragraph is replaced by the resolution. The same applies to
the loose occurrence in `docs/thesis/defense_memo.md:33`; that document's
Seam D body already states the correct form and needs no change.

**4. Nothing is re-run.** Arm 3 is closed (ADR 0031). No artifact is
regenerated, no figure changes, no hash changes. If `make arm3-kanazawa`
is ever re-run for reproduction, it must reproduce the same hashes.

## Consequences

- An examiner comparing ADR 0031's prose against `metrics.json` finds the
  discrepancy already recorded, quantified, and resolved, rather than
  finding it first.
- The verdict, its tier outcomes, the suspect protocol, and the ADR 0017
  bound are untouched.
- The scan claim is now stated at the grain the artifact supports: across
  all 24 target-by-specification rows, no run reaches p ≤ 0.05 on V1a;
  the smallest one-sided opening p is the primary's 0.181818.

## Rejected alternatives

- **Edit ADR 0031's three occurrences in place.** Breaks the append-only
  log for a wording fix and would leave no record that the accepted text
  ever said something else.
- **Leave it flagged.** The flag was correct as a seat-level action; it
  is a standing invitation for a later reader to quote "24
  specifications" from an accepted ADR.
- **Re-run the battery to produce 24 genuine specifications.** Absurd
  and forbidden — Arm 3 is closed, and re-running after seeing the
  verdict destroys the pre-specification discipline.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote the
affected analysis to exploratory, per ADR 0019.
