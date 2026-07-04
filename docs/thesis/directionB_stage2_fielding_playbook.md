# Direction B Stage-2 fielding playbook

**Status: operational contingency plan, not evidence and not analysis rules.**
The analysis and decision rules are frozen in
`docs/thesis/directionB_preregistration.md` (ADR 0018) and are not restated
as rules here; where this document quotes them, the pre-registration
governs. This playbook adds the *operational* layer: what gets executed, by
whom, in which window, under each Stage-1 outcome band. It is deliberately
written and reviewed **before Stage 1 closes (2026-08-16)**, so that every
operational choice below — arm counts, window selection, recruitment
sequencing — is fixed blind to d̂, extending the pre-registration's
discipline to logistics. Decision provenance: ADR 0022. Deviations after
acceptance are logged by ADR; deviations that touch ADR 0018's frozen rules
additionally demote the affected analysis to exploratory, per that ADR.

Direction B remains design, not evidence, until Stage 2 completes as
pre-registered.

## 1. Fixed reference points (from committed artifacts)

- Stage 1: n = 50/arm, N = 250, online panel, non-confirmatory by
  construction (MDE d ≥ 0.56); closes **2026-08-16**; deliverable is the
  effect-size prior (d̂, SE(d̂)), endpoint SDs, within-participant task
  correlation r̂, construct reliability, instrument behavior.
- Re-power rule (frozen): `d_plan = max(0.10, d̂ − SE(d̂))`.
- No-go rule (frozen): Stage-1 d̂ ≤ 0 on the primary contrast ⇒ Stage 2
  does not proceed under the pre-registration.
- Recruitment-mode rule (frozen): re-powered requirement > 360/arm ⇒
  hybrid recruitment (screened online-panel main sample + nested station-QR
  external-validity subsample, n ≈ 300–500, direction-consistency only);
  if hybrid is unavailable, arm reduction to
  `control`/`transport_access`/`combined` before any window extension.
- Sizing anchors (α = 0.05 two-sided, power 0.80, two-sample):
  d = 0.25 → 252/arm; 0.20 → 393; 0.15 → 698; 0.125 → 1,005; 0.10 → 1,570.
  Mixed-model credit enters only at the Stage-1-estimated r̂: required
  completes per arm ≈ n(d_plan) × (1 + r̂)/2 for two tasks per participant.
- Feasibility anchors: FTAS captured ~289 rail respondents/month
  prefecture-wide, ~120/month in the corridor; 2,010 completes ≈ 17 months
  at corridor-scale capture; intercept-only is "not credible below
  d_plan ≈ 0.21 (~360/arm ≈ six months)". Stage-2 intercept population:
  rail arrivers (7.09% transport-friction base rate) at Fukui, Awara-Onsen,
  Tsuruga stations.
- Planning value SE(d̂) ≈ 0.20 at n = 50/arm (ADR 0018). All band
  boundaries below are **illustrations at SE = 0.20**; the gates themselves
  are evaluated at the actual Stage-1 (d̂, SE, r̂) — the formulas, not the
  illustrations, govern.

## 2. The tree's shape: read this before the branches

One derived fact organizes everything. Intercept-only Stage 2 requires
n(d_plan) ≤ 360/arm ⇔ d_plan ≥ 0.21. Since d_plan = d̂ − SE(d̂) and
SE ≈ 0.20, intercept-only requires **d̂ ≳ 0.41 — 1.6× the d = 0.25
selection ceiling**. A Stage-1 estimate that large would itself be evidence
of something wrong (§3, Band S). Consequently:

> **For every plausible positive Stage-1 outcome, the frozen rules land
> Stage 2 in hybrid recruitment.** The station intercept is, in expectation,
> the nested 300–500-complete external-validity subsample — not the main
> sample. Permissions, ethics scope, and window planning below are sized to
> that reality, with the intercept-only branch retained for completeness.

This is good operational news: a 300–500-complete passive-QR subsample is
feasible in ~2–3 months at corridor scale, where a 2,010-complete
intercept-only Stage 2 never was.

## 3. Contingency tree by Stage-1 outcome band

Gate: Stage-1 readout memo (target **2026-08-31**; Codex computes per the
prereg's estimation plan; a mid-tier seat drafts, human reviews). The memo
states d̂, SE(d̂), r̂, SDs, reliability, completion/accuracy rates, and the
computed d_plan and N_req/arm = ceil(n(d_plan) × (1 + r̂)/2) — nothing else.
No hypothesis test on H1 is computed or reported (prereg §4).

### Band N — d̂ ≤ 0 (no-go)

Frozen consequence: Stage 2 does not proceed under this pre-registration.

Operational actions:
1. Stage-2 launch preparations stop. Station-permission applications are
   withdrawn or left to lapse with a courtesy notice; the ethics approval
   (if granted) is held open only if a redesign is actively contemplated,
   otherwise closed per the institution's procedure.
2. The thesis reverts to the already-written design-not-evidence framing
   (ADR 0016/0018 anticipated this); Chapter 6 requires no rewrite, only
   the Stage-1 estimation results reported as estimation.
3. Any redesigned experiment is a new ADR and a new pre-registration; the
   wrong-signed prior is reported, not buried.
4. Arms 2 and 3 are unaffected — the portfolio was built so this branch
   costs no other evidence stream (ADR 0019).

### Band W — weak-positive: 0 < d̂ and N_req > 360/arm (the expected branch)

At SE ≈ 0.20 this band spans essentially all of 0 < d̂ ≲ 0.41. Frozen
consequence: hybrid recruitment.

Operational sub-decisions, **fixed now, blind to d̂**:

- **W-arms (arm-count matrix).** Stage 2 fields:
  - **five arms** if d_plan ≥ 0.15 (N_req ≤ 698/arm before mixed-model
    credit) — the secondary contrasts (H3–H5) stay alive at tolerable cost;
  - **three arms** (`control`/`transport_access`/`combined`) if
    d_plan < 0.15 — the budget concentrates on the primary contrast, and
    H3/H4 (single-nudge secondary conditions) are explicitly priced as
    casualties of a weak prior, recorded in the launch ADR. This extends
    the prereg's arm-reduction ladder (there triggered by hybrid
    *unavailability*) to the cost dimension; it touches no analysis rule —
    the primary contrast and its test are identical under either arm count.
  - The d̂ ≤ 0.30 sub-case floors d_plan at 0.10 (N_req = 1,570/arm
    pre-credit; ≈ 1,180/arm at r̂ = 0.5). This is the maximum-spend case:
    the launch ADR must show the panel quote and affirm the budget before
    fielding, or invoke arm reduction above.
- **W-panel.** Main sample from an online panel screened for planned or
  recent Hokuriku rail travel. Screening incidence will be low; to avoid
  discovering pricing mid-decision, **panel-vendor quotes for screened
  EN+JP completes are obtained before Stage-1 readout** (human task with
  Codex-prepared screener spec; §7). If no vendor can screen at acceptable
  incidence, the prereg's ladder applies: arm reduction first, window
  extension last.
- **W-intercept.** The nested QR subsample (300–500 completes,
  direction-consistency only, never powered alone) fields in the §5 window
  under the §6 permissions. If intercept yield after two weeks projects
  the subsample below 300 by window end, the response is operational only:
  extend the subsample window within the same season or accept the
  shortfall and report it — the subsample gates nothing (prereg §5), so no
  analytic decision depends on it.

### Band S — strong: N_req ≤ 360/arm (requires d̂ ≳ 0.41; flagged as anomalous)

Frozen consequence: intercept-only Stage 2 is permitted.

But d̂ > 0.25 exceeds the selection ceiling — the observed car–rail gap
bounds what an information nudge can close, so an estimate materially above
it more likely reflects instrument artifact than a true effect. Operational
rule, fixed now: any d̂ > 0.25 (Band S is deep inside this) triggers an
**instrument-behavior review before the launch ADR** — accuracy-item pass
rates by arm, completion asymmetries, assignment-path integrity
(server-side only), condition-blinding of the panel header. The review is
outcome-neutral (no re-analysis of the endpoint, no exclusions — prereg §6
forbids outcome-based exclusions) and its finding goes in the launch ADR.
If the instrument is sound, the frozen rules govern: size at d_plan,
field intercept-only in the §5 window, with hybrid still available as the
conservative choice if permissions lag. Stage-1 estimates are still not
effects (prereg §7), however large.

### All positive bands — launch gate

Stage 2 fields only when **all** of the following hold, recorded in a
launch ADR with the byte-exact Stage-1 numbers:

1. Readout memo accepted; band and N_req computed per the frozen formulas.
2. Timetable-verification memo complete with every claim PASS or its
   amendment applied (§4).
3. Ethics approval covering the fielded configuration (§6).
4. Station/forecourt permissions for the intercept component (§6) — or the
   launch ADR records fielding the online main sample first and nesting
   the intercept later within the declared window (§5).
5. Server-side assignment path live end-to-end; fallback path disabled or
   flagged so fallback observations are excluded per prereg §6.
6. Fixed-n stopping restated: recruitment stops at planned n per arm; no
   interim looks. During-field monitoring is limited to completion counts
   and intercept yield — never outcomes.

## 4. Timetable-verification protocol (closes the open TODO)

The last open item in `docs/thesis/TODO.md`; ADR 0018 makes it a fielding
precondition ("fielding without it is a protocol deviation") and ADR 0019
routes execution to Codex. This section is the protocol Codex executes.

**Scope.** All transit facts in the `transport_access` nudge strings of
`experiments/nudge-pilot/study-config.json` (version 2026-07-02). The
`combined` condition concatenates the same strings at runtime
(`app.js: getActiveNudges`), so the config is the single source of truth —
one corrected string fixes every condition that shows it. The
`opening_hours_availability` strings deliberately instruct participants to
check current hours rather than asserting them; they carry no verifiable
timetable claim. Current claim inventory:

| # | Task | Claim (paraphrase) | Verify against |
|---|---|---|---|
| 1 | `eiheiji_half_day` | Direct "Eiheiji Liner" bus from Fukui Station exists; ~30 min; runs once–twice per hour | Keifuku Bus official Eiheiji Liner timetable |
| 2 | `eiheiji_half_day` | Alternative: Echizen Railway to Eiheijiguchi + local bus transfer exists | Echizen Railway (Katsuyama Eiheiji Line) + connecting bus timetable |
| 3 | `eiheiji_half_day` | Evening return departures are sparse; a "last return bus" exists to check; round-trip tickets sold | Same as #1; operator fare page |
| 4 | `museum_arrival` | Echizen Railway Fukui → Katsuyama ~55 min; ~twice per hour | Echizen Railway official timetable |
| 5 | `museum_arrival` | Connecting museum shuttle bus exists, timed to selected trains; missed connection can cost up to an hour | Katsuyama community/shuttle bus page; museum official access page |
| 6 | `tojinbo_awara` | Tojinbo-bound bus departs Awara-Onsen Station forecourt; ~40 min; roughly hourly | Keifuku Bus (Tojinbo line) official timetable |
| 7 | `tojinbo_awara` | After early evening, return is effectively taxi-only (last bus to note) | Same as #6 |

**Tolerance rules** (the copy is hedged — "about", "roughly" — so
verification is against bands, fixed here): "about 30 minutes" ⇢ scheduled
25–35 min; "about 55 minutes" ⇢ 50–60 min; "about 40 minutes" ⇢ 35–50 min;
"once or twice an hour" ⇢ headway 30–60 min over the 09:00–17:00 service
span; "about twice an hour" ⇢ headway 25–35 min; "roughly once an hour" ⇢
headway 45–75 min; "evening sparse / taxi-only" ⇢ last departure toward the
station exists and is no later than ~19:00, exact time recorded. Weekday
and weekend/holiday timetables both checked; if they differ enough to cross
a band, the claim FAILS and the copy is amended to the weaker truth.

**Procedure.** For each claim: fetch the operator's official current
timetable (operator page, not aggregators; Google Maps may corroborate,
never substitute), record scheduled duration, headway by daypart,
first/last departures for both day types, the timetable's stated validity
period, URL, and retrieval date; archive a copy (PDF/screenshot) under
`experiments/nudge-pilot/verification/` with a sha256 manifest. Output:
`experiments/nudge-pilot/timetable_verification.md`, one row per claim,
verdict **PASS / AMEND (with proposed replacement string) / STRUCTURAL**
(the service no longer exists in recognizable form).

**Failure handling.**
- AMEND: the config string is corrected to current reality (Codex proposes,
  human approves); an amended stimulus between stages is recorded in the
  launch ADR as a Stage-1→Stage-2 comparability note on the d̂ prior.
- STRUCTURAL (e.g., a route discontinued): the `transport_access` stimulus
  no longer describes a real last-mile option; that is a design-level
  problem — new ADR before any fielding, per ADR 0018's deviation rule.
- **Stage-1 interaction, flagged honestly:** verification was a fielding
  precondition for Stage 1, the TODO is still open, and Stage 1 closes
  2026-08-16. If Stage 1 launched before verification, that is a protocol
  deviation to log by ADR regardless of findings. Its practical impact is
  bounded — Stage 1 is non-confirmatory by construction — but the memo must
  add one verdict: *were Stage-1 participants shown a materially false
  transit fact?* If yes, the d̂ prior was measured on a flawed stimulus;
  feeding it unexamined into the re-power rule is not conservative, and the
  Band decision escalates to a human call recorded in a new ADR.

**Cadence.** Execute now (July 2026, closes the TODO). Re-verify at T−4
weeks and T−1 week before Stage-2 launch: Japanese rail and bus timetables
revise around April and October, and both candidate windows (§5) sit near a
revision boundary — an autumn launch must verify against the *October*
timetable, published typically in September, not the summer one.

## 5. Fielding windows

The window matters mainly for the intercept component (§2: the main sample
is an online panel in every plausible band and is season-independent).

- **Autumn 2026 (primary target): intercept subsample ≈ 2026-10-15 →
  2026-12-15.** Foliage season is the corridor's high-volume period —
  Eiheiji's peak draw — matching the FTAS capture rates the feasibility
  arithmetic assumes, and it keeps ADR 0019's Phase 2 schedule with slack
  before the 2027 phases. Requires the §3 launch gate (ethics + permissions
  + verification + readout) by ~2026-10-01 — about five weeks after the
  readout memo. Tight but real *for the subsample-sized intercept*; it was
  impossible for an intercept-only main sample, which is another reason §2
  matters. Hard stop 12-15: December weather and volume collapse make later
  extension worthless.
- **Spring 2027 (fallback): intercept subsample ≈ 2027-03-20 →
  2027-05-31.** Cherry-blossom-through-Golden-Week volume. Post-April
  timetable revision → re-verify stimuli (§4 cadence). Compresses Phase 3
  but remains inside ADR 0019's absorption (Stage-2 analysis 2027-04→09
  still holds if the main sample completed earlier).
- **Winter 2026–27 is not a window.** Corridor volume and Eiheiji access
  collapse; a passive QR intercept would starve.

**Window decision rule (fixed now):** if the full §3 launch gate is
satisfied by **2026-09-30**, the intercept fields in autumn 2026; otherwise
it fields in spring 2027, and the online main sample launches as soon as
the gate items that don't involve stations (readout, ethics for the online
component, verification) are satisfied — the launch ADR records the
main-sample/subsample timing split. Non-concurrent main and nested samples
are acceptable because the subsample is direction-consistency-only (prereg
§5); the timing split is disclosed wherever the subsample is reported.

**Yield tripwire (operational, outcome-blind):** if week-1–2 QR yield
projects < 300 subsample completes by window end, extend within the season
or accept and disclose the shortfall (§3, W-intercept). Yield numbers never
justify touching analysis rules.

## 6. Permissions and ethics — the long-lead dependency map

These are the two longest external leads in the plan (with FTAS new-wave
access, ADR 0019 Phase 1). **All three start now**; none blocks on Stage-1
results. Facts about operators/administrators below are planning
assumptions to be confirmed on first contact (Codex drafts, human sends and
verifies) — they are dependency mapping, not verified claims.

1. **Ethics/IRB (start immediately; longest internal lead).** Scope the
   application to cover *both* recruitment modes (online panel + station QR
   intercept), both windows, anonymous browser instrument, no minors
   targeted, QR-poster/flyer intercept with no personal-data collection at
   the station. Committee cycles are typically monthly with 1–2 revision
   rounds — assume 6–12 weeks, which is exactly the autumn-window margin.
   Ethics approval is usually a prerequisite document for station
   permission applications, so it leads the chain.
2. **Station/forecourt permission (start inquiries in parallel).** Three
   sites: Fukui, Awara-Onsen, Tsuruga. Planning assumptions to confirm:
   shinkansen station premises are JR West's (their survey/commercial-use
   permission process is slow and can decline); station *forecourts*
   (駅前広場) are typically municipally administered — Fukui City, Awara
   City, Tsuruga City — with shorter (~2–6 week) processes; a public-way
   position may additionally need a police road-use permit (道路使用許可).
   Preference order, fixed now: municipal forecourt permission first (site
   sketch per station), JR premises only if a forecourt position is
   unworkable at a specific station. Dropping one station is acceptable for
   the subsample (disclosed); dropping two is not — the subsample's
   external-validity value is corridor coverage.
3. **Sequencing.** Ethics submission (target July 2026) → permission
   applications with ethics reference (August) → both in hand by late
   September ⇒ autumn window; any slip ⇒ spring window per §5's rule. None
   of this waits for the 2026-08-31 readout: if Band N lands, applications
   are withdrawn (§3), a small sunk cost the schedule buys insurance with.

## 7. Action register (who does what, when)

| When | Actor | Action |
|---|---|---|
| Now (July 2026) | Human | Submit ethics/IRB application (scope per §6.1); begin municipal forecourt inquiries |
| Now | Codex | Execute §4 timetable verification; emit memo + archive + any AMEND proposals |
| Now | Codex | Draft screener spec for the hybrid panel (planned/recent Hokuriku rail travel, EN+JP); human requests vendor quotes |
| 2026-08-16 | — | Stage 1 closes (fixed-n; no looks before or after) |
| by 2026-08-31 | Codex + mid-tier | Stage-1 readout memo (estimation only, per prereg §4) |
| ≤ 1 week after readout | Human | Band decision per §3 (mechanical given the memo); if positive band: launch ADR drafted with byte-exact numbers |
| by 2026-09-30 | Human | Window decision per §5's rule (mechanical given gate status) |
| T−4w and T−1w before launch | Codex | Re-verify timetables (§4 cadence) |
| During field | Codex | Completion/yield monitoring only; no outcome access |

## 8. What this playbook does not do

It does not modify any ADR 0018 rule; it does not create any new analysis;
it does not read Stage-1 estimates as effects; it does not let any
operational number (yield, cost, calendar) alter the frozen gates — cost
and calendar pressure route only into the pre-declared operational choices
(arm count, window, recruitment mode) and always through a logged decision.
If Stage 2 dies at Band N, the thesis stands as written; that was the
portfolio's design.
