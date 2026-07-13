# Non-Survey Source Inventory

The physical-intervention reframe uses keyless Code4Fukui open-data sources
pinned in `data/nonsurvey/data_manifest.json`. The manifest records repository
commits and per-file SHA256 checksums for the seven source repos used by the
panel builder.

## Live (key-gated, keys supplied)

- JTA overnight guest-nights: prefecture × month, MLIT accommodation-survey
  Excel → `accommodation_panel.csv` → `gov/jta_overnight.parquet`. The e-Stat
  API for `00601020` is frozen at 2016; `0003313520` is reference-only. RESAS's
  API retired on 2025-03-24, so e-Stat/MLIT is the replacement path.
- Generic e-Stat tables: fetched through the existing
  `scripts/fetch_estat_data.py` machinery.
- FF-DATA: annual origin-destination inbound-foreign flow from the MLIT Data
  Platform catalog `ffd`, for 2018/2019/2022/2023/2024, written to
  `gov/ffdata_od_annual.parquet`.
