# ADR 0033: Normalize ADR 0019 and ADR 0023 to accepted-as-amended

Date: 2026-07-30
Status: accepted 2026-07-30 (normalizes ADR 0019 and ADR 0023; amends neither beyond consolidating amendments already made by ADR 0029 and ADR 0032, and outcomes already recorded by ADR 0031)

## Context

ADR 0019 (roadmap, 2026-07-03) and ADR 0023 (v2 chapter architecture,
2026-07-04) have carried `Status: proposed (pending human review)` since
they were written, while every subsequent decision has treated them as
binding governance:

- ADRs 0029, 0030, 0031 and 0032 each close with "post-acceptance
  deviations require a new ADR and demote the affected analysis to
  exploratory, **per ADR 0019**"; ADR 0020 states the same rule near its
  head and ADR 0021 in its Decision 9. That is the deviation discipline
  the whole pre-specification regime rests on, and it names ADR 0019 as
  its source.
- ADR 0023 §5 ("no chapter file changes before Phase 4, master map
  first") is the rule that has actually governed behaviour: ADR 0029 §4,
  ADR 0031 §"ADR 0023 Track T resolution", and the standing rules in
  `docs/thesis/TODO.md` all defer edits to Phase 4 on its authority.
- The defense memo's Seam D rests on ADR 0031 bounding ADR 0017's
  contribution claim. ADR 0031 binds Track T — a track defined by
  ADR 0023 — and inherits its deviation discipline from ADR 0019. The
  chain is accepted at both ends and `proposed` in the middle.

That gap is examiner-visible: the governance the thesis cites as binding
was never accepted, so an examiner can ask whether the discipline was
adopted or merely drafted. Nothing about the work changes; the record
does.

Both documents were also amended after the fact and have never been
reconciled in one place: ADR 0029 struck the Direction B items, ADR 0032
struck the FTAS long-lead item, and ADR 0031 resolved Track T.

## Decision

**1. ADR 0019 and ADR 0023 are accepted, as of 2026-07-30, as amended by
the ADRs listed below.** Their status lines are updated to point here.
Their bodies are not edited — the ADR log is append-only, so the
superseded Arm 1 text stays as written and this ADR is the reconciliation
layer.

**2. Consolidated amendment ledger for ADR 0019.**

| Part of ADR 0019 | Status now | Authority |
|---|---|---|
| Arm 1 (Direction B) as a primary arm | **struck** — retired as a data-collection path; a specified, unfielded protocol | ADR 0029 §1 |
| Phase 0 item 3 (Stage-2 fielding playbook) | **void** | ADR 0029 §1 |
| Phase 1 Direction B items (Stage 1 analysis, ethics/IRB, station-area permission, stimulus transit-fact verification) | **struck**; ADR 0029 §5 also strikes panel-vendor quotes, an item it names rather than one ADR 0019 Phase 1 listed | ADR 0029 §5 |
| Phase 1 "FTAS new-wave access request" as a human long-lead | **struck** — public open data, ordinary version bump | ADR 0032 §1 |
| Phase 2 Stage-2 fielding | **struck** | ADR 0029 §5 |
| Arm 2 (out-of-sample prediction) | in force; ADR 0020's both-of-two firewall condition is met (ADR accepted 2026-07-30, frozen scripts and oracles committed), so unseen data *may* be fetched by the frozen scripts. The production run itself is still an open human authorization (`docs/thesis/TODO.md`) and is unfired | ADR 0020, ADR 0032 |
| Arm 3 (Kanazawa replication) | **complete and closed**, ahead of its Phase 2 slot; verdict V1 fail / V2 fail / V3 descriptive | ADR 0031 |
| Arm 4 (review-corpus convergent validity) | unchanged — conditional, measurement-validation only, appendix-only per ADR 0023 §4 Track M | ADR 0019, ADR 0023 |
| Arm 5 (paid data) | unchanged — deferred under the (a)-and-(b) decision rule | ADR 0019 |
| Phase structure and Phase 4 dates | unchanged | — |
| Seat routing, gates, kill criteria, deviation discipline | unchanged and binding | — |

Everything not listed as struck or void is in force.

**3. Consolidated amendment ledger for ADR 0023.** The chapter map, the
seam-preservation rules, the stale-text matrix mechanism, and §5's
no-edits-before-Phase-4 rule are accepted unchanged. Track state:

| Track | State | Authority |
|---|---|---|
| D (durability / Arm 2) | **live, unresolved** — §7.1 drafted from the frozen prediction, §7.2 awaits the verdict; rows D1–D5 unfired | ADR 0020 |
| B (intervention / Arm 1) | **retired** — terminal branch added by ADR 0029 §4; rows B1 and B2 voided, B3 resolved-retired with its sentence staying **verbatim**, B4/B5 added, G3/G4 resolved | ADR 0029 §4 |
| T (template / Arm 3) | **resolved: V1 fail** — rows T1 and T2 both fire in Phase 4; §7.3 content supplied by ADR 0031 | ADR 0031 |
| M (measurement / Arm 4) | conditional, appendix-only, unstarted | — |

Chapter 7 survives every amendment: Track D alone guarantees it, and
Track T now supplies §7.3 with a bounded null rather than a deletion.
The conclusion renumbering 7→8 stands.

**4. What acceptance does not do.**

- It re-opens nothing. Every frozen contract (ADR 0018's retained text,
  ADR 0020's predictions and firewall, ADR 0021 §6 as corrected by
  ADR 0030, ADR 0025) stands exactly as written.
- It authorizes no chapter file edit. ADR 0023 §5 is now accepted rather
  than merely proposed, which makes the prohibition stronger, not weaker.
- It does not revive Arm 1, does not authorize the Arm 2 production run
  (that remains a separate human authorization), and does not re-open
  Arm 3.
- It does not retro-date the discipline. Everything decided while these
  two were `proposed` was decided under rules the project chose to
  follow; acceptance records that choice, it does not invent compliance.

**5. Phase 4 is now reasoned about on accepted ground.** Phase 4
(2027-10 → 2027-12) remains the single integration pass and the only
place chapter files change. Its known workload, as of today: matrix rows
G3, G4, G5, B4, B5 (Direction B retirement), T1, T2 and §7.3 (Arm 3
null), plus the always-stale set, plus whatever Track D fires. Rows are
executed against ADR 0023's mechanism column — Codex splice with
verbatim oracle, or ADR-gated rewrite — not by ad-hoc editing.

## Consequences

- The governance chain an examiner can walk — ADR 0019 discipline →
  ADR 0023 tracks → ADR 0031 verdict → ADR 0017 bound → Seam D — is
  accepted end to end. The soft spot closes without a single analytic
  change.
- The amendment ledger above is now the one place to read what survives
  of the July roadmap. Reading ADR 0019 alone still shows retired Arm 1
  text; the status line routes here.
- The human queue item "Resolve ADR 0019 and ADR 0023 statuses" is
  discharged. The remaining open decision is the Arm 2 production-run
  authorization.
- Deviations from ADR 0019 or ADR 0023 now carry the full cost the other
  accepted ADRs carry: a new ADR, and demotion of the affected analysis
  to exploratory.

## Rejected alternatives

- **Edit ADR 0019 and ADR 0023 in place to remove the Arm 1 text.**
  Breaks the append-only ADR log, destroys the record of what was
  believed when the pre-specifications were frozen, and makes the July
  reasoning unauditable at exactly the point where auditability is the
  product.
- **Supersede both with a fresh consolidated roadmap ADR.** More
  readable, but it would restate frozen rules in new words — and every
  restatement of a frozen rule is an opportunity to drift. Consolidating
  amendments while leaving the originals authoritative costs one
  indirection and risks nothing.
- **Leave them `proposed`.** The status is then either meaningless (the
  rules bind anyway) or dangerous (a future seat reads `proposed` as
  license to deviate without an ADR).
- **Accept only ADR 0023 and re-derive the roadmap.** ADR 0023's tracks
  and §5 inherit their deviation discipline from ADR 0019; accepting one
  without the other leaves the same gap one link down the chain.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote the
affected analysis to exploratory, per ADR 0019.
