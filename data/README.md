# Data

Raw and large intermediate data are not committed to this repository. They are
reconstructed from pinned sources. After cloning:

    make fetch

This repopulates `output/` from sources pinned in
`config/official_fukui_sources.yaml` and `config/national_data_sources.yaml`.

A backup of downloaded data is also in Google Drive. The fetch scripts are the
source of truth.

This project is early work. The pipeline does not yet enforce byte-level SHA
verification of fetched files, so upstream revisions may change a re-fetch.
