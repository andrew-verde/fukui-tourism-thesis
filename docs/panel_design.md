# Non-Survey Panel Design

The panel has two daily grains:

- `data/nonsurvey/panel_site_daily.parquet`: camera-site days for Tojinbo,
  Fukui Station East, and the two Rainbow Line parking gates, joined to
  Google Business Profile trend fields and a `post_shinkansen` date flag.
- `data/nonsurvey/panel_area_daily.parquet`: lodging-market days for Awara
  Onsen, Fukui Station, Echizen Coast, Obama, and Mikatagoko, with reservation
  counts, occupancy proxy, ADR proxy, hotel capacity, booking lead time, trend
  fields, and `post_shinkansen`.

Site-to-area links used downstream:

- `tojinbo -> awara_onsen`
- `fukui_station_east -> fukui_station`
- `rainbow_line_lot1 -> mikatagoko`
- `rainbow_line_lot2 -> mikatagoko`

The design is observational. The Shinkansen break flag is a structural marker,
not an identified treatment effect in this panel, because the reservation data
start in October 2023 and lack a seasonally comparable pre-extension window.
