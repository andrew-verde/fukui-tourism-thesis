# ADR 0024: Pre-fielding stimulus corrections from timetable verification

Date: 2026-07-07 (supersedes same-day draft that assumed Stage 1 was
already fielding; human confirmed 2026-07-07 the nudge-pilot instrument
has never been deployed, so this records a pre-fielding correction, not a
mid-stage deviation)

Status: proposed (pending human review)

## Context

The timetable-verification protocol (playbook ADR 0022 §4; the last open
TODO and the ADR 0018 fielding precondition) was executed 2026-07-07 by
Codex against operator-official sources
(`experiments/nudge-pilot/timetable_verification.md`; 25 archived evidence
files with sha256 manifest under `experiments/nudge-pilot/verification/`).
Verdicts: four PASS, three AMEND, zero STRUCTURAL. Two AMENDs were judged
materially false as written, both in the `eiheiji_half_day` task's
`transport_access` strings (shown in `transport_access` and `combined`):

1. The config claimed the direct Eiheiji Liner runs "roughly once or twice
   an hour"; the verified service (Keifuku, 2026-04-01 timetable) is six
   direct trips per day, hourly 09:50–14:50, none after.
2. The config implied an evening last-return bus; the verified last direct
   return leaves Eiheiji at 16:20. The round-trip-ticket claim could not
   be verified and is dropped.

A third AMEND (`tojinbo_awara` frequency wording) was merely imprecise.

**Deployment status, verified 2026-07-07:** the only Vercel project in the
account (`vignette-survey`) serves a separate two-arm PBL study built from
the `hokuriku-tourist-sentiment-analysis` source and contains none of
these strings; `experiments/nudge-pilot` has no Vercel project and has
never fielded. **No participant was ever exposed to the false facts.**
The ADR 0018 sequence therefore worked as designed: verification completed
and corrections landed before fielding, and no protocol deviation
occurred. (The prior working assumption that Stage 1 was "in the field
under the PBL companion deployment" — carried by ADR 0019 and the playbook
— was wrong; see Consequences for the schedule implication.)

## Decision

1. **The three replacement strings from the verification memo are adopted
   verbatim** into `experiments/nudge-pilot/study-config.json` (single
   source of truth; `combined` concatenates the same strings at runtime).
   Oracle: config strings byte-match the "Proposed replacement string"
   cells of `timetable_verification.md` rows 1, 3, 6. Applied and
   oracle-checked 2026-07-07.
2. **Config `version` bumps 2026-07-02 → 2026-07-07.** The instrument
   writes `version` into every submission (`study_version`,
   `api/submit.js`), so stimulus vintage is keyed in the data from the
   first real response onward.
3. **The ADR 0018 fielding precondition is satisfied** as of this
   correction, subject to the playbook's re-verification cadence (T−4
   weeks and T−1 week before any launch, against the then-current
   timetable revision).
4. **Stage-1 readout obligation (unchanged in spirit, simplified in
   fact):** all Stage-1 data will carry `study_version = 2026-07-07` or
   later; any earlier version appearing in the table indicates an
   unauthorized deployment and quarantines those rows from the prior.

## Consequences

- The materially-false-stimulus contingency (playbook §4; red-team memo)
  is closed with the best available outcome: caught pre-exposure, cost
  zero.
- **Schedule risk surfaced:** Stage 1 has not started as of 2026-07-07,
  while ADR 0019/0022 treat 2026-08-16 as its close. An n = 250 online
  panel is fieldable in roughly 2–4 weeks, so the date can hold only if
  launch happens promptly; otherwise the readout (2026-08-31) and the
  autumn-window gate (2026-09-30) slip together. The launch decision —
  panel procurement, ethics coverage for the online stage, deploy of the
  instrument as its own Vercel project — is a human action this ADR
  flags but does not decide.
- The consistency audit's FAIL-1 (close date sourced only from roadmap
  documents, not from any instrument artifact) is hereby explained: the
  date was a plan, not a deployment fact. Roadmap references to "Stage 1
  closes 2026-08-16 under the PBL companion deployment" should be read
  as superseded by this ADR's verified status.
- The corrected Eiheiji copy is less optimistic than the draft copy —
  the real last-mile service is sparser than the instrument assumed,
  which is the very friction Chapter 4 diagnoses; worth one line in the
  eventual write-up.

## Rejected alternatives

- **Treating the correction as a logged deviation with pre/post-split
  reporting** (the superseded same-day draft): predicated on Stage 1
  being mid-field; verified false, and keeping deviation machinery for a
  non-event would manufacture a caveat the data does not carry.
- **Deploying the amended nudge-pilot instrument immediately to the
  existing Vercel project:** that project serves a different live study;
  the nudge pilot fields as its own project, on a launch decision, not
  as a side effect of a copy fix.
- **Leaving the imprecise Tojinbo string for a later pass:** one version
  bump with all three verified corrections avoids version fragmentation.
