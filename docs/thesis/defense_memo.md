# Defense memo: five points for examination

Purpose: state the strongest questions a committee member may raise, the
evidence that addresses each question, and the remaining uncertainty. Every
number cited here is the committed, verified value from the thesis chapters
(§4.2, §4.3, §5.3–5.5, §6.2–6.3) or from a committed result artifact; none is
new. Companion decision record: ADR 0015.

Each section ends with a **short answer** that states the main point before a
longer discussion.

**Revised 2026-07-30 against ADRs 0029–0032.** Three changes reshape this memo
and the reader should hold them throughout:

1. **Direction B is retired and was never fielded** (ADR 0029). The Stage 1 /
   Stage 2 protocol survives as a specified-but-unfielded appendix. Every place
   the earlier edition answered a selection objection with "and the experiment
   settles it" has been rewritten, because that answer is no longer available.
   Seams A and B are weaker than they were. This memo states that directly.
2. **Arm 3 ran and returned a bounded null** (ADR 0031): V1 fail, V2 fail, V3
   met descriptively. The thesis attempted to replicate its own template and
   did not succeed. The result also shows that the project reports
   pre-specified nulls. New **Seam D**.
3. **Arm 2 is live, single-use, and unfired** (ADRs 0020, 0032). It has no
   result and this memo states none. The test's status creates a separate
   question. New **Seam E**.

**Reproduction.** Chapter 5's causal battery uses `make synth-causal-arm` and
`make causal-robustness`. The SEM uses `make sem-ftas`. Chapter 6's
prioritization uses `make nudge-ranking`. Arm 3 uses 12 specifications across
two targets and 24 target-by-specification rows (ADR 0035). Reproduce its
numbers with `make arm3-kanazawa` and its Kanazawa V3 series with
`make arm3-kanazawa-pdfs`. Provenance rows are in `docs/source_ledger.md`.

---

## Seam A: arrival-mode selection (§4.2, the lead result)

### A.1 Critical question

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

Every factual premise in this question is true. The response should explain how
those premises relate to the thesis's actual claim.

### A.2 Response

**1. The "mechanical" reading describes the mechanism.** The thesis does not
claim that the shinkansen makes people
friction-prone, nor that rail arrivers are psychologically different. The claim
(§4.2) is precisely the chain the attack calls definitional: rail arrival →
carless at the station → the last mile to the anchor is where friction bites.
"Rail arrivers have no car, so last-mile friction follows" is not an objection
to that chain; it is a restatement of it. What the extension changed is the
*scale and location* at which this definitional friction operates: it delivered
10,493 in-sample rail arrivers (and the demand surge Chapter 5 verifies) into a
region whose destination side is provisioned for the 74,266 who arrive by car.
A mechanically produced constraint can still affect the marginal visitor the
infrastructure delivers.

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

**5. The clean answer is specified but was not run.** The earlier edition of
this memo pointed to Direction
B: Stage 2 randomized *within* rail arrivers (intercepts at Fukui,
Awara-Onsen, and Tsuruga stations; §6.3), which would have severed the selection
channel **for the manipulability question only**. Be precise about this even
though the arm is retired, because overstating what it would have delivered
invites the follow-up at A-iv: randomizing within rail arrivers tests whether
relieving the friction changes an outcome; it never decomposes the arrival-mode
gap into carlessness versus composition, because it holds arrival mode fixed by
design. **Direction B was retired without fielding (ADR
0029)**, so that move is gone and must not be attempted in the room. What
remains is genuinely weaker and still worth stating: the thesis identifies the
design that would settle the question, specifies it to fielding standard, and
places it in an appendix as an unfielded protocol rather than implying it was
run. The honest formulation is "we know what the clean test is, we specified
it, and we did not run it" — offered before the examiner extracts it. Do not
say "future work" as though the design were vague; do not imply evidence
exists. Volunteering the retirement costs one sentence and buys the room's
trust for Seams D and E, where the thesis does have executed pre-specified
work to show.

### A.3 Residual concession, and how to frame it

**What we cannot rule out:** FTAS records response location, not residence,
demographics, or itinerary (§4.4), so we cannot run a covariate-adjusted
contrast and cannot exclude that some share of the 5.32 pp gap reflects who
chooses rail (first-timers without local knowledge) rather than carlessness
per se. We also cannot produce the within-person counterfactual "the same
visitor, arriving by car."

**Name the denominator before switching it.** This section uses two different
comparisons and they are not interchangeable. 7.09% against
0.66% is the **car** comparison, a 6.43 pp gap and a 10.74× ratio; 5.32 pp and
≈ 4.003× is the comparison against **pooled other modes**, whose denominator is
1.7711661764394693. Both are committed values, and the thesis's own ADR 0020 §2
adjudicated exactly this ambiguity when it found the S3 sentence quoting one
half of each — it froze **pooled other** for S3, on the grounds that it is the
harder test and the only ratio the committed artifact defines. Do not drift
between them mid-answer. State which one is in play, and prefer pooled other
when the point is the size of the gap, because it is the conservative choice and
the one already adjudicated in writing.

Since ADR 0029 there is a second, larger residual: **the manipulability of the
friction is now untested.** No executed component of the thesis shows that
relieving transport-access friction changes any visitor outcome. That was
Direction B's job.

**Framing:** concede the selection channel *into arrival mode* fully and
without discomfort, because the thesis never needs the within-person
counterfactual. The policy object is the arriving population as it actually
arrives: the shinkansen determines who lands carless at Fukui's stations, and
the binding constraint on *that* population is what a prefecture can act on.
Selection into rail is not a confound of the diagnosis — it is part of the
treatment. On manipulability, do not reach for a substitute: concede that the
distinction that matters most for intervention design is the one the retired
arm would have tested, and that the thesis therefore claims a diagnosis and a
specified remedy, not a demonstrated remedy. The claim that survives the
concession is exact and defensible: *this is the binding constraint on the
population the infrastructure delivers, and here is the design that would test
whether it can be relieved.*

**Short answer:** "The gap is mechanical. Carless arrival creates last-mile
exposure, and that mechanism is the finding. The
extension delivers thousands of carless visitors into a car-provisioned
region, the friction spikes only in the category the mechanism predicts, and it
predicts demand leakage in independent data. The randomized test that would
separate carlessness from composition was specified and not fielded, so I claim
the diagnosis, not a demonstrated remedy."

---

## Seam B: the durability reframe (Direction C)

### B.1 Critical question

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

### B.2 Response

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
the endpoint inversion the Direction B protocol specifies (primary outcome =
visit intention on the anchor task, not repeat conversion; §6.3, now the
unfielded-protocol appendix per ADR 0029). The anti-prediction selects a design
endpoint, in a design that was never fielded. It does not, and is never used
to, estimate a causal effect of repeat share on anything. Note the licensing
is unchanged by the retirement: a single, narrow, design-selecting use is what
ADR 0015 Seam B licensed, and an unfielded design still consumed exactly that
one use and no more.

**4. The ceiling-effect rival changes the label, not the implication.** Suppose
the examiner's mundane story is right: saturated destinations have high repeat
share and no headroom. Then new-arrival acquisition is still where durable
growth must come from, and the intervention should still target first-visit
conversion. The rival explanation and the conversion mechanism disagree about
*why* repeat share anti-predicts, but they converge on the design implication
the thesis actually draws. This is worth saying at the defense: the endpoint
choice is robust to losing the argument about the anti-prediction's cause.

### B.3 Remaining uncertainty and framing

**What we cannot rule out:** with n = 13, municipality-level confounding —
most plausibly, anchor presence itself driving both friction-report geography
and durability — cannot be excluded, and the anti-prediction would not survive
as a standalone finding in any journal. The regime thresholds involve
researcher judgment, recorded in ADR 0006 but judgment nonetheless.

**Framing:** the concession is the hinge of the thesis's structure, so make it
structural: Direction C is the bridge between a verified diagnosis (Chapters
4–5) and a pre-specified test, and bridges are allowed to be hypotheses. What
changed with ADR 0029 is *which* test the bridge leads to. It is no longer the
Direction B experiment; it is **Arm 2**, the out-of-sample prediction test
whose co-primary P1 is exactly this seam's claim — that the durable
municipalities (Sakai 18210, Eiheiji 18322) keep positive gaps and outrun the
transient set on unseen panel months. Claim this precisely, because it answers
one part of the attack and not the rest: the n = 13 pattern is no longer being
defended as an estimate, it is *held to a prediction on data that did not exist
when the pattern was described*, which is the right answer to "you are
over-reading a correlation." It is **not** an answer to the influential-point,
threshold-judgment, or generalizability halves of the attack — Arm 2 reuses the
same thirteen municipalities and the same regime assignments, so Fukui City can
still be doing the work and ADR 0006's thresholds are still the author's. Those
remain conceded at B.3. Say plainly that the test is specified and not yet run
(Seam E), and that its verdict meanings were written before any result existed.

**One-breath answer:** "The correlation is corroboration, not the claim — the
thesis says so in §4.1 — and rather than defend 0.826 as an estimate, the
durability account was written into a pre-specified out-of-sample prediction on
months that did not exist when the pattern was found; the endpoint logic also
survives even if the anti-prediction is a ceiling effect, because either story
says durable growth comes from new-arrival conversion."

---

## Seam C: SCM marginal significance (Direction D)

### C.1 Critical question

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

### C.2 Response

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

### C.3 Remaining uncertainty and framing

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

## Seam D: the Arm 3 replication null (ADR 0031)

Every number in this seam is byte-exact from
`output/arm3_kanazawa/causal_robustness/metrics.json`, reproduced by
`make arm3-kanazawa`.

### D.1 Critical question

"You claim to have built an exportable template. You then applied it to the
obvious test case — the 2015 Hokuriku Shinkansen extension to Kanazawa, a boom
so well documented that failing to find it should be impossible — and it did
not clear your own bar. V1 fails, V2 fails, and V3 is descriptive only. So the
one time your template was pointed at a case you did not design it around, it
returned nothing. That is not a bounded null; it is evidence that the Fukui
result is a Fukui-specific artifact of the analyst's choices, which is exactly
what the Chapter 5 critique alleged. And 'aggregation dilution' is an
unfalsifiable excuse that happens to be the one explanation you cannot check."

### D.2 Response

**1. Lead with the fact that the verdict was written first.** ADR 0021 §6
fixed the tier tests, the suspect-checking order, and the meaning of each
outcome *before any Kanazawa data was touched*, precisely so the verdict would
follow mechanically. When the result came back adverse, the contract obliged
the thesis to report it and to bound its own headline claim. ADR 0031 does
exactly that: ADR 0017's exportable-object claim is bounded to "specified for
export, not yet demonstrated," and two Phase 4 edits (T1, T2) are fired to
strip the generalization language out of §8.2 and §6.5. A project that
manufactures results does not write the contract that costs it its most
attractive claim and then honour it. This is the strongest single piece of
evidence in the thesis about how its other results were produced — and it is
the answer to C-iii.

**2. Specific failure modes are ruled out — claim that, and not more.** The
failure is confined to the significance tiers, and each diagnostic built to
catch a *particular* pathology comes back clean: Ishikawa's pre-period RMSPE is
0.041470 against the 0.15 good-fit gate, so the synthetic control tracks the
pre-period rather than straining; the backdated in-time negative control is
silent at −2.386% with p = 0.580645, so the design does not manufacture surges
on pre-event data; leave-one-out keeps the opening estimate bounded away from
zero at a minimum of +6.645%, so no single donor carries it; and the point
estimates are positive and sizeable in the predicted direction — +10.212% at the
opening and +10.511% late. What this licenses is narrow: a positive estimate
that is not separable from the placebo distribution (p = 0.181818).

**Do not upgrade this into "the pipeline works" or "the null is purely a power
problem."** Neither follows. A silent negative control and a stable
leave-one-out are also consistent with an estimator that recovers noise, or one
carrying a stable bias, and low power is an inference about the estimator's
sensitivity that this battery does not measure. The defensible sentence is that
the pre-declared failure modes were tested and did not fire, so the null is
*bounded* rather than uninterpretable — which is exactly what the verdict says
and no more.

**3. Both alternative explanations were pre-declared and both were ruled out
on the record.** §6 required three suspects checked in a fixed order before any
interpretation. The placebo floor is ruled out: Ishikawa retained 32 placebos,
so the attainable one-sided floor is 1/33 = 0.030303 and the α = 0.05 threshold
was genuinely reachable — the failures are real, not artifacts of a truncated
placebo distribution. Donor-pool contamination is ruled out: the strict
20-prefecture pool, dropping all 14 flagged codes, gives +7.430% with
p = 0.210526 — removing contaminated donors does not recover significance.
The failure is also not specification-dependent: no run in the battery reaches
p ≤ 0.05 on V1a, and the smallest one-sided opening p is the primary's
0.181818. State the battery's size carefully — the frozen artifact records
`specification_count: 12`, run against both targets (Ishikawa and Toyama) for
24 target-by-specification rows. Say "12 specifications across two targets," not
"24 specifications." (ADR 0031's looser wording is corrected by ADR 0035, which
retires "24-specification battery" everywhere.)

**4. Aggregation dilution is not an excuse invented after the fact — it was
named in advance and its untestability was documented in advance.** It appears
in ADR 0021 §6's pre-declared suspect list, written before the result. Its
untestability was established independently and earlier: the data audit §2
verdict records that no balanced municipality-month panel exists for Ishikawa
2013–2019, and design §7.1 records that no pre-2021 municipal mobile panel
exists from any provider. The surviving suspect is the one this grain cannot
probe, and that ordering — pre-declared, then found untestable — is the
opposite of a post-hoc rescue. V3 is what makes it more than a shrug: both
approved Kanazawa monthly series are positive on both the surge and the
persistence comparison, so the surge is visible *at the anchor city* while the
Ishikawa-wide gap is large but noisy. That is precisely the pattern dilution
predicts.

**5. Insist on the scope of what failed.** The tested proposition is
portability *at prefecture grain*, in 2015, for a different corridor. It is not
the Fukui result, which rests on its own committed battery — ADR 0021 §6 says
so in terms ("a V1 failure does not touch the 2024 Fukui results"), ADR 0031
records that no Track T row reaches Chapter 5, and nothing in Arm 3 re-opens
any Direction D analysis. Do not accept a reframe in which Arm 3 audits
Chapter 5. It tests a different claim, at a different grain, in a different
prefecture, nine years earlier.

**6. Refuse the two barred specifications even if the examiner offers them.**
The `japanese_only` specification gives the battery's smallest late p (0.090909,
at +14.333%); ADR 0021 §5 declares sensitivities "reported, never headline," so
it is reported and not leaned on. `foreign_only` fails the good-fit gate
outright — pre-RMSPE 0.214248 for Ishikawa and 0.342352 for Toyama, both above
0.15 — and ADR 0031 states it "must not be interpreted at all." Honour that
literally: cite the fit failure as the reason it is excluded and characterize
its estimates in no direction whatsoever, favourable or unfavourable. Naming
what its numbers look like is already interpretation. If an examiner reaches for
either specification to be generous, decline on the record. Declining a number
that might help is the cheapest credibility available in the room.

### D.3 Remaining uncertainty and framing

**What we cannot rule out:** that the template genuinely does not port — that
the 2024 Fukui pattern is corridor-specific or period-specific and would fail
replication wherever it were tried. Dilution is live but unproven, and it is
unprovable with any data that exists for 2015; "the grain is wrong" and "the
template is wrong" are observationally equivalent here. V2b's durable-where-
anchored pattern does appear at prefecture grain — Ishikawa retains 0.827568 of
its surge against Toyama's 0.030290 — but §6 declares V2b sign-level with no
p-value and forbids promoting any claim on it, so it is reported as
consistent-but-underpowered and cannot be used to soften the null.

**Framing:** the thesis's contribution claim was already written to survive
this. ADR 0017 claims an object *specified* for export, and after ADR 0031 it
claims exactly that and no more — the wording does not acquire a Kanazawa leg.
Present the null as the thesis's methodological centrepiece rather than its
wound: it is the one place where a pre-written contract was executed against an
unseen case and the project reported the answer it did not want. An examiner
who believes the null is a fatal blow should be asked what the alternative
looked like — a project that tried the replication and buried it, or one that
never tried. Both are worse, and both are common.

**One-breath answer:** "It failed the significance tiers and I report that as a
bounded null: the estimate is positive at +10.212% with a good pre-fit and a
silent backdated control, but not separable from the placebos at p = 0.181818,
and the pre-declared explanation that survives — Kanazawa's surge diluted
across Ishikawa — is untestable because no municipal panel exists for 2015. So
the template's portability is not demonstrated at prefecture grain, the
contribution claim is bounded to 'specified for export, not yet demonstrated,'
and the 2024 Fukui results are untouched."

---

## Seam E: the unfired prediction test (Arm 2)

**Standing constraint on this seam: Arm 2 has no result and this memo asserts
none.** It is a single-use test; the pre-specification option is spent the
moment unseen outcome values are observed. Nothing here may be phrased as
though an outcome were known or expected.

### E.1 Critical question

"You have written a pre-registered out-of-sample test, declared it live, and
not run it. That is the most convenient possible state: you get the rhetorical
credit of pre-registration with none of the risk. Nothing stops you from
running it, seeing an unfavourable answer, and quietly declining to mention it
— your own document says the option is spent on first look, which is precisely
the structure that makes selective reporting invisible. And if it does return a
null, your empirical upgrade is a retired survey arm, a replication null, and a
prediction failure."

### E.2 Response

**1. The precedent is on the record and it is adverse.** The right answer to
"you will only report it if it is favourable" is not a promise but a case: Arm
3. Its interpretation contract was written before the data was touched, it
returned a null, and the null is written into an accepted ADR that bounds the
thesis's own headline contribution claim and fires two edits stripping
generalization language from the chapters. The project has already paid this
price once, in public, in the same repository, weeks before the defense.

**2. The verdict meanings are committed in writing, in the chapter, in
pre-result tense.** §7.1 states what each outcome was committed to mean
"before the result existed," including the falsification branch: "the
falsification is a first-class result of this thesis." It also fixes that the
headline "requires both" co-primaries and that "one primary alone is reported
as partial support, never as confirmation." Quote that text; do not paraphrase
it and do not repair its pre-result tense. Its value at the defense is that it
was written when the answer was unknown.

**3. The single-use structure is a cost the thesis accepted, not a loophole it
built.** The frozen predictor deliberately forgoes any improvement from newer
survey waves as the price of a clean prediction (§7.1). A vintage-revision
guard runs before any unseen outcome is decoded, and if it trips — RMS relative
revision above 2% on a confirmatory municipality, or a donor exiting the fit
gate — the analysis stops and a logged deviation decision is forced rather than
quietly absorbed. Mixing vintages is forbidden outright. These are constraints
that only bind the analyst.

**4. Say what the honest answer is if it lands as a null — by quotation.**
§7.1 requires that the contract be "quoted, not paraphrased, wherever the
verdict is later discussed." The falsification branch, verbatim:

> Either primary falsified: the falsification is a first-class result of this
> thesis — the anchor-conversion account organizes 2024–2025 but fails
> prospectively; the claim is bounded to the seen window, the diagnosis of
> Chapter 4 is unaffected (it never depended on durability), and the
> contribution re-weights onto the diagnosis and the honest test itself.

That is a defensible thesis. It is also the version an examiner will respect,
because a project willing to state its own falsification condition in advance
is making a claim about method that survives either outcome. Read it out rather
than summarizing it — the provenance value is in the exactness.

### E.3 Remaining uncertainty and framing

**What we cannot rule out:** at the time of writing the test is unfired, so
this seam rests on Arm 3's precedent and on documentary commitment, not on a
second executed instance. If Arm 2 runs before the defense, this seam must be
rewritten around its actual verdict, quoting the §7.1 contract rather than
re-deriving it — and if it returns a null, the thesis's empirical upgrade does
reduce to the non-survey engine plus two honest nulls.

**The sharper residual, and it should be volunteered:** the specification is
frozen, but **the execution timing is not**. §7.1 sets a floor of six unseen
months, not a fixed window, and months keep accruing — so the analyst still
chooses *when* to run and therefore how long the unseen window is. That
discretion sits outside the frozen contract and no guard removes it. It is the
strongest pre-registration attack available on Arm 2, and the honest answer is
that it is a real residual degree of freedom, disclosed rather than defended.

**Framing:** do not oversell the unfired test as though it were evidence. Its
present value is structural: it shows the durability account was written down
in falsifiable form, on data that did not exist when the account was formed,
with the verdict meanings fixed in advance. If the examiner asks why it has not
been run, the answer is about execution timing and nothing else: a single-use
test is run once, and there is no reason to hurry the one attempt. Do **not** say
the delay is to get the specification right — ADR 0020 is accepted and binding,
the specification *is* frozen, and changing it now would require a deviation ADR
and demote the analysis to exploratory. The scripts and the run date are the
only live variables.

**One-breath answer:** "It is specified, single-use, and not yet run, so I
claim nothing from it — what I claim is the structure: the durability account
is written as a falsifiable prediction on months that did not exist when it was
formed, the verdict meanings are fixed in the chapter in pre-result tense, and
the project has already shown with Arm 3 that it reports a pre-specified null
even when the null costs it a headline claim."

---

## Second-order follow-ups (mock defense)

The defenses above are themselves attackable. For each seam, the sharpest
follow-up a committee member could put to the *defense*, and the prepared
answer. These are the questions that arrive after the one-breath answer
lands, so they are the ones that decide the room.

### Seam A follow-ups

**A-ii. "Your category-specificity argument cuts both ways: carless people
complain about transport, not cleanliness — so the single-category spike is
predicted by the composition story too. Specificity separates nothing."**
Half-right, and the answer is to say which confound each leg kills.
Specificity rules out the *generic* population confound (grievance-prone,
older, foreign visitors would elevate wayfinding, waiting, accessibility as
well — they do not). It cannot separate carlessness-as-mechanism from
carlessness-as-composition — but that separation is already conceded in
§7.3, and for policy the two are equivalent: both route the fix through
destination-side last-mile provision. The legs that work *across* that
concession are the leakage correlation and the destination-side
heterogeneity, not specificity.

**A-iii. "You lean on r = 0.826 to defend Seam A while conceding in Seam B
that it is pattern-level only. You cannot spend the same correlation twice
at two different prices."**
The weight claimed in Seam A is directional convergence — a survey artifact
should not co-locate with independently measured demand leakage *at all* —
not the magnitude 0.826. But the honest version of the answer: discount the
correlation entirely, and the Seam A defense still stands on specificity
plus the Eiheiji/Sakai-versus-Fukui-City heterogeneity. Say that
explicitly; it converts an apparent double-spend into a redundancy claim.

**A-iv. "Even the retired experiment would only have mooted selection for
the nudge effect. Your headline diagnosis is observational and stays that
way."**
Correct twice over, and concede both immediately. Direction B would have
tested *manipulability* of the friction, never the decomposition of the
5.32 pp gap — so even had it been fielded, §4.2 would remain observational.
And it was not fielded. The diagnosis never claims more than: this is the
binding, plausibly manipulable constraint on the arriving population. The
word carrying the weight is *plausibly*, and it is doing so unaided.

### Seam B follow-ups

**B-ii. "If the saturation story and your conversion mechanism imply the
same endpoint, the mechanism adds nothing — drop it and keep the endpoint."**
The convergence is on the endpoint only, not on the predicted result. The
conversion-gate mechanism predicts that relieving transport-access friction
raises anchor visit-intention (the retired H1); a pure saturation account
gives no reason an information nudge should move anything. The discriminating
test is therefore *specified and unfielded* — do not claim the pilot
discriminates, because the pilot does not exist. What can be claimed: the
mechanism is retained because it is the falsifiable member of the pair, and it
is not idle even so — Arm 2's P1/P2 put its observational implication (durable
municipalities keep their gaps; the friction ordering predicts the gap
ordering) at risk on unseen months. That is a weaker discrimination than the
experiment would have provided, and it is a real one.

**B-iii. "The design's tasks all point at anchors. If anchor presence is the
confounder, it tells you nothing about municipalities without anchors."**
Concede the scope: the template's conversion step presupposes an anchor to
convert *to*, and the thesis's advice to anchor-less municipalities is
outside the tested claim. This is a scope boundary, not a validity threat —
and it is worth stating at the defense before it is asked, because it
sounds like a damaging question and is actually a definitional one. Note the
scope boundary binds the specification too: an unfielded design is bounded by
the same limits its fielded version would have had.

### Seam C follow-ups

**C-ii. "Your 'conjunction' is verbal Bayesianism. Four legs on one vendor
panel are not four independent tests — a panel-level artifact synchronized
to March 2024 passes all of them."**
The legs are independent in *failure mode*, not in data: backdating catches
estimator-manufactured surges, leave-one-out catches donor luck, the
placebo rank catches noise, geography catches multiplicity — and that is
the claim, so grant the data-dependence. Then close the remaining gap: a
national panel artifact (vendor methodology change in March 2024) would
shift donors too, and the in-space placebo differences it out. What
survives is only a *Fukui-corridor-specific* vendor artifact coinciding
exactly with the opening month — a hypothesis with no independent evidence
and near-unfalsifiable structure. Name it, price it, move on.

**C-iii. "Where is the pre-registration of the SCM design? 'Ex ante' is an
assertion about your own mind."**
Concede: the SCM analysis was not pre-registered (§7.3 says so — the window
was not pre-registered either). The defense is structural, not
testimonial: the direction is entailed by the intervention's semantics
rather than chosen, and the backdated negative control performs the
discipline pre-registration would have — it is the test that would have
exposed a shopped design, and it is silent. Then close with the part that is
no longer a promise: the project's pre-specification standard is met, and
*demonstrated*, in Arm 3 — an interpretation contract written before any
result existed, executed, and returning a null that the contract then obliged
the thesis to report against its own interest (Seam D). The credibility of
"ex ante" is no longer an assertion about my own mind; there is a case where
it cost something.

### Seam D follow-ups

**D-ii. "If dilution is real, your Fukui result should dilute too — you
estimated Fukui at municipality grain and Kanazawa at prefecture grain, so
you have changed the estimand between the finding and its replication and
called the mismatch an explanation."**
This is the sharpest question in the memo and it should be conceded to, not
argued with: the grain difference is real and it is the reason the
replication is not a like-for-like test. Then be precise about direction.
Chapter 5 estimates Fukui at municipality grain because the municipal panel
exists for 2024; Arm 3 estimates Ishikawa at prefecture grain because — per
the data audit §2 verdict and design §7.1 — no municipal panel exists for
2015 from any provider. The grain was forced by data availability, not
selected after seeing an unwelcome result, and it was fixed in the accepted
design before execution. What follows is a genuine limitation on the
*replication attempt*, which is exactly why the verdict is worded as
portability "not demonstrated at prefecture grain" rather than as portability
refuted. The claim the thesis withdrew is the generalization claim; it did not
substitute a weaker test and call it a pass.

**D-iii. "You keep saying the pipeline works because V1b and V1c passed. Those
are null results too. A silent negative control and a stable leave-one-out are
also what a pipeline that detects nothing produces."**
Half-right, and the distinction matters. A pipeline that detects nothing would
also produce a null *point estimate*; this one produces +10.212% at the opening
and +10.511% late, positive and in the predicted direction, with a good
pre-period fit at RMSPE 0.041470. So the estimator is not inert — it recovers a
sizeable positive gap and fails to separate it from a placebo distribution of
32 retained units. The correct reading is low power at this grain, and the
honest consequence is the one on the record: not demonstrated, with dilution
live and untestable.

### Seam E follow-ups

**E-ii. "Then run it now, in front of me."**
Decline, and give the real reason rather than a procedural one: it is
single-use, and running it under time pressure is how a vintage-revision guard
gets waved through. The guard runs first, always, and if it trips the required
response is a logged deviation decision, not a judgment call made in a defense
room. Offer the falsifiable commitment instead — the verdict meanings are
already fixed in §7.1 in pre-result tense, so the examiner can read what each
outcome obliges the thesis to say before it is known which one applies.

**E-iii. "Your empirical upgrade is now one retired arm, one null, and one
unfired test. What is actually new?"**
Answer without inflation: the non-survey evidence engine (ADRs 0027/0028) —
an observational opportunity-prioritization layer built from public
Code4Fukui and government data, reproducible by `make panel`, `make fetch-gov`,
`make opportunity-scan`, and `make sem-nonsurvey` — plus a pre-specified
bounded null replication, plus a specified-and-live prediction test. That is a
smaller upgrade than the roadmap originally projected, and it is honestly
stated. The thesis's defensible core was never the upgrade; it is the
diagnosis and the causal battery in Chapters 3–5, which the retirement and the
null do not touch.

## Cross-seam posture

The five defenses share one spine, worth internalizing before the room:
**concede the channel, keep the claim.** Seam A concedes selection into rail —
and now also concedes that manipulability is untested — and keeps the
binding-constraint diagnosis; Seam B concedes the correlation's weakness and
keeps the endpoint choice; Seam C concedes the marginal p and keeps the
conjunction; Seam D concedes that portability is not demonstrated and keeps the
2024 results and the method claim; Seam E concedes that the prediction test is
unfired and keeps the structural claim about how the account was written down.
In each case the concession was already printed in the thesis's own text or in
an accepted ADR (§4.4, §5.2–5.3, §6.4, ADRs 0029 and 0031) before any examiner
raises it — the defense's job is to point at where, calmly, and then state the
one-breath answer.

Two of the five concessions are now *executed* rather than promised, and that
is the memo's centre of gravity after ADRs 0029–0032: the thesis withdrew a
generalization claim because its own pre-written contract told it to, and it
retired an arm it could not field rather than reporting a design as though it
were evidence. Lead with those when the room turns adversarial.

Task 2 (the limitations chapter) should be built directly from the "residual
concession" subsections above, in this order of prominence: A's
population-composition residual first (it attaches to the lead result), then A's
new untested-manipulability residual, then D's not-demonstrated portability,
then C's marginal-significance posture, then B's small-n bridge status, with E
last and explicitly provisional. Note the chapter edits themselves are Phase 4
work — ADR 0023 §5 remains binding and no chapter file changes before then.
