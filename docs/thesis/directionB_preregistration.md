# Direction B pre-registration: station→anchor last-mile nudge pilot

**Status: pre-registered design. This document is a plan, not evidence. No
result reported anywhere in the thesis derives from executing it, and nothing
in it should be read as an effect estimate.** It freezes, before any data
collection, the hypotheses, sampling plan, decision rules, and analysis of
the two-stage pilot specified in `experiments/nudge-pilot/DESIGN.md`
(design approved 2026-07-02). Where this document and DESIGN.md differ, this
document governs. Decision provenance: ADR 0018. Once fielding begins, this
file is frozen; any deviation is logged in a new ADR and the affected
analysis labeled exploratory.

## 1. Background and hypotheses

The diagnosis (thesis §4) identifies transport-access friction as the binding
constraint on converting rail arrivals into anchor visits: shinkansen
arrivers report it at 7.09% versus 0.66% for car arrivers, and it is the
largest SEM Stage-2 damage path to satisfaction (β ≈ −0.123, p ≈ 1.2 × 10⁻⁸).
The durability analysis (Direction C) implies the intervention target is
**first-visit station→anchor conversion**, not repeat visitation. The pilot
tests whether supplying concrete last-mile information (route, frequency,
transfer, last-return time) moves intention on exactly that conversion.

- **H1 (primary, confirmatory in Stage 2 only):** the `transport_access`
  nudge increases the visit-intention composite on the anchor tasks relative
  to `control`. Directional hypothesis; tested two-sided (§6) — the
  two-sided test is retained deliberately as the stricter standard, and
  because an information nudge, unlike a rail line, has a plausible backfire
  channel (salience of friction).
- **H2 (mediation):** the H1 effect is transmitted through the
  perceived-friction composite — the pilot analogue of the SEM
  friction→satisfaction path.
- **H3–H5 (secondary):** effects of `opening_hours_availability`,
  `itinerary_fit_time_cost`, and `combined` versus `control` on the primary
  endpoint; effects of the primary contrast on planning confidence and
  decision commitment.

## 2. Design (frozen from DESIGN.md)

Between-subjects information experiment, browser instrument at
`experiments/nudge-pilot/`. Five conditions with unchanged IDs: `control`,
`transport_access`, `opening_hours_availability`, `itinerary_fit_time_cost`,
`combined`. **The primary contrast is `control` vs `transport_access`; all
other contrasts are secondary.** Each participant completes two of three
station→anchor tasks (`eiheiji_half_day`, `tojinbo_awara`,
`museum_arrival`), the six ordered task pairs counterbalanced
deterministically from the session id. Assignment is stratified block
randomization, blocks of five, strata = `fukui_familiarity` ×
`japan_travel_experience`, positions issued by the server-side counter
(Vercel API + Supabase). **The static/local fallback assignment path is
valid only for dry runs; no observation assigned by the fallback enters a
confirmatory analysis.** Participants never see condition labels (nudge
panel header is neutral). Stimulus transit facts must be verified against
current timetables before fielding; verification is a fielding
precondition, not an analysis step.

## 3. Power anchor: d = 0.25 is a ceiling, not an expectation

The only observed effect-size anchor is the FTAS car-versus-rail
transport-satisfaction gap, d ≈ 0.25 (pooled SD; car 4.31 vs rail 4.11,
SD ≈ 0.74–0.84, n ≈ 8,800 scored). That gap is a **selection contrast
between two self-selected populations** and therefore bounds from above
what an information nudge could close; it is not the effect a nudge should
be expected to produce. Planning against d = 0.25 would be planning against
the theoretical maximum. The honest planning case is a fraction of the
ceiling, and the sample requirement is acutely sensitive to which fraction
(α = 0.05 two-sided, power 0.80, two-sample means;
`scripts/nudge_pilot_power.py` reproduces):

| Assumed true d | n/arm | Primary contrast (2 arms) |
|---:|---:|---:|
| 0.25 (full ceiling) | 252 | 504 |
| 0.20 | 393 | 786 |
| 0.15 | 698 | 1,396 |
| 0.125 (half ceiling) | 1,005 | 2,010 |
| 0.10 (floor) | 1,570 | 3,140 |

Because the true fraction is unknown, the design refuses to commit
confirmatory sample against an unmeasured effect: Stage 1 measures the
prior, Stage 2 is powered from it by a pre-specified rule.

## 4. Stage 1 (online panel — estimation only, never confirmatory)

- **Sample:** n = 50 per arm, N = 250, EN + JP online panel. Fixed n; no
  interim analysis; no early stopping.
- **Status:** with n = 50/arm, the minimal detectable effect is d ≥ 0.56 —
  more than twice the ceiling — so Stage 1 is structurally incapable of
  confirming H1 and is pre-registered as **non-confirmatory: no hypothesis
  test performed in Stage 1 will be reported as a test of H1.**
- **Deliverables (all estimation):** d̂ for the primary contrast with its
  standard error; endpoint SDs; the within-participant task correlation
  (credited in the Stage-2 mixed-model power only at its Stage-1-estimated
  value); construct reliability of the composites; instrument behavior
  (completion, accuracy-item pass rates).

## 5. Stage 2 sizing and decision rules (the irreversible part)

- **Re-power rule (frozen):** `d_plan = max(0.10, d̂ − SE(d̂))` — the Stage-2
  planning effect is the lower 68% bound of the Stage-1 estimate, floored at
  d = 0.10. Stage-2 n/arm is read from the §3 formula at d_plan. Powering on
  the lower bound rather than d̂ is deliberate: the cost asymmetry favors
  over-sampling against an optimistic prior.
- **No-go rule (frozen):** if Stage-1 d̂ ≤ 0 on the primary contrast, Stage 2
  does not proceed under this pre-registration. A wrong-signed prior means
  the mechanism translation (survey friction → manipulable information gap)
  failed at Stage 1's granularity; the correct response is design revision
  (logged in a new ADR), not confirmatory sampling against the floor.
- **Recruitment-mode rule (frozen):** the Stage-2 population is rail
  arrivers — the 7.09% base-rate population — via on-site QR intercept at
  Fukui, Awara-Onsen, and Tsuruga stations. Feasibility is flagged now, not
  after Stage 1: FTAS, an interviewer-run intercept operation, captured
  ~289 rail respondents/month prefecture-wide (~120/month in the corridor);
  at half-ceiling d_plan the primary contrast needs ~2,010 completes ≈ 17
  months of corridor-scale capture, and a passive QR intercept yields less.
  **An intercept-only Stage 2 is therefore not credible below d_plan ≈ 0.21
  (~360/arm ≈ six months).** Rule: if the re-powered requirement exceeds
  360/arm, Stage 2 uses **hybrid recruitment** — main sample from an online
  panel screened for planned/recent Hokuriku rail travel, with the station
  QR intercept nested as an external-validity subsample (target n ≈ 300–500,
  analyzed for direction-consistency, never powered alone). If hybrid
  recruitment proves unavailable, arm reduction to
  `control`/`transport_access`/`combined` applies before any fielding-window
  extension.
- **Stopping (frozen):** Stage 2 is fixed-n at the re-powered size; no
  interim efficacy or futility looks; recruitment stops when the planned n
  per primary arm is reached.

## 6. Analysis plan (frozen)

- **Primary:** mixed model — visit-intention composite ~ condition + strata
  + task, with participant random intercept — over each participant's two
  tasks; the `control` vs `transport_access` contrast tested two-sided at
  α = 0.05. One primary contrast; no multiplicity correction applies to it.
- **Mediation (H2):** condition → perceived-friction composite →
  visit-intention; bootstrap CI on the indirect path.
- **Secondary contrasts:** Holm-corrected within the secondary family.
- **Manipulation check (outcome-neutral):** accuracy item by arm; reported
  regardless of result.
- **Exclusions (frozen):** analysis includes participants who complete both
  assigned tasks and the pre-task strata items; partial completions are
  excluded from the primary model but counted in a CONSORT-style flow.
  Fallback-assigned observations (§2) are excluded from confirmatory
  analysis unconditionally. No exclusions on outcome values or accuracy
  performance (the accuracy item is a check, not a gate).
- **Missing data:** the mixed model uses all completed tasks of included
  participants; no imputation of the primary endpoint.

## 7. What this document does and does not license

It licenses exactly one confirmatory claim, available only after Stage 2
completes as specified: a two-sided test of H1 at α = 0.05 in the
pre-specified model. It does not license reading Stage-1 estimates as
effects, reading the d = 0.25 ceiling as an expected effect, reading the
intercept subsample (hybrid case) as an independent confirmation, or
reading any of Direction C's observational evidence as strengthened by the
existence of this design. If the selection-ceiling assumption itself is
wrong — if the manipulable margin lies outside the car–rail gap — the §3
table mis-prices Stage 2, which is precisely the risk the two-stage
structure and the re-power rule exist to absorb.
