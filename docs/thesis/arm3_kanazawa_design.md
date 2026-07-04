# Arm 3 design: Kanazawa 2015 template replication

**Status: design specification, not evidence. No result reported anywhere in
the thesis derives from executing it.** This document fixes, before any
analysis is run, what the Direction D pipeline template is, which of its
components transfer verbatim to the March 2015 Nagano–Kanazawa Hokuriku
Shinkansen extension, which are allowed to differ and why, the success
criteria, and the interpretation contract. Decision provenance: ADR 0021.
Data-availability facts are taken from the Codex audit
(`docs/arm3_kanazawa_data_audit.md`, checked 2026-07-03); every coverage claim
below cites that audit rather than asserting it fresh.

Arm 3 is a **replication/validation**, not a prospective prediction test. The
qualitative outcome — a large, sustained Kanazawa tourism boom after
2015-03-14 — is public knowledge. What is at stake is the ADR 0017 claim that
the *template* (fit-gated SCM, effect-shape-matched event window,
falsification battery, decay/anchor geography) is the exportable object:
whether the same frozen machinery, pointed at a different extension with its
constants declared ex ante, recovers and disciplines that known story. The
genuine out-of-sample test of the thesis's predictions is Arm 2 (ADR 0020);
Arm 3 must never be described with Arm 2's language.

## 1. The object under test

ADR 0017's contribution sentence names the template, subordinated to the
empirical claim; ADR 0019 adopts Arm 3 as the secondary arm ("publication
spine") that "validates the claim that the *template* is the exportable
object," covering "the SCM/decay/anchor-geography portions of the template
only." The template, as committed, consists of:

1. **Outcome construction** — log-transformed monthly panel; gap/relative
   inference only, never absolute levels
   (`scripts/build_causal_arm_summary.py`, thesis §5.1).
2. **Estimator** — Abadie convex-weight synthetic control fit by the
   deterministic Frank–Wolfe solver `fw_scm_sparse`, weights fit on pre-event
   months only, no randomness (`scripts/build_causal_arm_summary.py`).
3. **Fit gates** — `good_fit`: pre-period RMSPE ≤ 0.15 log units
   (`GOOD_FIT_RMSPE`); placebo restriction: drop placebos with pre-RMSPE
   > 5.0× the treated unit's (`RMSPE_FIT_MULT`).
4. **Effect-shape discipline** — the confirmatory statistic is the **opening
   window** (first two post-event months) gap, because a transient surge is
   averaged away by post-mean statistics (thesis §5.2); post-mean gap
   disclosed alongside.
5. **Falsification battery** (`scripts/causal_robustness.py`):
   (a) in-space placebo — every donor fit as-if-treated, one-sided p on the
   opening-window gap with the two-sided value disclosed;
   (b) backdated in-time placebo at event − 12 months, expected silent;
   (c) leave-one-out refits dropping each positive-weight donor.
6. **Decay/regime layer** — gap-trajectory shape after the surge: transient
   by default, durable where arrivals convert to destination anchors
   (regime map, thesis §4.1/§5.5).

Randomization p-value formula, verbatim from the committed scripts:
p = (1 + #{placebos ≥ treated}) / (1 + #placebos kept), one-sided; absolute
values for the two-sided variant.

## 2. Transfer map

### 2.1 Held fixed — transfers verbatim

| Component | Value (source) |
|---|---|
| Estimator | `fw_scm_sparse` Frank–Wolfe convex SCM, deterministic |
| Outcome transform | natural log (values strictly positive at prefecture grain) |
| `GOOD_FIT_RMSPE` | 0.15 log units |
| `RMSPE_FIT_MULT` | 5.0 |
| Opening window | first two post-event months (event month + next) |
| In-time placebo offset | event − 12 months |
| Sidedness | one-sided on the opening surge (directional prediction stated ex ante), two-sided disclosed — the Seam C posture (ADR 0015) |
| Leave-one-out | over positive-weight donors, range of opening surge reported |
| Inference formula | randomization p as above |
| Levels discipline | gap/relative inference only |
| Pre-window length | 38 months, matching Direction D's 2021-01..2024-02 |

A note on the 0.15 gate: prefecture-month overnight series are smoother than
municipal mobile-derived series, so the gate is easier to clear at this grain.
It is retained verbatim because the template's content is that the gates are
*fixed before results are seen*; the binding discipline at this grain is the
5.0× placebo restriction and the placebo comparison itself.

### 2.2 Allowed to differ — declared here, ex ante

| Parameter | Direction D value | Arm 3 value | Reason |
|---|---|---|---|
| `EVENT_YM` | 202403 (opened 2024-03-16) | **201503** (opened 2015-03-14; JRTT, audit §4) | The event under study. Both openings fall mid-March, so the half-treated event month is symmetric. |
| `INTIME_EVENT_YM` | 202303 | **201403** | Mechanical: event − 12. |
| Treated unit(s) | Fukui municipalities (17 units) | **Ishikawa (17) primary; Toyama (16) companion** | Grain is forced to prefecture (audit §§2–3). Ishikawa holds the terminus and the anchor city; Toyama is the pass-through case — the prefecture-grain analog of the durable/transient contrast. |
| Outcome layer | JTTA mobile-derived monthly municipal tourism visitors | **JTA 宿泊旅行統計調査 prefecture-month total overnight stays** (all-establishment series), Japanese/foreign split as secondary heterogeneity | Forced: the mobile layer begins 2021-01 (audit §3, VERIFIED). Overnight stays measure the staying margin rather than all visits; see §7. |
| Donor pool | 1,709 municipalities outside prefectures {15, 16, 17, 18} | **34 prefectures**: all 47 minus treated 17 and excluded {01, 02, 03, 04, 07, 15, 16, 20, 33, 34, 38, 43} (audit §4 verdict) | Co-treatment (new-segment prefectures 15/16/20; Hokkaido Shinkansen 2016-03 → 01, 02) and severe in-window disasters (2011 Tōhoku → 02/03/04/07; 2016 Kumamoto → 43; 2018 floods → 33/34/38). |
| Pre-period | 2021-01..2024-02 (38 months) | **2012-01..2015-02 (38 months)**; sensitivity: 2011-01..2015-02 (49 months) | 2011-01 is the earliest consistent post-frame-break month (audit §1 verdict), but 2011-03 (Great East Japan Earthquake) sits inside a 49-month window; the primary fit window starts after the shock year and matches the template's 38-month length. |
| Post-period | 2024-03..2025-12 (22 months) | **2015-03..2019-12 (58 months), confirmatory window ends 2019-12** | COVID (2020-01 onward) is a global shock that invalidates donor comparability; 2024-03 re-treats the corridor (Tsuruga extension). A descriptive appendix figure may extend the trajectory through 2024 using already-seen JTA vintages, clearly marked non-confirmatory. |
| Anchor candidates | Eiheiji (18322), Sakai (18210) vs Fukui City (18201) | **Kanazawa city lodging + Kenrokuen / 19-facility monthly series (descriptive only)** vs Toyama prefecture trajectory | Audit §2: Kanazawa monthly city-level lodging from 2014 and monthly point series (incl. 兼六園) exist in city-report PDFs; no balanced municipal panel exists, so anchors are descriptive, not SCM units. |

### 2.3 New components, required by the longer post window

Direction D never had to test *persistence* formally — its post window was 22
months. Arm 3's durability content needs one addition, declared here:

- **Late window** := 2018-01..2019-12 (the final 24 confirmatory post
  months, ~3–4.8 years after opening).
- **Late-window persistence statistic**: mean treated-minus-synthetic gap
  over the late window, tested against the in-space placebo null of
  late-window mean gaps (same donor pool, same fit-gate restriction,
  one-sided: persistence is the directional claim for the anchor prefecture).
- **Decay ratio** R := (late-window mean gap) / (first-12-post-months mean
  gap), reported descriptively per treated unit. R is a ratio of noisy
  quantities and gets no p-value; the confirmatory persistence inference is
  the placebo test above.

## 3. Data

- **Primary panel**: the pinned `推移表` workbook
  (`output/national_stats/raw/jta_accommodation_timeseries.xlsx`, config key
  `jta_accommodation_timeseries`). Audit §1 (VERIFIED, metadata-only):
  monthly 47-prefecture total/Japanese/foreign overnight stays, 2011-01
  through 2025-12, all-establishment series; the separate 従業者数10人以上
  sheets beginning 2007 are a different estimand and are never spliced in.
- **Load-time slice guard**: the workbook contains months after the Arm 3
  window, including rows that are *unseen* under ADR 0020 (JTA 2025
  confirmed values). The Arm 3 loader must slice to ym ≤ 201912 before any
  value is read into analysis, with a test asserting the boundary. No Arm 3
  artifact may surface any workbook value after 2019-12 except the
  descriptive appendix extension, which is restricted to vintages already
  declared seen in ADR 0020 (2018–2024 confirmed + 2025 preliminary annuals,
  already in `output/national_stats/raw/`) and never the 推移表's
  post-2024 columns.
- **Vintage/correction rule**: JTA corrected 2013 tables for, among others,
  Ishikawa and the Hokuriku block (audit §1). The canonical series is the
  single current 推移表 vintage, sha256-pinned in
  `config/national_data_sources.yaml` at fetch time. Cross-check oracle:
  for the treated units and every positive-weight donor, the 推移表 monthly
  values for 2012–2016 must match the corrected annual confirmed-value
  releases (audit §1 table lists the 2011–2017 URLs); any mismatch stops the
  run. Mixing vintages within one analysis is forbidden (mirrors ADR 0020's
  guard).
- **Descriptive anchor sources** (audit §2): Kanazawa City tourism survey
  PDFs — monthly lodging guests (persons, 2014–2019) and monthly counts for
  19 principal facilities including 兼六園 (2014/2015–2019). PDF-derived,
  point-utilization units, facility-set changes must be checked; labeled
  descriptive throughout. Extraction goes to Codex with a page-cited
  provenance manifest.

## 4. Specification summary

| Constant | Value |
|---|---|
| `EVENT_YM` | 201503 |
| `INTIME_EVENT_YM` | 201403 |
| Pre-window (primary) | 2012-01..2015-02 (38 months) |
| Pre-window (sensitivity) | 2011-01..2015-02 (49 months) |
| Confirmatory post-window | 2015-03..2019-12 (58 months) |
| Opening window | 2015-03..2015-04 |
| Late window | 2018-01..2019-12 |
| Treated | Ishikawa 17 (primary), Toyama 16 (companion) |
| Donor pool (primary) | 34 prefectures (audit §4 main rule) |
| Donor pool (strict sensitivity) | 20 prefectures (also dropping the 14 flagged codes {05, 06, 08, 12, 21, 26, 27, 28, 29, 31, 32, 35, 39, 44}) |
| `GOOD_FIT_RMSPE` / `RMSPE_FIT_MULT` | 0.15 / 5.0 (verbatim) |

Both treated units use the identical donor pool (each is already excluded
from it), so the Ishikawa and Toyama runs differ only in the treated series.

**Attainable-significance floor.** With 34 donors the minimum one-sided
randomization p is 1/35 ≈ 0.029; in the strict 20-donor pool it is
1/21 ≈ 0.048. The fit-gate restriction can only shrink the kept-placebo
count. Rule, fixed now: if fewer than 19 placebos survive the 5.0× gate for
a given treated unit, p ≤ 0.05 is arithmetically unattainable and that
test's outcome band is capped at **directional-only** — reported as a
granularity limit of the design, not as evidence against the effect.

## 5. Falsification battery (verbatim transfer)

Run for each treated unit, on the primary spec:

1. **In-space placebo, opening window** — every donor fit as-if-treated at
   201503; null = opening-window gaps of placebos within the 5.0× fit gate;
   one-sided p reported with two-sided disclosed.
2. **In-space placebo, late window** — same machinery, statistic = late-window
   mean gap (the §2.3 addition).
3. **Backdated in-time placebo** — full design re-run at 201403 using only
   genuinely pre-event data (fit window 2012-01..2014-02); the backdated
   opening window 2014-03..04 must be silent.
4. **Leave-one-out** — drop each positive-weight donor, refit, report the
   opening-surge range and the late-window mean-gap range.

Sensitivities (reported, never headline): 49-month pre-window; strict
20-donor pool; masking 2018-06..09 (Osaka quake / West-Japan floods months
in donors kept by the main rule) and 2019-10..12 (Typhoon Hagibis, to be
date-verified by Codex during implementation — it postdates the audit's
event table) from the late window; foreign-only and Japanese-only outcome
splits.

## 6. Success criteria and interpretation contract

Labels are fixed here and used verbatim in code, tests, and any later prose.

**Tier V1 — pipeline validation (all three required to claim "the template
transfers"):**

- **V1a** Ishikawa opening-window gap > 0 with one-sided in-space placebo
  p ≤ 0.05 (subject to the §4 floor rule).
- **V1b** Backdated placebo silent: Ishikawa backdated opening gap one-sided
  p > 0.10.
- **V1c** Leave-one-out opening-surge range for Ishikawa bounded away from
  zero (minimum of the range > 0).

**Tier V2 — durability geography (the ADR 0017 durable-where-anchored
clause at prefecture grain):**

- **V2a** Ishikawa late-window mean gap > 0 with one-sided placebo p ≤ 0.05
  (same floor rule).
- **V2b** Directional contrast: R_Ishikawa > R_Toyama and Ishikawa
  late-window mean gap > Toyama late-window mean gap. Descriptive
  (sign-level), no p-value.

**Tier V3 — anchor evidence (descriptive only, never confirmatory):**

- **V3** Kanazawa monthly lodging and Kenrokuen/19-facility series show the
  surge and its persistence concentrated at the anchor city, on the
  2014–2019 windows the PDFs support.

**Interpretation contract (written before any result exists):**

- **V1 pass + V2 pass** — the template is validated on a second extension at
  prefecture grain: the exportable-object claim (ADR 0017 §3) gains the
  Kanazawa leg, and the journal manuscript (ADR 0019 Phase 2) carries Arm 3
  as its replication section. No thesis-chapter language about 2024 changes.
- **V1 pass + V2 fail** (Ishikawa decays like Toyama, or persistence is
  directional-only) — the surge machinery replicates but the
  anchor-durability account does not generalize to 2015 at this grain.
  First-class result: the template claim is bounded to the surge/falsification
  portions, and the durable-where-anchored clause stays supported only by the
  2024 municipal evidence (and Arm 2's verdict, whichever lands). Reported
  without softening.
- **V1 fail** — the pipeline fails to recover a publicly known boom. Before
  any interpretation, the pre-declared suspects are checked in order:
  aggregation dilution (Kanazawa's surge diluted across Ishikawa, including
  Noto), the placebo floor, and donor-pool contamination. If none explains
  it, the honest conclusion is that the template's portability is not
  demonstrated at prefecture grain — which bounds the ADR 0017 template
  claim and is reported as such. A V1 failure does not touch the 2024
  Fukui results; they rest on their own committed battery.
- **Directional-only outcomes** (signs right, p above threshold or floor-
  capped): consistent-but-underpowered at this granularity; no promotion of
  any claim.
- No outcome licenses re-opening the Direction D analyses, and no Arm 3
  result may be described as a prediction test (that is Arm 2's word).

## 7. Honest limits — what the Kanazawa test does not cover

Stated here so no later text oversells the replication:

1. **No mobile-panel layer for 2015.** VERIFIED (audit §3): the JTTA
   smartphone-derived municipal series begins 2021-01; no provider offers a
   pre-2021 municipal panel. The 2024 template's municipal grain — 1,709
   donors, municipality-level regime map — does not transfer. Arm 3 tests
   the SCM/opening-surge/decay portions at prefecture grain plus descriptive
   anchor geography, exactly as ADR 0019 anticipated.
2. **No friction layer for 2015.** There is no FTAS-analog respondent-level
   survey for 2015, so the friction→durability association — the diagnostic
   heart of the template (§4, Direction C, Arm 2's P2) — is untestable at
   Kanazawa. Arm 3 validates the causal-demand and durability-shape
   machinery, not the diagnosis.
3. **Different outcome margin.** Overnight stays (including business travel)
   versus mobile-derived tourism visits. The Japanese/foreign split
   sensitivity partially isolates the tourism-driven component; the
   business-travel share difference between Ishikawa and Toyama is a named
   caveat on V2b.
4. **The result is publicly known.** Arm 3's evidentiary value is
   template-mechanical (frozen gates, declared windows, falsification
   behavior), not novelty. Pre-declaring the spec forecloses
   garden-of-forking-paths, not hindsight.
5. **Descriptive anchors are point-utilization counts** from PDFs with a
   2014 floor — one year of pre-event coverage — and possible facility-set
   changes; they can illustrate, never establish, the anchor mechanism.

## 8. Kill-criterion resolution

ADR 0019: "Arm 3 is killed if the data-availability audit shows the
pre-period cannot support the fit gates." Audit §1 verdict (VERIFIED): the
earliest clean start for a consistent 47-prefecture monthly panel is
2011-01, and the full 2011-01..2015-02 span is covered for total, Japanese,
and foreign stays on a single post-expansion design. The primary 38-month
pre-window sits entirely inside it. **The kill criterion is not triggered;
Arm 3 proceeds as specified.** Scope reduction relative to the most
ambitious reading — no municipal SCM — is already reflected in §2.2/§7 and
was anticipated by ADR 0019's "SCM/decay/anchor-geography portions only."

## 9. Execution routing

- **Codex** (per ADR 0019 seat routing), against this document as the
  oracle: fetch and sha256-pin the 2011–2017 confirmed annuals (audit §1
  URLs) for the cross-check oracle; build the prefecture panel loader with
  the ≤ 201912 slice guard; port the SCM/robustness scripts with tests
  asserting the §4 constants verbatim, the window boundaries, the donor
  exclusion lists, the cross-check oracle, and that weights are fit only on
  the declared pre-window; extract the Kanazawa PDF tables with page-cited
  provenance; run the battery; emit CSVs + metrics.json + figures mirroring
  the Direction D output layout.
- **Mid-tier seat, later**: interpretation memo against §6's contract.
- **Human**: reviews and commits this spec + ADR 0021 before any Arm 3
  computation; commits results separately.
- Any deviation from this document after acceptance is a new ADR and
  demotes the affected analysis to exploratory (the ADR 0018/0020
  discipline, applied here).
