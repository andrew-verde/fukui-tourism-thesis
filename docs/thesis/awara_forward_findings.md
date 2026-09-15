# The Awara forward prediction test: what it gives the thesis

2026-09-14. Companion to `awara_yield_findings.md` and `awara_oos_findings.md`.
Formal record: `docs/adr/0041-awara-forward-prediction-result.md`. Figure:
`output/awara_forward/awara_forward.png`.

---

## 1. You now have a confirmatory result

This is the part worth saying first, because it changes the thesis's status rather than
just adding a number. Every earlier arm was exploratory or closed. This one was
pre-registered properly and the ordering is verifiable from git history, not from anyone's
recollection:

| | commit | what it fixed |
|---|---|---|
| specification frozen | `e1fe0d4` | model, coefficients, thresholds, sidedness, sample minimum |
| data pinned | `21623ef` | upstream commit + checksums for all three files |
| result | `b4436ef` | single execution, guard first |

The guard ran before the unseen read and found **zero** revision across all 1012 seen
nights. The test was executed once. No refit, no threshold adjustment, no second look.

That means the headline claim is defensible in a way nothing else in this thesis currently
is. A committee can check the ordering themselves.

## 2. The finding

**At a 30-day horizon, reservation-curve state does not improve on "same night last year."**

MAE 7.58 pp for the frozen booking-state model against 6.20 pp for the one-line seasonal
rule, on 66 unseen nights. The naive rule is not merely competitive — it wins, on 34 of
66 nights, and the Wilcoxon test in the pre-registered direction returns p = 0.91.

Two things sit alongside it and neither rescues it:

- Booking state **does** beat a calendar-only model, and by a lot: 7.58 vs 12.30 pp,
  p = 6.4e-5. So the reservation data carries real information.
- Soft nights **are** identifiable seven weeks out: flag precision 52.9% against a 27.3%
  base rate, p = 0.0013, catching all 18 soft nights.

Put together, the story is coherent and it is the interesting version: the booking curve's
information is largely information about seasonality that a year-ago lag already encodes.
Once you have the lag, the curve adds little. Had I only compared against the calendar
model — the natural, and wrong, comparison — I would have reported a 40% error reduction
and called the chapter a success. That is the same error that sank the earlier arms, caught
this time by the benchmark rather than after the fact.

## 3. The mechanism, and why it is not a rescue

The loss is a **level** error, not a shape error. The frozen model under-predicts on 80.3%
of unseen nights, mean signed error −5.62 pp. The culprit is identifiable: the frozen
linear trend term (−0.0294/yr) contributes −8.42 pp at the unseen window's mean trend of
2.86 years. The model extrapolated a decline that stopped.

Remove the mean bias and the model's MAE would be 5.61 pp against the naive rule's 6.05 pp
— it would win. **This number is not a result and must not appear as one.** It uses the
unseen outcomes to correct the model, which is exactly the post-hoc reconciliation ADR 0040
forbids and exactly what cost the earlier arms their status. It is a *hypothesis with a
named defect*, and testing it needs a new pre-registration on a later window.

Write it in the thesis as a diagnosis, clearly fenced. Its value is that it converts "the
model lost" into "an unbounded linear trend extrapolated three years is the wrong level
term, and here is the pre-registration that would test the fix" — which is a contribution,
not an excuse.

## 4. What bounds it

1. **One season.** The 66 nights are 9 July – 12 September. The unseen window is far firmer
   than the seen window — 27.3% of nights below 60% against 52.8% — so the naive rule was
   tested precisely where year-over-year stability favours it most. The 60-night minimum was
   met; seasonal breadth was not a criterion and, in hindsight, should have been. State this
   as a limitation, not a hedge: the falsification is established for a summer peak.
2. **Serially correlated errors.** Adjacent nights are not independent and the tests treat
   them as such. P1 is a non-rejection in the predicted direction, so this cannot have
   manufactured it; P2's p = 0.0013 is optimistic.
3. **P2's practical value is modest.** Recall is 1.00 because the rule flags 34 of 66 nights.
   A trigger that fires on half the calendar is a signal, not an operational tool. Do not
   oversell this panel.
4. **Occupancy is a proxy** against a denominator frozen at 576 rooms.

## 5. How to write the chapter

The contribution is methodological as much as empirical, and it is publishable in that form:

> A pre-registered forward test finds that reservation-curve state at 30 days does not
> improve occupancy prediction over a parameterless seasonal benchmark, despite
> substantially outperforming a calendar model — with a diagnosed level-term defect and a
> registered follow-up.

That framing survives the result being negative, because the negative result is the finding.
For a DMO deciding whether to buy booking-curve access, "it beats a calendar but not last
year's occupancy" is directly actionable and nobody has published it for a Japanese onsen
resort.

Two things to do next, in this order:

1. **Back up `arm2_results.json`.** It still exists untracked on the fedora host only. That
   remains the single most fragile asset in the project.
2. **Decide whether to register the follow-up** — trend-term respecification, tested on a
   window with seasonal breadth. If yes, write it now, before looking at anything, and let
   the window accumulate. That is the cheap way to get a second confirmatory result.

Do not touch Arm 2 or Arm 3; nothing here licenses reopening either.
