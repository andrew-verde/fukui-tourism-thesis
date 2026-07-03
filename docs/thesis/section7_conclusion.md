# 7. Conclusion

## 7.1 What was established

Four findings, each carried by a different design, together answer the
thesis question. The Hokuriku Shinkansen extension *worked* as an experience
intervention: net promoter score rose +0.55 (strengthening to +0.65 once the
Noto earthquake's contamination of the control is removed) alongside a small,
robust gain in transport satisfaction, while a placebo-style outcome stayed
null (Chapter 3). The demand surge behind it was *real but mostly transient*:
Fukui City's opening-window lift of +29.2% clears a national in-space placebo
test (one-sided p = 0.041 against 1,538 well-fitting donors), survives a
backdated negative control and leave-one-out donor sensitivity, and appears
precisely along the new corridor — yet decays everywhere except the two
municipalities with strong destination anchors (Chapter 5). The binding
constraint on converting the surge is *transport-access friction among the
very visitors the extension delivers*: 7.09% of shinkansen arrivers report it,
against 0.66% of car arrivers, and it is simultaneously the largest structural
damage path to satisfaction (β ≈ −0.123), the most prevalent coded friction,
and the friction most correlated with demand leakage (Chapter 4). And the
mechanism that, on the pattern-level evidence, separates durable from
transient response is *station-to-anchor conversion, not repeat visitation* —
repeat-visit share anti-predicts durability — which inverts the natural
target of tourism promotion and fixes the endpoint of any intervention worth
running (Chapter 6). All quantities
regenerate from the committed pipeline (`make reproduce-submission`; evidence
bindings in `thesis_master.md`).

## 7.2 Contributions

The thesis's contributions reduce to one claim and three layers of support.
The claim: an infrastructure demand shock is transient by default, durable
only under station-to-anchor conversion, and gated by a friction the
infrastructure itself concentrates in its own arrivals — the last mile, not
the trunk line. The layers: **Empirically**, it provides causal estimates of an
infrastructure shock on both experience and demand margins for one prefecture,
at municipal grain, from open data — including the finding that the shock's
demand effect is transient by default and durable only under an identifiable
conversion condition. **Mechanistically**, it identifies and triangulates a
single dominant friction and shows that the survey's loudest complaint and the
demand data's leakage are the same phenomenon seen from two directions,
culminating in a falsifiable conversion mechanism with a pre-registered test
design. **Methodologically**, it demonstrates a reproducibility discipline in
which provenance rules are enforced by the test suite — pinned vintages,
checksum gates, a source ledger, and a guard that fails the build when a
document makes a statistical claim without naming its reproduction path. The
combination is a transferable template for evidence-based regional
revitalization: diagnose the dominant friction, identify the conversion
mechanism, and pre-register the experiment that tests the fix at its causal
joint.

This claim sits at the junction of two literatures that have not met. The
high-speed-rail evaluation literature asks whether openings raise visitor
numbers, almost always at prefectural or city aggregate, and reports mixed,
context-dependent effects (Hashimoto et al., 2017; Li et al., 2019;
Yamamoto, 2016); it treats the visitor as delivered once the train arrives,
and so has no vocabulary for a shock that arrives and then leaks away — the
modal outcome in Fukui's municipal-grain data. The tourism-behavior
literature, conversely, measures frictions and satisfaction at the
individual level (Bernini & Cagnone, 2014; Sánchez-Rebull et al., 2018;
Žabkar et al., 2010) and increasingly tests nudge-style interventions
(Bohner & Schlüter, 2014; Goldstein et al., 2008; Kallbekken & Sælen, 2013),
but its interventions are typically untethered from any causal evidence
about which friction binds, and its effect-size assumptions are rarely
disciplined by an observed ceiling. This thesis supplies the missing
junction from open data: a causal demand estimate at the grain where
durability is decided (the municipality), an individual-level diagnosis of
the binding friction in the same event, the observation that the two point
at the same phenomenon (r = 0.826 across high-confidence municipalities),
and a pre-registered two-stage design (Friede & Kieser, 2003, 2006;
Proschan, 2005; Wittes & Brittain, 1990) whose power analysis is bounded by
the measured selection ceiling (d = 0.25) rather than by convention. The
exportable object is the template — diagnose the binding friction, identify
the conversion condition, pre-register the test at the causal joint — not
the Fukui-specific estimates.

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

## 7.4 From design to field

The immediate next step is executing the two-stage pilot: Stage 1 (n = 50 per
arm, online, explicitly non-confirmatory) to estimate the effect-size prior,
then Stage 2 re-powered by the pre-registered rule d_plan = max(0.10, d̂ − se)
as an on-site QR intercept at the Fukui, Awara-Onsen, and Tsuruga stations.
The design's own feasibility flag stays live: if the nudge closes about half
the observed ceiling, Stage 2 requires on the order of a thousand respondents
per arm, which the 7.09%-friction rail-arriver base may not supply at
intercept rates — an argument for DMO partnership rather than against the
test. Beyond the pilot, two extensions follow naturally: archival deposit of
the replication package under a DOI (Chapter 2's publication rule), and
repetition of the template on the next corridor opening, where the diagnosis
machinery — not the Fukui-specific estimates — is the exportable object. The
thesis ends where the mission it serves points: past the statistical
description of a problem, at a mechanism that can be acted on and an
intervention that can be measured.
