# Ono grocery access prototype

Exploratory work for a possible transport-access thesis. This directory is
independent of the tourism thesis models and their registered analyses.
It contains methods, source records, and code-generated tables and figures.
It does not contain an AI-written findings chapter.

## Question

For ten named stop areas in Ono, when can a passenger take a direct bus to
either of two grocery stores, shop, and return by 18:00? How do the answers
change under a fixed timetable scenario and different time allowances?

This first example tests the data and calculations. Thesis novelty, resident
access, and the feasibility of operating a revised timetable remain open.

## Run

The calculation and tests require Python 3.10 or later, with no third-party
packages. Run from the repository root:

```bash
python3 experiments/transport-access/fetch_sources.py
python3 -m unittest discover -s experiments/transport-access -p 'test_*.py' -v
python3 experiments/transport-access/access.py
```

Figures require Python 3.11 or later and the optional package listed in
`requirements-plot.txt`:

```bash
python3 -m pip install -r experiments/transport-access/requirements-plot.txt
python3 experiments/transport-access/plot_results.py
```

Source snapshots live in `sources/` and are ignored by Git. Their URLs,
retrieval times, sizes and SHA256 hashes are in `sources/manifest.json`.
The fetch script restores missing snapshots only when their bytes match.
These are mutable publisher URLs. If a publisher changes a file, the script
stops; reproducing this version then requires the saved local snapshot.
Archival storage beyond this working directory remains to be arranged.

## Sources and scope

| Input | Source | Use |
|---|---|---|
| Ono GTFS feed | [Fukui bus-data catalogue](https://www.pref.fukui.lg.jp/doc/dx-suishin/opendata/gtfs_jp.html) | Routes 1 and 2 only, the red and blue town circular buses. Feed validity is 2026-04-01 through 2027-03-31. |
| Published timetable and route map | [Ono city timetable page](https://www.city.ono.fukui.jp/kurashi/douro-kotsu/bus/bus-taxi3.html) | Independent PDF comparison of stop times, service days and store-stop locations. |
| Store hours and closures | [Kajiso store directory](https://kajiso.com/store/) | Libre and Vio grocery stores, 09:30 to 20:00, closed January 1. Vio mall tenant hours are not substituted for grocery hours. |
| Schedule interpretation | [GTFS reference](https://gtfs.org/documentation/schedule/reference/) | Service calendars, exceptions, stop sequence, arrival/departure times, boarding restrictions and times after midnight. |

The feed is published through Fukui's open-data catalogue, which gives CC BY
4.0 as the default license unless otherwise indicated. Attribute the feed to
Ono City and the distribution to Fukui Prefecture. Store-page and timetable
snapshots retain their publishers' terms; they are local verification copies.

The study dates are Tuesday 2026-09-15 and Saturday 2026-09-19. The ten
origins were selected before calculating access to cover the north and south
loops. They are not a representative or population-weighted sample.

## Calculation

`study.json` fixes the inputs and assumptions:

- Readiness times run from 08:00 through 16:00 at 30-minute intervals.
- Each origin is a named stop area. Boarding or returning at either platform
  with that exact name is allowed. Two minutes are assumed between the origin
  area and a platform in each direction.
- Five minutes are assumed between a grocery stop and the store entrance in
  each direction. These are not measured walking paths.
- The baseline allows 45 minutes inside the store and two minutes before
  each bus boarding. Waiting until the store opens is allowed.
- Each leg uses one bus trip. Passengers may remain aboard through an
  intermediate station visit within that trip. Transfers between trips and
  walking-only journeys are excluded.
- Shopping must finish before closing, and the passenger must return to the
  origin area by 18:00.
- The selected itinerary minimizes return time for each readiness time.
  Elapsed time includes all waiting after readiness, both bus rides, shopping,
  and the assumed access walks. It is not just time aboard a bus or time
  away from home. Ties use the earlier outward departure.
- Three hours is an illustrative elapsed-time threshold, not a validated
  accessibility standard.

The loader applies `calendar.txt` and `calendar_dates.txt`, checks feed
validity, honors pickup/drop-off restrictions, and retains repeated stop
visits. It rejects incomplete times, non-monotone trips, frequency services
and on-demand boarding in the selected routes.

## Scenarios

`blue_plus_10` shifts every stop time on every active blue-route trip by ten
minutes. It changes both outward and return options. This is one fixed
illustration, not a search for the best timetable. It preserves trips and
scheduled running time. Vehicle availability, driver hours, connections to
other services and operating cost are not established.

Four separate sensitivities vary shopping duration to 30 or 60 minutes,
store walking time to ten minutes each way, or the boarding allowance to
five minutes. Each changes one assumption from baseline. They do not cover
interactions between assumptions or a walking-speed model.

## Outputs

All numeric tables below are generated by the scripts:

| File under `results/` | Contents |
|---|---|
| `audit.json` | Input hashes, implementation hash, feed dates, active trip counts and limitations. |
| `journeys.csv` | Each scenario, date, origin, specified store and readiness time, including failed cases and reasons. Successful rows retain trip IDs, stop IDs, sequence positions and all journey times. |
| `summary.csv` | Specified-store cases. The denominator is 10 origins times 2 stores times 17 readiness times per date and scenario. |
| `any_store_journeys.csv` | Earliest return when either selected store is allowed, one case per origin and readiness time. |
| `any_store_summary.csv` | Either-store cases. The denominator is 10 origins times 17 readiness times per date and scenario. The column `origin_store_ready_cases` counts these cases with store choice allowed. |
| `comparisons.csv` | Paired changes against baseline for each specified-store case, retaining gains and losses. Elapsed-time differences are blank unless both cases are feasible. |
| `access_matrix.png` | Baseline either-store elapsed times. Grey means no modeled return by 18:00. |
| `study_locations.png`, `stops.csv`, `origin_key.csv` | GTFS stop locations and the origin identifiers used in the figures. The plot has no street network or residential catchments. |

Medians and maxima describe feasible cases only. They can change because
different cases become feasible, so use paired rows when comparing scenarios.
Case counts are timetable queries, not residents, passengers or independent
observations. No statistical significance tests are performed.

## Validation and remaining work

`timetable_checks.json` records 12 stop-time values read visually from page
1 of the city's PDF. Tests compare those values with the GTFS feed. This is
an agent cross-format check, not field verification or human approval.
Synthetic tests cover missed returns, shopping hours, walks in both
directions, boarding allowances, repeated stops and calendar exceptions.

Before presenting this as a thesis proposal:

1. Review the source records and example journeys yourself, including the
   assumption that passengers can stay aboard through an intermediate
   station visit.
2. Verify pedestrian paths and add walking-only alternatives. Several
   origins are near stores. Bus-only journey times cannot establish poor
   access to groceries.
3. Add transfer alternatives and relevant routes outside the two circular
   services before describing the available public-transport options.
4. Decide whether to use residential origins, population weights and more
   grocery destinations. Check data availability before claiming resident
   coverage or equity.
5. Establish operating constraints before optimizing a timetable, or scope
   the thesis to access measurement and explicit scenarios.
6. Compare the proposed contribution with published accessibility studies.
   Working code alone does not establish novelty.

Use the generated tables to write your own interpretation. Keep the
difference between readiness time, boarding time and total elapsed time
explicit, and report unavailable journeys alongside the feasible ones.
