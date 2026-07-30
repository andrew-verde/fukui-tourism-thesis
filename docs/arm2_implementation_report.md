# Arm 2 frozen implementation report — seen data only

Date: 2026-07-30

## Scope and firewall statement

This change builds Arm 2's frozen execution path and test oracles. It does
not run Arm 2 and produces no prediction outcome.

No unseen data was fetched, opened, printed, plotted, sampled, or
summarized. Nothing was placed in `data/quarantine/arm2/`. No network
operation was used. In particular, no content was fetched from
`code4fukui/japan-kanko-stat` beyond `dfb9069`, no content was fetched from
`code4fukui/fukui-kanko-survey` beyond `5857c311`, and no JTA
2025-confirmed or 2026 outcome row was fetched or opened. Neither source
pin was changed.

Development and tests used only the already-present seen mobile panel
(2021-01 through 2025-12), seen synthesis artifacts, and synthetic or
held-out-seen fixtures explicitly marked as non-results.

## Built artifacts

- `scripts/freeze_arm2_seen_scm.py` is a one-time pre-registration build
  tool. It checksum-verifies the five pinned seen mobile files, refuses any
  month after 2025-12, fits only through 2024-02 with Direction D's
  deterministic solver, and persists the weights Direction D previously
  discarded.
- `data/causal/arm2_frozen_scm_weights.csv` contains the positive frozen
  weights for the 13 high-confidence Fukui units and the 1,709 donor
  placebos.
- `data/causal/arm2_frozen_scm_fits.csv` contains the frozen pre-RMSPEs and
  max-/min-anchor gate membership.
- `data/causal/arm2_frozen_friction_ranking.csv` contains the existing
  13-unit `transport_access` predictor. It is loaded, not re-estimated.
- `data/causal/arm2_frozen_scm_metadata.json` records the seen and fit
  windows, construction constants, row populations, and SHA-256 checksums
  for all three frozen inputs.
- `scripts/arm2_quarantine.py` is the sole filesystem gateway for Arm 2
  unseen data.
- `scripts/arm2_predictions.py` implements P1, P2, S1, S2, S3, and the
  headline verdict assembler.
- `tests/test_arm2_oracles.py` and `tests/test_arm2_firewall.py` encode the
  pre-registration and firewall contracts.

## Structural firewall

The production loader takes no caller-supplied data path. Its root is fixed
to `data/quarantine/arm2/`, and its CSV primitive resolves every path and
rejects anything outside that root.

The expected quarantine layout for a future authorized run is:

- `mobile/repository/`: a local checkout whose `origin` is the protected
  upstream and whose `HEAD` is the declared vintage;
- `mobile/repository/data/city2021.csv` through `city2025.csv`: revised
  historical siblings used by the guard;
- `mobile/repository/data/cityYYYYMM.csv`: unseen monthly files beginning
  at 2026-01;
- `mobile/vintage_manifest.json`: one full upstream commit SHA plus the
  same commit, Git blob ID, and SHA-256 digest for every historical and
  monthly file;
- `ftas/ftas_survey_all.csv`: full extended FTAS respondent file;
- `ftas/merged_survey_2023.csv` through
  `ftas/merged_survey_2026.csv`: full extended Chapter 3 DiD sample;
- `jta/jta_accommodation_panel.csv`: normalized extended JTA panel with
  vintage labels.

`load_guarded_arm2_data()` reads only revised historical mobile files
first. Before doing so, it reads only the outcome-free manifest metadata,
requires every mobile filename to belong to one upstream commit, and
checks that the checkout origin and `HEAD` match, checks every declared
blob against that commit's Git tree, and verifies the five historical
working-file digests. It then verifies the pinned reference checksums,
loads the frozen SCM artifacts, and runs the revision guard. Only the
statement after the passing guard verifies unseen working-file digests
and blob identities and calls the unseen mobile and secondary decoders. A
guard failure raises before an unseen file is hashed or decoded.

The loader returns a sealed `GuardedArm2Data` capability. Its constructor
always rejects direct callers. All post-guard decoders are closed inside
the loader and are not importable module functions. More importantly,
there is no secret-token convention to bypass: every gap application for a
month after 2025-12 mechanically reloads the frozen inputs and pinned seen
reference and reruns the revision guard before calculation. A forged object
therefore cannot reach a post-2025 gap merely by claiming a passing status.
The gap function additionally requires object identity with that guarded
panel and frozen-artifact object and requires the complete validated month
sequence; a valid guard cannot be paired with a detached panel. Guard
revalidation also rechecks the checkout-backed bytes, reloads the unseen
frames, and compares them with the in-memory panel, so complete forgery or
in-place mutation cannot substitute other outcome values.
The production analyzer and primary engine reject raw frames and incomplete
objects.

The held-out-seen fixture is a separate path bound to the SHA-256-pinned
seen panel. It retains its true 2025 month labels, so it cannot enter the
post-2025 gap path, and it discards every computed result field. No other
script contains a quarantine filesystem path.

## Vintage-revision guard

The guard enforces the corrected ADR 0020 population exactly:

`18201, 18202, 18204, 18205, 18207, 18208, 18210, 18322, 18404, 18423,
18481, 18483, 18501`.

For each of those 13 units it compares all 60 seen months with the
checksum-pinned `city2021.csv` through `city2025.csv` reference and stops
if root-mean-square relative revision exceeds `0.02`.

It then applies, without refitting, the frozen target and placebo weights
to revised pre-event history ending 2024-02. It recomputes the six P1
target pre-RMSPEs, anchors the primary gate at five times their maximum
and the sensitivity gate at five times their minimum, and stops if any
previously retained donor exits either applicable gate. The loader never
mixes a passing subset with another vintage.

Every target and donor matrix is required to be complete, finite, and
strictly positive for every requested month before the log transform.
Frozen weights must be finite and sum to one. The unseen window must begin
at 2026-01, be month-contiguous, and contain at least six months; six
arbitrary or sparse months cannot pass.

## ADR constants and verdict enforcement

### P1

- durable set: Sakai `18210`, Eiheiji `18322`;
- transient set: Awara `18208`, Fukui City `18201`, Tsuruga `18202`,
  Sabae `18207`;
- observed statistic: durable two-unit unseen-window mean gap minus
  transient four-unit unseen-window mean gap;
- minimum unseen window: six months beginning 2026-01;
- high-confidence fit gate: `pre_rmspe <= 0.15`;
- primary pool: placebo pre-RMSPE no greater than `5.0` times the maximum
  of the six target pre-RMSPEs;
- reported sensitivity: the identical calculation anchored at the
  minimum;
- null: `100,000` NumPy-generator draws with seed `202601`, selecting two
  pseudo-durable and four pseudo-transient donors without replacement;
- one-sided finite-sample p-value:
  `(1 + count(null >= observed)) / (1 + 100000)`;
- confirmed: both durable gaps are positive, the set difference is
  positive, and `p <= 0.05`;
- directional-only: both sign conditions hold and `p > 0.05`;
- falsified: the set difference is non-positive or either durable unit is
  non-positive.

The production module contains no SCM fitter and imports no Direction D
solver. It only applies checksum-verified frozen weights.

### P2

The predictor is the checksum-verified, frozen seen
`transport_access` ranking for the same 13 high-confidence units. The
outcome ranking is the unseen-window mean frozen-SCM gap. Spearman's rho
is classified exactly as:

- confirmed: `rho >= 0.48`;
- directional-only: `0 < rho < 0.48`;
- falsified: `rho <= 0`.

The in-sample association is not encoded as a threshold anywhere.

### S1

S1 calls the existing Chapter 3 clustered-SE specification on the full
extended sample. The frozen reported pair is the baseline and the
combined `drop_jan_mar_2024_and_noto` earthquake-robust specification,
matching ADR 0011's Chapter 3 pin. Both NPS and transport-satisfaction
estimates are required in each.

The seen 2023-2026 merged-wave files are SHA-256 frozen. On a production
load, 2023-2025 must remain byte-exact and the extended 2026 file must
begin with the value-exact frozen seen population before adding post-June
rows. Backfills into the frozen seen period and exact duplicates within the
suffix or against the frozen prefix are rejected.
The upstream seam rows newly published on 2026-06-30 are excluded: they
are not in the pinned seen population, but the frozen unseen definition
begins only after 2026-06. Only July onward is appended to S1.
This makes “full extended sample” an executable population check rather
than a date-range heuristic.

- prediction met: all required point estimates are non-negative;
- discordant: any required estimate is negative with its CI excluding
  zero;
- otherwise: `not confirmed, not discordant`.

S1 is explicitly marked secondary and cannot enter the headline.

### S2

S2 emits the extended, vintage-labelled Fukui JTA monthly series for the
pre-extension-trend/event-study description. ADR 0020 says this framing
remains descriptive and supplies no numerical verdict cutoff, so the
implementation deliberately does not invent one. Its status is
`descriptive only`; it gates nothing and cannot enter the headline.
The loader-facing report requires complete confirmed 2018-2024 history,
all 12 confirmed 2025 months, and at least one 2026 row before emitting
the descriptive series.

### S3

S3 normalizes and tags the full extended FTAS file, then assesses only rows
after 2026-06, using the existing codebook. It reproduces the denominator
used to calibrate the frozen
threshold: shinkansen arrivers versus the pooled counts and denominators
of private car, rental car, local train, airplane, and tour bus. It does
not use private car alone.

The secondary prediction is met only when `transport_access` is the
argmax shinkansen friction category and its
shinkansen-to-pooled-other ratio is strictly greater than `2.0`. The test
also asserts the committed seen calibration fields byte-exactly. S3
gates nothing.

### Headline assembler

Only `P1 == confirmed` and `P2 == confirmed` renders
`prediction confirmed`. One confirmed primary plus one
directional-only primary renders `partial support`; it can never render
confirmation. Any falsified primary renders `prediction falsified`.
Two directional-only primaries remain `directional-only`. Secondary
predictions are absent from this function.

## Oracle inventory

`tests/test_arm2_oracles.py` asserts:

1. all seen/unseen window boundaries;
2. the exact 13-, two-, and four-unit populations;
3. `0.02`, `0.15`, `5.0`, six months, seed `202601`, `100,000` draws, two/four
   partition sizes, without-replacement sampling, one-sidedness, and
   `alpha = 0.05`;
4. max-anchor primary and min-anchor sensitivity membership directly
   against the frozen pre-RMSPEs;
5. the finite-sample p-value formula;
6. frozen weight checksums, unit populations, and unit-sum weights;
7. absence of a fitter from both production modules;
8. every P1 and P2 boundary, including equality at `0.05`, `0.48`, and
   zero;
9. the both-primaries headline conjunction and partial-support rule;
10. S1's three bands and full-sample primary/earthquake-robust pin;
    its four frozen seen-wave checksums are also asserted;
11. S3's pooled-other mode set, strict `> 2.0` threshold, and exact seen
    pooled-other calibration fields;
12. S2's confirmed-2025 and 2026-row vintage boundary;
13. absence of the in-sample P2 association and private-car ratio as
    thresholds;
14. the exact `dfb9069...` and `5857c311...` config pins and absence of
    the two upstream HEAD commits named in ADR 0032;
15. a six-month held-out slice of the seen panel exercises frozen gap
    application, both P1 nulls, P2 ranking, and the 100,000-draw path,
    while returning no gap, p-value, rho, prediction status, or verdict.

`tests/test_arm2_firewall.py` asserts:

1. every outside-quarantine path is rejected;
2. a poisoned synthetic unseen file is never decoded when the revision
   guard fails;
3. `GuardedArm2Data` cannot be directly constructed, and a forged passing
   status still triggers mechanical guard revalidation;
4. the analyzer, guarded-primary entry point, and internal engine reject
   an unguarded frame;
5. no other production script has a quarantine filesystem path;
6. the guard call precedes every closed unseen decoder in the loader;
7. missing/non-finite SCM outcomes fail before a gap or null is formed;
8. late-starting and sparse unseen month sequences are rejected.
9. a non-finite post-event seen value cannot pass the revision guard.
10. S1's appended suffix cannot contain backfilled seen dates or duplicate
    rows.
11. a mobile manifest assigning one file to another commit is rejected.
12. manifest blob IDs must match the declared commit's local Git tree.
13. post-2025 gaps reject a panel detached from the exact guarded input.
14. guard revalidation rejects an in-memory mutation against the
    checkout-backed unseen frames.

The poison and held-out fixtures live under pytest temporary directories
or use already-seen local data. They are explicitly test fixtures, not
results, and write no Arm 2 output.

## Validation

The targeted Arm 2 suite passes:

```text
24 passed
```

No production Arm 2 command was run. The only executed builder was the
seen-only freezer, which verifies the pinned local input checksums and
refuses post-2025 data.

## What remains before any run is authorized

The firewall release remains both-of-two:

1. a human accepts ADR 0020; and
2. a human reviews and commits the frozen scripts, frozen inputs, report,
   and oracles.

Only after both conditions hold may a human fetch the unseen vintages into
the fixed quarantine layout. The first production action is then the
guarded loader. A revision-guard failure requires the deviation ADR choice
specified by ADR 0020; it must not be worked around. No chapter file may be
changed until the later ADR 0023 phase authorizes outcome-matched prose.
