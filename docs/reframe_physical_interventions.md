# Reframing the Thesis Around Physical Interventions

*Design document — how the "zoom out beyond the survey" instruction becomes a defensible thesis narrative anchored to SEM + non-survey behavioral evidence.*

Generated 2026-07-09. Companion artifacts: `source_inventory.md`, `panel_design.md`, `panel_site_daily.parquet`, `panel_area_daily.parquet`, `opportunity_signals.json`, `intervention_opportunity_analysis.md`, `sem_nonsurvey_spec.md`.

---

## 1. The reframe in one sentence

> **Old thesis question:** *Does a survey-measured nudge change stated intentions?*
> **New thesis question:** *Where in Hokuriku's tourism system would a physical intervention most plausibly change observed behavior — and how large would the effect have to be to matter — as identified by a structural model fit to non-survey behavioral data?*

The survey does not disappear. It becomes **one indicator block among many** inside a structural equation model whose other blocks are AI-camera footfall, license-plate origin, lodging reservations, digital-intent signals, weather, and official statistics. The thesis contribution moves from *"I ran a nudge experiment"* to *"I built the evidence engine that tells a site partner which physical change is worth trialing, and bounds the effect it would need to produce."*

This is a stronger contribution, not a weaker one, because it is the part that is **already defensible today** with data in hand, while the field trial (the part that needs a site partnership and cannot be completed now) becomes a *pre-registered next step* rather than a missing result.

## 2. Why this is the right move (and what the advisor is actually asking)

The advisor's instruction — zoom out on "nudge" and "SEM" opportunities *across the board*, including ones that require partnering with sites for physical changes, rather than pursuing the survey route — decomposes into three claims the thesis must now support:

1. **Nudge opportunities are not confined to what a survey can measure.** A survey measures stated intention. A camera measures whether people actually dispersed. The behavioral-economics literature on nudges (choice architecture, salience, defaults, friction) is fundamentally about *observed* behavior change; the non-survey panel is a better instrument for it than a questionnaire.
2. **SEM is the unifying method, not a survey-analysis tool.** SEM's value is relating *latent constructs* (physical friction, realized demand, visit intent) to *multiple noisy observed indicators*. The thesis already implements a two-stage FTAS SEM; the reframe feeds it behavioral indicators so the latents are grounded in what people do, not only what they say.
3. **Physical interventions are the high-value, under-explored class.** Signage, wayfinding, parking/shuttle infrastructure, timed entry, midweek programming — these are choice-architecture changes in physical space. They require a site partner and so cannot be A/B tested in a semester, but they can be *identified, prioritized, and effect-bounded* now.

## 3. What already exists (and is preserved)

The `fukui-tourism-thesis` repo is **not greenfield**. It already implements the analytical spine this reframe builds on:

| Existing asset | Role in the reframed thesis |
|---|---|
| Two-stage FTAS SEM (`scripts/sem_ftas.py` → `output/sem/`) | The structural core. Extended (not replaced) with non-survey indicator blocks — see `sem_nonsurvey_spec.md`. |
| Evidence-weighted nudge ranking (`scripts/rank_nudge_priorities.py`, `config/nudge_mapping.yaml`) | The prioritization layer. Now scored against observed behavioral signals, not only survey weights. |
| Hokuriku Shinkansen DiD / event study (`scripts/hokuriku_did_event_study.py`) | The causal identification story for the March 2024 extension — the one clean natural experiment. Kept as-is; the new panel does **not** duplicate it (see §6). |
| Fukui City synthetic control (`scripts/synthetic_control_fukui.py`) + SCM robustness | Municipality-level counterfactual for demand shifts. |
| Unfielded nudge-pilot app (`experiments/nudge-pilot/`) + power calc (`scripts/nudge_pilot_power.py`) | Becomes the *Arm 2/3 pre-registered field trial* — the explicitly-future component. |

The reframe **reorganizes the narrative around physical interventions and adds a non-survey evidence engine**; it does not discard the survey machinery or the causal designs.

## 4. The new evidence base (built, validated, in hand)

A unified non-survey panel was built on real public data and validated (`panel_design.md`, `coverage_report.md`):

- **`panel_site_daily`** — 2,245 rows, 4 AI-camera sites, 2024-12-20 → 2026-07-08. Footfall (Person), demographics (Face), and origin/vehicle mix (LicensePlate).
- **`panel_area_daily`** — 4,523 rows, 5 lodging markets, 2023-10-01 → 2026-10-08. Reservations, occupancy proxy, ADR proxy, GBP digital-intent, booking lead time.
- Full provenance: 7 Code4Fukui repos pinned by commit SHA, per-file SHA256.

An empirical **intervention-opportunity scan** over this panel (`opportunity_signals.json`) already surfaces five defensible observed patterns and one explicit negative result — detailed in `intervention_opportunity_analysis.md`. The headline signals:

- **Tojinbo footfall is sharply peak-concentrated** (95th-percentile day = 2.2× median; weekends 1.7× weekdays) → a temporal-dispersal opportunity.
- **Rainbow Line is car-access dominated** (66–70% out-of-prefecture vehicles, Aichi-led) → the intervention class here is parking/shuttle infrastructure, not rail-side nudges.
- **Awara & Echizen coast carry ~18pp weekend–weekday occupancy gaps** with rare saturation (<1.2% of days ≥90%) → the binding constraint is demand *distribution*, not capacity.
- **GBP "directions" requests co-move with realized stays** (r = 0.59 same-week) → a measurable intent→demand channel for the SEM.

## 5. The thesis arc, reframed

1. **Chapter framing — the system, not the survey.** Open on Hokuriku's post-Shinkansen tourism system as a set of physical sites with observable flows, and the question of *where a physical change would matter*.
2. **The evidence engine.** The non-survey panel + the extended SEM. This is the methodological contribution: fusing sensor, reservation, intent, and official data into latent constructs.
3. **Identification.** The Shinkansen extension (DiD/synthetic control, existing scripts) provides the one clean causal anchor for a system-level demand shift.
4. **Opportunity mapping.** The SEM + panel score each site/market for intervention leverage (`intervention_opportunity_analysis.md`).
5. **Effect-bounding & simulation.** The interactive SEM + demand-simulation webapp lets a partner ask "if this physical change moves friction indicator X by δ, what happens to realized demand?" — turning the SEM into a what-if tool.
6. **The pre-registered trial.** The nudge-pilot app + power calculation become the explicitly-future Arm 2/3: *this is the trial the evidence engine says to run, and here is the effect size it must detect.*

## 6. Honest scope boundary (the load-bearing caveat)

The core causal claim — *"this specific physical change will produce that specific behavioral effect"* — **cannot be established from observational data alone** and is not claimed. Two guardrails enforce this:

- **The Shinkansen panel is not a general intervention estimator.** The built reservation panels start Oct 2023, so their pre-extension window has no seasonal overlap with the post window; a naive pre/post comparison is confounded by season and is explicitly discarded (`opportunity_signals.json` → `S5_shinkansen_NOT_identifiable_here`). The clean natural-experiment estimate stays in the thesis repo's multi-year arrivals/accommodation series via the existing DiD/synthetic-control scripts.
- **Simulated intervention effects are labeled as elasticities/scenarios, not measured effects.** Where the webapp propagates a hypothetical δ through SEM path coefficients, at least one path is anchored to an *observed* elasticity (e.g. the intent→demand coupling, or a Shinkansen-identified demand shift) rather than a free parameter — and every simulated effect is visibly tagged as a scenario pending field validation.

The thesis is therefore honest about being *a rigorous method for identifying and prioritizing where physical-intervention trials should happen, with effect sizes bounded* — not a claim that any specific trial has succeeded. That is exactly the "identify areas for improvement even if not fully testable now" scope the project set.

## 7. What changes in the repo (handed to Codex)

See the codex handoff spec pack(s). At a high level: add the panel build under `scripts/`/`data/`, extend `config/` + `sem_ftas.py` with the non-survey indicator blocks (`sem_nonsurvey_spec.md`), add the opportunity-scan script, and scaffold the simulation webapp as a new `experiments/` app. A scope-honesty ADR (deferred per decision, to be written after this spike) records the §6 boundary as a project decision.
