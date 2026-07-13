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

## Open — decisions and acceptances (ordered)

- [ ] **Accept + commit ADR 0025** (Arm 2 P1 placebo construction, S1
  pinning). MUST precede any unseen-data fetch; until accepted, Arm 2
  implementation cannot start.
- [ ] **Accept + commit ADR 0026** (Stage 1 ≠ PBL vignette; usage rule).
  Best accepted before 2026-08-16, when the PBL results exist.
- [ ] **Stage-1 launch decision** — Direction B critical path. Checklist
  in ADR 0026 §3: deploy `experiments/nudge-pilot` as its own Vercel
  project (server-side assignment live), panel procurement n = 250 EN+JP,
  ethics coverage for the online stage, launch ADR with dates. Launch by
  ~late July keeps the autumn-2026 intercept window plausible; later
  makes spring 2027 the working assumption (ADR 0022 §5 rule).
- [ ] **Review/commit the accumulated working tree** (ADRs 0021–0026,
  design docs, playbook, v2 architecture, §7.1 draft, verification
  outputs, screener spec, memos, config amendment).

## Open — external long leads (start/continue now)

- [ ] **Ethics/IRB**: application with advisor. Add the ADR 0024/F5
  clause ("transit facts subject to factual correction before fielding")
  and scope to both recruitment modes + both windows (ADR 0022 §6).
- [ ] **Station-forecourt intercept permission**: inquiries to Fukui /
  Awara / Tsuruga municipal administrators (ADR 0022 §6 preference
  order; JR West premises only as fallback).
- [ ] **FTAS new-wave access request** (Arm 2 S1/S3 depend on post-2026-06
  waves; ADR 0019 Phase 1).
- [ ] **Panel-vendor quotes**: send
  `experiments/nudge-pilot/screener_spec.md` after deciding its three
  open items (recency window, EN panel composition, budget ceiling).

## Standing rules (do not lose)

- No unseen Arm 2 data (post-2025-12 mobile, post-2026-06 FTAS, JTA 2025
  confirmed/2026) fetched or opened until ADR 0025 is accepted and the
  frozen scripts + oracles are committed (ADR 0020 firewall).
- PBL vignette results (close 2026-08-16): informative for launch
  decisions only; never enter d_plan; never thesis evidence (ADR 0026 §2).
- Direction B is design, not evidence, until Stage 2 completes.
- Human commits; no seat commits or pushes.
