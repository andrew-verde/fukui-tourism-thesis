# Non-Survey Source Inventory

The physical-intervention reframe uses keyless Code4Fukui open-data sources
pinned in `data/nonsurvey/data_manifest.json`. The manifest records repository
commits and per-file SHA256 checksums for the seven source repos used by the
panel builder.

Key-gated government sources are deliberately not fetched or imputed in this
panel. Future authenticated fetchers attach at `scripts/fetch_gov_sources.py`:

- JTA overnight stays via e-Stat statsCode `00601020`: supply an e-Stat `appId`.
- Generic e-Stat table fetch: supply an e-Stat `appId`.
- FF-DATA, e-Stat toukei `00600466`: supply FF-DATA/e-Stat credentials.

Until those keys are supplied, the stubs raise `NotImplementedError` and the
panel remains limited to the pinned public sources.
