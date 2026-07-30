# ADR 0023: Thesis v2 chapter architecture — outcome-branched landing zones fixed before results exist

Date: 2026-07-04
Status: accepted 2026-07-30 as amended — see ADR 0033 for the consolidated
track ledger (Track B retired by ADR 0029 §4; Track T resolved V1-fail by
ADR 0031). §5's "no chapter file changes before Phase 4" is accepted and
binding. Body unedited.

## Context

Phase 0 item 4 of ADR 0019, and its last item: decide where each arm's
results land in the written thesis, how negative results are written up
without breaking the ADR 0015 seams, and which existing text goes stale
under each outcome branch. The seven v1 chapters are written, defended in
posture (ADR 0015), and protected by ADR 0019's rule that no arm may
silently edit them. The risk this ADR removes: chapter surgery designed
after results arrive bends toward the results — the prose-side analog of
the analytic flexibility ADRs 0018/0020/0021 already froze.

## Decision

Adopt `docs/thesis/thesis_v2_architecture.md` as the frozen integration
blueprint, executed only by the Phase 4 pass. Core choices:

1. **Chapter map: 1–6 numerically frozen; one new chapter; one renumber.**
   Chapter 6 absorbs Direction B's Stage-1 estimation and Stage-2
   result/no-go (its design already lives there; ADR 0019 Phase 3 said
   "Chapter 6 rewrite as results"). New Chapter 7 — "The template under
   test: out-of-sample and out-of-corridor" — carries Arm 2 (§7.1 frozen
   prediction, §7.2 verdict) and Arm 3 (§7.3, detachable). Conclusion
   renumbers 7→8, the only renumbering, chosen because nothing
   forward-references §7.x except the master file.
2. **Chapter 7 exists under every branch** (Arm 2 reports even when
   falsified, per ADR 0020's first-class-falsification contract), and
   §7.1 is drafted from the frozen prediction now — outcome-invariant,
   and at the defense it is the exhibit of ex-ante commitment. A
   coherence rule forbids "fixing" its pre-result tense after the
   verdict.
3. **Direction B never enters Chapter 7**: its result is intervention
   evidence under ADR 0018, not a template-prediction test under
   ADR 0020; the chapter boundary preserves the prereg boundary.
4. **Outcomes factor into independent claim tracks** — D (durability/
   Arm 2), B (intervention/Arm 1), T (template/Arm 3), M (measurement/
   Arm 4, appendix-only) — each with pre-written negative-outcome shapes:
   Band-N no-go framed as the sign rule working (and explicitly not as a
   mechanism falsification, which is Track D's verdict alone); a Stage-2
   null framed through the ceiling logic as an informative bound; a
   backfire result landing in the pre-built manipulable-margin
   limitation; Arm 2 falsification bounding the canonical claim sentence
   via a new ADR with §1.2 and §8.2 moving together (ADR 0017); Arm 3
   V1-failure readings confined to §7.3 with Chapter 5 untouched.
5. **Seam-preservation rules are binding on all branches**: concessions
   already priced are never re-argued and never retracted; upgrades and
   bounds route through the enumerated sentences only; Chapter 5 has no
   stale-text row under any branch; §6.2 keeps hypothesis staging even
   under Arm 2 confirmation.
6. **A stale-text matrix (G/D/B/T rows)** enumerates every edit with its
   trigger and mechanism — Codex splice with verbatim oracle vs
   ADR-gated rewrite. Notable: the always-stale set fires regardless of
   outcomes (§6.3's "not a run experiment" goes stale the moment Stage 1
   closes; §7.4 "From design to field" is future-tense about events that
   will have happened; §6.3's intercept-only Stage-2 description is
   already stale against ADR 0022's hybrid-by-arithmetic finding).
   Figures 10–13 are reserved for Arm 2/3 now to avoid renumbering.

## Consequences

- Every arm outcome, including every negative one, has a pre-committed
  prose destination; the Phase 4 pass becomes largely mechanical, and
  drafting can be routed to mid-tier seats against this blueprint.
- The degradation guarantee of ADR 0019 becomes concrete: the
  directional-only / Band-N / killed branches require between zero and a
  handful of bounded edits, so the submission-ready thesis is provably
  never hostage to results.
- The cost is two commitments made blind: the conclusion renumbering
  (7→8) and the reservation of Chapter 7's structure even if Arm 3 dies
  and §7.2 is a single directional-only paragraph — accepted, since a
  thin honest chapter beats a reflowed thesis.
- `thesis_master.md` remains normative for v1 until the Phase 4 pass
  adopts the v2 map by editing it first (matrix row G5); nothing changes
  in any chapter file before that.

## Rejected alternatives

- **Separate results chapters per arm** (Arm 2 chapter + Stage-2 chapter
  + Kanazawa chapter): produces empty or near-empty chapters on the
  no-go/killed branches and scatters the "claims exposed to new data"
  act across the book; one chapter with detachable sections degrades
  gracefully.
- **Folding Arm 2 into Chapter 5** ("more robustness"): breaks Seam C's
  narrow conjunction (Ch. 5 is about March 2024 and is untouched by
  design) and would let a falsified prediction read as a retraction of
  the robustness battery, which it is not.
- **Placing the durability test before the intervention chapter** (new
  Ch. 6, pushing C+B to 7): reads causally cleaner but renumbers §6.x,
  which §7 and multiple ADRs reference — maximal splice surface for
  zero evidentiary gain.
- **Appendix-only treatment of Arm 2**: the v2 thesis's entire upgrade is
  tested prediction as first-class evidence; an appendix placement
  contradicts ADR 0019's rationale for running the arm at all.
- **Deferring this architecture until results exist**: the failure mode
  this ADR exists to prevent; post-hoc architecture is post-hoc framing.
