# ADR 0020: Arm 2 — frozen out-of-sample prediction criteria for the transience/durability claim

Date: 2026-07-03
Status: **accepted 2026-07-30 — binding.** The two pre-acceptance drafting
corrections recorded at the end of this document were applied before
acceptance and before any unseen data was fetched or opened. Firewall
release requires this acceptance **and** the frozen scripts + oracles
committed (§"Unseen"); both conditions are met as of the commit that
carries this line.

## Context

ADR 0019 adopts Arm 2: testing the ADR 0017 headline — "a high-speed-rail
extension's demand shock is transient by default, durable only where station
arrivals convert to destination anchors" — as a *prediction* on data the
existing models have never seen. The evidentiary value of that test exists
only if the predictions, metrics, thresholds, and falsification conditions
are frozen before any unseen outcome data is pulled or inspected. Once new
data is seen, the option to pre-specify is gone permanently. This ADR is
that freeze. It plays the role ADR 0018 plays for Direction B: it governs
over any later analysis convenience, and post-acceptance deviations must be
logged in a new ADR and demote the affected analysis to exploratory.

### The seen/unseen boundary (declared now, verbatim)

Data already used by the thesis ("seen"):

- **Mobile-location municipal panel**: January 2021 – December 2025,
  vintage pinned in `config/national_data_sources.yaml`
  (`data/city2025.csv`, sha256 `7c31fed0…17d5216`, 22,434 rows; upstream
  commit `dfb9069`). Gap/rank inference only, never absolute headcounts.
- **FTAS / merged tri-prefecture survey**: responses April 2023 – June 2026
  (n = 103,807 as committed).
- **JTA accommodation panel**: 2018–2024 confirmed values plus 2025 annual
  preliminary vintage.

"Unseen" (the test set): any mobile-panel vintage covering months after
2025-12; any FTAS/merged waves after 2026-06; JTA 2025 confirmed and any
2026 rows. **Firewall:** fetch/build scaffolding may be developed and tested
against the seen vintages, but unseen outcome values must not be fetched,
opened, plotted, or summarized — by any seat, including Codex — until this
ADR is accepted and the analysis scripts with their oracles are committed.
Unseen pulls land in a quarantined directory and are touched only by the
frozen scripts.

### Frozen inputs from the existing results (the predictions' anchors)

- Regime assignments from `output/synthesis/durability_mechanisms.csv`:
  high-confidence **durable** = Sakai (18210), Eiheiji (18322);
  high-confidence **transient** = Awara (18208), Fukui City (18201),
  Tsuruga (18202), Sabae (18207); low-confidence rows (Katsuyama, Ikeda,
  Mihama, Echizen City) are excluded from confirmatory sets and reported
  descriptively only.
- The 13 high-confidence municipalities behind r = 0.826 are the
  `regime_confidence = high` rows of that table.
- SCM donor weights and fit gates as committed for Direction D
  (pre-period fit through 2024-02, `pre_rmspe ≤ 0.15`,
  `RMSPE_FIT_MULT = 5.0`, `EVENT_YM = 202403`). **Weights are frozen — the
  extension appends post-period months to existing fits; no refitting with
  any post-2024-02 data.** Refitting would absorb exactly the persistence
  the test is trying to measure.
- The existing municipal transport_access friction ranking (FTAS through
  2026-06) is the predictor; it is not re-estimated for the primary test.

## Decision

Two co-primary predictions, three secondary, all directional (sidedness
declared here, ex ante, mirroring the Seam C posture). The headline verdict
"prediction confirmed" requires **both** primaries; one alone is reported
as partial support, never as confirmation.

### P1 — regime persistence (co-primary)

On unseen mobile-panel months 2026-01 onward, using frozen donor weights:

- Compute each high-confidence municipality's mean monthly gap versus its
  synthetic control over the unseen window (minimum 6 unseen months
  required; else the test waits).
- **Prediction:** every durable-set municipality (Sakai, Eiheiji) shows a
  positive mean unseen-window gap, and the durable-set mean gap exceeds the
  transient-set (Awara, Fukui City, Tsuruga, Sabae) mean gap.
- **Inference:** one-sided in-space placebo test at α = 0.05 for the
  durable−transient gap difference, using the same well-fit donor
  municipalities and placebo machinery as Direction D (identical fit
  gates; no new discretion).
- **Confirmed:** both sign conditions hold and placebo p ≤ 0.05.
  **Directional-only:** signs hold, p > 0.05. **Falsified:** durable-set
  mean gap ≤ transient-set mean gap, or either durable municipality's mean
  gap ≤ 0.

### P2 — friction→durability association out of sample (co-primary)

- Spearman rank correlation, across the 13 high-confidence municipalities,
  between the *existing* transport_access friction ranking (seen data,
  frozen) and the *unseen-window* mean SCM gap ranking.
- **Prediction:** ρ > 0. **Confirmed:** ρ ≥ 0.48 (the one-sided α = 0.05
  critical value at n = 13). **Directional-only:** 0 < ρ < 0.48.
  **Falsified:** ρ ≤ 0.
- The in-sample value (r = 0.826) is explicitly *not* the bar; the claim
  is sign and ordering, not magnitude replication.

### Secondary predictions (reported, never headline)

- **S1 — DiD non-reversal:** on FTAS waves after 2026-06, the NPS and
  transport-satisfaction DiD coefficients (same specification, clustered
  SEs, earthquake-robust variant) remain non-negative. Point-estimate
  shrinkage is consistent with the claim (experience effects need not
  track demand durability); sign reversal with CI excluding zero is
  reported as a discordant result against Chapter 3.
- **S2 — JTA decay shape:** prefecture-level Fukui overnight stays in JTA
  2025-confirmed/2026 rows revert toward the pre-extension trend (the
  transient-by-default component at prefecture aggregation), while the
  event-study framing stays descriptive, as in the accommodation layer's
  existing role.
- **S3 — friction persistence:** transport_access friction prevalence
  among shinkansen arrivers in unseen FTAS waves remains the argmax
  friction category with a shinkansen-vs-pooled-other gap > 2× (seen value
  4.003×, 7.09% vs 1.7711661764394693 — the `shk_over_other_ratio` column
  of `output/synthesis/synthesis_mode_friction.csv`). The comparison is
  against **pooled other arrival modes**, not private car: the private-car
  ratio is 7.09 / 0.66 = 10.74×, against which a 2× floor would be a far
  weaker test than this threshold was calibrated for. Erosion below 2×
  would suggest the constraint is
  resolving itself and weakens the Direction B motivation; this feeds the
  Stage-2 fielding decision but gates nothing by itself.

### Vintage-revision guard

Vendor panels revise history. Before any unseen-window computation: verify
the new vintage's 2021-01 – 2025-12 series against `city2025.csv` for the
**13 high-confidence Fukui municipalities** and all retained donors. These
are pinned by area code as: 18201 Fukui City, 18202 Tsuruga, 18204 Obama,
18205 Ono, 18207 Sabae, 18208 Awara, 18210 Sakai, 18322 Eiheiji, 18404
Minami-Echizen, 18423 Echizen Town, 18481 Takahama, 18483 Oi, 18501
Wakasa — the `regime_confidence == "high"` rows of
`output/synthesis/durability_mechanisms.csv`, which are identical to its
`good_fit == True` rows. P2 ranks exactly this set and P1's six
confirmatory municipalities are a subset of it; the artifact's four
low-confidence municipalities enter no Arm 2 computation and are
therefore not guarded. "Confirmatory municipality" below means any of
these 13. If root-mean-square
relative revision exceeds 2% for any confirmatory municipality, or any
donor exits the fit gate under revised history, stop; log a deviation ADR
deciding between (a) re-running the *entire* Direction D + Arm 2 chain on
the revised vintage as the single canonical series, or (b) demoting Arm 2
to exploratory. Mixing vintages within one analysis is forbidden.

### Interpretation contract (written before the result exists)

- **Both primaries confirmed:** Direction C is promoted from
  hypothesis-bridge to tested prediction; Seam B's concession is rewritten
  to reflect out-of-sample corroboration; ADR 0017's sentence stands with
  "durable only where…" now carrying predictive, not just associative,
  weight.
- **Directional-only outcomes:** reported as consistent-but-underpowered;
  Seam B concession stays as written; no promotion.
- **Either primary falsified:** the falsification is a first-class result.
  The template claim is bounded to the seen window ("the anchor-conversion
  account organizes 2024–2025 but fails prospectively"), Chapter 4's
  diagnosis is unaffected (it never depended on durability), and the
  contribution reframes around the diagnosis template plus an honest
  prospective failure — via a new ADR before any chapter edits.
- No outcome licenses re-opening the seen-window analyses to "check";
  post-hoc reconciliation analyses are exploratory by definition.

### Execution routing

Codex implements the extension scripts against this ADR with tests
asserting: frozen weights are loaded (not refit), unseen-window boundaries
match the declared vintages, thresholds match this document verbatim, and
the vintage-revision guard runs first. Human accepts this ADR and commits
before any unseen data is fetched. Analysis runs are mechanical thereafter;
interpretation memos may go to a mid-tier seat, but any text change to
chapters routes through the outcome-matched branch above.

## Consequences

- The transience/durability claim acquires a genuine prospective test with
  its risk stated in advance; either outcome is publishable and neither
  destabilizes the already-written thesis.
- The cost of discipline is patience: at least six unseen panel months and
  a possibly slow vendor vintage mean the primary verdict likely lands
  mid-2027; the roadmap (ADR 0019 Phase 2–3) already absorbs this.
- Freezing the friction ranking as predictor deliberately forgoes any
  improvement from newer FTAS waves; that conservatism is the price of a
  clean prediction test.

## Rejected alternatives

- **Refit SCM including post-2024 data for "better fits":** absorbs the
  effect under test; rejected outright.
- **Magnitude-replication bar for P2 (ρ near 0.826):** in-sample magnitude
  at n = 13 is noise-inflated; a magnitude bar would manufacture failure.
- **Single primary (P1 only):** the association (P2) is what carries the
  template's diagnostic content; persistence without the friction ordering
  would corroborate durability but not the mechanism.
- **Two-sided tests:** the claim under test is directional and was
  published (in the thesis) before the data exist; unlike Direction B's
  backfire channel (ADR 0018 rule 4), there is no plausible symmetric
  alternative worth α here.

## Pre-acceptance drafting corrections (2026-07-30)

Two internal inconsistencies were found during Arm 2 implementation, while
this ADR was still `proposed`, and corrected here in draft. Both were
resolved **before any unseen data was fetched or opened** (firewall
intact; see ADR 0032) and before this ADR became binding, so neither is a
deviation and neither demotes any analysis.

1. **Vintage-revision guard population.** The guard specified "14 Fukui
   municipalities". No set of 14 exists: `durability_mechanisms.csv` holds
   17 municipalities, of which 13 are high-confidence (identically, 13 are
   `good_fit`) and 4 are low. Pinned to the 13 high-confidence
   municipalities by explicit area code, since P2 ranks exactly that set
   and P1's 6 are a subset.

2. **S3 denominator.** The S3 sentence named a "shinkansen-vs-car" gap and
   quoted "7.09% vs 0.66%" — the car comparison, whose ratio is 10.74× —
   while also quoting "≈ 4.0×", which is `shk_over_other_ratio` = 4.003,
   the comparison against pooled other modes (1.7711661764394693). The two
   halves of the sentence disagreed. Frozen as **pooled other**: it is the
   value the 2× threshold was calibrated against, the harder test, and the
   only ratio the committed artifact defines.

Both were surfaced by the implementing seat, which stopped rather than
choosing — selecting a denominator or a municipality set during
implementation would have been exactly the analyst discretion this ADR
exists to remove.
