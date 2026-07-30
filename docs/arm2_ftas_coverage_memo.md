# Arm 2 FTAS upstream coverage memo

## 1. Pinned commit versus upstream HEAD

The repository pins the three FTAS files in
`config/official_fukui_sources.yaml` to upstream commit
`5857c311acc5782eb44d85f06d95e6a2e6af4509`,
dated 2026-06-29 21:22:21 UTC (2026-06-30 JST). The upstream HEAD examined
here is
`22a95f3f2e941077ba1c557c5d4fca23fcc05e09`,
dated 2026-07-29 20:49:11 UTC (2026-07-30 JST). Both commits have the
subject `update data`.

| Upstream file | Pinned sha256 (`5857c311`) | HEAD sha256 (`22a95f3`) |
|---|---|---|
| `all.csv` | `440a88f2c4e37b9319a3c555716da9e24c33bd518db4dd21c761b00cd6f9b02b` | `a93838af4d8d3f1278f513281dd1c2c9faa783d32c03fca62d1c6e62f20a2a84` |
| `all-cnt.csv` | `82eecbf369e76e985751be48aecb1ef0a6e2e799d7105653944d93a1cf5a0028` | `2a1401dacd6bb3ac1549806a6126359856170b00471129565c7138a1fb2003b7` |
| `area.csv` | `4905bae83db0a2d2a1aaa21ec3b0de93261dded395db77693a8bbc47e2ecb254` | `4905bae83db0a2d2a1aaa21ec3b0de93261dded395db77693a8bbc47e2ecb254` |

The pinned digests independently calculated from upstream match the three
digests currently recorded in `config/official_fukui_sources.yaml`.

## 2. Period covered by the pinned vintage

The pinned `all-cnt.csv` has dated counter rows from 2022-04-01 through
2026-06-29. The first date with a positive response count is 2022-04-28,
so the response-bearing period is **2022-04-28 through 2026-06-29**.
Its daily counts sum to **97,866 responses**. This is the upstream FTAS
file's Fukui-only coverage. The 103,807 responses declared seen in ADR
0020 refer to the thesis's merged tri-prefecture survey analytical window
(April 2023 through June 2026), not this upstream Fukui-only count file.

## 3. Period covered at `22a95f3`

At `22a95f3`, `all-cnt.csv` has dated counter rows from 2022-04-01 through
2026-07-29. Its first positive-count date remains 2022-04-28 and its last
positive-count date is **2026-07-29**.

Rows after the pinned vintage ends:

| Month | Responses |
|---|---:|
| 2026-06 (June 30 only) | 57 |
| 2026-07 | 1,835 |
| **Total after 2026-06-29** | **1,892** |

## 4. Direct answer

**Yes.** FTAS responses after 2026-06 exist at `22a95f3`. They cover
**one month, July 2026, with 1,835 responses** through 2026-07-29.

## 5. Schema diff (column names only)

| File | Added columns | Removed columns | Renamed columns |
|---|---|---|---|
| `all.csv` | None | None | None |
| `all-cnt.csv` | None | None | None |
| `area.csv` | None | None | None |

The complete header row of each file is byte-identical between the pinned
commit and `22a95f3`.

## 6. Access assessment

Obtaining the newer waves is an **ordinary version bump**, not an external
access request. The source is a public GitHub repository, and the newer
commit exposes the same three file paths without authentication or a
request workflow. A future authorized bump would change the commit and
the changed file digests together; no pin was changed here. This access
finding does not relax ADR 0020's requirement to freeze and commit the
analysis scripts and oracles before any unseen outcome is opened.

## 7. Firewall audit statement

Read:

- ADR 0020, `SCIENCE_HANDOFF.md` section 6 trap 2, and the three FTAS pin
  entries in `config/official_fukui_sources.yaml`;
- upstream Git commit metadata, tree/file names, blob sizes, and sha256
  digests;
- the complete header row only of `all.csv`, `all-cnt.csv`, and `area.csv`
  at both commits;
- every row of `all-cnt.csv`, whose entire schema is only `day,count`, to
  validate date/count syntax and calculate the permitted date coverage,
  totals, and monthly count;
- one pinned-vintage, seen `day,count` row to identify the compact
  `YYYYMMDD` date format after an initial validator expected
  `YYYY-MM-DD`. The failed validator printed no data row.

Not read or computed:

- no data row from `all.csv` at either commit and no data row from
  `area.csv`;
- no unseen-period raw line;
- no outcome or response value, including NPS, satisfaction, intention,
  free text, friction/`transport_access`, arrival mode, or any field
  feeding the Chapter 3 DiD or ADR 0020's S1/S3 predictions;
- no outcome distribution, category count, sample, crosstab, plot,
  correlation, model, or rebuilt FTAS output.

The upstream clone and fetched blobs are confined to the gitignored
`data/quarantine/arm2/` directory. No source pin, build output, commit,
tag, or remote branch was changed.
