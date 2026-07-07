# Phase 0 mechanical consistency audit

Scope: ADRs 0019–0023 and the five specified companion documents. Local
working-tree files were audited; no network sources were consulted.

| Check | Verdict |
|---:|:---|
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
| 4 | PASS |
| 5 | PASS |
| 6 | PASS |
| 7 | PASS |
| 8 | FAIL |
| 9 | FAIL |
| 10 | PASS |
| 11 | PASS |
| 12 | PASS |

## 1. SCM constants — PASS

- PASS — `EVENT_YM`: cited Direction-D value `202403`
  (`docs/thesis/arm3_kanazawa_design.md:85`) = source `202403`
  (`scripts/build_causal_arm_summary.py:37`). Arm-3 overrides to `201503` are
  explicitly declared, not conflicting (`docs/adr/0021-arm3-kanazawa-template-replication-design.md:45`;
  `docs/thesis/arm3_kanazawa_design.md:147`).
- PASS — `INTIME_EVENT_YM`: cited Direction-D value `202303`
  (`docs/thesis/arm3_kanazawa_design.md:86`) = source `202303`
  (`scripts/causal_robustness.py:41`). Arm-3 overrides to `201403` are
  explicitly declared (`docs/adr/0021-arm3-kanazawa-template-replication-design.md:45`;
  `docs/thesis/arm3_kanazawa_design.md:148`).
- PASS — `GOOD_FIT_RMSPE`: cited `0.15`
  (`docs/adr/0021-arm3-kanazawa-template-replication-design.md:40`;
  `docs/thesis/arm3_kanazawa_design.md:65,157`) = source `0.15`
  (`scripts/build_causal_arm_summary.py:39`).
- PASS — `RMSPE_FIT_MULT`: cited `5.0`
  (`docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:53`;
  `docs/adr/0021-arm3-kanazawa-template-replication-design.md:40`;
  `docs/thesis/arm3_kanazawa_design.md:66,157`) = source `5.0`
  (`scripts/causal_robustness.py:42`).
- PASS — `HOKURIKU_PREFS`: audited-document donor exclusion `{15,16,17,18}`
  (`docs/thesis/arm3_kanazawa_design.md:89`) = source `(15,16,17,18)`
  (`scripts/build_causal_arm_summary.py:38`).
- PASS — ADR 0019, ADRs 0022–0023, the playbook, architecture, data audit,
  and Section 7 draft do not state additional values for these named
  constants; comparison set is empty, not skipped.

## 2. Direction D headline numbers — PASS

- PASS — `+29.2%` cited (`docs/adr/0021-arm3-kanazawa-template-replication-design.md:118`;
  `docs/thesis/arm3_kanazawa_design.md:82`) = `29.226952...%`
  (`output/national_stats/causal_robustness/metrics.json:7`) = `+29.2%`
  (`docs/thesis/section5_robustness.md:67`).
- PASS — `p=0.041` one-sided = `0.0409357`
  (`output/national_stats/causal_robustness/metrics.json:9`) = `0.041`
  (`docs/thesis/section5_robustness.md:67-68`).
- PASS — `1,538` well-fit placebos = `1538`
  (`output/national_stats/causal_robustness/metrics.json:12`) = `1,538`
  (`docs/thesis/section5_robustness.md:66`).
- PASS — backdated `p=0.47` = `0.4718447`
  (`output/national_stats/causal_robustness/metrics.json:25`) = `0.47`
  (`docs/thesis/section5_robustness.md:93-94`).
- PASS — leave-one-out `26.2–39.8%` = `26.20348–39.79712%`
  (`output/national_stats/causal_robustness/metrics.json:20-22`) =
  `26.2–39.8%` (`docs/thesis/section5_robustness.md:100`).
- PASS — significant set `{Eiheiji, Fukui City, Tsuruga, Sakai}`
  (`output/national_stats/causal_robustness/metrics.json:14-19`) = same set
  (`docs/thesis/section5_robustness.md:76-78`).
- PASS — ADRs 0019/0020 and `section7_template_test.md` do not restate these
  Direction-D headline values; ADR 0021/Arm-3 design restate only `+29.2%`.
  No contradictory citation occurs in the requested five-document set.

## 3. ADR 0020 frozen inputs — PASS

- PASS — `city2025.csv` abbreviated SHA
  `7c31fed0…17d5216`, `22,434` rows, commit `dfb9069`
  (`docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:23-26`) =
  full SHA `7c31fed0a71168b684e61ecc5e092cf8d63679494a9eeeac384ceb58f17d5216`,
  `22434`, commit
  `dfb906975b63adcaef20a3e7a35f2a10ab22ada5`
  (`config/national_data_sources.yaml:37,45`).
- PASS — durable `{Sakai 18210, Eiheiji 18322}`; transient
  `{Awara 18208, Fukui City 18201, Tsuruga 18202, Sabae 18207}`; low
  confidence `{Katsuyama, Ikeda, Mihama, Echizen City}` in ADR 0020
  (`docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:43-48`) =
  CSV rows 2–10 and 15
  (`output/synthesis/durability_mechanisms.csv:2-10,15`).
- PASS — ADR count `13` high-confidence municipalities
  (`docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:49-50`) =
  computed CSV count `13` where `regime_confidence == "high"`
  (`output/synthesis/durability_mechanisms.csv:2-18`).

## 4. ADR 0020 P2 threshold — PASS

- PASS — frozen `ρ ≥ 0.48` at one-sided `α=0.05`, `n=13`
  (`docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:88-93`) versus
  seeded permutation-null Monte Carlo: NumPy RNG seed `13`, `2,000,000`
  independent permutations, 95th percentile `0.4780219780`. To two decimals
  the critical value is `0.48`: **correct**, neither conservative nor
  anticonservative at the stated precision. Empirical `P(ρ ≥ 0.48)=0.048479`.

## 5. Power arithmetic — PASS

- PASS — raw `n(d)` values for `d={.25,.20,.15,.125,.10}` are
  `{251.1641,392.4439,697.6781,1004.6564,1569.7757}`; ceiling gives
  `{252,393,698,1005,1570}`, exactly the playbook
  (`docs/thesis/directionB_stage2_fielding_playbook.md:34`) and DESIGN table
  (`experiments/nudge-pilot/DESIGN.md:81-87`). Convention: **ceiling to the
  next integer**, not nearest-integer rounding (which fails for `.25` and
  `.20`).
- PASS — script formula `ceil(2*(zα+zpower)^2/d^2)`
  (`scripts/nudge_pilot_power.py:15-22,94`) = requested formula and rounding.
- PASS — computed `sqrt(2*(1.959964+0.841621)^2/360)=0.2088178` =
  claimed `0.2088/~0.21`
  (`docs/thesis/directionB_stage2_fielding_playbook.md:40,51`).
- PASS — with `SE=0.20`, boundary `0.20+0.2088178=0.4088178 ≈ 0.41` =
  playbook `d-hat ≳ 0.41`
  (`docs/thesis/directionB_stage2_fielding_playbook.md:51-52`).

## 6. Arm 3 donor arithmetic — PASS

- PASS — exclusion set has `12` codes and `47-12-1=34`, matching stated
  `34` donors (`docs/thesis/arm3_kanazawa_design.md:89,155`).
- PASS — flagged set has `14` codes and `34-14=20`, matching stated strict
  pool `20` (`docs/thesis/arm3_kanazawa_design.md:156`).
- PASS — randomization floors: `1/(1+34)=1/35≈0.0286` and
  `1/(1+20)=1/21≈0.0476`, matching `1/35≈0.029`, `1/21≈0.048`
  (`docs/thesis/arm3_kanazawa_design.md:162-164`).
- PASS — `1/(1+k)≤0.05` iff `k≥19` (algebra: `k+1≥20`).
- PASS — Toyama `16` is explicitly excluded and Ishikawa `17` explicitly
  treated/removed: both are inside the exclusion structure
  (`docs/thesis/arm3_kanazawa_design.md:89`;
  `docs/arm3_kanazawa_data_audit.md:240`).

## 7. Window arithmetic — PASS

- PASS — inclusive month counts: `2012-01..2015-02=38`,
  `2015-03..2019-12=58`, `2018-01..2019-12=24`,
  `2011-01..2015-02=49`; all equal design claims
  (`docs/thesis/arm3_kanazawa_design.md:90-91,99,149-153`).
- PASS — Direction-D `2021-01..2024-02=38`
  (`docs/thesis/arm3_kanazawa_design.md:73,90`) and Section 5's sample has
  `60` total / `38` pre (`docs/thesis/section5_robustness.md:31-33`).

## 8. Direction B numbers — FAIL

- PASS — playbook `d=.25` ceiling, Stage 1 `50/arm`, `N=250`, MDE `≥.56`,
  re-power rule, `SE≈.20`, `360/arm`, `d_plan≈.21`, subsample `300–500`,
  `~289/~120` monthly, `2,010≈17` months, stations
  Fukui/Awara-Onsen/Tsuruga, and `7.09%`
  (`docs/thesis/directionB_stage2_fielding_playbook.md:21-43`) match
  preregistration (`docs/thesis/directionB_preregistration.md:84-119`) and
  ADR 0018 (`docs/adr/0018-directionB-preregistration.md:24-38,67,83`).
- PASS — `car 4.31`, `rail 4.11`, `SD .74–.84`, `n≈8,800` occur in the
  committed preregistration (`docs/thesis/directionB_preregistration.md:60-61`)
  and DESIGN (`experiments/nudge-pilot/DESIGN.md:71-74`); the playbook does
  not restate them and does not contradict them.
- FAIL — requested claim “close date `2026-08-16` appears only in ADR 0019
  and the playbook” is false. Repo-wide occurrences are:
  `docs/adr/0019-eighteen-month-execution-roadmap.md:22,86`;
  `docs/adr/0022-directionB-stage2-fielding-playbook.md:13`; and
  `docs/thesis/directionB_stage2_fielding_playbook.md:9,22,217,309`.
  Value compared: expected file set `{ADR 0019, playbook}` versus actual
  `{ADR 0019, ADR 0022, playbook}`.

## 9. Cross-reference integrity — FAIL

- FAIL — dangling path
  `experiments/nudge-pilot/timetable_verification.md`
  (`docs/thesis/directionB_stage2_fielding_playbook.md:213`) versus working
  tree: **missing**.
- PASS — `study-config.json` in ADR 0022 resolves by its stated experiment
  context to existing `experiments/nudge-pilot/study-config.json`
  (`docs/adr/0022-directionB-stage2-fielding-playbook.md:72`;
  `experiments/nudge-pilot/study-config.json:1`).
- PASS — every other repo path mentioned in ADRs 0021–0023, Arm-3 design,
  playbook, architecture, and Section 7 draft exists. Compared path tokens
  include `docs/arm3_kanazawa_data_audit.md`,
  `docs/thesis/arm3_kanazawa_design.md`,
  `docs/thesis/directionB_stage2_fielding_playbook.md`,
  `docs/thesis/thesis_v2_architecture.md`, all named chapter/master/reference
  files, scripts/config sources, and experiment config.
- PASS — every cited ADR number exists under `docs/adr/`; dangling ADR
  references: **none**.

## 10. Section-anchor integrity — PASS

- PASS — matrix anchor `not a run experiment`
  (`docs/thesis/thesis_v2_architecture.md:207`) matches line-wrapped source
  “not a run / experiment” in §6.3
  (`docs/thesis/section6_intervention.md:73-74`).
- PASS — matrix `From design to field`
  (`docs/thesis/thesis_v2_architecture.md:208`) = §7.4 heading
  (`docs/thesis/section7_conclusion.md:184`).
- PASS — matrix `explicitly not as evidence`
  (`docs/thesis/thesis_v2_architecture.md:219`) = §1.3 wording
  (`docs/thesis/section1_introduction.md:67`).
- PASS — matrix `All seven chapters are written`
  (`docs/thesis/thesis_v2_architecture.md:209`) = master wording
  (`docs/thesis/thesis_master.md:43`).
- PASS — matrix `Chapter 7 concludes`
  (`docs/thesis/thesis_v2_architecture.md:205`) = §1.2 wording
  (`docs/thesis/section1_introduction.md:47`).

## 11. Section 7 fidelity to ADR 0020 — PASS

- PASS — draft/source pairs match: `0.15`, `5.0×`, `2024-02`
  (`docs/thesis/section7_template_test.md:51-54` vs ADR 0020:52-55);
  `α=.05`, `ρ≥.48`, `n=13`, `r=.826`
  (draft:66,73-79 vs ADR:77,88-95); six unseen months
  (draft:59-60 vs ADR:69-73); `2%` (draft:96-99 vs ADR:119-123);
  `103,807`, `2025-12`, `2026-06` (draft:44-50 vs ADR:23-34);
  `4.0×`, `7.09%`, `.66%`, `2×` (draft:89-93 vs ADR:110-115).
- PASS — municipality codes match exactly: durable
  `{Sakai 18210,Eiheiji 18322}` and transient
  `{Awara 18208,Fukui City 18201,Tsuruga 18202,Sabae 18207}`
  (`docs/thesis/section7_template_test.md:61-65` vs
  `docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:43-48,74-76`).
- PASS — P1/P2/S1–S3 numeric symmetric difference is empty: no numeric
  threshold/value appears in the draft but not ADR 0020, or vice versa.

## 12. Date stamps — PASS

- PASS — ADR dates: `2026-07-03` in ADRs 0019 and 0020
  (`docs/adr/0019-eighteen-month-execution-roadmap.md:3`;
  `docs/adr/0020-arm2-out-of-sample-prediction-criteria.md:3`);
  `2026-07-04` in ADRs 0021–0023
  (`docs/adr/0021-arm3-kanazawa-template-replication-design.md:3`;
  `docs/adr/0022-directionB-stage2-fielding-playbook.md:3`;
  `docs/adr/0023-thesis-v2-chapter-architecture.md:3`).
- PASS — checked stamps are consistently `2026-07-03`: Arm-3 design line 10,
  ADR 0021 line 12, and data-audit lines 29, 102, 105, 177, 187, 239–245
  (`docs/thesis/arm3_kanazawa_design.md`;
  `docs/adr/0021-arm3-kanazawa-template-replication-design.md`;
  `docs/arm3_kanazawa_data_audit.md`).
- PASS — month-only freeze stamps are `2026-07` in architecture
  (`docs/thesis/thesis_v2_architecture.md:60`) and “July 2026” in Section 7
  (`docs/thesis/section7_template_test.md:22,32,38`); consistent.
- PASS — the known `checked 2026-07-03` versus ADR 0021–0023
  `Date: 2026-07-04` difference is chronological provenance, not a
  contradictory same-field stamp. No inconsistent date string found.
