# ADR 0018: Direction B pre-registration — frozen decision rules

Date: 2026-07-03
Status: accepted

## Context

Task 4 of the reasoning queue, gated on the human confirming the pilot will
run (confirmed 2026-07-03). Pre-registration is the one artifact where
errors are irreversible — a stopping rule or power model cannot be fixed
post hoc — so the reasoning seat's job was to freeze the decision rules,
not to restate the instrument. `experiments/nudge-pilot/DESIGN.md`
(approved 2026-07-02) already specifies design, power table, the ceiling
framing, the re-power rule, and a feasibility mitigation ladder; it leaves
several confirmatory-critical rules implicit. Deliverable:
`docs/thesis/directionB_preregistration.md`, which governs over DESIGN.md
where they differ.

## Decision

The pre-registration freezes DESIGN.md's design verbatim (five conditions,
primary contrast `control` vs `transport_access`, three-task rotation,
stratified blocks of five, server-side assignment, mixed-model primary
analysis, d = 0.25 as selection ceiling, Stage-1 n = 50/arm non-confirmatory,
`d_plan = max(0.10, d̂ − SE(d̂))`) and makes the following previously
implicit rules explicit and binding:

1. **Sign-based no-go:** if Stage-1 d̂ ≤ 0 on the primary contrast, Stage 2
   does not proceed under this pre-registration; design revision is logged
   in a new ADR. Rationale: the re-power rule alone would send a wrong-signed
   prior to the d = 0.10 floor and command 1,570/arm — maximum confirmatory
   spend on the mechanism's worst news. The floor is for weak-positive
   priors, not negative ones.
2. **Quantified recruitment trigger:** the DESIGN.md mitigation ladder is
   converted into a rule with a threshold — re-powered requirement
   > 360/arm (the ~six-month intercept-only bound at d_plan ≈ 0.21) ⇒
   hybrid recruitment (screened online panel main sample + nested QR
   intercept external-validity subsample, n ≈ 300–500, direction-consistency
   only); arm reduction before window extension if hybrid is unavailable.
3. **Fixed-n stopping, both stages:** no interim efficacy or futility looks
   anywhere; Stage 1's estimates flow only into the re-power rule.
4. **Two-sided primary test retained** (α = 0.05) despite the directional
   H1: stricter standard, and an information nudge has a plausible backfire
   channel (friction salience) that a one-sided test would define away.
   This is deliberately opposite to the SCM's one-sided posture, where
   direction was entailed by the intervention (ADR 0015, Seam C) — recorded
   here so the asymmetry reads as reasoned, not inconsistent.
5. **Exclusion and validity rules:** completes-only primary analysis with
   CONSORT-style flow; fallback-assigned (non-server) observations
   unconditionally barred from confirmatory analysis; no outcome- or
   accuracy-based exclusions; no imputation of the primary endpoint.
6. **Evidence firewall:** the document licenses exactly one confirmatory
   claim (Stage-2 H1 test) and enumerates the readings it forbids —
   Stage-1 estimates as effects, the ceiling as an expectation, the nested
   intercept as independent confirmation, or the design's existence as
   support for Direction C. Post-fielding deviations are logged by ADR and
   demote affected analyses to exploratory.

## Consequences

- Stage 2 cannot be silently launched against a wrong-signed or unmeasured
  prior, and cannot silently drift to intercept-only fielding at an
  infeasible n; both failure modes now require a visible, logged decision.
- The thesis (§6.3–6.4) and the pre-registration state the same rules; the
  prereg adds bindingness, not content — no chapter edits required.
- The ~1,000/arm half-ceiling case is publicly priced as beyond intercept
  reach (17 months at FTAS-scale capture), which commits the project to the
  hybrid path early rather than discovering it mid-field.
- Timetable verification of stimulus facts is a named fielding
  precondition; fielding without it is a protocol deviation.

## Rejected alternatives

- **One-sided primary test:** rejected — see Decision 4; symmetry with the
  SCM posture was considered and deliberately not adopted because the
  epistemic situations differ (predicted-direction infrastructure shock vs
  manipulable nudge with a backfire channel).
- **Group-sequential Stage 2 with interim looks:** rejected — sequential
  boundaries buy little at these effect sizes, complicate the mixed-model
  primary analysis, and reintroduce exactly the post-hoc flexibility the
  pre-registration exists to remove.
- **A futility bound above zero (e.g., no-go if d̂ + SE < 0.10):** rejected —
  Stage-1 SE at n = 50/arm (~0.20) makes such a rule trigger-happy against
  true small-positive effects; the sign rule catches the decisive failure
  mode without eating the weak-positive region the floor exists to protect.
- **Powering Stage 2 at d̂ (point estimate):** rejected — winner's-curse
  exposure on an optimistic prior; the lower-bound rule was already the
  design's intent and is kept.
- **Absorbing the prereg into DESIGN.md:** rejected — the instrument doc
  legitimately keeps evolving (copy, stimuli, engineering); the prereg must
  freeze. Governance is one-directional: prereg governs on conflict.
