# ADR 0026: Direction B Stage 1 ≠ the PBL vignette experiment — correction of record and frozen usage rule

Date: 2026-07-07
Status: proposed (pending human review; the §2 usage rule should be
accepted before 2026-08-16, when the PBL experiment's results exist)

## Context

Verified 2026-07-07 by deployment audit and a read-only survey of
`hokuriku-tourist-sentiment-analysis`:

- The only live survey deployment (`vignette-survey.vercel.app`, repo
  `vignette-survey-app`) serves a **two-arm** experiment from the PBL
  side-project repo: "visit-readiness card" vs plain-text control, a
  **fictional** attraction ("Echizen Heritage Museum"), primary outcome =
  planning-uncertainty composite (u1–u4), unpaid QR/personal-network
  convenience sample, fixed close **2026-08-16** (pinned 2026-07-03 in
  that repo), Welch-t analysis plan, no IRB reference.
- The pre-registered Direction B Stage 1 (ADR 0018;
  `docs/thesis/directionB_preregistration.md`) — five conditions, primary
  contrast `control` vs `transport_access`, visit-intention endpoint,
  real anchor tasks, n = 50/arm, stratified server-side assignment —
  **has never been deployed and has no schedule.**
- ADR 0019's line "Stage 1 (online vignette, closes 2026-08-16 under the
  PBL companion deployment)" therefore mislabels the PBL experiment as
  prereg Stage 1; the shared date and same-day authorship (2026-07-03)
  explain the conflation. The playbook (ADR 0022) inherited the date.
- The PBL repo contains no reference to Direction B, Stage 1, the thesis
  repo, or the five-condition design; its `card` bundles hours / closed
  day / duration / transfer / booking / backup — mechanism-adjacent to
  the prereg's `combined` condition but not any frozen contrast, and its
  primary outcome corresponds to the prereg's *mediator*, not its
  endpoint.

One asset of the confusion: because the PBL stimulus is fictional, no
real transit claims ever fielded, so the ADR 0024 verification findings
affected no live participants.

## Decision

1. **Correction of record.** The date 2026-08-16 belongs to the PBL
   vignette experiment, not to prereg Stage 1. ADR 0019 Phase 1 and
   ADR 0022's calendar are read with this correction: the readout memo,
   band decision, and window gates re-anchor to the *actual* Stage-1
   close once a launch ADR sets it (structure unchanged: readout ≈ close
   + 2 weeks; autumn intercept window iff the full ADR 0022 §3 launch
   gate closes by 2026-09-30 — increasingly tight). ADR 0019 is not
   reopened; this ADR is the correction record.
2. **PBL-vignette usage rule (frozen now, before its results exist).**
   The PBL experiment's results, whatever they show:
   - MAY inform the human's Stage-1 launch decision, expectation-setting,
     and design commentary (e.g., as an order-of-magnitude check that a
     bundled information nudge moves planning uncertainty at all);
   - MUST NOT enter `d_plan`, the sign-based no-go, or any other ADR 0018
     frozen rule — those consume the pre-registered instrument's estimate
     of the pre-registered contrast, and nothing in the PBL design maps
     to it (different arms, endpoint, population, stimulus);
   - MUST NOT be cited as Direction B evidence or as thesis inferential
     evidence — it inherits the CONTEXT.md side-layer guardrail; any
     promotion would require its own ADR and would face the missing-IRB
     and convenience-sample problems on the record.
3. **Stage-1 launch checklist** (the launch ADR the human writes when
   ready must record): deployment of `experiments/nudge-pilot` as its own
   Vercel project with the server-side assignment path live end-to-end
   (fallback-assigned observations are barred from everything
   confirmatory, prereg §2); panel procurement for n = 250 EN+JP;
   confirmation that ethics coverage extends to the online stage; the
   corrected stimulus vintage (`study_version` 2026-07-07 or later, per
   ADR 0024); launch and close dates; and a note that Stage-1 recruitment
   channels may overlap the PBL experiment's (university/personal
   networks), so cross-participation is possible and should be
   discouraged in the invitation text.
4. **Documentation propagation:** `SCIENCE_HANDOFF.md` and
   `docs/thesis/TODO.md` carry the corrected calendar; no chapter text
   changes (the thesis never stated the wrong date).

## Consequences

- Direction B's true state is: pre-registration frozen, playbook frozen,
  stimuli verified and corrected, instrument built — and *nothing
  fielded*. The arm's critical path is the human launch decision, ahead
  of every other open item except ADR 0025's acceptance.
- The 2026-08-16 "Stage 1 close" milestones in ADR 0019/0022 are
  inoperative as dates while remaining correct as structure; slipping
  past a ~late-July Stage-1 launch makes the autumn intercept window
  unlikely and the spring-2027 fallback the working assumption.
- The PBL experiment proceeds untouched to its own close; its results
  arrive with their role already bounded, which protects both projects —
  the thesis from contaminated priors, the PBL work from being
  retconned into a prereg it never had.

## Rejected alternatives

- **Adopting the PBL experiment as Stage 1 retroactively:** would
  substitute a two-arm test of a different endpoint on a different
  population for the frozen five-condition design — a prereg violation
  with nothing gained except a date.
- **Editing ADR 0019 in place:** accepted ADRs are immutable history;
  corrections are new ADRs (house discipline since ADR 0018).
- **Leaving the usage rule until the PBL results are visible:** the rule
  is only credible written blind; after 2026-08-16 it would be
  post-hoc by construction.
