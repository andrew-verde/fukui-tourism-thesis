# ADR 0015: Defense posture for the three identification threats

Date: 2026-07-03
Status: accepted

## Context

The thesis has three attackable identification seams that a committee is
likely to probe: (A) the §4.2 arrival-mode contrast (7.09% vs 0.66%) can be
read as mechanical/selection rather than a shinkansen effect; (B) the
Direction C durability reframe rests on n = 13 municipalities, an r = 0.826
correlation, and the counterintuitive claim that repeat-visit share
anti-predicts durability; (C) the Direction D causal anchor is a one-sided
p = 0.041 (two-sided 0.168) on an opening-window statistic adopted after the
post-period-mean statistic proved null, with a potential circularity charge
against the friction–leakage correlation. A defense memo
(`docs/thesis/defense_memo.md`) steel-mans each attack and grounds each defense in committed
numbers. This ADR records the posture chosen per seam and the concessions
accepted, so the reasoning survives the drafting session.

## Decision

Adopt a single cross-seam posture — **concede the channel, keep the claim** —
instantiated per seam as follows.

1. **Seam A — own the mechanism, concede composition.** Do not dispute that
   the arrival-mode gap is "mechanical" (carless arrival → last-mile
   exposure); argue that this chain *is* the finding, made policy-relevant by
   the scale of carless arrivals the extension delivers. Load-bearing
   supports: category specificity (transport_access is the argmax of the
   shinkansen-minus-other gap across all twelve friction types, next gap ~6×
   smaller — inconsistent with a generic grievance-prone-population confound);
   prediction of independent demand leakage (r = 0.826); destination-side
   heterogeneity (Eiheiji/Sakai convert the same rail arrivers Fukui City
   leaks); and the SEM's distinct role (β = −0.123 shows the friction damages
   the outcome; the split shows where it concentrates — neither substitutes
   for the other). Direction B's within-rail-arriver randomization is cited as
   the design that moots selection for the intervention claim. **Accepted
   concession:** FTAS lacks demographics/residence/itinerary, so a
   covariate-adjusted contrast and the within-person "same visitor by car"
   counterfactual are unavailable; selection into rail is reframed as part of
   the treatment, not a confound of the diagnosis.

2. **Seam B — stage the correlation as corroboration, hang the weight on the
   endpoint choice.** Defend the mechanism (station→anchor conversion) as
   independently interpretable — it assigns the anchor-possessing pair
   (Eiheiji, Sakai) to durable and the pass-through terminal (Fukui City) to
   transient, as predicted — and confine the anti-prediction's license to one
   targeting decision: Direction B's primary endpoint is first-visit anchor
   conversion, not repeat conversion. Key argument: even the strongest rival
   explanation (saturation/ceiling effect) implies the same endpoint choice,
   so the design decision is robust to losing the argument about the
   anti-prediction's cause. **Accepted concession:** n = 13 cannot exclude
   municipality-level confounding (anchor presence driving both friction
   geography and durability); Direction C is framed as the hypothesis-bridge
   whose test is Direction B, not as an established result.

3. **Seam C — defend sidedness as ex ante, lead with the falsification
   architecture, answer multiplicity with geography.** One-sided testing is
   entailed by the intervention's predicted direction, with the two-sided
   value disclosed adjacently; the opening-window estimand is matched to the
   documented transient effect shape (§5.2) with the discarded post-mean null
   (p = 0.83) printed, not buried. The affirmative case is the conjunction:
   silent backdated-2023 negative control (p = 0.47), leave-one-out surge
   bounded 26.2–39.8%, a fit gate that discards the prefecture's two largest
   point estimates (Katsuyama, Ikeda), and a well-fit significant set that is
   exactly the new-corridor geography {Eiheiji, Fukui City, Tsuruga, Sakai}.
   The circularity charge is rejected on structure: the friction–leakage
   correlation never enters Chapter 5's inference, and survey friction never
   enters the SCM fit. **Accepted concession:** p = 0.041 alone is marginal,
   would not survive family-wise correction, and the window was not
   pre-registered; the causal claim is deliberately narrowed to "the opening
   surge is real, directional, and corridor-shaped," carried by the
   conjunction rather than any single test.

4. **Feed-forward.** Task 2's limitations chapter is to be built from the
   three residual-concession subsections of the memo, ordered A (population
   composition, attaches to the lead result), then C (one-sided marginal
   significance), then B (small-n bridge status) — naming each threat on the
   thesis's terms before an examiner can.

## Consequences

- The defense never disputes a true premise of an attack; each seam's
  concession is one the thesis text already prints (§4.4, §5.2–5.3, §6.4),
  so the oral defense can point to anticipation in situ.
- Direction C is explicitly positioned as hypothesis, which lowers its
  evidentiary billing but makes Chapter 6's existence the answer to Seam B.
- The Chapter 5 claim is narrowed to the conjunction; no future edit should
  headline p = 0.041 as standalone confirmation.
- `defense_memo.md` supplies Task 2 (limitations) and the one-breath answers
  for the oral defense with no further derivation needed.

## Rejected alternatives

- **Contesting the mechanical-contrast premise of Seam A** (arguing the gap
  is not definitional): rejected — the premise is true, and disputing it
  spends credibility where conceding it converts the attack into the
  mechanism statement.
- **Defending r = 0.826 statistically** (e.g., leaning on its nominal p under
  normality): rejected — small-n municipal correlation cannot carry inference
  weight, and the thesis text already stages it as pattern-level; a
  statistical defense would contradict the printed staging.
- **Reporting only two-sided SCM p-values to preempt the sidedness attack:**
  rejected — it abandons a correctly pre-specified directional hypothesis and
  turns a defensible posture into an apparent retreat; disclosure of both,
  with the one-sided choice argued ex ante, dominates.
- **Applying a formal multiplicity correction across treated municipalities:**
  rejected as the headline response — the informative object is the corridor
  geography of the significant set, which a correction ignores; the memo
  instead concedes the correction would not be survived and relocates the
  claim to the conjunction.
