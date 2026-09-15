# Intervention-site opportunity analysis

*Candidate Hokuriku sites, physical changes, and required effect sizes from the non-survey panel.*

Generated 2026-07-09. Evidence: `panel_site_daily.parquet`,
`panel_area_daily.parquet`, `opportunity_signals.json`, and
`site_leverage.csv`. Related documents: `reframe_physical_interventions.md`
and `sem_nonsurvey_spec.md`.

The public-data panel produces every number below. Each intervention is a
hypothesis. The SEM and simulation bound its required effect size, and a future
field trial tests it. This document does not report measured intervention
effects.

---

## 1. Opportunity ranking

The score gives equal weight to three observed measures: peak concentration
(95th-percentile day divided by median), weekend-to-weekday footfall ratio,
and the linked lodging market's weekend-to-weekday occupancy gap. Each measure
is min-max normalized across the three camera sites.

| Rank | Site | Linked lodging | Peak/median | Weekend/weekday | Out-of-pref | Occ gap | **Opportunity score** |
|---|---|---|---|---|---|---|---|
| 1 | **Tojinbo** | Awara Onsen | 2.24 | 1.72 | N/A | 0.18 | **0.88** |
| 2 | **Rainbow Line** | Mikatagoko | 2.54 | 1.56 | 0.66 | 0.09 | **0.64** |
| 3 | Fukui Station East | Fukui Station | 1.67 | 1.42 | N/A | 0.02 | **0.00** |

![Site opportunity ranking and its drivers](../output/opportunity/site_leverage.png)

The ranking does not say Fukui Station has no opportunity. It has the broadest
downstream reach as the rail gateway. Its flows are the least physically
concentrated, so a fixed physical change acts on a flatter distribution.

## 2. Site 1: Tojinbo (東尋坊), peak-day dispersal

**What the data shows.** Tojinbo has the most concentrated footfall. The
95th-percentile day has 2.24 times the median number of people, weekend
footfall is 1.72 times weekday footfall, and the busiest observed day had
26,574 people. Awara Onsen has an 18 percentage-point weekend-to-weekday
occupancy gap and reaches saturation on only 1.2% of days. The relevant
constraint is the timing of demand, not available beds.

**Physical intervention hypotheses.**
- **Timed-entry / peak-hour signage** at the cliff approach to smooth intra-day load.
- **Midweek last-mile shuttle** from Awara Onsen / Awara-Yunomachi station, priced or scheduled to make a midweek Tojinbo trip frictionless.
- **Dynamic peak-day messaging** on the GBP profile and approach signage (for
  example, "today is busy. Thursday is quiet.").

**Effect it would need.** A dispersal intervention would need to shift enough
weekend footfall to narrow the 18 percentage-point occupancy gap. In practical
terms, it would need to raise midweek Awara occupancy from about 50% toward the
weekend level of about 68%. The SEM and simulation express this as a target
elasticity on the friction-to-demand path. The webapp lets a partner set an
assumed shift and inspect the resulting demand scenario.

**Why it ranks first.** It has the highest opportunity score. The cliff
geography channels flow through a defined point, and an existing AI camera can
measure the outcome in a future trial.

## 3. Site 2: Rainbow Line (レインボーライン), car access and parking

**What the data shows.** Rainbow Line visitors mainly arrive by car. Between
66% of lot 1 and 70% of lot 2 license plates are from outside the prefecture.
About 10% are rental cars, so most visitors drive privately owned cars. Aichi
(Nagoya and Chubu) is the dominant external origin, rather than the
Shinkansen-served Kanto corridor. Median throughput at lot 1 is about 145
vehicles per day, with a peak-to-median ratio of 2.54, the highest of the
three sites.

**Physical intervention hypotheses.**
- **Park-and-ride and an EV shuttle** for peak days to manage parking demand.
- **Dynamic parking guidance** to balance lots 1 and 2. The two gates already
  measure entries.
- **Chubu-targeted routing and signage** because the marginal visitor arrives
  by car from Aichi rather than by rail.

**Effect it would need.** The intervention must reduce peak-day parking
pressure without reducing total visits. The target is redistribution between
the two lots and across days, not an increase in total volume. Since both gates
measure entries, a trial can directly measure lot balancing.

**Interpretation.** A survey or rail-centered analysis would miss that parking
and road access are the relevant constraints because about two-thirds of demand
does not use a train.

## 4. Site 3: Fukui Station East (福井駅東口), wayfinding and dispersal

**What the data shows.** The rail gateway has the least concentrated footfall
(peak-to-median 1.67 and weekend-to-weekday 1.42). Its linked lodging market
has a weekend-to-weekday gap of only 2 percentage points. This is consistent
with relatively smooth mixed business and tourism demand.

**Physical intervention hypotheses.**
- **Wayfinding signage at the east exit** to direct arrivals toward
  under-visited quarters.
- **Digital-intent capture.** The station's GBP directions signal can test
  whether map and routing information changes where visitors go next.

**Effect it would need.** Since flows are already smooth, the target is
redistribution across neighborhoods rather than across time. The opportunity
score places this site below the other two, despite its broad reach.

## 5. Demand signal across lodging markets

Google Business Profile "directions" requests co-move with realized stays in
Awara. The correlation is r = 0.59 in the same week, 0.49 one week later, and
0.34 two weeks later. This supports an intent-to-realized-demand path in the
SEM and provides a measurable path for a digital component of a physical
intervention, such as updated GBP hours, routing, or peak messaging.

## 6. Claims outside this analysis

- This analysis does not estimate a causal intervention effect. Opportunity
  scores rank candidate sites, not proven impact.
- It does not use the reservation panels for a Shinkansen DiD. Those series
  begin in October 2023 and have no seasonally comparable pre-extension
  window. See `opportunity_signals.json` (`S5`). The existing multi-year
  series produces the natural-experiment estimate.
- Effect-size statements describe the shift an intervention would need to
  produce. The SEM and simulation bound the shift, and the pre-registered
  field trial tests it. They do not describe observed outcomes.
