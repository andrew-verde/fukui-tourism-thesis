# ADR 0041: Awara forward prediction test — result

Date: 2026-09-14
Status: **Accepted.** Records the outcome of the single execution authorised by ADR 0040.

## Result

**Headline verdict: prediction falsified**, per ADR 0040's contract, which requires both
primaries to confirm and treats either falsification as decisive.

Executed once, on 66 eligible unseen nights (2026-07-09 → 2026-09-12) at the pin
`d30a3f079cbb`. Vintage guard passed before the unseen read with **zero** revision across
all 1012 seen nights (rms 0.0, max 0.0, against limits 0.02 and 1 pp): upstream is
append-only over the seen window, so the vintage concern that motivated the guard is
empirically nil here. Of 157 post-2026-07-08 nights, 5 were excluded as flat-curve
forward-fills and the remainder lie at or beyond the pull date.

| | predicted | observed | status |
|---|---|---|---|
| **P1** MAE(M3) < MAE(M0) | state beats the naive rule | **7.58 pp vs 6.20 pp** — naive wins; Wilcoxon p = 0.910 | **falsified** |
| **P2** flag precision > base rate | soft nights identifiable | **52.9% vs 27.3%**, p = 0.0013, recall 1.00 | **confirmed** |
| S1 MAE ≤ 9.0 pp | no accuracy collapse | 7.58 pp | held |
| S2 M3 beats calendar-only | state adds over calendar | 7.58 vs 12.30 pp, p = 6.4e-5 | replicated |
| S3 peak−midweek ≥ 15 pp | demand gap persists | 17.9 pp | persists |

Secondaries are reported, never headline, per ADR 0040.

## What this licenses

The interpretation contract was written before the result existed, and its P1-falsified
branch applies verbatim: **at a 30-day horizon, a one-line seasonal rule is not improved
upon by reservation-curve state.** This is a substantive negative finding about the marginal
value of booking data, directly relevant to any DMO considering acquiring it, and it is
confirmatory — the specification, coefficients, thresholds and sidedness were committed in
`e1fe0d4` and the data pinned in `21623ef`, both before the unseen read.

It also replicates prospectively what the exploratory holdout found: the naive rule won
there too. Two independent windows, same direction.

The yield chapter is unaffected; it never depended on occupancy being forecastable. The
intervention-horizon framing survives in weakened form via P2 — soft nights *are*
identifiable seven weeks out — but the operational recommendation is now the naive rule,
being both more accurate and simpler.

## Diagnosis (exploratory — does not modify the verdict)

The loss is a **level** error, not a shape error. M3 under-predicts on 80.3% of unseen
nights, mean signed error −5.62 pp. The frozen linear trend term (−0.0294/yr) contributes
−8.42 pp at the unseen window's mean trend of 2.86 years: the model extrapolated a decline
that did not continue.

Removing the mean bias would put M3 at 5.61 pp against the naive rule's 6.05 pp. **That
number is not a rescue and is not reported as a result**: it uses the unseen outcomes to
correct the model, which is precisely the post-hoc reconciliation ADR 0040 forbids. It is
recorded as a hypothesis with a named defect — an unbounded linear trend extrapolated
nearly three years — and testing it requires a **new** pre-registration on a later window
with a differently specified level term. Nothing in this ADR licenses refitting M3.

## Bounds on the finding

1. **One season, not a cycle.** The 66 nights are 9 July – 12 September. The unseen window
   is far firmer than the seen window (27.3% vs 52.8% of nights below 60%), so the naive
   rule was tested where year-over-year stability is most favourable to it. The 60-night
   minimum was met; seasonal breadth was not a criterion and should have been.
2. **Serially correlated errors.** Adjacent nights are not independent; the Wilcoxon and
   binomial treat them as such. P1 is a non-rejection in the predicted direction, so this
   does not threaten it, but P2's p = 0.0013 is optimistic.
3. **P2's practical value is modest.** Recall is 1.00 because the rule flags 34 of 66
   nights — over half the calendar. It is a genuine signal, not a useful trigger on its own.
4. **Occupancy is a proxy** against a denominator frozen at 576 rooms, and the
   `rsv_adr_proxy` composition caveat from the yield memo applies downstream.

## Standing prohibitions restated

Arm 2 and Arm 3 stay closed; this was a new test on a different data layer and nothing here
licenses re-running either on a later vintage. The PBL vignette numbers (ADR 0026 §2) enter
no quantity here.
