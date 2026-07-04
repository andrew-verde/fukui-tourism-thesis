# ADR 0022: Direction B Stage-2 fielding playbook — operational contingencies frozen before Stage-1 readout

Date: 2026-07-04
Status: proposed (pending human review)

## Context

Phase 0 item 3 of ADR 0019. ADR 0018 froze Direction B's analysis and
decision rules (sign-based no-go, `d_plan = max(0.10, d̂ − SE(d̂))`, the
360/arm hybrid trigger, fixed-n stopping, two-sided primary). What remained
unfrozen was everything operational: which arms field under which prior,
which season the station intercept uses, how permissions and ethics
sequence against the 2026-08-16 Stage-1 close, and the
timetable-verification protocol that is both the last open TODO and an
ADR 0018 fielding precondition. Operational choices made *after* seeing d̂
are a quieter form of the flexibility pre-registration exists to remove, so
the playbook is written and reviewed now, blind to Stage-1 results.

A derived fact shapes the whole plan: intercept-only Stage 2 requires
n(d_plan) ≤ 360/arm ⇔ d_plan ≥ 0.21, and with Stage-1 SE ≈ 0.20 that
requires d̂ ≳ 0.41 — 1.6× the d = 0.25 selection ceiling. Every plausible
positive Stage-1 outcome therefore lands in hybrid recruitment, making the
station intercept the nested 300–500-complete external-validity subsample,
not the main sample. Permissions, windows, and budgets are sized to that.

## Decision

Adopt `docs/thesis/directionB_stage2_fielding_playbook.md` as the frozen
operational plan. Its commitments:

1. **Contingency tree per Stage-1 band**, gated on a readout memo (target
   2026-08-31) that reports estimation quantities only. Band N (d̂ ≤ 0):
   Stage 2 dies per ADR 0018; permissions withdrawn; thesis stands as
   written; redesign only via new ADR. Band W (positive, N_req > 360/arm —
   the expected branch): hybrid recruitment with sub-decisions fixed now.
   Band S (N_req ≤ 360/arm, i.e. d̂ ≳ 0.41): permitted intercept-only, but
   any d̂ > 0.25 first triggers an outcome-neutral instrument-behavior
   review, since an estimate above the selection ceiling more likely
   signals artifact than effect.
2. **Arm-count matrix, fixed blind to d̂**: five arms if d_plan ≥ 0.15;
   three arms (`control`/`transport_access`/`combined`) if d_plan < 0.15,
   pricing the loss of the single-nudge secondary contrasts in advance.
   This extends ADR 0018's arm-reduction ladder to the cost dimension and
   touches no analysis rule — the primary contrast is identical either way.
3. **Timetable-verification protocol** (closes the TODO): a seven-claim
   inventory from `study-config.json` (single source of truth — `combined`
   concatenates the same strings at runtime), per-claim tolerance bands
   matching the copy's hedged language, operator-official sources with
   archived evidence and sha256 manifest, PASS/AMEND/STRUCTURAL verdicts,
   and re-verification at T−4w/T−1w against Japan's April/October timetable
   revisions. STRUCTURAL findings (a route no longer exists) are
   design-level and require a new ADR before fielding. If Stage 1 fielded
   before verification, that is logged as a protocol deviation, and the
   memo must render one extra verdict — whether Stage-1 participants saw a
   materially false transit fact — because a flawed stimulus contaminates
   the d̂ prior that the re-power rule consumes.
4. **Window rule, fixed now**: intercept subsample fields autumn 2026
   (≈ 10-15 → 12-15, foliage volume) if the full launch gate — readout,
   ethics, permissions, verification — closes by 2026-09-30; otherwise
   spring 2027 (≈ 03-20 → 05-31), with the online main sample launching as
   soon as its own gate items clear. Winter is not a window. Non-concurrent
   main/nested samples are acceptable because the subsample is
   direction-consistency-only; the split is disclosed.
5. **Long-lead sequencing starts now, not at readout**: ethics/IRB
   submission (6–12-week assumption, scoped to both recruitment modes and
   both windows) leads; municipal-forecourt permission inquiries for
   Fukui/Awara-Onsen/Tsuruga follow with the ethics reference
   (station-premises JR West permission only as fallback; police road-use
   permit flagged). A Band-N withdrawal wastes only application effort —
   cheap insurance for the autumn window. Operator/administrator facts are
   marked planning assumptions to confirm on first contact.
6. **Launch gate**: Stage 2 fields only with readout memo accepted,
   verification all-PASS/amended, ethics approved, permissions (or the
   declared main-first split) in hand, server-side assignment live, and a
   launch ADR recording the byte-exact Stage-1 numbers, band, arm count,
   and window.

## Consequences

- Every operational lever that could be bent post-hoc around a
  disappointing d̂ — arm count, window, recruitment mode, yield response —
  now has a pre-committed setting and a logged escape path.
- The autumn-2026 window becomes genuinely reachable because the intercept
  is subsample-sized; if ethics or permissions slip past 2026-09-30, the
  fallback costs one season, not the design.
- The maximum-spend case (d_plan floored at 0.10 → 1,570/arm pre-credit)
  is visible before any money moves: vendor quotes are requested before
  readout, and the launch ADR must affirm the budget or invoke the
  three-arm matrix.
- The still-open Stage-1 verification precondition is surfaced rather than
  papered over; whichever way the facts land, the handling is pre-written.
- Codex and human tasks are separated with an action register; nothing in
  the field path requires the reasoning seat after this document.

## Rejected alternatives

- **Deciding arm count after the Stage-1 readout**: the standard path, and
  exactly the researcher-degrees-of-freedom this playbook exists to close;
  the cost matrix is knowable now, so it is fixed now.
- **Holding the intercept to concurrency with the online main sample**:
  would sacrifice the autumn window (or the spring fallback) for a
  property the prereg never demanded of a direction-consistency subsample.
- **Winter fielding to save the 2026 calendar**: corridor volume and
  Eiheiji access collapse; a passive QR intercept would starve below the
  300 floor and the shortfall would be structural, not operational.
- **Treating d̂ > 0.25 as good news to fast-track**: an estimate above the
  selection ceiling contradicts the design's own effect-size logic; the
  outcome-neutral instrument review is the honest response, and it changes
  no frozen rule.
- **Waiting for Stage-1 results before starting ethics/permissions**:
  saves nothing (applications are band-independent) and forfeits the
  autumn window entirely; the Band-N sunk cost is trivial by comparison.
