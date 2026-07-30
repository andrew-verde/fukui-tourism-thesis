# Pending human tasks

Updated 2026-07-30. Successor-seat task routing lives in
`SCIENCE_HANDOFF.md`; thread/session state lives in `HANDOFF.md` (both
untracked by design). This file is the *human* queue.

## Scope change 2026-07-29/30

Direction B (survey arm) retired (ADR 0029). Arm 3 complete and closed
with a bounded null (ADR 0031). Arm 2 built, committed, and **live**
(ADR 0020 accepted). The project has no external dependencies.

## Done

- [x] **ADR 0029** — Direction B retired, Ch. 6 refocused. Accepted 2026-07-29.
- [x] **ADR 0021** — Arm 3 Kanazawa design. Accepted 2026-07-29.
- [x] **ADR 0025** — Arm 2 P1 placebo construction, S1 pinning. Accepted 2026-07-29.
- [x] **ADR 0030** — Arm 3 implementation corrections (50-month window;
      Hagibis primary `2019-10` + `2019-10..12` sensitivity; V3 = 19-facility
      aggregate). Accepted 2026-07-30.
- [x] **ADR 0031** — Arm 3 verdict: V1 fail, V2 fail, V3 met descriptively.
      Portability not demonstrated at prefecture grain. **Arm 3 is closed.**
- [x] **ADR 0032** — Arm 2 data-availability correction. Both supposed
      external dependencies were phantoms.
- [x] **ADR 0020 accepted 2026-07-30 — binding.** Two pre-acceptance
      drafting corrections applied first (guard population → the 13
      high-confidence municipalities by area code; S3 denominator →
      pooled other, 4.003×).
- [x] **Merged to `main`** — both `reframe/*` branches, merge `476b37d`.
- [x] **Arm 3 work committed and pushed** — 11 commits, suite 217 passed /
      1 skipped at that point, Arm 3 artifacts force-added per
      `docs/arm3_implementation_report.md`. **Later work on 2026-07-30 is
      uncommitted:** two new test files (suite now 243 passed / 1 skipped),
      the CI deselect list, the defense-memo rewrite, and two provenance
      blocks. See `SCIENCE_HANDOFF.md` §6.
- [x] **ADR 0033** — ADR 0019 and ADR 0023 normalized to accepted-as-amended
      2026-07-30, with one consolidated amendment/track ledger. Bodies
      unedited; ADR log stays append-only.
- [x] **ADR 0034** — journal-manuscript framing settled before drafting
      (ADR 0031's instruction): one paper, Chapters 3–4 spine, Arm 3 as a
      bounded null, bound in the abstract, Arm 2 excluded, reviewer-pressure
      answers fixed in advance.
- [x] **Pushed 2026-07-30.** Clean fast-forward onto `origin/main`; no
      force-push, no published SHA changed. `SCIENCE_HANDOFF.md` had been
      force-added against `.gitignore:170-173` and was scrubbed from history
      the same day — zero handoff objects in the object store, and both
      handoff documents remain on disk, untracked. `main` now in sync.

## Open — decisions awaiting you

- [x] **Arm 2 run authorized 2026-07-30 — held, not fired.** You chose to
      rehearse now and fire on a later, larger vintage. Rehearsal passed
      (guard-only, nothing decoded; see `SCIENCE_HANDOFF.md` §6.1). The
      single-use rule is unchanged: whatever vintage you fire on is the
      vintage the confirmatory claim is made on, and months published after
      it cannot be added without a new ADR and a demotion to exploratory.
- [ ] **Fire the Arm 2 production run — when you pick the vintage.** See the
  standing rules below. One-shot; no reason to hurry. More unseen months
  publish monthly, and six is the floor, not a target. **Blocked on one
  build task first:** only the mobile leg has quarantine assembly tooling
  (`tools/arm2_assemble_quarantine.py`); the `ftas/` and `jta/` legs still
  need theirs.

## Open — external long leads

**None.** Struck by ADR 0029: ethics/IRB, station-forecourt permission,
panel-vendor quotes. Struck by ADR 0032: the "FTAS new-wave access
request" — FTAS and the mobile panel are both public Code for Fukui repos
and both have already published the unseen window (six mobile-panel months
2026-01..2026-06; 1,892 new FTAS responses). Obtaining either is an
ordinary version bump.

## Standing rules (do not lose)

- **THE ARM 2 FIREWALL IS RELEASED.** ADR 0020's both-of-two condition
  (ADR accepted **and** frozen scripts + oracles committed) is met as of
  2026-07-30. Unseen data may now be fetched — but **only** into
  `data/quarantine/arm2/`, **only** by the frozen scripts, with the
  vintage-revision guard first, always.
- **Arm 2 is single-use.** The moment unseen outcome values are observed,
  the pre-specification option is spent. No re-running with a tweaked
  donor pool, window, or "quick sanity check". Any re-specification after
  seeing results requires a new ADR and demotes the analysis to
  exploratory. Never open unseen data outside the frozen scripts — not
  with pandas, not with `head`, not to check a parse.
- **Guard first.** If RMS relative revision exceeds 2% for any of the 13
  pinned confirmatory municipalities, or any donor exits the fit gate,
  stop and write a deviation ADR choosing between re-running the entire
  Direction D + Arm 2 chain on the revised vintage, or demoting Arm 2 to
  exploratory. Mixing vintages is forbidden.
- **Quarantine is empty and that is its resting state** until an
  authorized run. A coverage check left 30 MB there on 2026-07-30; it was
  deleted the same day (ADR 0032 §Audit trail).
- **Arm 3 is closed.** No further Arm 3 computation without a new ADR;
  re-specifying after seeing the verdict destroys what makes the null
  credible.
- PBL vignette results: never thesis evidence, never any planning quantity
  (ADR 0026 §2, survives ADR 0029). Retiring Direction B removed d_plan
  and therefore *raises* the temptation to substitute these numbers. The
  prohibition is absolute.
- Direction B is a specified protocol that was never fielded. Nothing is
  estimated under ADR 0018.
- No chapter file changes before Phase 4 (ADR 0023 §5).
- Agent handoff docs are never tracked (`.gitignore:170-173`). One was
  force-added on 2026-07-30 and was scrubbed from history the same day.
- **Human commits; no seat commits or pushes.** The 2026-07-30 commit and
  merge were a one-off explicit authorization, not a change to this rule.
