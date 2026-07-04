# Phase 0 red-team memo: ADRs 0020–0023 as a system

**Status: review memo, not a decision document.** Second-order review of
the frozen set — ADR 0020 (Arm 2 criteria), 0021 (Arm 3 design), 0022
(Stage-2 playbook), 0023 (v2 architecture) plus their companion documents —
hunting for contradictions, underspecification, and seams a referee or
examiner could exploit. Companion: `docs/phase0_consistency_audit.md`
(Codex mechanical audit: constants vs sources, threshold re-derivations,
cross-reference integrity). Findings are ranked by how much they could
cost if left unfixed. Each ends with a concrete action and its owner.

## F1 — ADR 0020's P1 placebo test is underspecified for a *set-difference* statistic (highest priority)

**The gap.** P1's inference: "one-sided in-space placebo test at α = 0.05
for the durable−transient gap difference, using the same well-fit donor
municipalities and placebo machinery as Direction D (identical fit gates;
no new discretion)." Direction D's committed machinery
(`causal_robustness.py`) produces *per-unit* placebo gaps and per-unit
fit-gating (drop placebos with pre-RMSPE > 5.0× *the treated unit's*).
P1's statistic is a difference of *set means* — mean gap of {Sakai,
Eiheiji} minus mean gap of {Awara, Fukui City, Tsuruga, Sabae} — and the
committed machinery contains no construction for a set-level null. Two
choices are genuinely open: (a) how pseudo-durable/pseudo-transient donor
sets are formed for the null, and (b) which treated unit's pre-RMSPE
anchors the 5.0× gate when there are six treated units. An examiner who
finds these decided *after* the unseen data arrived can argue the
co-primary's inference was chosen post hoc — exactly the charge ADR 0020
exists to kill.

**Why it is recoverable now.** No unseen data has been fetched. ADR 0020
already requires the analysis scripts and their oracles to be committed
before any unseen pull; pinning the construction there, via a short
addendum ADR, preserves the freeze's value entirely.

**Proposed construction (for the human to freeze in an addendum ADR,
amendable before — never after — first unseen fetch):**
- Null population: donors passing the fit gate, where the gate anchor is
  the **maximum** pre-RMSPE across the six high-confidence treated
  municipalities (most inclusive symmetric reading; sensitivity reported
  at the minimum).
- Null draws: 100,000 seeded partitions (seed = 202601) drawing 2 donors
  as pseudo-durable and 4 as pseudo-transient without replacement;
  statistic = mean(2) − mean(4) of unseen-window mean gaps.
- p = (1 + #{null ≥ observed}) / (1 + N_draws), one-sided, matching the
  committed formula's form.
- Test oracle asserts: seed, N_draws, gate anchor, and that no unseen
  value is read before the vintage-revision guard passes.

**Action:** human accepts/edits the construction → addendum ADR (next
free number) → folded into the Arm 2 Codex implementation spec. Before
any unseen data is touched.

## F2 — Stage-2 population language will be quoted against the hybrid reality (medium)

ADR 0018/prereg §5 leads with "the Stage-2 population is rail arrivers —
the 7.09% base-rate population — via on-site QR intercept," and then, in
the same frozen rule, authorizes the hybrid mode whose *main confirmatory
sample* is a screened online panel. ADR 0022's arithmetic makes hybrid
near-certain. The rule is internally coherent, but its lead sentence
overpromises, and a committee member reading prereg-then-thesis will ask
why the confirmatory population changed. No rule needs amending; the
*framing* must be pre-built: the launch ADR and the §6.3 rewrite (v2
architecture row B1) must define the confirmatory population as screened
Hokuriku rail travelers with the intercept subsample as the
external-validity bridge to actual arrivers, and the defense one-breath
answer is: *the population definition was frozen together with its
feasibility ladder; the ladder fired on pre-registered arithmetic, not on
results.* **Action:** carry this framing into the launch ADR template
(playbook §3) — one paragraph, written at launch, quoting the prereg's
own hybrid clause.

## F3 — ADR 0022's arm-count matrix silently amends ADR 0018's ladder (low, one-sentence fix)

ADR 0018 rule 2 permits arm reduction *if hybrid is unavailable*. ADR 0022
adds cost-triggered arm reduction (d_plan < 0.15 ⇒ three arms) even when
hybrid is available. The playbook argues this "touches no analysis rule" —
true for H1, and it was adopted blind to d̂, which is the substance of the
freeze. But formally it is an amendment to a frozen rule's trigger
conditions, and it should say so rather than be discovered by a careful
reader. Consequences are bounded: H3/H4 die unrun under the three-arm
branch (nothing is demoted because nothing fields). **Action:** on
accepting ADR 0022, add one sentence to its Decision §2 (or record in the
acceptance note): "This is a pre-Stage-1-readout amendment to ADR 0018's
mitigation ladder, adopted blind to Stage-1 outcomes; H1's confirmatory
status is unaffected."

## F4 — ADR 0020's S1 leaves its middle band and estimation window ambiguous (low; fix in implementation spec)

S1: DiD coefficients "remain non-negative" on post-2026-06 waves;
discordant = "sign reversal with CI excluding zero." Two ambiguities:
(a) whether the DiD is re-estimated on the full extended sample or on new
waves only — "same specification" implies full-sample with extended post
window, but it should be pinned; (b) the middle band (negative point
estimate, CI spanning zero) is neither "non-negative" nor "discordant."
S1 is secondary and gates nothing, so this costs little — but pin it
before data: full-sample re-estimation, prediction met iff both point
estimates ≥ 0, middle band reported as "not confirmed, not discordant."
**Action:** into the Arm 2 implementation spec/tests alongside F1; no
separate ADR needed if the addendum ADR from F1 carries both.

## F5 — Late timetable amendments could collide with ethics-approved materials (low; cheap insurance)

Playbook §4 re-verifies stimuli at T−1 week; October revisions publish in
September. If a claim AMENDs a week before launch, the fielded copy
differs from what the ethics application showed. **Action (now, while the
application is with the advisor):** scope the stimuli description as
"transit facts verified against current official timetables, subject to
factual correction before fielding" so factual AMENDs are pre-covered and
never trigger re-review.

## F6 — Known cosmetic and process notes

- The Kanazawa audit's "checked 2026-07-03" stamps are off by one day
  (actual run 2026-07-04; wrong date supplied in the dispatch prompt).
  One-line correction note in the audit header, or accept as-is.
- `docs/arm3_kanazawa_data_audit.md` overwrote an earlier untracked draft
  of the same name (flagged in ADR 0021); if the earlier draft had unique
  content, it is unrecoverable — confirm it didn't.
- `section7_template_test.md` and `section7_conclusion.md` both carry a
  "# 7." heading until the Phase 4 pass renumbers the conclusion; the new
  file's status note declares it inert, and `thesis_master.md` remains
  normative. Expected, not a defect.
- Typhoon Hagibis (2019-10) is flagged in the Arm 3 spec's sensitivities
  but absent from the audit's verified event table; it postdates nothing —
  it simply wasn't in the audit's question list. It remains an open
  Codex verification item at Arm 3 implementation time.

## What was checked and found sound (so the review is not just its findings)

- ADR 0020's firewall vs Arm 3's data needs: the 推移表 slice guard
  (≤ 201912) resolves the only overlap; descriptive extensions restricted
  to declared-seen vintages. No leak path found.
- Arm 3's late-window placebo is per-unit and fully specified — the F1
  set-construction gap does not recur there; V2b's ratio contrast is
  correctly kept descriptive.
- The three claim tracks in ADR 0023 touch disjoint sentences; no
  outcome combination requires contradictory edits to the same passage.
- Direction B language firewall survives every branch of every track,
  including Band N and backfire.
- The one-sided/two-sided asymmetry across the set (SCM and Arm 2/3
  one-sided; Direction B two-sided) is consistently reasoned in each
  document with the same rationale as ADR 0015/0018 — an examiner probing
  for opportunistic sidedness finds the asymmetry argued identically
  everywhere, ex ante.
- §7.1 as drafted (`section7_template_test.md`) restates ADR 0020 without
  adding, dropping, or strengthening any commitment (checked
  clause-by-clause against the ADR).

## Mechanical audit (Codex)

See `docs/phase0_consistency_audit.md` for the full check-by-check table:
constants vs script definitions, Direction D headline numbers vs
`metrics.json`, ADR 0020 frozen inputs vs config and the durability CSV,
the Spearman n = 13 critical-value re-derivation (bears on P2's 0.48),
power-table arithmetic and the 0.21/0.41 boundary re-derivations, Arm 3
donor/window arithmetic, dangling-reference and section-anchor checks.
Any FAIL there that touches a frozen threshold is a candidate for the F1
addendum ADR; cosmetic FAILs route to Codex as splice fixes.
