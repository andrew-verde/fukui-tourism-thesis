# ADR 0040: Awara occupancy — frozen forward prediction test at a 30-day horizon

Date drafted: 2026-09-14
Date accepted: 2026-09-14
Status: **Accepted.**

Drafted by Claude Science at the author's request and accepted on the author's explicit
in-session instruction of 2026-09-14 ("Can you do those changes? Then do the pull?"), which
authorised the preconditions, the acceptance, and the pull in that order. The acceptance is
recorded here rather than assumed, because the credibility of a pre-registration rests on
who committed to it and when. Numbering follows 0039.

Binding from commit `<this commit>`: `scripts/awara_forward_test.py`,
`data/frozen/awara_frozen_model_coefficients.csv` and
`data/frozen/awara_frozen_m1_coefficients.csv` are committed together with this document
and precede the unseen pull in git history. That ordering is the evidence that the
specification was fixed before the outcomes were available; it is verifiable with
`git log --follow` and does not depend on anyone's recollection.

## Context

`docs/adr/0020` froze Arm 2's out-of-sample criteria and ADRs 0037–0039 demoted it before
any estimate was produced, for three upstream-data reasons in sequence. The ambition it
carried — testing a thesis claim as a *prediction* on data the models have never seen —
is still unmet, and the repo still has no confirmatory out-of-sample result.

The reservation layer permits a second attempt with one structural advantage Arm 2 could
never have. Arm 2's "unseen" data existed upstream throughout and could be revised
underneath the pre-registration, which is precisely how ADR 0038 killed it. The outcomes
this ADR predicts **do not exist yet in realised form anywhere**: they are Awara stay
nights after the panel's 2026-07-08 pull, whose final occupancy is determined by bookings
that have not been taken. The firewall holds by construction rather than by discipline.

The companion analysis (`awara_oos_findings.md`) is **exploratory** and this ADR does not
launder it. It is exploratory for two reasons stated there: aggregate statistics over the
whole realised sample were computed before any model was specified, and the specification
frozen below (M3) was selected after seeing holdout performance. The holdout's role here
is model selection. This document is the confirmation.

### Relation to Arm 2's firewall

ADR 0020's seen/unseen declaration names the mobile-location municipal panel, the
FTAS/merged survey, and the JTA accommodation panel. The locality reservation panel used
here is not named in either set and sits in the non-survey layer governed by ADR 0027, so
this analysis does not touch Arm 2's firewall. Awara (18208) is a confirmatory
municipality in ADR 0020's transient set and appears in its vintage guard; that guard
concerns the mobile panel, not reservations. Confirm against ADR 0027 before acceptance.

### The seen/unseen boundary (declared now, verbatim)

**Seen.** Awara stay nights **2023-10-01 through 2026-07-08** in
`data/nonsurvey/booking_curve_awara.parquet` and `data/nonsurvey/panel_area_daily.parquet`,
as committed, panel generated 2026-07-09 from upstream sources pinned 2026-07-08 per
`data/nonsurvey/coverage_report.md`. All 1,012 realised nights are seen, in aggregate and
individually.

**Unseen (the test set).** Awara stay nights **2026-07-09 onward**, with realised final
occupancy, from a fresh pull of `booking_curve.csv` in the upstream reservation source
`code4fukui/fukui-kanko-reservation` (head `f58e4d8fdc34` recorded at the seen-vintage
fetch; head is `d30a3f079cbb` as of 2026-09-13, so an unseen window of ≈67 nights is
already available).

**Explicitly excluded from the unseen set:** the **90 post-pull nights** already present in
the committed booking curve (the corresponding figure for `panel_area_daily` is 455 rows
across five areas). For stay nights after 2026-07-08 the upstream curve forward-fills the
on-hand count to every horizon — October 2026 nights carry an identical value at `ago_0` through
`ago_60` — and `rsv_occ_proxy` on those rows is partial booking, not outcome. These rows
are not evidence of anything and must not enter the test at either end. The fresh pull
must supply both the curve and the outcome for every unseen night.

**Firewall.** Fetch and build scaffolding may be developed against the seen vintage.
Unseen outcome values must not be fetched, opened, plotted or summarised until this ADR is
accepted and the frozen script and coefficient table are committed. Unseen pulls land in a
quarantined directory and are touched only by the frozen script.

### Frozen inputs

- **Specification M3**, verbatim: `rsv_occ_proxy ~ C(dow) + C(is_hol) + C(eve_hol) +
  trend + occ_lag364 + l_ago30 + l_ago60 + l_ago90 + pickup_60_30 + pickup_90_60`.
- **Coefficients frozen** as fitted on all 644 eligible seen nights ≤ 2026-07-08
  (R² = 0.811), committed in `awara_frozen_model_coefficients.csv`. **No refitting on any
  post-2026-07-08 data.** Refitting would absorb exactly the prospective accuracy the test
  measures — the same error ADR 0020 guards against for SCM donor weights.
- **Benchmark M0**, verbatim: predicted occupancy = realised occupancy 364 days earlier.
  No parameters, nothing to freeze.
- **Horizon 30 days.** No `ago_N` with N < 30 enters any prediction, asserted in code.
- **Flag threshold 60% occupancy**, as used in the seen-window analysis.

## Decision

One primary and one co-primary, both directional, sidedness declared here ex ante. The
headline verdict "prediction confirmed" requires **both**; one alone is partial support and
is never reported as confirmation. Minimum **60 unseen nights** with complete 30/60/90-day
state and realised occupancy; below that the test waits.

### P1 — booking state beats the naive seasonal rule (primary)

- On unseen nights, compute absolute errors of frozen M3 and of M0.
- **Prediction:** mean absolute error of M3 < mean absolute error of M0.
- **Inference:** paired one-sided Wilcoxon signed-rank on absolute errors, α = 0.05.
- **Confirmed:** MAE(M3) < MAE(M0) and p ≤ 0.05. **Directional-only:** MAE(M3) < MAE(M0),
  p > 0.05. **Falsified:** MAE(M3) ≥ MAE(M0).
- The seen-window margin was thin — 7.93 → 7.00 pp, +0.28 pp at the median, p = 0.034,
  with serially correlated errors left uncorrected. This prediction can fail, and its
  ability to fail is the point. The seen-window magnitude is **not** the bar; sign and
  significance are.

### P2 — soft nights are identifiable seven weeks out (co-primary)

- Flag each unseen night where frozen M3 predicts occupancy < 60%. Compare against
  realised sub-60% status.
- **Prediction:** flag precision exceeds the unseen-window base rate of sub-60% nights
  (i.e. the flag beats flagging everything).
- **Inference:** one-sided exact binomial against the unseen base rate, α = 0.05.
- **Confirmed:** p ≤ 0.05. **Directional-only:** precision > base rate, p > 0.05.
  **Falsified:** precision ≤ base rate.
- Recall is reported alongside but gates nothing: the seen window showed M3 trading
  precision (0.901 → 0.817) for recall (0.873 → 0.975) against M0, and the correct
  operating point depends on an intervention-cost parameter the thesis does not have.

### Secondary predictions (reported, never headline)

- **S1 — no accuracy collapse:** frozen M3's unseen MAE ≤ 9.0 pp, against 7.00 pp in the
  holdout. A larger value indicates the frozen coefficients do not transport and is
  reported as such, whatever P1 does.
- **S2 — the decisive seen-window comparison replicates:** calendar-plus-state beats
  calendar-only on unseen nights (seen: 9.03 vs 11.64 pp, p = 2e-12). This is the one
  comparison that was unambiguous; failure to replicate it would indicate a regime change
  rather than a modelling problem.
- **S3 — the demand gap persists:** the peak-versus-midweek occupancy gap in the unseen
  window remains ≥ 15 pp (seen value 21.4 pp). Erosion below that would mean the midweek
  problem the yield chapter is built on is resolving itself, which feeds the framing of
  that chapter but gates nothing here.

### Vintage-revision guard

Reservation systems restate. Before any unseen-window computation, verify the fresh pull's
**2023-10-01 – 2026-07-08** Awara series against the committed panel. If root-mean-square
relative revision of `rsv_occ_proxy` exceeds **2%**, or any single seen night's occupancy
differs by more than **1 percentage point**, stop; log a deviation ADR deciding between
(a) re-running the entire Awara chain — yield analysis, holdout and this test — on the
revised vintage as the single canonical series, or (b) demoting this test to exploratory.
Mixing vintages within one analysis is forbidden. This is ADR 0038's failure mode and it
is the most likely way this test dies.

### Provenance preconditions

Resolved 2026-09-14 by recovering the builder from the fedora host; see
`provenance_addendum.md`. The curve is produced by `~/panel_build_work/build_panel.py`,
which **fetches `booking_curve.csv` from `code4fukui/fukui-kanko-reservation` and passes
`ago_*` through unchanged** — the column semantics are an upstream definition. Three fixes
are preconditions for reporting this test as confirmatory. If it executes without them it is
reported as exploratory regardless of outcome — the same demotion ADR 0039 applied for a
lesser defect.

1. **Commit the builder and pin the source — done.** The builder is committed as
   `scripts/build_panel.py` (recovered from `~/panel_build_work/build_panel.py` on the
   fedora host, where it had never been committed). `fetch()` no longer requests a branch
   tip: it resolves a per-repository commit from a `PINS` dict and **raises** on an
   unpinned repository, so an unreproducible fetch is now an error rather than a silent
   default. A deliberate re-vintage goes through `PANEL_PINS` and logs itself in the
   manifest. `booking_curve.csv`, `latest_rsv_sum.csv` and `latest_hotel.csv` are added to
   `config/official_fukui_sources.yaml` with commit and checksum at the pull below.
2. **Fix the transposed municipal codes — done.** `awara_onsen` now carries
   `muni_jis = 18208` (= あわら市 Awara) and `tojinbo` now carries `18210` (= 坂井市
   Sakai), verified against `data/causal/fukui_municipalities_scm.csv`. No committed
   estimate changes: capacity is keyed on the upstream repo name and no committed script
   joins on `muni_jis`. The reason it mattered is that ADR 0020's regime sets are keyed by
   JIS code and place these two municipalities in **opposite** classes. The panels carry
   the old codes until they are rebuilt; the rebuild is deferred because rebuilding now
   would move the seen vintage underneath this test.
3. **Flag the post-pull rows — deferred, and handled in code instead.** The booking curve
   carries no `coverage_flag`; on `panel_area_daily` the flag reads `ok` for all 455
   post-pull rows (the curve's own post-pull count is 90). Rather than rebuild the panel
   before this test, `awara_forward_test.py` excludes forward-filled nights directly, by
   the rule in the amendments below. The panel flag remains to be fixed on the next
   rebuild.
4. **Unresolved and recorded, not fixed:** `echizen_coast` carries `muni_jis = 18423`
   (越前町 Echizen *Town*, correct for the coast) but `trend_muni = "越前市"` (Echizen
   *City*), so its Google-trends covariate is drawn for a different municipality. Outside
   this test's scope; changing it would alter panel data for an area under no current
   analysis. Flagged for whoever next touches `trend_directions`.

### Amendments made before the pull (2026-09-14)

Three quantities the draft left implicit are frozen here. All three were fixed before any
unseen night was fetched, and each is a constant in the committed script.

- **Capacity denominator frozen at 576 rooms.** `rsv_occ_proxy` divides by
  `hotel_capacity_rooms`, which the builder computes as a *moving* sum of `nrooms` over
  upstream `latest_hotel.csv`. Recomputing it from a fresh pull would rescale the outcome
  and silently invalidate the frozen coefficients — a hotel opening or closing would read
  as an occupancy shift. The fresh capacity value is recorded for the provenance record and
  not used.
- **Trend origin frozen at 2023-10-01**, the first night of the seen panel, so that `trend`
  in the frozen specification means the same thing at evaluation as it did at fitting.
- **Eligibility rule for unseen nights.** A night enters the test only if it falls after
  2026-07-08, strictly precedes the pull date, has complete 30/60/90-day state and a
  realised occupancy, and its booking curve is **not flat across horizons**. The flatness
  test is what excludes the upstream forward-fill: a night whose on-hand count is identical
  at every horizon is a booking snapshot, not an outcome.

One further gap is closed for completeness: **S2's calendar-only comparator (M1) had never
been frozen.** It is fitted on the 644 eligible seen nights only — no unseen data enters —
and frozen as `data/frozen/awara_frozen_m1_coefficients.csv` before the pull. The committed
M3 table was reproduced from the seen window as a check before being relied on, matching to
9.7e-17 at n = 644 and R² = 0.8108.

### Interpretation contract (written before the result exists)

- **Both confirmed:** reservation-curve state has demonstrated prospective forecast value
  beyond a naive seasonal benchmark at a 30-day horizon, and soft nights are identifiable
  seven weeks ahead with quantified precision and recall. The yield chapter's
  intervention-horizon claim gains predictive rather than merely descriptive weight, and
  the thesis acquires the confirmatory out-of-sample result Arm 2 was meant to supply.
- **Directional-only:** reported as consistent but underpowered. No promotion. The naive
  rule stands as the operational recommendation, being simpler and statistically
  indistinguishable — and that recommendation is itself a defensible finding.
- **P1 falsified:** a first-class result, not a setback. The honest claim becomes "at a
  30-day horizon, a one-line seasonal rule is not improved upon by reservation-curve
  state", which is a substantive negative finding about the marginal value of booking data
  and directly relevant to any DMO considering acquiring it. The yield findings are
  unaffected: they never depended on occupancy being forecastable.
- **P2 falsified with P1 confirmed:** accuracy gains do not convert into a usable
  operational rule. Reported as such; the intervention-horizon framing is withdrawn.
- No outcome licenses re-opening the holdout, re-specifying M3, or re-selecting the
  horizon or flag threshold. Post-hoc reconciliation is exploratory by definition.

### Execution routing

Fresh pull → quarantined directory. Guard check (vintage) → frozen script → single
evaluation → result recorded in a new ADR. One execution. If the script errors in a way
that requires a specification change, the change is logged in a new ADR and demotes this
test to exploratory.

### Standing prohibitions restated

- Arm 2 and Arm 3 stay closed. This is a new test on a different data layer, not a
  re-opening of either, and nothing here licenses re-running them on a later vintage.
- The PBL vignette numbers (ADR 0026 §2) enter no quantity in this document, including any
  effect-size or power calculation.
