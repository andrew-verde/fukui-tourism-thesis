# Pending human tasks

Updated 2026-07-07 (end of Fable reasoning window). Successor-seat task
routing lives in `SCIENCE_HANDOFF.md`; this file is the *human* queue.

- [x] **Fill citations in §7.2**: DONE 2026-07-03 (see git history).
- [x] **Verify stimulus transit facts against current timetables**: DONE
  2026-07-07. Protocol executed by Codex
  (`experiments/nudge-pilot/timetable_verification.md`, evidence archive +
  sha256 manifest under `experiments/nudge-pilot/verification/`); three
  corrections applied to `study-config.json` (version 2026-07-07) per
  ADR 0024. No participant exposure occurred — the instrument had never
  fielded (ADR 0026). Re-verification at T−4w/T−1w before any launch
  remains a fielding precondition (ADR 0022 §4).

## Scope change 2026-07-29

Direction B (survey arm) retired — see draft ADR 0029. Arm 2 + Arm 3 +
the non-survey engine now carry the empirical upgrade. Items below are
rewritten against that decision.

## Open — decisions and acceptances (ordered)

- [ ] **Accept + commit ADR 0029** (retire Direction B; refocus Ch. 6;
  amend ADRs 0019/0023). Gates everything else in this file.
- [x] **ADR 0021** (Arm 3 Kanazawa design) accepted 2026-07-29.
- [x] **Arm 3 complete** 2026-07-30. Verdict: V1 fail, V2 fail, V3 met
  descriptively — portability not demonstrated at prefecture grain
  (ADR 0031; corrections in ADR 0030). Force-add the 12 result artifacts
  + 2 pinned PDFs per `docs/arm3_implementation_report.md`; they sit under
  the blanket `output/*` ignore.
- [x] **ADR 0025** (Arm 2 P1 placebo construction, S1 pinning) accepted
  2026-07-29.
- [ ] **Resolve ADR 0020's status** — still `proposed`. It is the binding
  Arm 2 contract that 0025 is an addendum to, and SCIENCE_HANDOFF
  describes it as accepted while the file disagrees. **The firewall
  releases only when 0020 is accepted AND the frozen scripts + oracles
  are committed — both.** Scripts are being built now; this is the other
  half.
- [ ] **Merge the non-survey branches to `main`** —
  `reframe/gov-estat-fetchers` is 3 commits ahead (ADR 0028 + gov
  parquets + Makefile targets) and unmerged. Arm 3 work should not be
  built on a side branch. (`mac/FukudaIdea-Contest` was an identical
  duplicate; deleted 2026-07-29.)
- [ ] **Review/commit the accumulated working tree** (ADRs 0021–0026,
  0029, design docs, v2 architecture, §7.1 draft, memos).

## Open — external long leads

**None.** Struck by ADR 0029: ethics/IRB application, station-forecourt
intercept permission, panel-vendor quotes. Struck by ADR 0032: the "FTAS
new-wave access request" — FTAS and the mobile panel are both public Code
for Fukui repos, and both have already published the unseen window
(six mobile-panel months 2026-01..2026-06; 1,892 new FTAS responses).
Obtaining either is an ordinary version bump.

The project now has no external dependencies. Everything remaining is
work under your own control.

## Standing rules (do not lose)

- No unseen Arm 2 data (post-2025-12 mobile, post-2026-06 FTAS, JTA 2025
  confirmed/2026) fetched or opened until **ADR 0020 is accepted AND** the
  frozen scripts + oracles are committed — both conditions (ADR 0020:34).
  ADR 0025 is accepted; ADR 0020 is not.
- **The unseen data is public and one `git clone` away** (ADR 0032). The
  firewall is now the only thing protecting Arm 2's out-of-sample claim.
  A single careless `head()` destroys it permanently, with no undo and no
  audit trail. This was previously protected by accident — the data did
  not exist yet. That protection is gone.
- PBL vignette results (close 2026-08-16): never thesis evidence, never
  any planning quantity (ADR 0026 §2, survives ADR 0029). Retiring
  Direction B removes d_plan but raises the temptation to substitute
  these numbers. The prohibition is absolute.
- Direction B is a specified protocol that was never fielded. Nothing is
  estimated under ADR 0018.
- No chapter file changes before Phase 4 (ADR 0023 §5, unchanged).
- Human commits; no seat commits or pushes.
