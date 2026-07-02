# Limitations

*Drop-in replacement for §7.3 (see ADR 0016 for placement decision). Ordered
by how much each limit could change the thesis's reading, not by chapter.
Companion reasoning in `docs/thesis/defense_memo.md`; posture in ADR 0015.*

## 7.3 Limitations

The honest measure of a limitations section is whether it names the
objections a skeptical reader would raise before that reader does, and states
plainly what each objection reaches and what it does not. Three limits attach
to the thesis's identification claims and are treated first, in order of how
much of the argument they touch; the remaining limits are properties of the
data layer and are inherited by everything built on it.

**First, the arrival-mode contrast cannot separate carlessness from the
population that chooses rail.** The lead result — transport-access friction at
7.09% among shinkansen arrivers against 0.66% among car arrivers (§4.2) — is,
in one sense, mechanical: rail arrivers land without a car, and last-mile
friction follows. The thesis embraces that reading, because the chain *is*
the claimed mechanism, and the extension's contribution is the scale at which
it now operates — thousands of carless arrivals delivered into a region
provisioned for the car majority. What the design cannot do is adjust the
contrast for who the rail arrivers are: FTAS records the response location
but not residence, demographics, or itinerary, so some share of the 5.32
percentage-point gap may reflect first-time visitors' unfamiliarity rather
than carlessness itself, and the within-person counterfactual — the same
visitor arriving by car — is unobservable. Three facts bound how far this
concern can run. The gap is category-specific: transport access is the
largest shinkansen-minus-other gap across all twelve coded friction types,
with the runner-up smaller by a factor of almost six — where a
grievance-prone-population account predicts elevation smeared across
categories. The friction predicts an outcome measured in a different
instrument: its prevalence correlates at r = 0.826 with leaked
synthetic-control lift across the thirteen high-confidence municipalities.
And the same arriving population converts durably where the destination side
provides the last mile (Eiheiji, Sakai) and leaks where it does not (Fukui
City) — a pattern that follows destinations, not people. For the diagnosis,
selection into rail is therefore read as part of the treatment rather than a
confound of it; for the intervention, the question dissolves by design, since
Direction B randomizes within rail arrivers. What is conceded is the
population-composition residual on the descriptive contrast itself; what is
retained is the constraint diagnosis on the visitors the infrastructure
actually delivers.

**Second, the demand signal's significance is one-sided and marginal, and the
claim is sized accordingly.** The opening-window surge for Fukui City clears
its national in-space placebo at a one-sided p = 0.041; the two-sided value is
0.168, and no family-wise correction across treated municipalities would
leave the headline test standing alone. The sidedness was fixed ex ante by
the intervention's predicted direction — a rail extension is not a hypothesis
about demand suppression — and the opening-window estimand was matched to the
transient effect shape the regime map had already documented, with the
conventional post-period-mean statistic reported as the null it is (p = 0.83,
the correct description of a spike that faded). But the thesis does not ask
p = 0.041 to carry the causal claim by itself, and no reader should either.
The claim — the March 2024 surge is real, directional as predicted, and
corridor-shaped — rests on a conjunction: the placebo rank against 1,538
well-fitting donors, a backdated-2023 negative control that is silent
(p = 0.47), leave-one-out donor bounds of 26.2–39.8% that never approach
zero, a fit gate that discarded the prefecture's two most spectacular point
estimates for pre-period misfit, and a significant set that is exactly the
new-corridor geography rather than a scatter. Each leg is individually
attackable; each has a dedicated falsification test that came back clean.
What is conceded is that the evidence is marginal test-by-test; what is
retained is the narrow conjunction the chapters actually use.

**Third, the durability mechanism is a bridge, not an established result, and
the thesis prices it that way.** Direction C's claims — durability is
station-to-anchor conversion, and repeat-visit share anti-predicts it — rest
on thirteen high-confidence municipalities and a correlation of 0.826, staged
in §4.1 as pattern-level corroboration rather than a headline estimate. With
n = 13, municipality-level confounding cannot be excluded; most plausibly,
anchor presence itself drives both the geography of friction reports and the
durability of demand. The anti-prediction, moreover, is licensed for exactly
one use: choosing the experiment's endpoint. Direction B measures first-visit
anchor conversion rather than repeat conversion because that is what the
mechanism implies — and, notably, it is also what the strongest rival
explanation implies, since a saturation account of high repeat share equally
locates durable growth in new-arrival acquisition. The endpoint choice
therefore survives even if the mechanism's causal story does not. What is
conceded is that Direction C would not stand as a finding on its own; what is
retained is its role as the hypothesis that Chapter 6's pre-registered design
exists to test.

**The remaining limits are properties of the data layer.** The experience
estimates of Chapter 3 rest on an earthquake-compromised control, mitigated
but not cured by the specifications that remove the Noto shock's
contamination, and their pre-trends are read against a stated wobble. The
demand panel is mobile-location-derived vendor estimation, which supports gap
and rank inference, never absolute headcounts. FTAS is an intercept survey:
every prevalence is a floor (visitors deterred entirely are never
intercepted), locations are response sites, and the trustworthy objects are
magnitudes and rank order rather than population rates — a censoring that
cuts against the null of the arrival-mode contrast, not in its favor.
Finally, Direction B is a design and produces no evidence of efficacy: its
power analysis treats the observed car–rail satisfaction gap (d = 0.25) as a
selection ceiling under a named assumption — that this gap bounds the
manipulable margin — and the two-stage structure exists precisely because
that assumption is untested; Stage 1's only deliverable is the effect-size
prior that disciplines Stage 2's sample.

None of these limits reaches the central diagnosis — that transport-access
friction among rail arrivers is the binding constraint on converting the
extension's demand shock — because each was absorbed into the design that
produced it: the selection channel became the treatment definition, the
marginal significance became a conjunction of falsification tests, the
small-n mechanism became a pre-registered endpoint, and the data-layer floors
became directional arguments. What the limits discipline is everything the
thesis is *not* entitled to say: population friction rates, absolute demand
levels, a confirmed causal mechanism for durability, and any claim that the
proposed intervention works.
