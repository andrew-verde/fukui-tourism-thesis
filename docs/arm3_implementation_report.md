# Arm 3 implementation report

Date: 2026-07-30 (Asia/Tokyo)

Status: **complete against ADR 0030 and the frozen Arm 3 design.** The
production vintage gate passed, the full battery ran under both pre-declared
Hagibis masks, and byte-exact result artifacts are pinned. No chapter file was
changed and no post-2019 outcome cell was decoded.

## ADR 0030 resolutions implemented

1. The sensitivity pre-window is `2011-01..2015-02`, exactly **50 months**.
   The primary `2012-01..2015-02` window remains exactly 38 months.
2. Every declared sensitivity was run under both permitted Hagibis readings:
   the primary event mask excludes `2019-10`; the recovery sensitivity
   excludes `2019-10..12`. There is no third Hagibis mask.
3. V3 uses Kanazawa monthly lodging guests and the 19-facility aggregate.
   The Kenrokuen single-site monthly fixture is not used. It begins only in
   2017 and therefore cannot cover the 2015 opening window.

No further contradiction in a frozen §4 constant was found.

## Production data and vintage gate

`scripts/arm3_kanazawa_scm.py` now checksum-verifies and parses the seven
official JTA confirmed annual releases directly:

| Years | Format | Monthly table | Total | Foreign | Japanese |
|---|---|---|---|---|---|
| 2011–2014 | XLS | `第4表(<month>月)` | discovered `延べ宿泊者数` column | discovered `うち外国人延べ宿泊者数` column (H in these vintages) | total − foreign |
| 2015–2017 | XLSX | `第4表(<month>月)` | same header rule | same header rule (I in these vintages) | total − foreign |

The parser validates the pinned SHA-256 for each release, all 47 prefectures
in every monthly sheet, unique prefecture-month keys, finite nonnegative
components, and full `2011-01..2017-12` coverage (3,948 rows).

Two exact comparisons passed:

- Parser-wide diagnostic oracle: all 47 prefectures × 60 months
  (`2012-01..2016-12`) × three outcomes = **8,460 cells, zero differences**.
- Production gate required by the design: the two treated units plus the 16
  unique positive-weight primary donors = 18 prefectures × 60 months × three
  outcomes = **3,240 cells, zero differences**.

The production gate now runs after the primary weights identify the required
donors and before any non-primary sensitivity is computed. There is no
unchecked-vintage production option.

## Outcome firewall

The canonical 推移表 loader continues to inspect worksheet structure directly
and rejects outcome cells after column `2019-12` before calling the cell
decoder. A new sentinel test writes the nonnumeric value
`POST_2019_SENTINEL` into the `2020-01` outcome cell of all three required
worksheets. The loader succeeds and returns exactly 47 × 108 admitted rows,
proving those post-window cells were not decoded. Every causal result artifact
has `ym <= 201912`.

No post-2025-12 mobile data, post-2026-06 FTAS data, JTA 2025-confirmed data,
or 2026 release was fetched, opened, or listed for this work.

## Placebo and leave-one-out review

The review found and fixed one statistical bug before the final run:
`_run_intime()` measured the treated backdated opening gap in `2014-03..04`
but compared it with placebo opening gaps hard-coded to `2015-03..04`.
The placebo opening window is now an explicit argument, so both sides use
`2014-03..04`.

For Ishikawa, the corrected backdate is:

- gap −0.024147 log points (−2.386%);
- one-sided p = 0.580645;
- two-sided p = 0.709677;
- 30 placebos retained.

The prior bug happened not to change the V1b one-sided verdict, but it did
make the null invalid and changed the two-sided p-value. A regression test pins
the corrected statistics.

Leave-one-out is run under both Hagibis masks for every positive-weight donor.
The V1c range excludes the `(none: baseline)` reference row. Ishikawa has 14
positive-weight donors:

| Hagibis mask | Opening log-gap range | Opening percent range | Late percent range |
|---|---:|---:|---:|
| Primary: `2019-10` | 0.064337..0.105568 | +6.645%..+11.134% | +9.215%..+13.362% |
| Sensitivity: `2019-10..12` | 0.064337..0.105568 | +6.645%..+11.134% | +9.038%..+13.064% |

The raw in-space placebo distributions are now retained in
`placebo_distributions.csv`, rather than discarded after p-value calculation.

## Primary results and §6 tier outcomes

### Primary treated-unit statistics

The primary late window excludes October 2019, leaving 23 of 24 months.

| Unit | Pre RMSPE | Good fit | Opening gap | Opening p (1s / 2s) | Late gap | Late p (1s / 2s) | Decay ratio |
|---|---:|---|---:|---:|---:|---:|---:|
| Ishikawa | 0.041470 | yes | +0.097238 log / +10.212% | 0.181818 / 0.393939 | +0.099941 log / +10.511% | 0.212121 / 0.484848 | 0.827568 |
| Toyama | 0.082582 | yes | +0.078602 log / +8.177% | 0.205882 / 0.411765 | +0.003136 log / +0.314% | 0.529412 / 1.000000 | 0.030290 |

Ishikawa retained 32 placebos, so the attainable one-sided floor is 1/33 =
0.030303 and neither V1a nor V2a is capped at directional-only.

### Tier table

| Criterion | Fixed §6 test | Result | Outcome |
|---|---|---|---|
| V1a | Ishikawa opening gap > 0 and one-sided p ≤ 0.05, subject to floor | +10.212%; p = 0.181818; not floor-capped | **fail** |
| V1b | Ishikawa backdated opening one-sided p > 0.10 | −2.386%; p = 0.580645 | **pass** |
| V1c | Ishikawa leave-one-out opening minimum > 0 | minimum +0.064337 log / +6.645% | **pass** |
| **V1** | V1a + V1b + V1c all required | V1a fails | **fail** |
| V2a | Ishikawa primary-mask late gap > 0 and one-sided p ≤ 0.05, subject to floor | +10.511%; p = 0.212121; not floor-capped | **fail** |
| V2b | `R_Ishikawa > R_Toyama` and Ishikawa late gap > Toyama late gap | 0.827568 > 0.030290 and 0.099941 > 0.003136 | **pass** |
| **V2** | V2a + V2b both required | V2a fails | **fail** |
| V3 | Both approved Kanazawa monthly series show surge and persistence; descriptive only | both series positive on both comparisons below | **met descriptively** |

These are tier outcomes and measurements only. This report does not write the
§6 interpretation contract as thesis prose.

## Primary versus sensitivity Hagibis result

| Reading | Masked months | Late months used | Ishikawa late gap | p (1s / 2s) | Ishikawa R | Toyama late gap | Toyama R | V2a | V2b |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Primary event mask | `2019-10` | 23 | +0.099941 log / +10.511% | 0.212121 / 0.484848 | 0.827568 | +0.003136 log / +0.314% | 0.030290 | fail | pass |
| Recovery sensitivity | `2019-10..12` | 21 | +0.098293 log / +10.329% | 0.212121 / 0.454545 | 0.813927 | +0.000443 log / +0.044% | 0.004283 | fail | pass |

**V2a disagreement: no.** Both masks give the same V2a failure. The recovery
reading is reported separately and was not used to select the primary result.

## Sensitivity battery

Every base specification below was run under both Hagibis masks. Percentages
and p-values are Ishikawa; the complete Ishikawa and Toyama rows, including
two-sided p-values, are in `specification_summary.csv`.

| Specification | Hagibis mask | Pre RMSPE | Opening % | Opening p (1s) | Late % | Late p (1s) | Floor-capped |
|---|---|---:|---:|---:|---:|---:|---|
| Primary | event | 0.041470 | +10.212 | 0.181818 | +10.511 | 0.212121 | no |
| 50-month pre | event | 0.044503 | +6.455 | 0.333333 | +17.441 | 0.121212 | no |
| Strict donors | event | 0.044158 | +7.430 | 0.210526 | +10.705 | 0.210526 | **yes (18 retained)** |
| Mask 2018-06..09 | event | 0.041470 | +10.212 | 0.181818 | +10.602 | 0.212121 | no |
| Japanese only | event | 0.045261 | +7.536 | 0.212121 | +14.333 | 0.090909 | no |
| Foreign only | event | 0.214248 | −0.770 | 0.600000 | +4.963 | 0.428571 | no |
| Primary | recovery | 0.041470 | +10.212 | 0.181818 | +10.329 | 0.212121 | no |
| 50-month pre | recovery | 0.044503 | +6.455 | 0.333333 | +16.905 | 0.151515 | no |
| Strict donors | recovery | 0.044158 | +7.430 | 0.210526 | +10.677 | 0.210526 | **yes (18 retained)** |
| Mask 2018-06..09 | recovery | 0.041470 | +10.212 | 0.181818 | +10.388 | 0.212121 | no |
| Japanese only | recovery | 0.045261 | +7.536 | 0.212121 | +14.002 | 0.090909 | no |
| Foreign only | recovery | 0.214248 | −0.770 | 0.600000 | +5.725 | 0.428571 | no |

The foreign-only Ishikawa pre-RMSPE exceeds `GOOD_FIT_RMSPE = 0.15`; it is
reported as a sensitivity and is not used for a tier verdict. The strict-donor
Ishikawa tests retain only 18 placebos, making p ≤ 0.05 unattainable and
therefore invoking the pre-declared directional-only cap.

## V3 descriptive anchor result

V3 keeps the two units distinct and applies simple, disclosed same-period
comparisons; it is not an SCM or a confirmatory test.

| Series | Opening 2015 vs same months 2014 | 2015 vs 2014 annual | Mean annual 2018–2019 vs 2014 | 2019 vs 2014 annual | V3 component |
|---|---:|---:|---:|---:|---|
| Kanazawa lodging guests (persons) | +6.500% | +6.038% | +26.790% | +29.169% | surge and persistence positive |
| Kanazawa 19-facility aggregate (person-visits) | +30.069% | +51.067% | +52.229% | +53.119% | surge and persistence positive |

The Kenrokuen single-site series remains available only for
`2017-01..2019-12`; it was not used and no alternative source was sought.

The previously disclosed source limitations remain binding:

1. Printed lodging months do not sum to the adjacent 2014/2015 annual totals.
2. The 2019 report revises every 2018 19-facility aggregate month.
3. The 2019 dedicated aggregate table has small January–June differences from
   facility-detail totals; the dedicated time-series table is retained.
4. The lodging reporting universe grows from 112 facilities in 2014 to 345 in
   2019.
5. All anchor series remain descriptive point-utilization counts.

## Result artifacts and byte-exact hashes

All files are under `output/arm3_kanazawa/causal_robustness/`.

| Artifact | SHA-256 |
|---|---|
| `specification_summary.csv` | `820283199be89ae5335d22dc6df514a6b47fb1c2ad31851aa72285833113ed0b` |
| `scm_weights.csv` | `94701d0c6bc987416326997a1069d10309b57e15453a6e39a9d9e071bf87c83b` |
| `target_gap_trajectories.csv` | `ba40112813a45a89af5d2b14a07fcd35a18a5bdef770b3f2f32118e1b40f517f` |
| `intime_placebo.csv` | `3570e8a032891813393d30a8e4ed3b112082213f018de77d102114f1ac21063e` |
| `leave_one_out.csv` | `151319a8ef4f444953db2087fa5b4a6c62b2c9395fa83ef05751f37d039ad230` |
| `placebo_distributions.csv` | `5f826b5e06df609969cca075ac1c3fcb2fb2e329853e7b72f9283c96446f3749` |
| `v3_anchor_indices.csv` | `03034000eac9db3710a3b0abd6b56d92c762d8e122853d1483d96c317b321858` |
| `metrics.json` | `8af45d7d583bf9687f00dae3aed437ddebd74d4c01202314720be21bc2992f44` |
| `figures/fig1_scm_trajectories.png` | `bd72d7aa40aac89fbdea4c98e90964c3fb723ac88e53caf853e21fad7a98a657` |
| `figures/fig2_gap_trajectories.png` | `6664ea09f8e55e83795b1dfeb9016a23ee14faf1e7ec8719512119873cdbaddd` |
| `figures/fig3_placebo_distributions.png` | `8b4493618855c5edc1bf7a6558c23bd3f40974a554e633f822f23ca28bdd675e` |
| `figures/fig4_v3_anchor_indices.png` | `d4634635464241e7bed5c7040b56788da0a4fc3d71e3dcc6d03d01dee3db34dd` |

The producer checks this complete recursive hash map after writing. The test
suite also regenerates the entire result tree in a temporary directory and
requires byte-for-byte equality.

## Tests and verification

New or expanded Arm 3 tests cover:

- exact frozen constants, donor exclusion tuples, 38/50/58-month counts, and
  exactly two Hagibis masks across the 12-specification battery;
- checksum-pinned annual parsing, the corrected 2013 Ishikawa cell, all 8,460
  parser-wide vintage cells, and the executable production gate;
- poisoned `2020-01` sentinels proving post-2019 outcome cells are not decoded;
- the corrected backdated placebo window and exact p-values;
- V1/V2/V3 result semantics, mask agreement, result date limits, complete
  artifact hashes, figures, and deterministic regeneration;
- the existing source fetch and page-cited PDF extraction contracts.

Focused Arm 3/fetch result: **18 passed**.

## Force-add instructions for the human commit

The blanket `output/*` ignore rule covers all Arm 3 artifacts. After review,
force-add the complete **12-file**
`output/arm3_kanazawa/causal_robustness/` tree; these are the committed result
oracles pinned above.

The earlier PDF-extraction tests also require the five derived fixtures:

- `kanazawa_lodging_guests_monthly.csv`
- `kanazawa_19_facility_visits_monthly.csv`
- `kenrokuen_visits_monthly.csv`
- `kanazawa_19_facility_membership.csv`
- `kanazawa_pdf_provenance.json`

If those extraction fixtures are intended to run without a fetch step, also
force-add the two pinned PDFs under `output/arm3_kanazawa/raw/`. The JTA
workbooks may remain fetch-managed raw inputs via `docs/source_ledger.md`;
they are not result artifacts.

Nothing remains analytically open. The only remaining action is human review
and commit; this implementation did not commit, push, tag, switch branches, or
merge.
