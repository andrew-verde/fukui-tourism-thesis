# ADR 0032: Arm 2 data-availability correction — both "long leads" were phantoms; the firewall is now the only protection

Date: 2026-07-30
Status: accepted 2026-07-30 (corrects ADR 0019 Phase 1, ADR 0029 §Consequences, ADR 0031 §Consequences; does not amend ADR 0020's contract)

## Context

ADR 0019 Phase 1 listed "FTAS new-wave access request" as a human
long-lead item, grouped with ethics/IRB and station-area intercept
permission. That grouping propagated: ADR 0029 (`:134`) and ADR 0031
(`:136`) both describe FTAS access as Arm 2's single point of failure,
and ADR 0020 (`:161-163`) plus `SCIENCE_HANDOFF.md` §3 set the earliest
Arm 2 verdict at ~mid-2027 on the assumption that unseen months had to
accumulate.

A coverage verification on 2026-07-30 (`docs/arm2_ftas_coverage_memo.md`)
established that this is wrong. Both Arm 2 inputs are public open data
published by Code for Fukui, pinned in this repository the same way every
other source is, and both have already published the unseen window.

## Findings

**FTAS is public open data, not a gated dataset.**
`config/official_fukui_sources.yaml:8-27` pins three files from
`https://github.com/code4fukui/fukui-kanko-survey`. The pinned commit
`5857c311acc5782eb44d85f06d95e6a2e6af4509` is dated 2026-06-29 UTC;
upstream HEAD `22a95f3f2e941077ba1c557c5d4fca23fcc05e09` is dated
2026-07-29 UTC. Both carry the subject `update data`.

Coverage at HEAD, established from date/count metadata only:

- Pinned response-bearing period: 2022-04-28 – 2026-06-29.
- New: 57 responses on 2026-06-30, plus 1,835 in July 2026 through
  2026-07-29. **1,892 responses after the pinned endpoint.**
- All three schemas unchanged.

**The mobile-location municipal panel is also public open data.**
`config/national_data_sources.yaml:35-45` pins
`https://github.com/code4fukui/japan-kanko-stat` at commit `dfb9069`.
Upstream HEAD is `6d8dccf1514262c1d13acb3e00072f6dc5b55ae9`. A tree
listing (filenames only, no blob content — cloned with
`--filter=blob:none --no-checkout`) shows `data/city202601.csv` through
`data/city202606.csv` present upstream.

**ADR 0020's six-unseen-month condition is already satisfied.** ADR 0020
§"Primary predictions" (`:69-72`) runs P1/P2 on unseen mobile-panel months
2026-01 onward with a minimum of six unseen months. Six exist:
2026-01..2026-06.

**Obtaining either input is an ordinary version bump** — change commit +
checksum together, fetch with `--force`, rebuild, review estimate changes,
per the procedure already documented in the header of
`config/official_fukui_sources.yaml`. No external request, no
gatekeeper, no institutional lead time.

## Decision

1. **The characterization is corrected.** "FTAS new-wave access request"
   is struck as a long-lead human dependency wherever ADR 0019 Phase 1,
   ADR 0029, and ADR 0031 assert it. Arm 2 has **no external dependency
   and no external point of failure.** ADR 0029's contingency ("if FTAS
   access is denied, the upgrade narrows to Arm 3 plus the non-survey
   engine") describes a scenario that cannot occur as written; it is
   withdrawn. ADR 0031's consequence paragraph is corrected to the same
   effect.

2. **The ~mid-2027 earliest-verdict estimate is withdrawn** as a
   data-availability claim. It was predicated on waiting for months that
   have already published. Arm 2's schedule is now governed solely by how
   long it takes to build and commit the frozen scripts and oracles.

3. **ADR 0020's contract is NOT amended.** Every prediction, threshold,
   seen/unseen boundary, firewall rule, and the vintage-revision-guard-first
   ordering stands exactly as written. This ADR corrects a factual belief
   about data logistics, nothing about the analysis.

4. **The firewall release condition is unchanged and is BOTH-of-two.**
   ADR 0020 (`:34`) permits unseen outcome values to be fetched or opened
   only once *this ADR is accepted* **and** *the analysis scripts with
   their oracles are committed*. **ADR 0020 is still `Status: proposed`.**
   Building the scripts satisfies one condition and does not release the
   firewall. No unseen fetch is authorized by this ADR.

5. **Scaffolding work is authorized now.** ADR 0020 (`:33-34`) explicitly
   permits fetch/build scaffolding to be developed and tested against the
   seen vintages. Arm 2 script construction proceeds on that basis, seen
   data only.

## Consequences

- **Arm 2 moves from "blocked on an external request" to "blocked on work
  we control."** It is now the critical path in the literal sense — the
  only thing between the current state and a verdict is Codex output and
  one ADR status decision.
- **The firewall is now the sole protection, and it is load-bearing
  today.** Previously, the unseen data's unavailability was an accidental
  second line of defence. It is gone. The complete test set is one
  `git clone` away from any seat or person with the repository URL. A
  single careless `head()` permanently destroys the out-of-sample claim,
  with no way to undo or audit it away. SCIENCE_HANDOFF §6 trap 2 should
  be read as active operational risk, not background caution.
- **Six months is the floor, not a target.** More unseen months publish
  every month that passes. Nothing is lost by taking the time to build
  the scripts correctly, and the temptation to hurry has no data-side
  justification.
- **Filenames were verified, contents were not.** `city202606.csv`
  existing does not establish that the month is complete, final, or
  unrevised. Vendor panels revise history; ADR 0020's vintage-revision
  guard runs first, always, and could still fail on the new vintage. Six
  published files is a necessary, not sufficient, condition.
- This ADR corrects the record only. No analysis is demoted; no result
  changes; nothing has been fetched or opened.

## Audit trail

What was read to establish the above: upstream Git commit metadata, tree
and file names, blob sizes, sha256 digests, the header rows of the three
FTAS files at both commits, and every row of `all-cnt.csv` (schema
`day,count` — response counts by date, coverage metadata carrying no
outcome). One *seen*-vintage `day,count` row was read to identify the
compact `YYYYMMDD` date format after a validator expected `YYYY-MM-DD`;
the failed validator printed no data row.

What was not read: no data row of `all.csv` at either commit, no data row
of `area.csv`, and no blob content whatsoever from the mobile-panel
repository. Full statement: `docs/arm2_ftas_coverage_memo.md` §7.

**Quarantine state (2026-07-30).** Answering the schema question required
materialising `all.csv`'s blob at both commits — a header row cannot be
read from Git without fetching the object — so the coverage check left a
30 MB blobless clone of the FTAS repository at HEAD `22a95f3` under
`data/quarantine/arm2/upstream_repo`, including the unseen `all.csv`
object (96,707,587 bytes). No value in it was ever decoded beyond the
header row.

That clone was **deleted the same day**. The quarantine directory is empty
(0 files, 0 bytes) and no unseen bytes remain on disk. ADR 0020 designates
quarantine as where unseen pulls live, so retaining it would have been
defensible; it was removed because the firewall's release conditions
(ADR 0020 accepted **and** frozen scripts committed) are not yet met, the
clone is reproducible in minutes, and leaving it created a standing risk
that some later seat, tool, or index would touch it. No mobile-panel data
was ever fetched — P1 and P2's inputs have never been on this machine
beyond the pinned seen vintage.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote the
affected analysis to exploratory, per ADR 0019.
