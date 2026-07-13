# ADR 0028 — Government prefecture-level context layer (JTA overnight + FF-DATA)

- **Date:** 2026-07-13
- **Status:** accepted
- **Extends:** ADR 0027 (non-survey scope boundary)

## Context

ADR 0027 fixed the scope of the non-survey evidence engine: it identifies and
effect-bounds physical-intervention opportunities, it does not estimate causal
intervention effects, and the Shinkansen natural experiment is estimated only
from the multi-year arrivals/accommodation series — never from the reservation
panels, which have no seasonally comparable pre-extension window
(`S5_shinkansen_NOT_identifiable_here`).

The advisor asked to bring Japanese-government arrivals-by-prefecture and
origin-of-arrivals-over-time series into the reframe — the data RESAS served
before its 2025-03-24 API shutdown, now reachable through e-Stat and the MLIT
Data Platform. Pack 06 framed this as building new authenticated e-Stat
fetchers from scratch.

During scoping (2026-07-13) two facts changed that framing:

1. The repo already contains a complete e-Stat REST fetcher
   (`scripts/fetch_estat_data.py`) and a complete FF-DATA fetcher
   (`scripts/fetch_ff_data.py`), plus a working JTA prefecture×month parser
   (`scripts/build_accommodation_panel.py` → `accommodation_panel.csv`,
   2018–2025, 47 prefectures).
2. The e-Stat API DB for the JTA overnight survey (statsCode `00601020`) is
   frozen at 2016 (32 tables, all `SURVEY_DATE = 201601-201612`; overnight
   guest-nights table `0003313520`). Recent monthly overnight data is published
   only as MLIT Excel, which the repo already ingests.

## Decision

Government prefecture-level series enter the non-survey panel as a **context /
validation layer**, assembled from data the repo already fetches, exposed
through a thin panel-facing seam rather than a second copy of the fetch stack:

1. **JTA overnight** is reshaped from the existing `accommodation_panel.csv`
   (MLIT-Excel provenance) into the panel contract, keyed prefecture × month.
   It is **not** re-pulled from the e-Stat API, because that API ends at 2016.
2. **`fetch_estat_generic`** is a thin wrapper that delegates to the existing
   `scripts/fetch_estat_data.py` machinery; it does not re-implement the
   getStatsList→getStatsData flow.
3. **FF-DATA** enters as its own tidy table at its native grain —
   origin-prefecture × destination-prefecture × year × transport-mode inbound
   foreign-visitor flow — pulled via the existing FF-DATA fetcher
   (`MLIT_DATA_APP_ID`). It is never coerced into prefecture × month.
4. The new `panel_pref_monthly` table is **strictly additive**: the existing
   daily panels (`panel_site_daily` = 2245 rows, `panel_area_daily` = 4523
   rows) remain byte-for-byte reproducible when the gov files are absent, and
   the new table is guarded by a file-exists check.

## Consequences

- The thesis gains a prefecture-level arrivals/overnight and inbound-flow
  context layer with honest provenance, without duplicating fetch code.
- This layer is context and validation only. It does **not** convert the
  associational SEM path (0.17) into a causal estimate, and it does **not**
  resurrect the Shinkansen natural experiment inside the reservation panels —
  `S5_shinkansen_NOT_identifiable_here` stays intact and ADR 0027 is unchanged.
- Cadence is kept honest: prefecture × month overnight and prefecture-pair ×
  year flow are separate tables, never forced into the daily panels.
- Missing prefecture/month cells are left NaN with a coverage flag; no value is
  imputed or interpolated.

## Alternatives

- **Build fresh e-Stat REST fetchers as Pack 06 literally specified.** Rejected:
  duplicates `fetch_estat_data.py`, and the JTA API path returns only ≤2016
  data, so the "recent month" acceptance target is unmeetable via the API.
- **Pull JTA overnight from the e-Stat API anyway.** Rejected: the API DB ends
  2016; the MLIT-Excel-derived `accommodation_panel.csv` is the current,
  higher-coverage source the repo already validates.
- **Fold FF-DATA O-D flow into the prefecture×month panel.** Rejected: it is a
  different grain (annual origin→destination), and flattening it would
  misrepresent the cadence ADR 0027 requires be kept honest.
