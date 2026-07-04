# Arm 3 Kanazawa replication: data-availability audit

Checked: **2026-07-03** (Asia/Tokyo).

This is a coverage audit, not an outcome analysis. **VERIFIED** means that the
linked page/file or local artifact was fetched and inspected in this audit.
**REPORTED** means that a publisher page or existing repository note makes the
claim, but this audit did not independently inspect the underlying data.

## Preregistration firewall

ADR 0020 was observed. No JTA 2025 confirmed-value data, JTA 2026 data values,
post-2025-12 mobile-panel values, or FTAS data were used. The current JTA
`推移表` workbook necessarily contains later vintages; inspection was restricted
to coverage metadata (sheet names, titles, dimensions, and date/geography axes).
Likewise, the GitHub repository tree and the upstream publication index were
used only to establish filenames/coverage; no post-2025-12 mobile-data file was
opened.

## 1. JTA 宿泊旅行統計調査: prefecture-month coverage through 2011

### Local pinned `推移表`

**VERIFIED (local artifact, 2026-07-03):**
`output/national_stats/raw/jta_accommodation_timeseries.xlsx` exists and is the
file configured as `jta_accommodation_timeseries.xlsx` in
`config/national_data_sources.yaml`. The configured source is the JTA
[`推移表` Excel](https://www.mlit.go.jp/kankocho/content/002002831.xlsx)
(checked 2026-07-03). The JTA survey page labels the link `推移表` (checked
2026-07-03), although its current URL/vintage may change:
[宿泊旅行統計調査](https://www.mlit.go.jp/kankocho/tokei_hakusyo/shukuhakutokei.html).

Metadata-only workbook inspection found:

- `旧1-2`: 都道府県別 延べ宿泊者数（月別）, range `A1:FY53`;
- `旧2-2`: 都道府県別 日本人延べ宿泊者数（月別), range `A1:FZ53`;
- `旧3-2`: 都道府県別 外国人延べ宿泊者数（月別), range `A1:FY53`;
- each has a national row plus prefecture codes `01`–`47`;
- the month axis of the all-establishment series spans **2011-01 through
  2025-12** (180 months). Thus the requested 2011–2019 interval is present for
  total, Japanese, and foreign overnight stays at prefecture-month level.

The workbook also has separate `従業者数10人以上` monthly series beginning in
2007. Those are not the same estimand as the all-establishment series and
should not be spliced into it.

### Annual confirmed-value releases, 2011–2017

**VERIFIED (publisher page and link targets, 2026-07-03):** the JTA
[confirmed-values list](https://www.mlit.go.jp/kankocho/tokei_hakusyo/shukuhakutokei.html)
contains the following exact labels and downloads. The binary links resolved,
but this audit did not need to read their outcome values because the local
`推移表` supplied the coverage check.

| Year | Exact JTA label | Download |
|---|---|---|
| 2011 | `2011年（平成23年）1月～12月分（年の確定値）集計結果［Excel:4.7MB］` | [000216576.xls](https://www.mlit.go.jp/kankocho/content/000216576.xls) |
| 2012 | `2012年（平成24年）1月～12月分（年の確定値）集計結果［Excel:4.7MB］` | [001002144.xls](https://www.mlit.go.jp/kankocho/content/001002144.xls) |
| 2013 | `2013年（平成25年）1月～12月分（年の確定値）集計結果［Excel:4.8MB］` | [001046404.xls](https://www.mlit.go.jp/kankocho/content/001046404.xls) |
| 2014 | `2014年（平成26年）1月～12月分（年の確定値）集計結果［Excel:4.8MB］` | [001094684.xls](https://www.mlit.go.jp/kankocho/content/001094684.xls) |
| 2015 | `2015年（平成27年）1月～12月分（年の確定値）集計結果［Excel:2.5MB］` | [001312940.xlsx](https://www.mlit.go.jp/kankocho/tokei_hakusyo/content/001312940.xlsx) |
| 2016 | `2016年（平成28年）1月～12月分（年の確定値）集計結果［Excel:2.7MB］` | [001190399.xlsx](https://www.mlit.go.jp/kankocho/content/001190399.xlsx) |
| 2017 | `2017年（平成29年）1月～12月分（年の確定値）集計結果［Excel:2.7MB］` | [001247521.xlsx](https://www.mlit.go.jp/kankocho/content/001247521.xlsx) |

The same page warns that 2013 tables were corrected for the national total,
Chiba, Ishikawa, Kanto, and Hokuriku-Shinetsu, and that a 2012 reference table
was corrected. Use the current corrected annual files or current `推移表`, not
an archived uncorrected vintage.

### e-Stat API/DB coverage

`ESTAT_APP_ID` was **not set** on 2026-07-03.

- **VERIFIED:** e-Stat identifies government-statistics code `00601020` as
  宿泊旅行統計調査, and its public
  [annual confirmed-value file index](https://www.e-stat.go.jp/stat-search/files?cycle=7&layout=datalist&page=1&tclass1val=0&toukei=00601020&tstat=000001079598)
  lists 2014, 2015, and 2016 (as well as 2007 onward).
- **VERIFIED:** e-Stat's
  [API specification](https://www.e-stat.go.jp/api/api-info/e-stat-manual)
  documents `getStatsList`, `getMetaInfo`, and `getStatsData`, and the e-Stat
  page states that an application ID is required for API requests.
- **REPORTED, not independently API-confirmed in this audit:** the repository
  config says that `getStatsList` previously returned 32 DB tables whose time
  axes end in 2016 and describes them as frozen at 2014–2016. Without an app ID,
  this audit could not re-run `getStatsList`/`getMetaInfo` to prove that the DB
  tables themselves contain all monthly prefecture cells. Therefore the narrow
  claim “the API DB tables themselves cover 2014–2016 monthly by prefecture”
  remains **REPORTED**, not VERIFIED. This does not block replication because
  the official annual Excel releases and pinned long-run workbook cover the
  interval directly.

### Methodology and comparability

**VERIFIED (JTA methodology/publication page, 2026-07-03):** JTA states that
from the **2010 Q2 (April–June) survey**, establishments with 9 or fewer
employees were added and warns against comparisons across that break:
[宿泊旅行統計調査](https://www.mlit.go.jp/kankocho/tokei_hakusyo/shukuhakutokei.html).
A JTA methodological note in its published survey material describes the
post-expansion design as a census for establishments with 10+ employees,
sampling 1/3 of establishments with 5–9 employees, and 1/9 with 0–4 employees:
[JTA survey-use cautions](https://www.mlit.go.jp/kankocho/content/001984052.pdf)
(checked 2026-07-03; methodology text only, no prohibited values inspected).
The 2015 annual report also documents the survey period and an `抽出方法`
section: [2015 annual report](https://www.mlit.go.jp/kankocho/content/001183124.pdf)
(checked 2026-07-03).

Consequences:

- 2007–2010 Q1 all-establishment totals are not comparable to the expanded
  universe; the 10+-employee series is a different, narrower estimand.
- **2011-01 onward is wholly after the 2010 Q2 expansion.** No further
  questionnaire/sample-scope break was found on the JTA page for 2011–2019.
- Annual population-frame refreshes and survey nonresponse still affect
  estimates, so “consistent basis” means a common published design/estimand,
  not an invariant panel of establishments.
- The Great East Japan Earthquake is a substantive shock beginning 2011-03,
  not a measurement-method break.

**VERDICT — VERIFIED: the earliest clean start for a consistent, expanded-universe, 47-prefecture monthly overnight-stays panel is 2011-01. The entire 2011-01..2015-02 pre-period (49 months) is covered for total, Japanese, and foreign stays. Do not splice the pre-2011 10+-employee series into it.**

## 2. Official municipal and tourist-point monthly series for Ishikawa, 2013–2019

### Ishikawa Prefecture: `統計からみた石川県の観光`

**VERIFIED (2026-07-03):** Ishikawa's
[official archive page](https://www.pref.ishikawa.lg.jp/kankou/siryo.html)
links annual PDF editions for every year 2013–2019 (and adjacent years). The
[statistics portal index](https://toukei.pref.ishikawa.lg.jp/search/min.asp?sc_id=56)
also lists editions from 2010 onward.

Representative files inspected:

- [2013 edition](https://toukei.pref.ishikawa.lg.jp/dl/2848/kankoutoukei25.pdf);
- [2015 edition](https://www.pref.ishikawa.lg.jp/kankou/documents/ishikawa_kankou_toukei2015.pdf);
- [2017 edition](https://www.pref.ishikawa.lg.jp/kankou/documents/ishikawa_kankou_toukei2017.pdf);
- [2018 edition](https://www.pref.ishikawa.lg.jp/kankou/documents/ishikawa_kankou_toukei2018.pdf);
- [2019 edition](https://www.pref.ishikawa.lg.jp/kankou/documents/ishikawa_kankou_toukei2019.pdf).

What they provide:

| Series | Granularity | Unit | Format | Verified coverage/use |
|---|---|---|---|---|
| Prefecture/region tourism entries | quarter and, in detailed tables, month by broad tourism region | person-visits (`入り込み客数`, generally thousands) | PDF | Annual editions 2013–2019 |
| Principal tourism facilities | facility × year | facility users/person-visits | PDF | Annual comparison tables |
| Accommodation supply | municipality/region × facility type, annual snapshot | facilities/rooms/capacity | PDF | Annual, not a monthly outcome |
| Selected transport/park indicators | month within each edition, often current and prior year | vehicles or users | PDF | Descriptive anchors, not a common municipal outcome |

The 2015 edition was visually inspected page by page where text extraction was
poor. It contains monthly broad-region arrivals and annual principal-facility
counts, but not a balanced **municipality × month** visitor/overnight panel for
all Ishikawa municipalities. The archive supplies PDFs, not analysis-ready
Excel workbooks.

### Kanazawa City tourism survey

**VERIFIED (2026-07-03):** the current
[金沢市観光調査結果報告書 page](https://www4.city.kanazawa.lg.jp/soshikikarasagasu/kankoseisakuka/gyomuannai/1/2/30429.html)
publishes PDFs for 2018 onward. The
[2018 report](https://www4.city.kanazawa.lg.jp/material/files/group/32/houkoku_2018.pdf)
contains:

- monthly users of 19 principal attractions, in **persons/visits**, with a
  2014–2018 comparison;
- monthly Kanazawa lodging guests, in **persons** (not person-nights), with a
  2014–2018 comparison;
- monthly foreign lodging guests; and
- annual facility/room/capacity and occupancy material.

The
[2019 report](https://www4.city.kanazawa.lg.jp/material/files/group/32/houkoku_2019.pdf)
contains monthly 19-attraction totals for 2015–2019 and facility-level monthly
tables for the report year. Thus Kanazawa has a credible monthly city-level
lodging outcome from **2014**, not a verified 2013 start, and a monthly
attraction aggregate from at least 2014. The older 2013 report's existence is
**REPORTED** by the
[Ishikawa Prefectural Library catalogue](https://www.library.pref.ishikawa.lg.jp/shosho/detail/bib/1100000937232)
(checked 2026-07-03), but its tables were not available for inspection here.

### `主要観光地点`, including 兼六園

**VERIFIED:** Kanazawa's 2018/2019 reports identify 兼六園 among the 19
principal facilities and provide monthly person-visit counts. Therefore
Kenrokuen can serve as a high-salience monthly anchor over the opening window.
The city explains that its
[入込客数調査](https://www4.city.kanazawa.lg.jp/bunka_sports_kanko/kanko/2/17190.html)
collects tourism-facility counts and publishes results through the city and
prefectural reports (checked 2026-07-03).

This is **point utilization**, not unique visitors, not overnight stays, and
not a municipality-wide outcome. Changes in the included facility set must be
checked before using the 19-facility aggregate.

**VERDICT — A Kanazawa-only monthly outcome is available from 2014, and monthly point anchors such as 兼六園 are available, but no official balanced monthly panel across Ishikawa municipalities for 2013–2019 was verified. A municipal-level SCM with comparable municipal donors is therefore not supported by these sources. Use the 47-prefecture JTA panel for SCM and Kanazawa lodging/attraction series only as descriptive anchor evidence.**

## 3. `code4fukui/japan-kanko-stat` before 2021

**VERIFIED (coverage metadata only, 2026-07-03):**

- Pinned commit/tree:
  [dfb906975b63adcaef20a3e7a35f2a10ab22ada5](https://github.com/code4fukui/japan-kanko-stat/tree/dfb906975b63adcaef20a3e7a35f2a10ab22ada5).
- Pinned
  [README](https://raw.githubusercontent.com/code4fukui/japan-kanko-stat/dfb906975b63adcaef20a3e7a35f2a10ab22ada5/README.md)
  and
  [Japanese README](https://raw.githubusercontent.com/code4fukui/japan-kanko-stat/dfb906975b63adcaef20a3e7a35f2a10ab22ada5/README.ja.md).
- Machine-readable pinned
  [Git tree](https://api.github.com/repos/code4fukui/japan-kanko-stat/git/trees/dfb906975b63adcaef20a3e7a35f2a10ab22ada5?recursive=1).

The tree contains annual `city2021.csv` through `city2025.csv` and no
`city2015.csv`–`city2020.csv` (nor any other pre-2021 municipal file). No
post-2025-12 data file was opened. The READMEs call the source “Digital Tourism
Statistics Open Data,” describe prefecture/city monthly visitor estimates, and
link the Japan Travel and Tourism Association (JTTA), although they
misattribute the publisher as JTA.

**VERIFIED:** JTTA's
[Digital Tourism Statistics Open Data index](https://www.nihon-kankou.or.jp/home/jigyou/research/d-toukei/)
starts its historical downloads at 2021. Its
[method overview](https://www.nihon-kankou.or.jp/home/userfiles/files/d-toukei/gaiyou240924.pdf)
states that:

- coverage begins **2021-01**;
- estimates use smartphone location data obtained with prior consent by
  Blogwatcher;
- counts are expanded using the share of app users in resident-register
  population;
- the outcome is monthly domestic-resident tourism visitors to prefectures and
  municipalities, subject to distance/workplace exclusions.

**VERDICT — VERIFIED: neither the pinned commit nor the upstream publisher offers municipal data before 2021. There are no `city2015.csv`–`city2020.csv` files, and the underlying smartphone-derived series explicitly begins at 2021-01. It cannot support the 2015 replication.**

## 4. Donor-pool contamination, 2011–2019

Months below are conservative SCM handling windows. “Exclude” means structural
treatment/direct severe shock; “flag” means sensitivity exclusion or
month-specific masking is defensible.

| Event | Verified timing and geography | Plausible contaminated prefectures/months | Handling |
|---|---|---|---|
| Great East Japan Earthquake | JMA gives **2011-03-11 14:46**, M9.0, maximum intensity 7 in Miyagi: [JMA portal](https://www.jma.go.jp/jma/menu/jishin-portal.html) (checked 2026-07-03). | Direct/coastal: Aomori `02`, Iwate `03`, Miyagi `04`, Fukushima `07`, Ibaraki `08`, Chiba `12`; broad demand/transport shock nationwide from 2011-03. Akita `05` and Yamagata `06` are Tohoku spillovers. | Exclude `02,03,04,07` for the main SCM; flag `05,06,08,12`; treat 2011-03 onward as a national pre-period break and run a pre-period sensitivity starting 2012-01. |
| Hokuriku Shinkansen Nagano–Kanazawa | JRTT verifies **2015-03-14** and lists stations: Nagano, Iiyama (Nagano); Joetsumyoko, Itoigawa (Niigata); Kurobe-Unazukionsen, Toyama, Shin-Takaoka (Toyama); Kanazawa (Ishikawa): [JRTT](https://www.jrtt.go.jp/construction/achievement/hokuriku2.html) (checked 2026-07-03). | Nagano `20`, Niigata `15`, Toyama `16`, treated Ishikawa `17`, from 2015-03 through the post-period. | Exclude `15,16,20` as directly co-treated/spillover donors; `17` is treated and never a donor. |
| Hokkaido Shinkansen | JR Hokkaido verifies Shin-Aomori–Shin-Hakodate-Hokuto opened **2016-03-26**: [JR Hokkaido](https://www.jrhokkaido.co.jp/corporate/shinkansen/) (checked 2026-07-03). | Hokkaido `01`, Aomori `02`, from 2016-03 onward. | Exclude/flag `01,02`; `02` is already excluded for 2011. |
| Kumamoto earthquakes | JMA verifies shocks on **2016-04-14** and **2016-04-16**, both centered in Kumamoto: [JMA](https://www.data.jma.go.jp/eqev/data/2016_04_14_kumamoto/index.html) (checked 2026-07-03). | Kumamoto `43` direct; Oita `44` strong tourism/transport spillover; wider Kyushu demand effects. At minimum 2016-04 through 2016-06, with annual sensitivity through 2016-12. | Exclude `43`; flag `44` and mask/sensitivity-test 2016-04..12. |
| Osaka north earthquake | JMA verifies **2018-06-18 07:58**, maximum intensity 6-lower in northern Osaka: [JMA](https://www.data.jma.go.jp/eqev/data/higai/20180618_oosaka_jishin_menu.html) (checked 2026-07-03). | Osaka `27` direct in 2018-06; transport/tourism spillovers Kyoto `26`, Hyogo `28`, Nara `29` in 2018-06. | Flag `27` (and `26,28,29` in a regional sensitivity); mask 2018-06 if retained. |
| West Japan floods (`平成30年7月豪雨`) | Cabinet Office documents the event; the Fire and Disaster Management Agency identifies especially severe flooding/landslides in Okayama, Hiroshima, and Ehime: [Cabinet Office](https://www.bousai.go.jp/updates/h30typhoon7/h30typhoon7/index.html), [FDMA white paper](https://www.fdma.go.jp/publication/hakusho/r1/chapter1/section5/para3/56030.html) (both checked 2026-07-03). | Core: Okayama `33`, Hiroshima `34`, Ehime `38`, from 2018-07, with disruption into subsequent months. Wider affected prefectures include Gifu `21`, Kyoto `26`, Hyogo `28`, Tottori `31`, Shimane `32`, Yamaguchi `35`, Kochi `39`, and parts of northern Kyushu. | Exclude `33,34,38` or mask 2018-07..09; flag the wider set for sensitivity. |
| Hokkaido Eastern Iburi earthquake | JMA verifies **2018-09-06 03:07**, M6.7, maximum intensity 7 in Atsuma: [JMA Sapporo](https://www.data.jma.go.jp/sapporo/jishin/iburi_tobu.html) (checked 2026-07-03). | Hokkaido `01`, from 2018-09; tourism/power disruption plausibly extends through late 2018. | Exclude/flag `01`; mask or sensitivity-test 2018-09..12. |

### Recommended donor rule

For a simple preregistered main specification, exclude the union of directly
treated or severely shocked units:

`01, 02, 03, 04, 07, 15, 16, 17, 20, 33, 34, 38, 43`

where `17` is the treated unit, not a candidate donor. Flag the following
additional codes for leave-group-out sensitivity analyses:

`05, 06, 08, 12, 21, 26, 27, 28, 29, 31, 32, 35, 39, 44`

This rule is deliberately stricter than merely adding event dummies: SCM donor
weights can concentrate on one contaminated unit, and several shocks occur in
the post-period where outcome masking alone weakens the comparison. Report
weights under both the main exclusion rule and the expanded flagged exclusion
rule. Because the 2011 earthquake occurs inside the proposed pre-period,
also report a design sensitivity using 2012-01..2015-02 as the fitting window.

**VERDICT — The main donor pool must exclude codes `01,02,03,04,07,15,16,20,33,34,38,43` (plus treated `17`), with `05,06,08,12,21,26,27,28,29,31,32,35,39,44` flagged for event-window or leave-group-out sensitivity. The 2011-03 national shock requires an explicit shorter-pre-period robustness check.**
