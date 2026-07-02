# Defense memo: the three identification threats

Purpose: steel-man the three attacks an examiner is most likely to mount, state
the defense each one meets, and record the residual concession — what we
honestly cannot rule out — framed so that conceding it strengthens the thesis.
Every number cited here is the committed, verified value from the thesis
chapters (§4.2, §4.3, §5.3–5.5, §6.2–6.3); none is new. Companion decision
record: ADR 0015.

Reading guide for the defense itself: each seam ends with a **one-breath
answer** — the sentence to say first when the question lands, before expanding.

---

## Seam A — arrival-mode selection (§4.2, the lead result)

### A.1 The attack, steel-manned

"Your headline contrast — 7.09% transport-access friction among shinkansen
arrivers versus 0.66% among car arrivers — is mechanical, not causal. Rail
arrivers do not have a car; asking whether they experienced difficulty moving
around without one is close to definitional. The same fourfold gap would appear
on any rail line into any car-dependent region, with or without a new
shinkansen. Worse, the populations differ: people who choose rail are
disproportionately first-time visitors, non-drivers, urban residents, and
inbound tourists — groups that would report more friction of every kind under
any transport regime. And your SEM coefficient cannot rescue this, because
Stage 2 is estimated on pooled friction-reporters, not within arrival mode. So
the 'lead result' is a composition artifact dressed as a finding about the
shinkansen."

This is the strongest form of the question because every factual premise in it
is true. The defense must not dispute the premises; it must show they support
the thesis's actual claim.

### A.2 The defense

**1. The "mechanical" reading concedes the mechanism — it does not refute the
finding.** The thesis's claim is not that the shinkansen makes people
friction-prone, nor that rail arrivers are psychologically different. The claim
(§4.2) is precisely the chain the attack calls definitional: rail arrival →
carless at the station → the last mile to the anchor is where friction bites.
"Rail arrivers have no car, so last-mile friction follows" is not an objection
to that chain; it is a restatement of it. What the extension changed is the
*scale and location* at which this definitional friction operates: it delivered
10,493 in-sample rail arrivers (and the demand surge Chapter 5 verifies) into a
region whose destination side is provisioned for the 74,266 who arrive by car.
A constraint can be mechanically produced and still be the binding constraint
on the marginal visitor the infrastructure delivers — that is exactly what
makes it actionable rather than mysterious.

**2. The contrast is category-specific in a way composition confounds are
not.** If the gap reflected "rail arrivers are different people who complain
more," the elevation should smear across friction categories — wayfinding,
waiting/crowding, accessibility, opening hours — because the postulated
differences (first-timers, older visitors, foreign tourists, non-drivers) touch
all of them. It does not smear. Transport access is the argmax of the
shinkansen-minus-other gap across all twelve coded friction types, and the
next-largest gap (waiting/crowding, 0.92 pp) is smaller by a factor of almost
six (§4.2). A single-category spike at the exact category the mechanism
predicts is the signature of a mechanism, not of a grievance-prone population.

**3. The friction predicts an independent outcome it should not predict under
the artifact reading.** Survey friction prevalence correlates at r = 0.826
with the leaked synthetic-control lift across the thirteen high-confidence
municipalities (§4.1, §6.2) — a quantity measured from mobile-location demand
data, in a different instrument, with different failure modes. A pure
survey-composition artifact has no business predicting where an independently
measured demand shock fails to stick. And the heterogeneity points the same
way: Eiheiji and Sakai durably convert *the same rail-arriving population*
that Fukui City leaks (§6.2). If the friction were a property of the people,
it would travel with the people; instead it varies with destination-side
last-mile provision, which is the treatment-side reading.

**4. What the SEM β = −0.123 adds beyond the raw split.** The split shows
where friction concentrates; it cannot show that the friction *matters*.
Stage 2 shows transport access is the largest and most precisely estimated
per-report damage path to satisfaction (β ≈ −0.123, p ≈ 1.2 × 10⁻⁸), and
Stage 1 shows ~73% of friction damage transmits through satisfaction into
visit intention (§4.1). Without the SEM, 7.09% could be prevalent but
harmless grumbling; with it, the concentrated friction is tied to the outcome
the thesis cares about. The two results answer different questions (*where*
vs *how much damage*), which is why neither substitutes for the other and why
the attack's observation that the SEM is pooled does not undercut the split —
the split, not the SEM, carries the arrival-mode claim.

**5. The design already contains the clean answer.** Direction B randomizes
*within* rail arrivers (Stage 2 intercepts rail arrivers at Fukui,
Awara-Onsen, and Tsuruga stations; §6.3), which severs the selection channel
entirely. The thesis does not merely acknowledge the selection problem — it
built the experiment whose randomization makes the selection question moot for
the intervention claim.

### A.3 Residual concession, and how to frame it

**What we cannot rule out:** FTAS records response location, not residence,
demographics, or itinerary (§4.4), so we cannot run a covariate-adjusted
contrast and cannot exclude that some share of the 5.32 pp gap reflects who
chooses rail (first-timers without local knowledge) rather than carlessness
per se. We also cannot produce the within-person counterfactual "the same
visitor, arriving by car."

**Framing:** concede the selection channel *into arrival mode* fully and
without discomfort, because the thesis never needs the within-person
counterfactual. The policy object is the arriving population as it actually
arrives: the shinkansen determines who lands carless at Fukui's stations, and
the binding constraint on *that* population is what a prefecture can act on.
Selection into rail is not a confound of the diagnosis — it is part of the
treatment. The one distinction that matters for intervention design — is the
friction manipulable at the destination side? — is precisely what Direction B
tests. Framed this way, the concession converts the examiner's strongest
question into the motivation for the thesis's closing chapter.

**One-breath answer:** "You're right that the gap is mechanical — carless
arrival creates last-mile exposure — and that mechanism *is* the finding: the
extension delivers thousands of carless visitors into a car-provisioned
region, the friction spikes only in the category the mechanism predicts, it
predicts demand leakage in independent data, and Direction B randomizes within
rail arrivers so the intervention claim never rests on the selection contrast."

---

## Seam B — the durability reframe (Direction C)

### B.1 The attack, steel-manned

"Your durability story rests on thirteen municipalities. An r = 0.826 with
n = 13 has a confidence interval stretching roughly from 0.5 to 0.95, one or
two influential points — Fukui City's 40.5 pp leaked lift above all — could be
doing most of the work, and the regime classification itself (durable /
transient / none) is your own construction with researcher degrees of freedom
(ADR 0006). On top of that you assert the counterintuitive claim that
repeat-visit share *anti-predicts* durability, which has a mundane rival
explanation: mature destinations near saturation naturally show high repeat
share and low headroom for a new-demand lift — a ceiling effect, not a
conversion mechanism. Two anchor municipalities and a just-so story do not
license inverting the received wisdom that repeat visitation is the goal of
destination management."

### B.2 The defense

**1. The thesis already stages this evidence at the weight it can bear.**
§4.1 states in text that with n = 13 this is "a pattern-level observation, not
an estimate to headline," and §4.4 makes the regime dose–response explicitly
corroborative, with the arrival-mode contrast as the load-bearing result. §6.4
repeats that the r = 0.826 is observational and motivates rather than
establishes the mechanism. The examiner's characterization of the evidence's
strength is one the thesis printed first, in its own voice. The defense is not
"the correlation is strong"; it is "the correlation was never asked to carry
the claim."

**2. The mechanism, not the correlation, carries the weight — and the
mechanism is independently interpretable.** Station→anchor conversion was
derived from the arrival-mode result (the last mile is where friction bites),
then checked against the regime map. The municipalities it picks out are not
arbitrary: the durable set is exactly the anchor-possessing pair — Eiheiji
(JIS 18322, the Eihei-ji temple complex, +49.0% opening lift sustaining at
+14.5%) and Sakai (18210, Tōjinbō) — while the leaky one is the pass-through
terminal, Fukui City (18201, +29.2% decaying to −11.3%). A story fit post hoc
to noise does not usually assign the temple to "converts arrivals" and the
station city to "captures arrivals but leaks conversion" — that assignment
is what the mechanism predicts before looking.

**3. The anti-prediction licenses one narrow thing, and the thesis uses it
for exactly that.** The claim is not "repeat visitation is bad" or "repeat
share causes leakage." It is a *targeting* result: a high repeat share is the
signature of a destination recirculating an existing base rather than
acquiring new station-to-anchor conversions (§6.2), so an intervention aimed
at durability should target first-visit anchor conversion — which is precisely
the endpoint inversion Direction B implements (primary outcome = visit
intention on the anchor task, not repeat conversion; §6.3). The anti-prediction
selects an experimental endpoint. It does not, and is never used to, estimate
a causal effect of repeat share on anything.

**4. The ceiling-effect rival changes the label, not the implication.** Suppose
the examiner's mundane story is right: saturated destinations have high repeat
share and no headroom. Then new-arrival acquisition is still where durable
growth must come from, and the intervention should still target first-visit
conversion. The rival explanation and the conversion mechanism disagree about
*why* repeat share anti-predicts, but they converge on the design implication
the thesis actually draws. This is worth saying at the defense: the endpoint
choice is robust to losing the argument about the anti-prediction's cause.

### B.3 Residual concession, and how to frame it

**What we cannot rule out:** with n = 13, municipality-level confounding —
most plausibly, anchor presence itself driving both friction-report geography
and durability — cannot be excluded, and the anti-prediction would not survive
as a standalone finding in any journal. The regime thresholds involve
researcher judgment, recorded in ADR 0006 but judgment nonetheless.

**Framing:** the concession is the hinge of the thesis's structure, so make it
structural: Direction C is the bridge between a verified diagnosis (Chapters
4–5) and a pre-registered test (Direction B), and bridges are allowed to be
hypotheses. Its two design-relevant outputs — target the last mile, measure
first-visit anchor conversion — are exactly the two things the experiment
exists to test, and the endpoint choice survives even the strongest rival
explanation. "This is the part of the thesis that is a hypothesis, which is
why the next chapter is an experiment" is a stronger position than defending
0.826 as if it were an estimate.

**One-breath answer:** "The correlation is corroboration, not the claim — the
thesis says so in §4.1 — and the mechanism's only load-bearing use is picking
the experiment's endpoint, a choice that survives even if the anti-prediction
turns out to be a ceiling effect, because either story says durable growth
comes from new-arrival conversion."

---

## Seam C — SCM marginal significance (Direction D)

### C.1 The attack, steel-manned

"Your causal anchor is a one-sided p = 0.041 — two-sided 0.168, which you
report but do not headline. One naturally suspects the sidedness was chosen
because the two-sided test fails. The suspicion deepens on the test statistic:
the conventional post-period-mean gap for Fukui City is null (p = 0.83), and
only after seeing that did the analysis move to an 'opening window' where the
result clears. That is test-statistic shopping. Four municipalities clearing a
10% one-sided threshold invites a multiplicity correction that none would
survive. And the r = 0.826 'corroboration' is circular: the leaked lift is
computed from the same synthetic-control gaps whose reality is in question, so
you are using the estimator to validate the estimator."

### C.2 The defense

**1. The sidedness is entailed by the intervention, not extracted from the
data.** A high-speed rail extension predicts a demand *increase*; no reviewer
would have accepted "the shinkansen may have suppressed Fukui tourism" as the
alternative hypothesis worth power. The direction was fixed by the
intervention before estimation (§5.3), the two-sided value is disclosed in the
same sentence, and §6.4 carries the one-sided posture forward as a named
limitation. Choosing the test the hypothesis implies, then disclosing the
stricter one, is the opposite of concealment.

**2. The window is disciplined by the effect's shape, and the null post-mean
is evidence of honesty, not of shopping.** §5.2 argues *before* the test that
for a transient effect the post-period mean averages the surge away — and the
regime map (§4.1) had already established transience as the dominant response
shape from an independent direction. Fukui City's post-mean null (p = 0.83) is
printed in the thesis as the correct description of a spike that faded. The
shopping accusation requires the window to have been selected to manufacture
significance; the actual sequence is that the estimand was matched to an
effect shape documented elsewhere first, and the discarded statistic is
reported rather than buried.

**3. The real strength is the falsification architecture, and it should be
led with.** Three tests, each aimed at a distinct failure mode: (a) the
backdated in-time negative control — the full design re-run at March 2023 on
genuinely pre-event data — is silent (−3.5%, p = 0.47 against 1,544 well-fit
placebos), which is the direct answer to "your estimator manufactures
surges"; (b) leave-one-out donor sensitivity bounds the surge at 26.2–39.8%,
never near zero, so no single donor carries it; (c) the fit gate discards the
two most spectacular point estimates in the prefecture — Katsuyama (+58.5%)
and Ikeda (+48.0%), pre-RMSPE 0.30 against the 0.15 bar — demonstrating the
battery binds against the researcher's interest. A design that deletes its own
best numbers for fit reasons is not one tuning choices toward significance.

**4. Multiplicity is answered by geography, not by correction.** Under the
noise hypothesis, the municipalities clearing the placebo test should scatter
across the prefecture. Instead the well-fit significant set is exactly the
new-corridor geography — {Eiheiji, Fukui City, Tsuruga, Sakai}: the terminal
city, the two other new-station catchments, and the temple anchor one valley
over (§5.3). The joint event "the survivors are precisely the corridor" is far
less probable under noise than any single p-value suggests, and it is the
corridor pattern, not the count of survivors, that the thesis reads.

**5. The circularity charge conflates two claims with two evidence bases.**
The claim "the demand signal is real" rests on the placebo battery alone —
nowhere does the r = 0.826 correlation enter Chapter 5's inference. The
correlation joins SCM leakage to *survey friction*, an independent instrument
that never enters the synthetic-control fitting. Using estimator outputs on
the demand side of a demand–friction correlation is not the estimator
validating itself; circularity would require friction data inside the SCM or
SCM output inside the friction measurement, and neither occurs.

### C.3 Residual concession, and how to frame it

**What we cannot rule out:** p = 0.041 is marginal by any reading; it would
not survive a family-wise correction across treated municipalities, a
two-sided reader sees 0.168, and the opening-window estimand — however
well-motivated — was not pre-registered before the data existed. The panel is
vendor mobile-location data supporting gap, not level, inference (§5.1).

**Framing:** narrow the claim until the concession cannot reach it. The thesis
needs one thing from Chapter 5: that the March 2024 opening surge is real,
directional as predicted, and corridor-shaped — not that any individual
p-value is decisive. The identification is by conjunction: a directionally
pre-specified surge at placebo rank ~1/24, a silent negative control, donor
stability, and corridor geography. Any single leg is attackable; the examiner
should be invited to name which leg they doubt, because each has a dedicated
falsification test that came back clean. Conceding "0.041 alone would be
thin" while standing on the conjunction reads as calibration, and it is also
simply true.

**One-breath answer:** "One-sided was fixed by the intervention's predicted
direction and the two-sided value is printed beside it; but the claim never
rested on 0.041 alone — it rests on the conjunction of a silent backdated
negative control, leave-one-out stability away from zero, a fit gate that
discarded our two biggest estimates, and a significant set that is exactly the
new corridor."

---

## Cross-seam posture

The three defenses share one spine, worth internalizing before the room:
**concede the channel, keep the claim.** Seam A concedes selection into rail
and keeps the binding-constraint diagnosis; Seam B concedes the correlation's
weakness and keeps the endpoint choice; Seam C concedes the marginal p and
keeps the conjunction. In each case the concession was already printed in the
thesis's own text (§4.4, §5.2–5.3, §6.4) before any examiner raises it — the
defense's job is to point at where, calmly, and then state the one-breath
answer. Task 2 (the limitations chapter) should be built directly from the
three "residual concession" subsections above, in this order of prominence:
A's population-composition residual first (it attaches to the lead result),
then C's marginal-significance posture, then B's small-n bridge status.
