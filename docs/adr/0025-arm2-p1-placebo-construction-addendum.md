# ADR 0025: Arm 2 addendum — P1 set-difference placebo construction and S1 operational pinning

Date: 2026-07-07
Status: accepted 2026-07-29 (accepted and committed BEFORE any unseen
outcome data was fetched, as this specification required; after that
point it could no longer have been added without demoting P1)

## Context

The Phase 0 red-team (`docs/phase0_redteam_memo.md`, finding F1) found the
one genuine hole in the ADR 0020 freeze: P1's inference is "one-sided
in-space placebo test … for the durable−transient gap difference, using
the same well-fit donor municipalities and placebo machinery as
Direction D," but the committed machinery (`scripts/causal_robustness.py`)
defines only *per-unit* placebo gaps and a per-unit fit gate anchored at
*the* treated unit's pre-RMSPE. P1's statistic is a difference of set
means over six treated units, leaving two choices genuinely open: how
pseudo-durable/pseudo-transient donor sets are formed for the null, and
which treated unit anchors the 5.0× gate. Decided after unseen data
exists, either choice is analyst discretion on a co-primary — the exact
charge ADR 0020 exists to kill. No unseen data has been fetched, so the
specification can still be added at full pre-registered strength.
Finding F4 (S1's ambiguous estimation window and middle band) rides along
because it is fixed by the same implementation spec.

## Decision

This ADR amends ADR 0020 by *adding specification only*: no threshold,
direction, or verdict boundary of ADR 0020 changes.

### P1 placebo construction (frozen)

1. **Placebo donor pool:** donor municipalities (non-Hokuriku, full
   coverage, as in Direction D) whose own placebo pre-RMSPE is
   ≤ 5.0 × the **maximum** pre-period RMSPE across the six
   high-confidence treated municipalities (Sakai 18210, Eiheiji 18322,
   Awara 18208, Fukui City 18201, Tsuruga 18202, Sabae 18207) — the most
   inclusive symmetric reading of the Direction D gate. Sensitivity:
   the same test with the anchor at the **minimum** of the six, reported
   alongside, never headline.
2. **Null distribution:** 100,000 partitions drawn with NumPy seed
   **202601**, each selecting, without replacement from the gated pool,
   2 donors as pseudo-durable and 4 as pseudo-transient. Null statistic
   per draw: mean unseen-window mean-gap of the 2 minus mean of the 4.
3. **Observed statistic:** mean unseen-window mean gap of {Sakai,
   Eiheiji} minus mean of {Awara, Fukui City, Tsuruga, Sabae}, using the
   frozen weights per ADR 0020.
4. **p-value:** one-sided, p = (1 + #{null ≥ observed}) / (1 + 100,000),
   matching the committed formula's finite-sample form. Verdict bands
   exactly as ADR 0020 P1 wrote them.
5. **Test oracle (Codex implementation):** tests assert the seed, the
   draw count, the max-anchored gate (and min-anchored sensitivity), the
   2/4 partition sizes, that frozen weights are loaded (not refit), and
   that the vintage-revision guard runs before any unseen value is read.

### S1 operational pinning (frozen)

1. **Estimation:** the Chapter 3 DiD specifications (NPS and transport
   satisfaction; clustered SEs; earthquake-robust variant) are
   re-estimated on the **full extended sample** — all seen waves plus
   unseen waves after 2026-06 — with the same specification and an
   extended post window; no new-waves-only estimation.
2. **Verdict bands:** prediction met iff **both point estimates ≥ 0**;
   *discordant* iff either coefficient is negative with its confidence
   interval excluding zero; the middle band (negative point, CI spanning
   zero) is reported as "not confirmed, not discordant." S1 remains
   secondary and gates nothing, exactly as ADR 0020 wrote.

## Consequences

- P1's inference machinery is now as fully specified as Direction D's,
  and the freeze's evidentiary value survives intact because the
  addendum precedes any unseen fetch.
- The max-anchored gate choice deliberately favors a larger, harder null
  (more placebos kept) over a flattering small one; the min-anchor
  sensitivity bounds the other direction.
- Codex's Arm 2 implementation task now has a complete oracle; nothing
  about P1 or S1 is left to implementation-time judgment.

## Rejected alternatives

- **Anchoring the gate at each pseudo-set's own units** (per-draw gates):
  makes the null's membership vary by draw, conflating fit selection
  with the statistic; a fixed pool is cleaner and matches Direction D's
  fixed-pool spirit.
- **All possible partitions instead of 100,000 draws:** the exact count
  (pool-choose-2 × remaining-choose-4) is computable but varies with the
  realized pool size; a fixed seeded draw count keeps the oracle
  byte-stable across vintages that pass the revision guard.
- **Deciding this in the implementation PR without an ADR:** the whole
  point is that a co-primary's inference must not be decided by whoever
  writes the code; ADR 0020's own deviation discipline demands the ADR.
