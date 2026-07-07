# ADR 0024: Mid-Stage-1 amendment of materially false transit stimuli

Date: 2026-07-07
Status: proposed (pending human review; effective on deploy)

## Context

The timetable-verification protocol (playbook ADR 0022 §4; the last open
TODO and an ADR 0018 fielding precondition) was executed 2026-07-07 by
Codex against operator-official sources
(`experiments/nudge-pilot/timetable_verification.md`; 25 archived evidence
files with sha256 manifest under `experiments/nudge-pilot/verification/`).
Verdicts: four PASS, three AMEND, zero STRUCTURAL. Two AMENDs were judged
**materially false**, both in the `eiheiji_half_day` task's
`transport_access` strings shown in the `transport_access` and `combined`
conditions:

1. The config claimed the direct Eiheiji Liner runs "roughly once or twice
   an hour"; the verified service (Keifuku, 2026-04-01 timetable) is six
   direct trips per day, hourly 09:50–14:50, with no departures after.
2. The config implied an evening last-return bus; the verified last direct
   return leaves Eiheiji at 16:20. The round-trip-ticket claim could not
   be verified and is dropped.

A third AMEND (`tojinbo_awara` frequency wording) was judged merely
imprecise. Both false facts err optimistic — they present the last mile as
easier than it is — so continued exposure plausibly inflates the
treatment-arm response and thereby the Stage-1 d̂ prior that the frozen
re-power rule (ADR 0018) consumes. Stage 1 is in the field until
2026-08-16; the playbook pre-committed this situation to a human decision
logged by ADR. Human decision 2026-07-07: **amend now**, mid-Stage-1.

## Decision

1. **The three replacement strings from the verification memo are adopted
   verbatim** into `experiments/nudge-pilot/study-config.json` (the single
   source of truth; the `combined` condition concatenates the same strings
   at runtime). Oracle: the config strings byte-match the "Proposed
   replacement string" cells of `timetable_verification.md` rows 1, 3, 6.
2. **Config `version` bumps 2026-07-02 → 2026-07-07.** The instrument
   writes `version` into every submission (`study_version` in
   `api/submit.js`), so the pre/post-amendment split is keyed in the data
   itself; no timestamp reconstruction is needed once the deploy lands.
3. **Effectiveness requires deployment.** The repo edit changes nothing
   live. The human deploys the amended instrument and records the deploy
   timestamp (UTC) in this ADR's acceptance note; the split key is
   `study_version`, with the deploy timestamp as corroboration.
4. **Stage-1 readout consequences (binding on the readout memo):**
   - Stage 1 remains fixed-n, non-confirmatory, with no interim analysis;
     this amendment is a stimulus correction, not an analysis event, and
     no outcome data is examined in making it.
   - The readout memo reports d̂ and SE(d̂) as pre-registered, and
     additionally reports the pre/post-amendment composition of the
     sample (counts per `study_version` per arm) and a
     direction-of-exposure note as instrument behavior — not as an
     effect estimate and not as a subgroup hypothesis test.
   - The d̂ prior flows through the frozen rules (sign no-go, re-power)
     unchanged, with the contamination disclosed wherever the prior is
     cited: pre-amendment exposure was to optimistically false Eiheiji
     transit facts, biasing d̂ plausibly upward, which the lower-bound
     re-power rule partially — not fully — absorbs.
   - Per ADR 0018's deviation discipline, any analysis distinguishing
     pre/post-amendment responses is exploratory by construction.
5. **Ethics note.** If the ethics application (in advisor review) shows
   stimulus copy, the amended strings replace it, and the F5 clause
   ("transit facts subject to factual correction before fielding")
   covers this class of change going forward.

## Consequences

- Participants stop seeing false transit facts as of the deploy — the
  defensible posture once the falsehood is known, and the reason "amend
  now" beat "hold for uniformity."
- The Stage-1 sample is stimulus-heterogeneous for the primary-contrast
  arms; this is a disclosure burden on a stage that was already
  non-confirmatory, not a validity loss for any confirmatory claim.
- The corrected Eiheiji copy is *less* optimistic than what Stage 2 would
  have inherited unverified, so Stage-2 stimuli now match operator
  reality as of the 2026-04-01 timetables; the T−4w/T−1w re-verification
  cadence (ADR 0022 §4) still applies before fielding.
- The finding itself is thesis-relevant context: the stimulus was false
  in the optimistic direction because the real last-mile service is
  sparser than assumed — the friction Chapter 4 diagnoses, encountered
  by the project's own instrument.

## Rejected alternatives

- **Hold amendment until Stage 1 closes (2026-08-16):** preserves
  stimulus uniformity at the cost of ~6 more weeks of knowingly false
  facts shown to participants; indefensible to an ethics committee and
  unnecessary, since uniformity buys nothing for a non-confirmatory
  stage whose deliverable is a prior that must carry the contamination
  caveat either way.
- **Amend only the two materially false strings, leave the imprecise
  Tojinbo string:** would require a second amendment cycle before
  Stage 2 anyway; one version bump with all three verified corrections
  minimizes version fragmentation.
- **Discard pre-amendment Stage-1 data:** an outcome-blind exclusion the
  pre-registration does not authorize; fixed-n stopping and
  completes-only analysis stand, with composition disclosed instead.
