# ADR 0034: Journal-manuscript framing — one paper, Chapters 3–5 spine, Arm 3 as a bounded null replication

Date: 2026-07-30
Status: accepted 2026-07-30 (settles ADR 0019 Phase 2's manuscript item and the ADR 0031 §Consequences instruction to fix this before drafting; amends no analysis)

## Context

ADR 0019 Phase 2 schedules a journal manuscript "from existing Chapters
3–4 (+ Arm 3 if timely)", submitted early in the phase so one review
cycle doubles as an external mock defense. ADR 0031 closed Arm 3 with a
bounded null and instructed, explicitly:

> The journal manuscript (ADR 0019 Phase 2) carries Arm 3 as a **bounded
> null replication**, not a confirmation. This should be settled before
> the manuscript is drafted, not during.

Settling it during drafting is the failure mode: a null that has to be
positioned while prose is being written gets positioned to make the prose
work. Three things changed since ADR 0019 wrote that line, and each moves
the framing:

1. Arm 3 is complete and null (ADR 0031) — earlier than its Phase 2 slot,
   so "if timely" is now "yes, and it is a null".
2. Direction B is retired (ADR 0029), so the pre-registered experiment is
   a specified, unfielded protocol — it can no longer carry weight in a
   paper's contribution claim.
3. Arm 2 is live and unfired (ADRs 0020, 0032): the firewall is
   released and the production run still awaits its own human
   authorization. ADR 0019 Phase 2 schedules the run and the manuscript
   in the same phase without ordering them, so the framing must hold
   whether or not the single-use test has fired by drafting time
   (§6 fixes it either way).

`docs/thesis/contribution_framing.md` §3 already routes the contribution
sentence to a future paper's abstract and the positioning paragraph to
its introduction. Both predate ADR 0029 and ADR 0031 and are stale for
paper use (see §4 below).

## Decision

**1. One manuscript, not two.** Fukui and Kanazawa go in the same paper.
The Kanazawa result is a replication of a template, and a template's
replication is only interpretable beside the case that produced it; a
standalone prefecture-grain null with one untestable surviving suspect
is thin on its own and reads as "failed replication of someone else's
finding" rather than as the authors' own bounded self-test. Keeping them
together is also what makes the paper's honesty legible in one read.

**2. Spine and structure — Chapters 3–5, correcting ADR 0019's
"Chapters 3–4" shorthand.** The claim sentence has two halves and they
live in different chapters: transience/durability and the municipal-grain
regime map are carried by **Chapter 5**'s national synthetic control
(ADR 0005; §3.0 states explicitly that the demand-*volume* claim is
Chapter 5's, not Chapter 3's), while the friction diagnosis is
Chapters 3–4. A manuscript built from Chapters 3–4 alone would state the
durability half without its estimator. The paper's spine is therefore:
Chapter 3's DiD on experience outcomes (estimand: experience quality,
with the Noto-earthquake control limitation stated as the chapter states
it), Chapter 4's SEM diagnosis and arrival-mode split, Chapter 5's
synthetic control and placebo battery for the volume/durability claim,
and the convergence between the diagnosis and the regime map. Arm 3 is
the last substantive section: the template as a portable procedure,
applied once out of corridor, then the verdict.

**3. The claim, and its bound, are one sentence apart.** The paper
claims what the thesis proves — the shock is transient by default,
durable where station arrivals convert to anchors, and the binding
constraint is measurable in the visitors the line delivers — and states,
in the same breath as the template is introduced, that the template is
**specified for export, not yet demonstrated** (ADR 0031 §Decision 1,
ADR 0017 as bounded). The bound belongs in the abstract, not only in a
limitations paragraph. A reader who reads only the abstract must not come
away believing the template replicated.

**4. Arm 3 is reported as a well-behaved null, with the suspects, in the
pre-declared order.** Non-negotiable content. Every quantity below is
quoted from ADR 0031, which records them byte-exact from
`output/arm3_kanazawa/causal_robustness/metrics.json`; the manuscript
quotes that artifact, not this ADR. Reproduction: `make arm3-kanazawa`.

- V1 fails on V1a (p = 0.181818) while V1b and V1c pass, and Ishikawa
  pre-period RMSPE is 0.041470 against a 0.15 gate — the pipeline is
  working; the effect is not separable from the placebo distribution.
- The §6 suspects, presented in ADR 0021's declared order with the
  outcomes ADR 0031 records: **aggregation dilution** — survives, and is
  untestable at this grain, since the data audit §2 verdict found no
  balanced monthly panel across Ishikawa municipalities for 2013–2019
  and design §7.1 records no pre-2021 municipal mobile panel from any
  provider; **placebo floor** — ruled out (32 retained placebos, floor
  1/33, so p ≤ 0.05 was reachable); **donor-pool contamination** — ruled
  out (strict 20-prefecture pool, p = 0.210526). The declared order is
  the order the paper presents them in, so the one suspect that survives
  is not held back to the end. (ADR 0031's own prose presents them
  floor-first; the ordering carries no analytic weight — all three were
  checked before any interpretation — but the manuscript follows the
  declared order.)
- The grain mismatch is conceded outright — Fukui at municipality grain,
  Ishikawa at prefecture grain — as the reason this is not a like-for-like
  test (defense memo D-ii). It is a limitation the paper states, not a
  defense the paper deploys.
- V2b is not promoted, `foreign_only` is not interpreted at all (fails
  the fit gate), `japanese_only` is a sensitivity and never a headline.

**5. Forbidden framings.** The manuscript may not, in any draft or
revision: describe Arm 3 as a confirmation, a partial confirmation, or
"directionally supportive"; lead with the positive point estimate
(+10.212%) ahead of its p-value; use dilution as an explanation of the
null rather than as an unexcluded suspect; use the word *prediction* for
any Arm 3 result (that word is Arm 2's, per ADR 0021 §6); or present the
V3 descriptive series as evidence for V1 or V2.

**6. Arm 2 is out of the paper.** No Arm 2 result exists, and the paper
makes no claim contingent on one. The manuscript **may** state that a
pre-specified out-of-sample test of the same claim is registered in the
public repository, citing the commit — disclosing a frozen prediction
costs nothing and is itself the evidence of ex-ante discipline that the
Arm 3 null is being read against. Adding any Arm 2 *result* to this
manuscript, before or after submission, requires a new ADR. Nothing in
the drafting or review process may cause unseen data to be opened; the
ADR 0020 firewall rules are unchanged and apply to manuscript work
exactly as to thesis work.

**7. Direction B appears as design provenance only, or not at all.** It
is a specified protocol that was never fielded (ADR 0029). It may be
cited as the intervention design the diagnosis implies; it may not appear
in the contribution claim, and the paper claims nothing about nudge
effectiveness.

**8. Reviewer-pressure rules, fixed now.** These are the predictable
asks, and the answers are decided before they arrive:

- *"Run it at municipal grain / a different donor pool / more
  specifications."* Arm 3 is closed (ADR 0031). No balanced monthly
  municipal panel for Ishikawa 2013–2019 was found (data audit §2
  VERDICT) and no pre-2021 municipal mobile panel exists from any
  provider (design §7.1); that is the answer to the first ask and it is
  a data fact, stated at that precision and not as a stronger
  nonexistence claim. Any new
  specification run in response to review requires a new ADR, is
  post-hoc by construction, and must be labelled exploratory in both the
  manuscript and the thesis.
- *"Reframe the null as supportive."* Refused; see §5. If a venue makes
  this a condition of acceptance, the paper goes elsewhere.
- *"Drop the Kanazawa section, it weakens the paper."* Refused. Removing
  it after having run it is selective reporting, and the thesis reports
  it (§7.3) either way.
- *"Add the pending out-of-sample results."* See §6 — new ADR, and only
  if the run has actually been authorized and fired on its own schedule.

**9. Venue criteria, not a venue.** Choose a venue that (a) accepts
replication and null results as substantive, (b) permits open-data and
open-code availability statements pointing at the public repository, and
(c) reviews in a cycle that fits ADR 0019 Phase 2. No venue is named
here; naming one is a Phase 2 task and not a framing decision.

**10. Drafting mechanics.** The manuscript is a new artifact under
`docs/paper/`, drafted *from* the committed chapter text and result
artifacts. It is not produced by editing chapter files: ADR 0023 §5
stands, and no chapter file changes before Phase 4 — the paper does not
become a back door into the thesis. Availability statement points at
pinned public sources and `docs/source_ledger.md`; no supplement ever
contains quarantine contents.

## Consequences

- ADR 0031's instruction is discharged: when drafting starts, the null's
  position, wording constraints, and the answers to the foreseeable
  reviewer asks are already fixed, so no framing decision is made while
  prose is being fitted around a result.
- The paper and the thesis state the same bound in the same shape. The
  thesis's §8.2 and §6.5 carry "specified for export, not yet
  demonstrated" (ADR 0031 T1/T2, Phase 4); the abstract carries it too.
  Divergence between the two would be the most easily-found inconsistency
  an examiner could locate, and this rules it out in advance.
- Peer review functions as the intended external mock defense on the
  seams that are actually live — Seams A, C and D — rather than on
  Direction B, which no longer exists as an empirical claim.
- **`contribution_framing.md` is stale for paper use and is not spliced
  into the manuscript verbatim.** Its positioning paragraph ends on the
  pre-registered two-stage design and on "the exportable object is the
  template", both written before ADR 0029 and ADR 0031. Its thesis-side
  splice targets (§3 rows 1–2) are unaffected and remain Phase 4 work;
  only the "Paper manuscript (future)" row is superseded by this ADR. The
  paper's introduction is written fresh against the bounded claim.
- Risk accepted: a bounded-null paper is harder to place than a
  confirmatory one, and the review cycle may run longer than Phase 2
  budgets. The mitigation is venue choice (§9), not framing.

## Rejected alternatives

- **Two papers — a Fukui paper and a standalone Kanazawa null note.**
  Splits the evidence from its interpretation, doubles the review
  overhead against a fixed Phase 2 window, and makes the null publishable
  only as a curiosity. Also invites the reading that the null was
  quarantined away from the headline result.
- **Hold the manuscript until Arm 2 returns a verdict.** ADR 0019
  rejected deferring submission until the Direction B Stage-2 results
  for a reason that transfers intact: waiting spends the review cycle
  that was supposed to serve as a mock defense. Here it would also make
  publication hostage to a single-use test whose authorization is
  deliberately unhurried.
- **Frame the paper around the template as the contribution.** The one
  case where the template was tested out of corridor returned a null;
  leading with portability would be claiming precisely what was not
  demonstrated.
- **Report Arm 3 in an appendix or a footnote.** Formally honest,
  substantively evasive, and it discards the paper's strongest
  credibility asset — a pre-written verdict contract that cost something
  when it fired.
- **Defer the framing to drafting time.** The failure mode ADR 0031
  named. Framing settled under the pressure of a half-written
  introduction is framing chosen by the introduction.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote the
affected analysis to exploratory, per ADR 0019.
