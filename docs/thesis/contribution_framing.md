# Contribution framing: the one sentence and its positioning

Task 3 deliverable. Contains: (1) the single defensible contribution
sentence, with the §1 and §7 variants; (2) the positioning paragraph against
the regional-revitalization and behavioral-nudge literatures; (3) splice
targets. Framing decision recorded in ADR 0017. The citation slots have been filled
with the verified references in `references.md`; none are invented here.

## 1. The contribution sentence

The discipline: one sentence, containing only what the thesis *proves* —
Direction C is a hypothesis and Direction B is a design, so neither may
appear as a result. What the thesis proves that was not known:

> **A high-speed-rail extension's demand shock is transient by default —
> durable only where station arrivals convert to destination anchors — and
> the binding constraint on that conversion is measurable in the visitors
> the line itself delivers: transport-access friction concentrated fourfold
> at the last mile, not the trunk line.**

Everything in the sentence is carried by committed evidence: transience and
corridor shape by Chapter 5's placebo battery, the durable/transient split by
the regime map, the fourfold concentration (7.09% vs 1.77% pooled) and its
convergent diagnosis by Chapter 4. The conversion *mechanism* enters only as
the observed condition ("where station arrivals convert"), not as a causal
claim; the intervention does not enter at all.

### §1 variant (insert as closing paragraph of §1.2)

> The contribution, compressed to one claim: the extension's demand shock is
> real but transient by default, endures only where station arrivals convert
> into visits to a destination anchor, and the constraint gating that
> conversion is concentrated — fourfold — in the very visitors the extension
> delivers. The last mile, not the trunk line, is where regional
> revitalization by infrastructure succeeds or fails; and the diagnosis is
> sharp enough to specify, in Chapter 6, the pre-registered experiment that
> would test the fix.

### §7 variant (replace the opening sentence of §7.2, "The thesis offers three.")

> The thesis's contributions reduce to one claim and three layers of support.
> The claim: an infrastructure demand shock is transient by default, durable
> only under station-to-anchor conversion, and gated by a friction the
> infrastructure itself concentrates in its own arrivals — the last mile, not
> the trunk line. The layers:

(The existing **Empirically / Mechanistically / Methodologically** sentences
then follow unchanged as the three layers; only their lead-in sentence is
replaced, so the two chapters state the same claim in the same shape.)

## 2. Positioning paragraph (thesis → paper)

For §7.2 (after the three layers) or the paper's introduction; the four
The citation slots were load-bearing; they have been filled from the
literature (see `references.md`), not from memory.

> This claim sits at the junction of two literatures that have not met. The
> high-speed-rail evaluation literature asks whether openings raise visitor
> numbers, almost always at prefectural or city aggregate, and reports mixed,
> context-dependent effects (Hashimoto et al., 2017; Li et al., 2019;
> Yamamoto, 2016); it treats the visitor as delivered once the train arrives,
> and so has no vocabulary for a shock that arrives and then leaks away — the
> modal outcome in Fukui's municipal-grain data. The tourism-behavior
> literature, conversely, measures frictions and satisfaction at the
> individual level (Bernini & Cagnone, 2014; Sánchez-Rebull et al., 2018;
> Žabkar et al., 2010) and increasingly tests nudge-style interventions
> (Bohner & Schlüter, 2014; Goldstein et al., 2008; Kallbekken & Sælen, 2013),
> but its interventions are typically untethered from any causal evidence
> about which friction binds, and its effect-size assumptions are rarely
> disciplined by an observed ceiling. This thesis supplies the missing
> junction from open data: a causal demand estimate at the grain where
> durability is decided (the municipality), an individual-level diagnosis of
> the binding friction in the same event, the observation that the two point
> at the same phenomenon (r = 0.826 across high-confidence municipalities),
> and a pre-registered two-stage design (Friede & Kieser, 2003, 2006;
> Proschan, 2005; Wittes & Brittain, 1990) whose power analysis is bounded by
> the measured selection ceiling (d = 0.25) rather than by convention. The
> exportable object is the template — diagnose the binding friction, identify
> the conversion condition, pre-register the test at the causal joint — not
> the Fukui-specific estimates.

## 3. Splice targets (mechanical, post-approval)

| Target | Edit |
|---|---|
| `section1_introduction.md` §1.2 | Append §1 variant as final paragraph |
| `section7_conclusion.md` §7.2 | Replace opening sentence with §7 variant lead-in; keep three layers; append positioning paragraph after them |
| Paper manuscript (future) | Contribution sentence → abstract; positioning paragraph → introduction |

Oracle for the Codex splice: the inserted texts match this file verbatim;
no other sentence in either chapter changes. The citation slots have since
been filled with the verified references in `references.md`.
