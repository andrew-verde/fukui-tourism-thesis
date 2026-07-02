# ADR 0017: Contribution framing — last mile, not trunk line

Date: 2026-07-03
Status: accepted

## Context

Task 3 of the reasoning queue: compress the §4 → C → B arc into a single
defensible contribution sentence for §1 and §7, and position the thesis
against the regional-revitalization and behavioral-nudge literatures. The
constraint that shapes everything: Direction C is a hypothesis and
Direction B is a design (ADR 0015, brief checkpoint 5), so the contribution
sentence may contain only what Chapters 3–5 prove. Deliverable:
`docs/thesis/contribution_framing.md`.

## Decision

1. **The claim is framed as "the last mile, not the trunk line."** Canonical
   sentence: *a high-speed-rail extension's demand shock is transient by
   default — durable only where station arrivals convert to destination
   anchors — and the binding constraint on that conversion is measurable in
   the visitors the line itself delivers: transport-access friction
   concentrated fourfold at the last mile.* Every clause maps to committed
   evidence (Ch. 5 placebo battery for transience; regime map for the
   durable/transient split; Ch. 4 arrival-mode contrast and convergent
   diagnosis for the concentration). The conversion mechanism appears only
   as an observed condition ("where … convert"), never as a causal claim;
   the nudge pilot does not appear in the sentence at all.

2. **§1 and §7 state the same claim in the same shape.** §1.2 gains a
   closing contribution paragraph; §7.2's lead-in sentence is replaced so
   the existing three support layers (empirical / mechanistic /
   methodological) hang off the one claim instead of standing as three
   parallel contributions. Rationale: examiners test whether the candidate
   can say what the thesis proves in one breath; three coordinate
   contributions invite "which one is the contribution?" — one claim with
   three layers does not.

3. **Positioning: the junction of two literatures that have not met.** The
   HSR-evaluation literature (aggregate, "did visitors increase," mixed
   findings) lacks vocabulary for a shock that arrives and leaks; the
   tourism-behavior/nudge literature tests interventions untethered from
   causal evidence about which friction binds. The thesis is positioned as
   supplying the junction — municipal-grain causal demand estimate +
   individual-level binding-friction diagnosis in the same event + a
   pre-registered test whose power is bounded by a measured ceiling — with
   the *template* named as the exportable object, not the Fukui estimates.

4. **No citations are invented.** The positioning paragraph carries four
   load-bearing `[REF: …]` slots to be filled with real references before
   submission; the deliverable's splice oracle requires the slots to survive
   verbatim so an unfilled slot fails loudly (grep for `[REF:`) rather than
   silently shipping.

## Consequences

- The thesis's elevator claim is now fixed; future edits to §1/§7 should
  preserve the sentence's evidence discipline (nothing from C-as-result or
  B-as-evidence may migrate into it).
- §7.2's "three contributions" survive as support layers, demoted from
  coordinate billing — a framing change, not a content change.
- A literature pass (real references for the four slots) is now a named
  pre-submission dependency; it is mechanical retrieval work suited to the
  Codex/orchestration seat with the `[REF]` slots as the checklist.
- The splices into §1.2 and §7.2 are pending mechanical edits with a
  verbatim-match oracle (see deliverable §3), gated on human approval.

## Rejected alternatives

- **"Template" as the headline contribution** (diagnose → mechanism →
  pre-register, as in §6.5/§7.2): rejected as the lead — a template is a
  promise about other places; examiners weigh what was shown, not what is
  exportable. The template is kept, subordinated to the empirical claim.
- **"Transience by default" alone as the claim**: rejected — true and
  proven, but without the last-mile constraint it reads as a null-adjacent
  finding ("shocks fade"), and it drops Chapter 4, the thesis's strongest
  chapter.
- **Including the anti-prediction (repeat share) in the sentence**: rejected
  — it is the most quotable finding but the least defensible (Seam B,
  ADR 0015); putting it in the headline invites the committee to attack the
  weakest link first. It stays in §7.1's findings, priced as corroboration.
- **A contribution sentence with the nudge pilot as co-equal clause**:
  rejected — violates the design-not-evidence checkpoint; the pilot enters
  the §1 variant only as "sharp enough to specify the experiment."
