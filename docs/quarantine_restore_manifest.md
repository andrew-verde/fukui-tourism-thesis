# Quarantine restore manifest — Arm 2 operator inputs

Recorded 2026-09-15, after migrating the fedora working copy to the fujitsu server.

## Why this file exists

`data/quarantine/arm2/` is 1.9 GB and git-ignored, so it has never been in version
control. It was previously described — in this repo's own notes and in my earlier
summaries — as un-refetchable operator-supplied material. **That was wrong for the bulk
of it.** 1.35 GB of the 1.6 GB in `operator_inputs/` is three clean clones of two PUBLIC
GitHub repositories, with no local-only commits, no stashes and no modified files.
They do not need backing up; they need pinning. That is what this file does.

Only `operator_inputs/jta/` (4.6 MB, 7 files) is genuinely operator-supplied with no
upstream, and it is now committed to this repo under `data/operator_supplied/jta/`.

## Re-clonable sources (verified present on GitHub 2026-09-15)

### fukui-kanko-survey — 1.3 GB of the total
- URL:    https://github.com/code4fukui/fukui-kanko-survey  (public, not archived)
- PIN:    07a0460cd80b4f8826457b5cd131df0c02c68d65   (branch master, committed 2026-09-13T21:46:55Z)
- Local:  data/quarantine/arm2/operator_inputs/ftas_source
- Pack:   807.52 MiB, 56354 objects, working tree clean at the pin
- NOTE:   upstream master has since moved to c36b9aa8 — the pin is load-bearing, do not
          restore from HEAD.

### japan-kanko-stat — 23 MB, cloned twice
- URL:    https://github.com/code4fukui/japan-kanko-stat  (public, not archived)
- PIN:    fd936d6ff3c036d0d53f5ab775ef25ba24c8ca43   (branch main, committed 2026-09-11T21:52:07Z)
- Local:  data/quarantine/arm2/operator_inputs/mobile_source
          data/quarantine/arm2/mobile/repository        (identical clone, same pin)
- NOTE:   upstream HEAD currently equals the pin. Restore by SHA regardless.

### Restore procedure

    cd data/quarantine/arm2/operator_inputs
    git clone https://github.com/code4fukui/fukui-kanko-survey ftas_source
    git -C ftas_source checkout 07a0460cd80b4f8826457b5cd131df0c02c68d65
    git clone https://github.com/code4fukui/japan-kanko-stat mobile_source
    git -C mobile_source checkout fd936d6ff3c036d0d53f5ab775ef25ba24c8ca43
    cp -r mobile_source ../mobile/repository

Then verify against `arm2_quarantine_inventory.csv` (SHA-256 for all 3,094 files),
archived alongside this record.

## Operator-supplied, NO upstream — now committed here

`data/operator_supplied/jta/` — Japan Tourism Agency accommodation survey releases
(宿泊旅行統計調査), downloaded by hand. These are the only files in the whole quarantine
with no reproducible source, which is why they are in git despite `*.xlsx` being
git-ignored (force-added deliberately — the same ignore rule is what left Arm 2's
results on a single machine).

SHA-256:
  f248106e23d058ad9f49efd85c80ebb5...  2025_confirmed.xlsx
  717b492a79276073a2f15bfaf712941f...  2026_01_second_preliminary.xlsx
  16422ebe4b3f8892ae9eb977a5a46616...  2026_02_second_preliminary.xlsx
  fbd467594bebc2bc55655349707199c3...  2026_03_second_preliminary.xlsx
  5ea7fba6267d25e9a9e76b36db98f905...  2026_04_second_preliminary.xlsx
  1d1dd6be51058219cb79c96d1572e06d...  2026_05_second_preliminary.xlsx
  23dde1846dde19d7b3f98c67aeb652af...  2026_06_second_preliminary.xlsx

## Derived, NOT re-clonable but reproducible from the pins above

- `operator_inputs/merged_candidates/` — 136 MB, 6 CSVs named `<date>_<sha>.csv`;
  each filename records the source commit it was cut from.
- `operator_inputs/failed_ftas_prefix_attempt_20260914/` — 168 MB, 4 CSVs; the failed
  prefix-matching attempt, retained as evidence for ADR 0037, not as an input.
- `ftas/`, `jta/`, `mobile/` assembled outputs — products of the assembly tools in
  `tools/arm2_assemble_*.py`.

These exist on fedora and fujitsu only. They are regenerable from the pinned sources
plus the committed assembly tools, so they are not backed up off-machine.

## Standing constraints (unchanged)

Arms 2 and 3 remain closed. Nothing in this record licenses reopening either on a
fresher data vintage; the pins above exist to make the CLOSED vintage reconstructable,
not to support a re-run.
