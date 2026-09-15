# ADR 0019: Eighteen-month execution roadmap, from diagnosis and design to tested prediction and causal evidence

Date: 2026-07-03
Status: accepted 2026-07-30 as amended. See ADR 0033 for the consolidated
amendment ledger (Arm 1 struck by ADR 0029; Phase 1 FTAS long-lead struck by
ADR 0032; Arm 3 closed by ADR 0031). The Arm 1 text below records what was
believed when the pre-specifications were frozen. Later prose edits preserve
the decisions, dates, and pre-specification record.

## Context

The thesis is written end-to-end (ADR 0014), defended in posture (ADR 0015),
bounded (ADR 0016), framed (ADR 0017), and carries a frozen intervention
pre-registration (ADR 0018). About 18 months remain, with a target of
December 2027. The current thesis is *diagnosis + design*. The remaining time
can add tested prediction and causal evidence if confirmatory reasoning is
frozen before new outcomes are inspected. Mechanical work, drafting, and
interpretation then follow the written specifications.

Candidate arms considered:

- **Arm 1. Run Direction B.** Stage 1 (online vignette, closes
  2026-08-16 under the PBL companion deployment) → prereg gates (ADR 0018)
  → Stage 2 on-site QR intercept. Converts Chapter 6 from proposal to
  confirmatory result.
- **Arm 2. Out-of-sample test of the transience/durability claim.** Extend
  JTA, FTAS, and mobile-panel windows through 2025–2026 and test the
  ADR 0017 headline as a *prediction*: decay where anchors are absent,
  persistence at Eiheiji/Sakai, and the friction→lift association
  (r = 0.826, n = 13) evaluated on months the model has never seen. This is
  the direct answer to Seam B: it turns Direction C from hypothesis-bridge
  into a tested prediction. A falsification is also a thesis result.
- **Arm 3. Kanazawa 2015 template replication.** Apply the same pipeline
  (SCM opening surge, decay curve, anchor-conversion geography) to the 2015
  Hokuriku extension terminus, which now has 9+ years of post-period data.
  Validates the ADR 0017 claim that the *template* is the exportable object.
  Also the natural spine of a journal manuscript.
- **Arm 4. PBL review corpus as a convergent-validity layer.** Correlate
  review-derived friction rates (6,036 deduplicated multilingual Google
  reviews, human-reviewed codebooks) with FTAS friction prevalence by
  POI/municipality. Strengthens Seam A (independent instrument agreeing with
  the survey tags). Measurement validation only. It is never causal evidence
  (CONTEXT.md guardrail stands).
- **Arm 5. New paid data pulls (TripAdvisor; Korean/Japanese platform
  APIs).** Deferred; see decision rule below.

## Decision

Adopt Arms 1 and 2 as primary, Arm 3 as secondary (publication spine),
Arm 4 as conditional, Arm 5 as deferred-with-decision-rule.

### Roadmap

**Phase 0, now through the next few days.** Produce, in priority order, the
artifacts that must be written before new outcomes are inspected:

1. **ADR 0020 — frozen out-of-sample prediction criteria for Arm 2.** The
   whole evidentiary value of Arm 2 depends on the predictions (which
   municipalities decay, which persist, what association magnitude counts as
   confirmation, what falsifies) being written down *before* any post-2024
   extension data is pulled or inspected. This is the single most
   time-critical task. Once new data is seen, the option to pre-specify is
   gone.
2. **Arm 3 design spec.** Template-transfer definition: what must be held
   fixed (fit gates, event-window logic, falsification battery), what is
   allowed to differ (donor pool, anchor candidates), success criteria, and
   the limit that 2015 lacks the mobile-panel layer, so the Kanazawa
   test covers the SCM/decay/anchor-geography portions of the template only.
3. **Direction B Stage-2 fielding playbook.** Contingency tree around the
   ADR 0018 gates: timetable-verification protocol (the open TODO), station
   permission and ethics-approval dependencies, seasonal fielding windows
   (autumn 2026 foliage vs spring 2027), and what each Stage-1 outcome band
   (d̂ ≤ 0; weak-positive; strong) triggers operationally.
4. **Thesis v2 chapter architecture.** Where each arm's results land, how a
   *negative* result in each arm is written up without breaking the ADR 0015
   seams, and which existing chapter text becomes stale under each outcome.

Rhythm unchanged: one artifact at a time, human review between, human
commits.

**Phase 1, 2026-07 to 2026-09.**
- Human, long-lead (start immediately): FTAS new-wave access request;
  station-area intercept permission for Stage 2; ethics/IRB process for
  on-site intercept.
- Codex: stimulus transit-fact verification against current timetables
  (closes the last TODO and the ADR 0018 fielding precondition).
- Stage 1 closes 2026-08-16 → analyze exactly per prereg → apply sign-based
  no-go and re-power rule.
- Codex: data-pull scaffolding for extended JTA/FTAS/mobile windows. Build
  and test it, but do not inspect post-2024-extension outcomes until
  ADR 0020 is accepted.
- Codex: Kanazawa data-availability audit (JTA prefecture-month coverage
  back through 2013, municipal overnight series, donor-pool candidates).

**Phase 2, 2026-10 to 2027-03.**
- Stage 2 fielding (window per playbook; hybrid recruitment if re-powered
  n > 360/arm per ADR 0018).
- Codex: run Arm 2 per frozen ADR 0020; run Arm 3 per design spec.
- Journal manuscript from existing Chapters 3–4 (+ Arm 3 if timely):
  submit early in this phase so one review cycle fits before submission.
  Peer review doubles as an external mock defense.
- Arm 4 if capacity permits: it reuses committed aggregates and existing
  pipelines; no new data spend.

**Phase 3, 2027-04 to 2027-09.** Stage 2 analysis (frozen plan), Chapter 6
rewrite as results, Arm 2/3 results chapters, revise-and-resubmit handling.

**Phase 4, 2027-10 to 2027-12.** Integration pass (successor to ADR 0014),
limitations refresh, defense preparation.

### Arm 5 decision rule (paid data)

Do not pay yet. Rule: spend on new platform data only if (a) Arm 4 on the
*existing free* corpus shows a validation signal worth reporting, and (b) the
new source adds coverage the corpus lacks, not volume it already has.

- **TripAdvisor:** fails (b) as proposed. It skews to the same
  English-language inbound perspective already covered by 919 EN Google
  reviews, and the official Content API is believed to return only a
  handful of recent reviews per location (full pulls require third-party
  scrapers at real cost). Verify limits before any spend (Codex task).
- **Korean sources (e.g., Naver blog/café search):** the only new language
  coverage. The corpus currently has zero Korean-language data while Korea
  is the largest inbound market to Japan. Real cost is not API fees but a
  Korean friction codebook requiring native-speaker validation. If pursued:
  free-tier pilot of 100–200 items first; promote only if friction
  categories are extractable at rates comparable to zh/EN/JP.
- **Japanese OTA sources (Jalan, Rakuten Travel, Tabelog):** review text is
  largely not available via official APIs; scraping is ToS-risky and the
  4,037 JP Google reviews already cover the language group. Skip.

All Arm 5 outputs, if any, inherit the side-layer guardrail: measurement
validation and description only, never thesis causal evidence.

### Work allocation

- **Research lead:** Phase 0 artifacts only: frozen rules, designs,
  contingency trees, and chapter architecture.
- **Codex:** data pulls, pipeline ports, verification scripts, splices with
  verbatim-match oracles, citation filling, running pre-specified analyses.
- **Drafting support:** interpretation memos as results land, chapter drafting
  against the Phase 0 architecture, and journal-response drafting. The research
  lead records any decision that amends a frozen rule in a new ADR. Under ADR
  0018's deviation discipline, that amendment demotes the affected analysis to
  exploratory.

### Gates and stopping criteria

- Arm 1 is governed entirely by ADR 0018; this roadmap adds no new analysis
  discretion. If Stage 1 returns d̂ ≤ 0, Stage 2 dies under the current
  preregistration and the thesis returns to design-not-evidence framing, which is
  already written and defensible.
- Arm 2 proceeds only after ADR 0020 is accepted; if the prediction fails,
  the falsification is reported as a first-class result (the template
  claim of ADR 0017 is what's at stake, and a bounded template is still a
  contribution).
- Arm 3 stops if the data-availability audit shows the pre-period cannot
  support the fit gates. It supports publication but is not a
  submission dependency.
- No arm may silently edit the existing seven chapters; all integration
  goes through the Phase 4 pass with its own review.

## Consequences

- The submission-ready thesis is never at risk: every arm degrades to the
  current, already-defensible text on failure.
- Phase 0 focuses on artifacts that cannot be recovered later:
  pre-specification, designs, and contingency trees. It does not cover
  mechanical execution governed by written specifications.
- Two long-lead human dependencies (FTAS access, station/ethics permission)
  are surfaced now; either one slipping compresses Phase 2 and makes the
  spring-2027 fielding window the fallback.
- Paid data acquisition is bounded by a rule instead of appetite.

## Rejected alternatives

- **Journal submission after Stage 2 results (late 2027):** would leave no
  room for a review cycle before submission. Existing Chapters 3–4 are
  publishable.
- **Committing to TripAdvisor/Korean pulls now:** spends money before the
  free validation test (Arm 4) establishes that review-corpus validation
  earns thesis space at all.
- **Treating Arm 3 as primary:** highest novelty, but it neither closes a
  seam (Arm 2 does) nor produces causal evidence (Arm 1 does); it serves
  publication, which is secondary to the degree.
