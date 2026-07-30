# ADR 0029: Retire the Direction B survey arm; refocus Chapter 6 on the non-survey evidence engine

Date: 2026-07-29
Status: accepted 2026-07-29 (supersedes ADR 0022, ADR 0024, ADR 0026 §1/§3, and closes ADR 0018 as unexecuted; amends ADR 0019 and ADR 0023)

## Context

ADR 0019's roadmap upgraded the thesis from *diagnosis + design* to
*diagnosis + tested prediction + causal evidence* across three arms.
Direction B (the pre-registered two-stage nudge experiment) was the only
arm requiring primary human-subjects data collection, and the only arm
with an external clock.

As of today none of its launch-gate items has been met. ADR 0026 §3
required: a live Vercel deployment with server-side assignment verified
end-to-end (`experiments/nudge-pilot` has `api/assign.js` implemented but
no linked project, and a client-side `hash_fallback` at `app.js:101-127`
whose observations are barred from anything confirmatory); panel
procurement of n = 250 EN+JP (`experiments/nudge-pilot/screener_spec.md`
is a quote-request package with three undecided items — recency window,
EN panel composition, budget ceiling); ethics coverage for the online
stage (no artifact exists); and a launch ADR with dates (none exists).
Only the corrected stimulus vintage was satisfied (`study-config.json`
version 2026-07-07, per ADR 0024).

ADR 0022 §5's window rule made autumn 2026 conditional on the full launch
gate clearing by 2026-09-30. That is no longer attainable: panel
procurement and ethics review are multi-week institutional leads that
have not started. Spring 2027 would push Stage 2 analysis past ADR 0019
Phase 3 and make Direction B the sole determinant of the thesis
timetable — for the one arm that, by ADR 0018's own framing, is design
rather than evidence until Stage 2 completes.

Meanwhile the non-survey evidence engine landed and is accepted (ADR
0027, ADR 0028): a reproducible panel, an extended SEM, an opportunity
scan, and a government prefecture context layer, all from official open
data with no funding or human-subjects dependency. This mirrors the
situation ADR 0002 resolved when it retired the Likert pilot: the
observational path had matured to the point where the collection path
was cost without corresponding evidentiary return.

## Decision

**1. Direction B is retired as a data-collection path.** Stage 1 and
Stage 2 will not field. No participant recruitment, no panel
procurement, no station-forecourt intercept, no ethics submission for
this instrument. Consequently:

- ADR 0018 (`directionB_preregistration.md`) is **closed as unexecuted**.
  Its analysis and decision rules are retained in the repository as a
  written pre-registration that was never fielded — a design artifact,
  not a live contract. Nothing may be estimated under it.
- ADR 0022 (Stage-2 fielding playbook) is **superseded**. Its band
  rules, window rule, and action register are void.
- ADR 0024 (stimulus corrections) is **superseded as an operational
  amendment**; the corrections remain in `study-config.json` v2026-07-07
  as the accurate final state of the instrument. The T−4w/T−1w
  re-verification cadence is void along with the fielding it gated.
- ADR 0026 §1 (Stage 1 ≠ PBL vignette) and §3 (launch checklist) are
  **superseded**. **ADR 0026 §2 survives unchanged and remains
  binding**: the PBL vignette study closing 2026-08-16 is a separate
  two-arm side-project whose results never enter thesis evidence and
  never enter any planning quantity. Retiring Direction B removes the
  d_plan pathway but *increases* the temptation to repurpose PBL numbers
  as a substitute; the prohibition is absolute.
- `experiments/nudge-pilot/` is retained exactly as ADR 0002 retained
  it: a built, deployable artifact referenced as the implementation
  vehicle for the ranked interventions, not as an experiment. No
  deployment occurs.

**2. Arm 2 and Arm 3 continue and become the thesis's empirical
upgrade.** Both are non-survey. Neither is affected by this retirement
except that each is now on the critical path. Their gates are unchanged:
Arm 2 requires ADR 0025 accepted and committed before any unseen-data
fetch, plus the FTAS new-wave access request; Arm 3 requires ADR 0021
accepted. The ADR 0020 firewall and quarantine discipline stand in full.

**3. Chapter 6 is refocused; the Direction B design moves to an
appendix.** In the v2 architecture, Chapter 6's spine becomes the
non-survey evidence engine — the opportunity scan and SEM-based
intervention prioritization (`scripts/opportunity_scan.py`,
`scripts/sem_nonsurvey.py`, ADR 0027's scope rules) — rather than the
pre-registered experiment. The existing §6.3 pre-registered pilot
material moves to an appendix as a designed-but-unfielded protocol.

**4. Track B in ADR 0023 resolves as a new terminal branch,
`retired`.** This is the mechanism that keeps ADR 0023's Phase 4
discipline intact. Track B is no longer awaiting an outcome; its
branch language is settled now, but **no chapter file is edited before
Phase 4**. The matrix is amended as follows:

| # | Location | Trigger | Edit |
|---|---|---|---|
| G3 | `section6_intervention.md` §6.3 + §6.4 first limitation | resolved: retired | §6.3 moves to appendix wholesale; the "design, not evidence" framing is preserved verbatim and becomes literally final — the arm was never run. No tense repair needed, only relocation |
| G4 | `section7_conclusion.md` §7.4 "From design to field" | resolved: retired | Rewrite as §8.4: the field step did not occur; the forward-looking claim narrows to Arm 2/Arm 3 |
| B1 | §6.3 power/feasibility prose | **retired** — row voided | The intercept-vs-hybrid staleness is moot once §6.3 is an unfielded-protocol appendix; ADR 0022's hybrid arithmetic is superseded and must not be spliced in |
| B2 | §8.1 findings list | **retired** — row voided | No fifth finding. Stage 2 produced no result |
| B3 | §1.3 "presented as a pre-registered design, explicitly not as evidence" | **retired** | Stays **verbatim**. The sentence was always true and is now permanently true |
| B4 *(new)* | `section6_intervention.md` whole-chapter | v2 map adoption | ADR-gated: rebuild Ch. 6 around the non-survey opportunity scan + SEM prioritization; §6.1/§6.2/§6.5 retained, §6.3 excised to appendix |
| B5 *(new)* | new appendix + `thesis_master.md` chapter map | v2 map adoption | Splice: create the unfielded-protocol appendix from excised §6.3, register it in the master map (G5 still runs first) |

Rows D1–D5 (Arm 2) and T1–T2 (Arm 3) are unaffected. ADR 0023 §5's
rule — no chapter file changes before Phase 4, master map first —
is **unchanged and still binding**. B4 and B5 are ADR-gated rows that
execute in Phase 4 alongside everything else.

**5. ADR 0019 is amended.** Phase 1's Direction B items (Stage 1
analysis, ethics, station permission, panel quotes) are struck. Phase
2's Stage 2 fielding is struck. Phase 2 and 3 remain Arm 2 + Arm 3 +
the journal manuscript. Phase 4's date is unchanged.

## Consequences

- The thesis's evidentiary claims rest entirely on official open data
  and reproducible pipelines — no funding dependency, no human-subjects
  collection, consistent with ADR 0002's precedent and CONTEXT.md's
  guardrails.
- The contribution framing (ADR 0017) shifts weight from "pre-registered
  intervention design" to "out-of-sample prediction (Arm 2) + template
  replication (Arm 3) + observational opportunity prioritization
  (ADR 0027)". Direction B remains a contribution, but as a specified
  protocol rather than a staged experiment. ADR 0017 is not amended
  here; if the human judges the shift material, a separate ADR should
  restate the framing.
- Causal evidence about *nudge effectiveness* is out of scope, as it was
  before ADR 0018. The thesis claims mechanism (SEM), impact of a
  friction shock (DiD/SCM), an out-of-sample prediction test (Arm 2), a
  template replication (Arm 3), and an evidence-ranked intervention
  design (bridge + artifact + protocol).
- The 2026-09-30 gate, the autumn-2026 and spring-2027 intercept
  windows, and all ADR 0022 §7 action-register items cease to exist as
  obligations.
- Risk accepted: the thesis now has no primary-data arm, so Arm 2's
  verdict (earliest ~mid-2027, dependent on FTAS new-wave access) and
  Arm 3 carry the entire empirical upgrade. If FTAS access is denied,
  Arm 3 plus the non-survey engine is the fallback, and the upgrade
  narrows to replication + prioritization. This should be revisited if
  the access request stalls past ADR 0019 Phase 2.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote
the affected analysis to exploratory, per ADR 0019.
