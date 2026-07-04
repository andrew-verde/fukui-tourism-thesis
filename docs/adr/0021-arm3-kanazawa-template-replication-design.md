# ADR 0021: Arm 3 — Kanazawa 2015 template-replication design

Date: 2026-07-04
Status: proposed (pending human review)

## Context

ADR 0019 adopts Arm 3 — replicating the Direction D pipeline on the March
2015 Nagano–Kanazawa Hokuriku Shinkansen extension — as the secondary arm
and publication spine, killed "if the data-availability audit shows the
pre-period cannot support the fit gates." The Codex audit
(`docs/arm3_kanazawa_data_audit.md`, checked 2026-07-03) has now
established, VERIFIED: (a) the pinned JTA 推移表 workbook carries a
consistent 47-prefecture monthly overnight-stays panel (total/Japanese/
foreign) from 2011-01 — wholly after the 2010-Q2 survey-frame expansion —
through the full replication window; (b) no municipal monthly panel exists
for 2015 anywhere: the JTTA mobile-derived series begins 2021-01, and
Ishikawa publishes no balanced municipality-month series, only Kanazawa
city monthly lodging (2014+) and monthly point counts (incl. 兼六園) in
PDF reports; (c) the donor pool must handle co-treatment (new-segment
prefectures; Hokkaido Shinkansen 2016-03) and in-window disasters (2011
Tōhoku, 2016 Kumamoto, 2018 floods/quakes).

What Arm 3 is for: ADR 0017 names the *template* as the exportable object,
subordinated to the empirical claim. The 2015 Kanazawa boom is public
knowledge, so Arm 3 is a replication/validation of the template's
machinery — never a prediction test (that is Arm 2 / ADR 0020's word).

## Decision

Adopt `docs/thesis/arm3_kanazawa_design.md` as the frozen Arm 3
specification. Its core commitments:

1. **Kill criterion resolved: proceed.** The audit's §1 verdict places the
   entire 38-month primary pre-window (2012-01..2015-02) inside a
   consistent single-design panel. Scope is reduced to the
   SCM/decay/anchor-geography portions at prefecture grain, exactly as
   ADR 0019 anticipated.
2. **Verbatim transfers** (template held fixed): Frank–Wolfe convex SCM,
   log outcome, `GOOD_FIT_RMSPE = 0.15`, `RMSPE_FIT_MULT = 5.0`,
   opening window = first two post-event months, one-sided in-space
   placebo with two-sided disclosed, backdated in-time placebo at
   event − 12, leave-one-out donors, gap-only inference, 38-month
   pre-window, randomization p-value formula.
3. **Declared differences**: `EVENT_YM = 201503`, `INTIME_EVENT_YM =
   201403`; treated = Ishikawa (17) primary + Toyama (16) companion;
   outcome = JTA prefecture-month total overnight stays (mobile layer
   does not exist pre-2021); donor pool = 34 prefectures (audit §4 main
   exclusion rule; strict 20-donor sensitivity); confirmatory post-window
   2015-03..2019-12, ending before COVID and the 2024 corridor
   re-treatment.
4. **One new component**, forced by the 58-month post window: a late
   window (2018-01..2019-12) persistence statistic tested with the same
   in-space placebo machinery, plus a descriptive decay ratio. Direction D
   could not test persistence in 22 post months; the durability clause
   needs it here.
5. **Attainable-significance floor rule**: with ≤ 34 donors the one-sided
   p floor is ≈ 0.029; if fit-gate attrition leaves < 19 placebos, p ≤
   0.05 is unattainable and the affected test is capped at
   directional-only — a granularity limit, not evidence.
6. **Success criteria and interpretation contract** fixed ex ante: V1
   (opening surge + silent backdate + leave-one-out away from zero) must
   all pass to claim the template transfers; V2 (Ishikawa late-window
   persistence + Ishikawa > Toyama contrast) carries the
   durable-where-anchored clause; V3 (Kanazawa lodging / Kenrokuen
   series) is descriptive only. Each failure branch has a pre-written
   reading; none touches the committed 2024 results or Arm 2's language.
7. **ADR 0020 firewall interaction**: the 推移表 workbook physically
   contains months that are unseen under ADR 0020 (JTA 2025 confirmed
   values). The Arm 3 loader slices to ym ≤ 201912 before any value is
   read, with a test asserting the boundary; the descriptive
   through-2024 appendix figure may use only vintages ADR 0020 already
   declares seen.
8. **Honest limits stated in the spec and binding on later prose**: no
   mobile-panel layer and no friction-survey layer exist for 2015, so
   Arm 3 validates the causal-demand and durability-shape machinery, not
   the friction diagnosis; outcome margin differs (overnight stays incl.
   business travel); anchors are PDF-derived point counts with a 2014
   floor.
9. **Routing**: Codex implements against the spec's oracles (constants
   verbatim, window boundaries, donor lists, vintage cross-check against
   the corrected 2011–2017 annuals, slice guard); mid-tier seat writes
   interpretation memos; human commits before any computation runs.
   Post-acceptance deviations require a new ADR and demote the affected
   analysis to exploratory.

## Consequences

- The journal manuscript (ADR 0019 Phase 2) gains its replication spine
  with every analytic choice pre-declared; referee questions about
  forking paths have a dated answer.
- A V2 failure would bound the durable-where-anchored clause to the 2024
  event — priced in advance as a first-class, publishable outcome.
- The prefecture grain means Arm 3 can corroborate but never substitute
  for Arm 2: only Arm 2 tests the friction→durability mechanism, and the
  two arms' vocabularies (replication vs prediction) are kept disjoint.
- The 2013 JTA corrections (which touched Ishikawa specifically) make the
  vintage cross-check oracle load-bearing, not ceremonial.
- Codex overwrote the pre-existing untracked audit draft at
  `docs/arm3_kanazawa_data_audit.md` with the 2026-07-03 audit; the
  committed history is unaffected, but any content unique to the earlier
  draft is gone and should be re-flagged by the human if it mattered.

## Rejected alternatives

- **Municipal SCM for Ishikawa 2015**: no balanced municipality-month
  panel exists (audit §§2–3, VERIFIED); Kanazawa-only city series lack
  donors at like grain. Municipal ambition survives only as descriptive
  anchor evidence.
- **Post-window through 2024 ("9+ years")**: COVID from 2020-01 destroys
  donor comparability and the 2024-03 Tsuruga extension re-treats the
  corridor; a 58-month clean window beats a 116-month contaminated one.
  The longer arc appears only as a marked descriptive figure.
- **Framing Arm 3 as an out-of-sample prediction test**: the outcome is
  common knowledge; claiming prediction credit would be dishonest and
  would cheapen Arm 2's genuine freeze. Rejected outright.
- **Magnitude-replication success bar** (Kanazawa surge ≈ Fukui's
  +29.2%): different outcome variable, grain, era, and inbound regime
  make magnitudes incommensurable; sign/ordering criteria carry the
  claim (mirrors ADR 0020's rejection of a magnitude bar).
- **Two-sided primary tests**: the surge and persistence predictions are
  directional and pre-declared; the Seam C posture (one-sided by design,
  two-sided disclosed) transfers with the template.
- **Adding event dummies instead of donor exclusions**: SCM weights can
  concentrate on a contaminated donor, and several shocks fall in the
  post-period where masking weakens the comparison (audit §4); exclusion
  plus leave-group-out sensitivity is the conservative default.
