# ADR 0031: Arm 3 Kanazawa replication — verdict (V1 fail, V2 fail, V3 met descriptively)

Date: 2026-07-30
Status: accepted 2026-07-30 (records the ADR 0021 §6 interpretation contract's outcome; binds ADR 0023 Track T)

**Wording corrected by ADR 0035 (2026-07-30):** the phrase
"24-specification battery" below (`:21`, `:29`, `:80`) is loose against the
frozen artifact, which records `design.specification_count: 12` run against
two targets — 12 specifications, 24 target-by-specification rows. Read every
occurrence that way. No number, tier outcome, or verdict in this ADR changes;
the p-value scan covers every row either way.

## Context

Arm 3 ran to completion on 2026-07-30 under ADR 0021 (accepted
2026-07-29) as corrected by ADR 0030. The §6 interpretation contract was
written before any result existed, precisely so that the verdict would
follow mechanically from the tier outcomes rather than from post-hoc
reading. This ADR records that verdict.

Implementation, artifact hashes, and the full 24-specification battery:
`docs/arm3_implementation_report.md`. Result artifacts:
`output/arm3_kanazawa/causal_robustness/`.

All numbers below are byte-exact from
`output/arm3_kanazawa/causal_robustness/metrics.json`.

**Reproduction:** `make arm3-kanazawa` regenerates the full
24-specification battery and every figure and hash quoted here; the
Kanazawa V3 series come from `make arm3-kanazawa-pdfs`.
Oracles: `tests/test_arm3_kanazawa_scm.py`,
`tests/test_arm3_kanazawa_pdf_extraction.py`,
`tests/test_arm3_kanazawa_design_guard.py`. See `docs/source_ledger.md`.

## Tier outcomes

| Criterion | Fixed §6 test | Result | Outcome |
|---|---|---|---|
| V1a | opening gap > 0 and one-sided p ≤ 0.05, subject to floor | +0.097238 log / +10.212%; p = 0.181818; not floor-capped | **fail** |
| V1b | backdated opening one-sided p > 0.10 | −0.024147 log / −2.386%; p = 0.580645 | pass |
| V1c | leave-one-out opening minimum > 0 | minimum +0.064337 log / +6.645% | pass |
| **V1** | all three required | V1a fails | **fail** |
| V2a | late gap > 0 and one-sided p ≤ 0.05, subject to floor | +0.099941 log / +10.511%; p = 0.212121; not floor-capped | **fail** |
| V2b | R_Ishikawa > R_Toyama and Ishikawa late gap > Toyama late gap | 0.827568 > 0.030290 and 0.099941 > 0.003136 | pass |
| **V2** | both required | V2a fails | **fail** |
| V3 | both approved Kanazawa monthly series show surge and persistence, descriptive only | both series positive on both comparisons | **met descriptively** |

Both Hagibis masks (ADR 0030 §2) agree on V2a; there is no
primary-versus-sensitivity disagreement to report. Ishikawa pre-period
RMSPE is 0.041470 against the 0.15 good-fit gate.

## The §6 suspect protocol, executed in order

ADR 0021 §6 requires that before any interpretation of a V1 failure, three
pre-declared suspects are checked in order.

**Placebo floor — ruled out.** Ishikawa retained 32 placebos, so the
attainable one-sided floor is 1/33 = 0.030303 and
`directional_only_floor = False`. The p ≤ 0.05 threshold was reachable;
V1a and V2a are genuine failures, not artifacts of a truncated placebo
distribution. (The floor rule did fire correctly on the strict-donor
specification, where 18 retained placebos give a floor of 0.052632 and the
threshold is unattainable by construction — that specification is
directional-only, as designed.)

**Donor-pool contamination — ruled out.** The strict 20-prefecture pool,
dropping all 14 flagged codes, gives Ishikawa +0.071667 log / +7.430%,
p = 0.210526. The failure is unchanged. Removing contaminated donors does
not recover significance.

**Aggregation dilution — survives, and is not testable with available
data.** V3 shows the surge concentrated at the anchor city while the
Ishikawa-wide gap is large but noisy, which is the signature dilution
would produce. It cannot be probed directly: data audit §2 established
(VERDICT) that no balanced municipality-month panel exists for Ishikawa
2013–2019, and design §7.1 records that no pre-2021 municipal mobile panel
exists from any provider. The one surviving suspect is the one this grain
cannot test.

Across all 24 specifications, no run reaches p ≤ 0.05 on V1a; the smallest
one-sided opening p is 0.181818 (primary). The failure is consistent, not
specification-dependent.

## Decision — the verdict

Per the §6 contract, quoted verbatim:

> **V1 fail** — the pipeline fails to recover a publicly known boom.
> Before any interpretation, the pre-declared suspects are checked in
> order: aggregation dilution (Kanazawa's surge diluted across Ishikawa,
> including Noto), the placebo floor, and donor-pool contamination. If
> none explains it, the honest conclusion is that the template's
> portability is not demonstrated at prefecture grain — which bounds the
> ADR 0017 template claim and is reported as such. A V1 failure does not
> touch the 2024 Fukui results; they rest on their own committed battery.

Dilution is not excluded and is untestable here, so the contract's
"if none explains it" branch is not reached in its strict form. The
recorded verdict is therefore:

**The template's portability is not demonstrated at prefecture grain.
The leading pre-declared explanation — aggregation dilution — remains
live and is untestable with any data that exists for 2015. The ADR 0017
template claim is bounded accordingly. The 2024 Fukui results are
untouched.**

Consequences that follow directly:

1. **ADR 0017's exportable-object claim is bounded** to
   "specified for export, not yet demonstrated." It does not gain a
   Kanazawa leg.
2. **No Direction D analysis is re-opened** (§6 final bullet).
3. **No Arm 3 result is described as a prediction test.** That word
   belongs to Arm 2 (§6 final bullet).
4. **Chapter 5 is untouched.** No Track T row reaches it (ADR 0023 §4,
   "stable by design"), and §6 states a V1 failure does not touch the
   2024 results.
5. **V2b is not promoted.** Ishikawa retains 0.827568 of its surge against
   Toyama's 0.030290 — the durable-where-anchored pattern appearing at
   prefecture grain — but §6 declares V2b sign-level with no p-value, and
   the "directional-only outcomes" bullet forbids promoting any claim on
   it. It is reported as consistent-but-underpowered at this granularity.
6. **Two sensitivity results are explicitly barred from headline use.**
   `foreign_only` fails the good-fit gate (pre-RMSPE 0.214248 Ishikawa,
   0.342352 Toyama, both > 0.15) and must not be interpreted at all.
   `japanese_only` gives the smallest late p in the battery (0.090909,
   +14.333%) and is a sensitivity — §5 declares sensitivities "reported,
   never headline."

## ADR 0023 Track T resolution

Track T resolves as **V1 fail**. Both T-rows fire, and both are Phase 4
edits — no chapter file changes now (ADR 0023 §5, unchanged and binding):

| # | Location | Edit |
|---|---|---|
| T1 | §8.2 exportable-object paragraph | Withhold the Kanazawa clause; the portability claim stays "specified for export, not yet demonstrated" |
| T2 | §6.5 template paragraph | Soften "the pattern generalizes" to the specified-not-demonstrated form (T2's trigger is V1 fail only — it fires) |

Per ADR 0023 §3 Track T, the V1-fail branch also governs §7.3: it reports
the failure with the pre-declared suspects. This ADR supplies that
content; the splice is a Phase 4 action.

## Consequences

- The journal manuscript (ADR 0019 Phase 2) carries Arm 3 as a **bounded
  null replication**, not a confirmation. This should be settled before
  the manuscript is drafted, not during.
- The thesis's empirical upgrade now rests disproportionately on Arm 2,
  which remains blocked on ADR 0020's status and on FTAS new-wave access.
  If Arm 2 also fails to land, the upgrade reduces to the non-survey
  engine (ADR 0027/0028) plus this bounded null.
  **Corrected same day by ADR 0032:** there is no FTAS access dependency —
  FTAS and the mobile panel are public repositories and both have already
  published the unseen window. Arm 2 is blocked only on ADR 0020's status
  and on committing the frozen scripts.
- Reporting a well-behaved null — good pre-fit, silent backdated placebo,
  leave-one-out bounded away from zero, positive point estimate that is
  simply not separable from the placebo distribution — is a defensible
  result and is what the pre-written contract was for. It is not a
  failure of the pipeline; V1b and V1c passing is evidence the pipeline
  works.
- Arm 3 is complete. No further Arm 3 computation is authorized without a
  new ADR; re-running specifications after seeing this verdict would
  destroy the pre-specification discipline that makes it credible.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote the
affected analysis to exploratory, per ADR 0019.
