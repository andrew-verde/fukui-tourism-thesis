# Non-Survey Panel

Regenerate the reference panel from the pinned artifact/raw cache:

```sh
PANEL_RAW_DIR=/path/to/pinned-panel-cache make panel
```

With the committed reference artifacts present, `make panel` also performs a
self-refresh/contract check using `data/nonsurvey` as the input cache.

The panel is observational. The reservation panels begin in October 2023, so
they do not identify a Hokuriku Shinkansen pre/post effect; that effect remains
in the repo's multi-year arrivals/accommodation scripts.
