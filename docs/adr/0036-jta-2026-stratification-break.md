# ADR 0036: The JTA 2026 stratification break — S2's 2026 rows sit on a different sampling frame, and the disclosure is fixed before any S2 output exists

Date: 2026-07-30
Status: accepted 2026-07-30 (records a data fact affecting ADR 0020 §S2's interpretation; amends no prediction, no threshold, and no firewall rule)

## Context

Arm 2's secondary prediction S2 describes the decay shape of Fukui
prefecture-level overnight stays in the JTA 宿泊旅行統計調査 panel, using
"JTA 2025-confirmed/2026 rows" (ADR 0020 §S2). The frozen consumer
`arm2_predictions.build_s2_descriptive_report` enforces that literally: it
requires complete confirmed years 2018–2024, complete confirmed 2025, and
**at least one row at year ≥ 2026** (`scripts/arm2_predictions.py:420-421`;
oracle `tests/test_arm2_oracles.py:229`).

Establishing where those 2026 rows come from surfaced a data fact that
was not known when ADR 0020 was written:

**From the 2026-01 survey month, the 宿泊旅行統計調査 changed its
stratification basis from 従業者数 (employee count) to 客室数 (room
count).** The change is stated in the 観光庁 monthly releases as a
precision improvement, with an explicit caution that year-on-year
comparisons spanning the change may reflect it. Every 2026 month
therefore rests on a different sampling frame from the 2018–2025 series
S2 compares it against.

Two related availability facts, established from release metadata only
(no values ingested): the 2025 **annual confirmed** (確定値) has
published, so S2's confirmed-2025 requirement is satisfiable; and 2026
data exists so far only as **monthly** 速報 releases (through 2026-05).
Those monthly workbooks use the same sheet naming as the annual ones
(`第2表(1月)`, `参考第1表(1月)`, …), so
`build_accommodation_panel.parse_workbook` reads them unchanged — it
iterates months 1..12, warns on missing sheets, and emits rows only for
the months present. It does require the year from its caller; the year is
not inferred from workbook contents.

## Decision

**1. The break is recorded now, before any S2 series exists.** This is the
ADR 0034 discipline applied to a second case: a framing decision made
after seeing an output is a framing decision shaped by the output. S2 has
never been run.

**2. S2's status is unchanged: descriptive only, gates nothing, never
headline.** ADR 0020 already fixed that (`S2 ... the event-study framing
stays descriptive`), and the frozen report emits
`"status": "descriptive only", "secondary_only": true,
"gates_nothing": true`. The break does not demote S2, because S2 was
never carrying inferential weight. Nothing about P1, P2, S1 or S3 is
touched — they do not use the JTA panel.

**3. Mandatory disclosure wording.** Wherever the S2 series is reported —
thesis §7.2, the journal manuscript, any interpretation memo — the
following must appear with it, and may not be softened:

> JTA revised the survey's stratification basis from employee count to
> room count beginning with the 2026-01 survey month. The 2026 observations
> therefore rest on a different sampling frame from the 2018–2025 series
> and are not a like-for-like continuation of it. S2 is reported as a
> descriptive shape, and no part of the Arm 2 verdict rests on it.

**4. No 2026-vs-earlier difference may be quantified as an estimate.**
The 2026 points may be plotted and described in shape terms alongside the
earlier series. A numeric year-on-year change, growth rate, or gap that
straddles 2025→2026 must not be computed, reported, or read aloud at the
defense as if it measured a real-world change: any such number confounds
the frame revision with the phenomenon. If the shape reads as reversion,
it is stated as "consistent with reversion, on a revised frame".

**5. The frame basis is carried in the data where it is free to do so.**
The quarantined JTA panel should label each row's frame basis (e.g. a
`frame_basis` column with `employee_count` / `room_count`) **if and only
if** the extra column perturbs neither the frozen consumer nor its
oracle — `build_s2_descriptive_report` checks a required-column subset
and projects `["ym", "total_stays", "vintage"]`, so an extra column is
expected to be inert. If it turns out not to be inert, the label is
dropped and the disclosure remains prose-only; the frozen contract is not
edited to accommodate a label.

**6. One row per prefecture-month: confirmed supersedes preliminary.** The
quarantined panel carries exactly one observation per prefecture-month,
at the best vintage available, with its `vintage` label retained. When the
2025 confirmed values are added, the 2025 **preliminary** rows already in
the committed seen panel are dropped rather than kept alongside them.
Reason: the frozen consumer emits `["ym", "total_stays", "vintage"]`
sorted by `ym` and does not deduplicate, so keeping both vintages would
put two rows on the same month into the S2 series with no rule for
reading them. The committed seen panel is not modified — the supersession
happens only in the quarantine copy. This was surfaced by a smoke run:
the first implementation appended confirmed rows on top of preliminary
ones and produced 1,128 rows for 2025 where 564 are correct.

**7. This does not amend ADR 0020.** No prediction, threshold, seen/unseen
boundary, or firewall rule changes. Under ADR 0019's deviation discipline
an amendment to a frozen rule would demote the affected analysis; nothing
here is an amendment, so nothing is demoted.

## Consequences

- The S2 write-up's honesty problem is solved before the series exists,
  which is the only time it can be solved without the result influencing
  the wording.
- The break is present under every route to a 2026 row — monthly 速報 now
  or the 2026 annual release later — because it is a property of the
  survey, not of the file format. Choosing a source does not avoid it.
- An examiner who knows the survey's history finds the break already
  disclosed rather than discovering it in the series.
- ADR 0032's "Arm 2 has no external dependency" holds for the primaries
  and is **too strong for S2**, which depends on a JTA release schedule.
  Recorded here rather than by amending ADR 0032, which was correct about
  the mobile panel and FTAS.

## Rejected alternatives

- **Say nothing; S2 is descriptive anyway.** The series would show a
  2025→2026 discontinuity that a reader would attribute to Fukui rather
  than to the sampling frame. Silence here is the cheapest possible way to
  lose the credibility the pre-specification discipline bought.
- **Drop 2026 from S2 and report 2018–2025 only.** Contradicts the frozen
  consumer's ≥ 2026 requirement and would need a deviation ADR; it also
  discards the only post-window observation S2 exists to describe.
- **Adjust or splice the 2026 values onto the old frame.** No public
  bridge exists between the two frames at prefecture-month grain, so any
  adjustment would be invented, and inventing an adjustment inside a
  pre-registered arm is exactly what the arm's design forbids.
- **Wait for JTA to publish a back-cast on the new frame.** None is
  announced; the thesis cannot be scheduled against a hypothetical release.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote the
affected analysis to exploratory, per ADR 0019.
