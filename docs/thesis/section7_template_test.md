# 7. The Template Under Test: Out of Sample and Out of Corridor

> **Status note (remove at Phase 4 integration).** This file is the v2
> Chapter 7 established by ADR 0023. Until the Phase 4 pass adopts the v2
> chapter map in `thesis_master.md`, the v1 numbering remains normative and
> `section7_conclusion.md` keeps the number 7; this draft is inert. §7.1 is
> drafted now, before any test data exist, because its value at the defense
> is precisely its date; per ADR 0023 §5, its pre-result tense is preserved
> verbatim once results arrive. §7.2 and §7.3 are reserved stubs whose
> shapes are pre-committed elsewhere (ADR 0020; ADR 0021).

## 7.0 Purpose

Chapters 4–6 close on two claims that data available at the time of writing
could motivate but not test: that the extension's demand shock is durable
only where station arrivals convert to destination anchors, and that the
diagnostic template — fit-gated synthetic control, an event window matched
to the effect's shape, a falsification battery, and a friction diagnosis
pointing at the conversion — is an exportable object rather than a
Fukui-specific artifact. This chapter exposes both claims to data that
could not have shaped them. Section 7.1 states the predictions exactly as
they were frozen in July 2026, before any of the test data existed; it is
reproduced from the governing pre-specification (ADR 0020) and is quoted,
not paraphrased, wherever the verdict is later discussed. Section 7.2
reports the out-of-sample verdict on the durability claim. Section 7.3
reports the template's replication on the March 2015 Kanazawa extension —
out of corridor, on frozen constants (ADR 0021). The two tests are
deliberately different in kind: §7.2 risks the *claim* on months the models
have never seen; §7.3 risks the *machinery* on an event the pipeline was
never tuned to.

## 7.1 The prediction, frozen July 2026

Everything in this section was fixed — thresholds, sidedness, falsification
conditions, and the boundary between data the thesis had seen and data it
had not — before any post-freeze observation was fetched, opened, or
summarized, by any seat of the project, human or automated. The governing
document is ADR 0020 (accepted July 2026); deviations after its acceptance
are themselves logged and demote the affected analysis to exploratory. The
freeze exists because the option to pre-specify dies the moment new data is
seen: this section is the thesis's answer to the reasonable suspicion that
a durability story assembled on 2024–2025 data merely organizes the past.

**The seen/unseen boundary.** Seen: the mobile-location municipal panel
through December 2025 (vintage pinned by checksum); FTAS and the merged
tri-prefecture survey through the June 2026 waves (n = 103,807 as
committed); the JTA accommodation panel through the 2024 confirmed and 2025
preliminary vintages. Unseen, and quarantined until the frozen scripts run:
any mobile-panel months after 2025-12, any survey waves after 2026-06, and
the JTA 2025-confirmed and 2026 rows. The synthetic-control donor weights
are frozen as committed for Chapter 5 (pre-period fit through 2024-02,
pre-RMSPE ≤ 0.15, placebo restriction at 5.0× the treated unit's fit);
the extension *appends* unseen months to existing fits. Nothing is refit
with post-2024-02 data — refitting would absorb exactly the persistence
under test. The predictor — the municipal transport-access friction ranking
from the seen survey waves — is likewise frozen, deliberately forgoing any
improvement from newer waves as the price of a clean prediction.

**P1 — regime persistence (co-primary).** On unseen panel months from
January 2026 onward (minimum six unseen months, else the test waits), using
the frozen weights: both high-confidence durable municipalities — Sakai
(JIS 18210) and Eiheiji (JIS 18322) — show a positive mean gap over their
synthetic controls, and the durable-set mean gap exceeds the mean gap of
the high-confidence transient set — Awara (18208), Fukui City (18201),
Tsuruga (18202), Sabae (18207). Inference is a one-sided in-space placebo
test at α = 0.05 on the durable-minus-transient difference, using the same
well-fit donor machinery as Chapter 5, with no new discretion. *Confirmed*
requires both sign conditions and placebo p ≤ 0.05; signs without
significance is *directional-only*; a durable-set mean at or below the
transient-set mean, or either durable municipality's mean gap at or below
zero, is *falsified*.

**P2 — the friction ordering out of sample (co-primary).** Across the
thirteen high-confidence municipalities, the Spearman rank correlation
between the frozen transport-access friction ranking and the unseen-window
mean gap ranking is positive. *Confirmed* at ρ ≥ 0.48 (the one-sided
α = 0.05 critical value at n = 13); 0 < ρ < 0.48 is *directional-only*;
ρ ≤ 0 is *falsified*. The in-sample correlation (r = 0.826) is explicitly
not the bar: at n = 13 that magnitude is noise-inflated, and the claim
under test is sign and ordering, not magnitude replication.

**The headline requires both.** One primary alone is reported as partial
support, never as confirmation. Three secondary predictions are reported
but never headlined: the Chapter 3 DiD coefficients remain non-negative on
unseen survey waves (S1 — shrinkage is consistent with the claim; a sign
reversal with confidence interval excluding zero is reported as discordant
with Chapter 3); prefecture-level overnight stays revert toward the
pre-extension trend in the unseen JTA rows (S2 — the transient-by-default
component at the aggregation where it should appear); and transport-access
friction among shinkansen arrivers remains the largest friction category
with a rail-versus-car gap above 2× in unseen waves (S3 — the seen value is
≈ 4.0×, 7.09% against 0.66%; erosion below 2× would say the constraint is
resolving itself, which feeds the intervention's fielding decision and
gates nothing else).

**Guards.** Vendor panels revise history, so before any unseen-window
computation the new vintage's 2021–2025 series is verified against the
pinned one; a root-mean-square relative revision above 2% for any
confirmatory municipality, or any donor exiting the fit gate under revised
history, stops the analysis and forces a logged decision between re-running
the entire chain on the revised vintage as the single canonical series or
demoting the test to exploratory. Mixing vintages within one analysis is
forbidden.

**What each verdict was committed to mean — written before the result
existed.** Both primaries confirmed: the durability account of Chapter 6 is
promoted from hypothesis-bridge to tested prediction, and the third
limitation of the conclusion is rewritten to say so. Directional-only:
consistent but underpowered; the limitation stands as written; nothing is
promoted. Either primary falsified: the falsification is a first-class
result of this thesis — the anchor-conversion account organizes 2024–2025
but fails prospectively; the claim is bounded to the seen window, the
diagnosis of Chapter 4 is unaffected (it never depended on durability), and
the contribution re-weights onto the diagnosis and the honest test itself.
No outcome licenses reopening the seen-window analyses: post-hoc
reconciliation is exploratory by definition. The reader holding this
chapter therefore holds, in either direction, a result whose meaning was
priced before it was known.

## 7.2 The verdict

*(Reserved. Reported per the ADR 0020 interpretation contract quoted in
§7.1; drafted only after the frozen scripts run on the quarantined data.
Secondary predictions S1–S3 are reported here, never headlined.)*

## 7.3 The template out of corridor: Kanazawa 2015

*(Reserved. Reported per the ADR 0021 success criteria and interpretation
contract — V1 pipeline validation, V2 durability geography, V3 descriptive
anchors — with the specification frozen in `arm3_kanazawa_design.md`
before any Arm 3 computation. If the replication publishes first in the
journal manuscript, this section compresses to its result and citation.)*
