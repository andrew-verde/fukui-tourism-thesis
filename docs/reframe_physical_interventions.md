# Reframing the thesis around physical interventions

*Design document for a thesis narrative based on SEM and non-survey behavioral evidence.*

Generated 2026-07-09. Companion artifacts: `source_inventory.md`, `panel_design.md`, `panel_site_daily.parquet`, `panel_area_daily.parquet`, `opportunity_signals.json`, `intervention_opportunity_analysis.md`, `sem_nonsurvey_spec.md`.

---

## 1. The question

> **Previous thesis question:** *Does a survey-measured nudge change stated intentions?*
> **Revised thesis question:** *Where in Hokuriku's tourism system might a physical intervention change observed behavior, and what effect would it need to have to matter, according to a structural model fit to non-survey behavioral data?*

The survey remains one indicator block in a structural equation model. Other
blocks use AI-camera footfall, license-plate origin, lodging reservations,
digital-intent signals, weather, and official statistics. The contribution is
the analysis that identifies candidate physical changes for a site partner and
bounds the effect each would need to have.

The available data can support this analysis now. A field trial requires a site
partner and remains a pre-registered next step.

## 2. What this change requires

The revised scope requires support for three claims:

1. **Surveys and behavioral measures answer different questions.** A survey
   measures stated intention. A camera can measure whether people disperse.
   The non-survey panel therefore measures behavior that a questionnaire
   cannot.
2. **SEM links the measures.** It relates latent constructs such as physical
   friction, realized demand, and visit intention to several noisy indicators.
   The existing two-stage FTAS SEM can incorporate behavioral indicators.
3. **Physical interventions require a separate test.** Signage, wayfinding,
   parking and shuttle infrastructure, timed entry, and midweek programming
   change choices in physical space. A site partner is needed to test them,
   but the current analysis can identify and prioritize candidate tests and
   bound the effects they would need to have.

## 3. Existing work

The `fukui-tourism-thesis` repository already contains the analysis used here:

| Existing asset | Role in the reframed thesis |
|---|---|
| Two-stage FTAS SEM (`scripts/sem_ftas.py` → `output/sem/`) | The structural model. It is extended with non-survey indicator blocks. See `sem_nonsurvey_spec.md`. |
| Evidence-weighted nudge ranking (`scripts/rank_nudge_priorities.py`, `config/nudge_mapping.yaml`) | The prioritization method. It can use observed behavioral signals as well as survey weights. |
| Hokuriku Shinkansen DiD / event study (`scripts/hokuriku_did_event_study.py`) | The causal design for the March 2024 extension. The new panel does not duplicate it. See §6. |
| Fukui City synthetic control (`scripts/synthetic_control_fukui.py`) + SCM robustness | Municipality-level counterfactual for demand shifts. |
| Unfielded nudge-pilot app (`experiments/nudge-pilot/`) + power calculation (`scripts/nudge_pilot_power.py`) | The Arm 2/3 pre-registered field trial, which remains future work. |

The revised narrative centers physical interventions and adds non-survey
evidence. It retains the survey and causal designs.

## 4. Non-survey evidence

A unified non-survey panel uses public data. `panel_design.md` and
`coverage_report.md` document its construction and checks.

- **`panel_site_daily`:** 2,245 rows from 4 AI-camera sites, dated 2024-12-20
  to 2026-07-08. It includes footfall (Person), demographics (Face), and
  origin and vehicle mix (LicensePlate).
- **`panel_area_daily`:** 4,523 rows from 5 lodging markets, dated 2023-10-01
  to 2026-10-08. It includes reservations, an occupancy proxy, an ADR proxy,
  GBP digital-intent, and booking lead time.
- **Provenance:** 7 Code4Fukui repositories are pinned by commit SHA, with a
  SHA256 hash for each file.

`opportunity_signals.json` records five observed patterns and one negative
result from the panel. `intervention_opportunity_analysis.md` gives the
details. The main signals are:

- **Tojinbo footfall is concentrated on peak days.** The 95th-percentile day
  is 2.2 times the median, and weekend footfall is 1.7 times weekday
  footfall. This indicates an opportunity to disperse visits over time.
- **Rainbow Line visitors mainly arrive by car.** Between 66% and 70% of
  vehicles come from outside the prefecture, led by Aichi. Parking and
  shuttle infrastructure are therefore the relevant intervention class.
- **Awara and the Echizen coast have weekend to weekday occupancy gaps of
  about 18 percentage points.** Saturation is rare, with fewer than 1.2% of
  days at or above 90% occupancy. The analysis points to demand distribution
  rather than capacity as the constraint.
- **GBP "directions" requests co-move with realized stays.** The same-week
  correlation is r = 0.59. This provides a measurable intent-to-demand
  channel for the SEM.

## 5. Revised thesis structure

1. **Chapter framing.** The thesis opens with physical sites, observable
   flows, and the question of where a physical change may matter.
2. **Evidence.** The non-survey panel and extended SEM combine sensor,
   reservation, intent, and official data into latent constructs.
3. **Identification.** The existing DiD and synthetic-control analyses of the
   Shinkansen extension provide the causal estimate of a system-level demand
   shift.
4. **Opportunity mapping.** The SEM and panel score site and market
   opportunities in `intervention_opportunity_analysis.md`.
5. **Effect bounds and simulation.** The webapp asks how a specified change
   in friction indicator X would propagate to realized demand according to the
   SEM. Its output is a scenario, not an estimated intervention effect.
6. **Pre-registered trial.** The nudge-pilot app and power calculation specify
   the future Arm 2/3 trial and its detectable effect size.

## 6. Scope boundary

The data cannot establish that a particular physical change will produce a
particular behavioral effect. This document makes no such claim. Two rules
keep the boundary clear:

- **The Shinkansen panel does not estimate general intervention effects.** The
  reservation panels begin in October 2023. Their pre-extension period has no
  seasonal overlap with the post-extension period, so a simple pre/post
  comparison would be confounded by season and is discarded. See
  `opportunity_signals.json` (`S5_shinkansen_NOT_identifiable_here`). The
  existing DiD and synthetic-control scripts use the repository's multi-year
  arrivals and accommodation series for the natural-experiment estimate.
- **The webapp labels simulated effects as elasticities or scenarios.** When it
  propagates a hypothetical δ through SEM coefficients, at least one path is
  anchored to an observed elasticity, such as the intent-to-demand coupling or
  a Shinkansen-identified demand shift. The app labels every result as a
  scenario pending field validation.

The thesis identifies and prioritizes locations for physical-intervention
trials and bounds the effects those trials would need to have. It does not
claim that a trial has succeeded.

## 7. Repository work

The implemented artifacts are the panel builder under `scripts/`/`data/`, the non-survey indicator mapping in `config/` plus sibling `scripts/sem_nonsurvey.py`, the opportunity scan, and the simulation webapp under `experiments/`. ADR 0027 records the §6 scope boundary.
