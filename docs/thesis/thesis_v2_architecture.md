# Thesis v2 chapter architecture

**Status: architecture plan, not prose. No chapter text changes with this
document.** It fixes, before any arm returns a result, where each arm's
results land in the thesis, how every *negative* outcome is written up
without breaking the ADR 0015 defense seams, and which existing text goes
stale under each outcome branch. It is the blueprint the Phase 4
integration pass (ADR 0019; successor to ADR 0014) executes. Decision
provenance: ADR 0023. The v1 chapter map in `thesis_master.md` remains
normative until the Phase 4 pass adopts the v2 map below by updating that
file.

Why this is written now: outcome-contingent chapter surgery designed
*after* results arrive drifts toward flattering the results. Fixing the
landing zones, the negative-outcome write-ups, and the stale-text
inventory while every branch is still live is the prose-side analog of
ADR 0020's freeze.

## 1. The v2 chapter map

| Ch. | v1 | v2 | Change |
|---|---|---|---|
| 1 | Introduction | Introduction | Bounded splices only (§4 matrix) |
| 2 | Data, provenance, reproducibility | same | Grows provenance entries for every new dataset |
| 3 | Impact (DiD) | same | Untouched except Track-D S1 addendum rule |
| 4 | Diagnosis (SEM + synthesis) | same | Untouched except vintage-bounding sentence |
| 5 | Robustness (Direction D) | same | **Untouched under every branch** |
| 6 | From diagnosis to intervention (C + B design) | From diagnosis to intervention: design **and result** | Absorbs Stage-1 estimation + Stage-2 result / no-go |
| 7 | Conclusion | **NEW — The template under test: out-of-sample and out-of-corridor** | Arm 2 (§7.1–7.2) + Arm 3 (§7.3) |
| 8 | — | Conclusion (v1 Ch. 7 renumbered) | §8.4 always rewritten |

Design principles behind the map:

1. **Chapters 1–5 are the diagnosis era and stay numerically frozen.**
   `thesis_master.md` declares numbering normative and §6 cross-references
   §4.x/§5 heavily; the only renumbering v2 performs is Conclusion 7→8,
   the cheapest possible cut (nothing forward-references §7.x except the
   master file and ADR history, which is immutable by design).
2. **Direction B's result lands where its design lives (Ch. 6).** ADR 0019
   Phase 3 already says "Chapter 6 rewrite as results." The chapter's
   §4→C→B spine is the thesis's argument; splitting design and result
   into different chapters would force every reader through a
   forward-reference at the argument's climax.
3. **Arms 2 and 3 share the new Chapter 7 because they are the same kind
   of act**: the claims of Chapters 4–6, exposed to data that could not
   have shaped them — out-of-sample *in time* (Arm 2: unseen months of
   the same event) and out-of-corridor *in space* (Arm 3: a different
   extension, frozen constants). The chapter title carries that logic.
4. **Chapter 7 exists under every branch.** Arm 2 reports regardless of
   outcome (falsification is first-class per ADR 0020); Arm 3 is
   detachable (§3, Track T) without renumbering anything — its section is
   the chapter's last.
5. **Direction B never enters Chapter 7.** Its result is causal evidence
   about an intervention, not a test of the template's predictions; mixing
   it in would blur the prereg boundary between ADR 0018 (B) and ADR 0020
   (Arm 2) that the defense posture relies on.

### New Chapter 7 internal structure

- **§7.1 The prediction (frozen 2026-07).** Restates ADR 0020's P1/P2,
  the seen/unseen boundary, and the interpretation contract *as written
  before the data* — this section can be drafted today and is
  outcome-invariant. Its function at the defense: proof of ex-ante
  commitment, the direct answer to Seam B.
- **§7.2 The verdict.** One of three pre-written shapes (Track D, §3).
  Secondary predictions S1–S3 reported here, never headlined.
- **§7.3 The template out of corridor (Kanazawa 2015).** Arm 3 per
  `arm3_kanazawa_design.md` §6's contract. If Arm 3 is delayed to the
  journal track, this section compresses to one paragraph citing the
  manuscript; if killed, it is deleted and §8.2's template sentence loses
  its Kanazawa clause — both moves leave §7.1–7.2 intact.

## 2. Seam-preservation rules (binding on all branches)

The ADR 0015 posture is **concede the channel, keep the claim**. New
results may *upgrade* a claim or *bound* it; they may never be spent
re-arguing a conceded channel, and a negative result never retracts a
concession that was already priced.

- **Seam A (arrival-mode composition).** No arm tests composition, so no
  outcome touches the concession. Arm 2's S3 (friction persistence) and
  Arm 4 (convergent validity) may only *add* corroboration sentences to
  the §8.3 first limitation; if S3 shows erosion below 2×, that is
  reported in §7.2 as a boundary on the constraint's persistence — the
  diagnosis of the 2023–2026 window stands (it is about those waves), and
  §4 text is protected by the vintage-bounding rule (§4 matrix, row G2).
- **Seam B (durability bridge).** Arm 2 is the seam's designated answer;
  ADR 0020's interpretation contract governs the rewrite of the §8.3
  third limitation verbatim (confirmed → out-of-sample corroboration;
  directional-only → concession stays as written; falsified →
  prospective-failure disclosure). Under no branch does Direction C
  become "established" retroactively in Chapters 4–6: §6.2 keeps its
  hypothesis staging in all branches, with at most a forward reference
  ("tested in Chapter 7").
- **Seam C (one-sided marginal significance).** Chapter 5 is untouched
  under every branch — its claim is a conjunction about March 2024 and no
  new data revisits it (ADR 0020 forbids reopening seen-window analyses).
  Arm 3's V1 outcome may be cited in the §8.3 second limitation only
  directionally: a passing V1 adds "the same one-sided posture, frozen
  ex ante, replicated at the 2015 terminus"; a failing V1 adds nothing
  there (its pre-declared reading — dilution, placebo floor — lives in
  §7.3), because Ch. 5's conjunction never depended on Kanazawa.
- **Direction B language firewall.** Until a Stage-2 result exists,
  "design, not evidence" survives every splice; after Stage 2, exactly
  one confirmatory sentence enters §6 (the prereg licenses one claim),
  and Stage-1 numbers are never printed as effects in any branch,
  including the no-go branch.

## 3. Claim tracks: landing zones and negative-outcome write-ups

Outcomes factor into three independent tracks (plus conditional Arm 4).
No global "good/bad scenario" exists; each track's branch is decided by
its own frozen gate, and the combinations compose because the tracks
touch disjoint claim sentences.

### Track D — durability claim (Arm 2, ADR 0020)

Lands: new §7.1–7.2. Verdict shapes for §7.2:

- **Confirmed (both primaries):** §7.2 reports the promotion; §8.1's
  fourth finding gains "and held out of sample"; §8.3 third limitation
  rewritten per contract; §1.2/§8.2 claim sentence upgrades "on the
  pattern-level evidence" to predictive framing. New ADR before the
  claim-sentence edit (ADR 0017 requires §1 and §8 to move together).
- **Directional-only:** §7.2 reports consistent-but-underpowered; *zero*
  edits elsewhere — this is the cheapest branch by construction, and the
  architecture treats it as the default drafting assumption.
- **Falsified (either primary):** §7.2 reports the falsification as a
  result, not a caveat. The canonical claim sentence (§1.2 ¶3 and §8.2
  ¶1) is revised by a new ADR to the bounded form: the anchor-conversion
  account organizes 2024–2025 but failed prospectively; the contribution
  re-weights onto the diagnosis (Ch. 4, untouched) and the honest
  prospective test itself. §6.2 gains one staging sentence pointing to
  §7.2; its mechanism prose survives because it was always priced as
  hypothesis. §8.3 third limitation rewritten to disclosure form.
  **What does not happen:** no re-litigation in Ch. 4–5, no softening of
  the anti-prediction's single license (the endpoint choice — which
  survives falsification, as §8.3 already argues via the saturation
  account).

### Track B — intervention claim (Arm 1, ADR 0018 + playbook ADR 0022)

Lands: Ch. 6, rewritten §6.3–6.4 (+ new §6.6 if needed for CONSORT
detail; appendix for instrument tables). Branch shapes:

- **Band N (Stage-1 d̂ ≤ 0, no Stage 2):** §6.3 gains the Stage-1
  estimation report and the no-go disclosure, framed exactly as ADR 0018
  pre-committed: the sign rule fired, confirmatory spend was refused, the
  mechanism translation failed at Stage-1 granularity. Chapter 6 keeps
  its design-not-evidence framing (already written and defensible —
  ADR 0019's degradation guarantee). §8.4 rewritten to "what the no-go
  taught." Seam B note: a Band-N outcome is about the *nudge's*
  manipulability, not about Direction C — the write-up must not let the
  intervention's failure read as a mechanism falsification (that verdict
  belongs to Track D alone).
- **Stage 2 run, H1 positive:** §6.3–6.4 rewritten as result (one
  confirmatory sentence + estimates with CIs); §8.1 gains a fifth
  finding; §1.2 ¶3 "sharp enough to specify the experiment" upgrades to
  "and the experiment ran"; contribution sentence gains its intervention
  clause only here.
- **Stage 2 run, null:** reported with the same prominence; the ceiling
  logic (§6.3) already prices a null as informative (the manipulable
  margin is below the floor); design-not-evidence becomes
  tested-and-not-supported — a *stronger* limitations posture, written as
  such, not as apology. No other chapter moves.
- **Stage 2 run, significant backfire (the two-sided test's reason for
  existing):** reported as a first-class finding about friction salience;
  §6.4's second limitation (manipulable-margin assumption) is the
  pre-built frame; policy-recommendation sentences (§6.5, §8.2 template
  clause "test the fix") gain a caution clause via the same ADR.

### Track T — template claim (Arm 3, ADR 0021)

Lands: new §7.3. Branch shapes per `arm3_kanazawa_design.md` §6:

- **V1 + V2 pass:** §7.3 reports replication; §8.2's exportable-object
  paragraph gains the Kanazawa clause; §6.5 unchanged (its template
  statement was already conditional).
- **V1 pass, V2 fail:** template bounded to surge/falsification
  machinery; §8.2 keeps the template claim with the durability clause
  attributed to Fukui-2024 evidence only. §7.3 carries the bound.
- **V1 fail:** §7.3 reports the failure with the pre-declared suspects
  (dilution, floor, contamination); §8.2 drops any portability sentence
  beyond "specified for export, not yet demonstrated." Chapter 5
  untouched (see Seam C rule).
- **Killed/delayed:** §7.3 deleted or compressed to a manuscript citation;
  no other text depends on it (the v1 thesis never mentions Kanazawa).

### Track M — measurement validation (Arm 4, conditional)

Lands: appendix + one paragraph in §2 (data) and at most one sentence in
the §8.3 first limitation ("an independent instrument agrees").
Guardrail: CONTEXT.md side-layer rule — never causal evidence, so no
branch of Arm 4 touches Chapters 3–7. A null validation is reported in
the appendix and cited nowhere.

## 4. Stale-text matrix

**G-rows fire on every branch** (they are about time passing, not
outcomes); track rows fire per branch. "Splice" = Codex mechanical edit
with verbatim oracle; "ADR-gated" = requires its own ADR first.

| # | Location | Trigger | Edit |
|---|---|---|---|
| G1 | `section1_introduction.md` §1.2 ¶2 ("Chapter 7 concludes…") and chapter roadmap | v2 map adoption | Splice: roadmap sentence covers Ch. 7 (new) + Ch. 8 |
| G2 | `section4_diagnosis.md` (and §6.1 recap) | first unseen FTAS wave enters repo | Splice: one vintage-bounding sentence ("waves 2023-04…2026-06") so §4 reads as bounded, not current |
| G3 | `section6_intervention.md` §6.3 "It is a design… not a run experiment" + §6.4 first limitation | Stage 1 closes (already imminent) | Rewrite per Track B branch; tense is stale in *every* branch incl. Band N |
| G4 | `section7_conclusion.md` §7.4 "From design to field" | any Track B branch | Full rewrite as §8.4; v1 text is future-tense about events that will have happened |
| G5 | `thesis_master.md` chapter map, "All seven chapters are written," figure table (new figs 10+), evidence bindings | v2 map adoption | Master updated first; it coordinates every other splice |
| G6 | `section2_data.md` | each new dataset (extended JTA, unseen panel vintage, Kanazawa panel/PDFs, Stage data) | Splice: provenance entries mirroring `source_ledger.md` |
| G7 | `references.md` / §8 back matter | new-chapter citations | Mechanical |
| D1 | §8.3 third limitation (Seam B block) | Track D confirmed or falsified | ADR-gated rewrite per ADR 0020 contract (directional-only: no edit) |
| D2 | §1.2 ¶3 + §8.2 ¶1 canonical claim sentence | Track D confirmed or falsified | ADR-gated; §1 and §8 move together (ADR 0017) |
| D3 | §8.1 fourth finding ("on the pattern-level evidence…") | Track D any verdict | Splice keyed to verdict shape |
| D4 | `section3_impact.md` §3.2/§3.4 | only if S1 shows sign reversal, CI excluding 0 | ADR-gated bounded addendum ("discordant later-wave result"), never a silent edit |
| D5 | §6.2 closing | Track D falsified | One staging sentence forward-referencing §7.2 |
| B1 | §6.3 power/feasibility prose (intercept-only framing) | any positive band | Update to hybrid reality per ADR 0022 (the playbook's §2 fact makes v1's intercept description stale) |
| B2 | §8.1 findings list | Stage 2 run | Add fifth finding (positive, null, or backfire — all listed) |
| B3 | §1.3 "presented as a pre-registered design, explicitly not as evidence" | Stage 2 run | Splice to past-tense truthful form; stays verbatim under Band N |
| T1 | §8.2 exportable-object paragraph | Track T any outcome incl. kill | Add/withhold Kanazawa clause per branch |
| T2 | §6.5 template paragraph | Track T V1 fail only | Soften "the pattern generalizes" to the specified-not-demonstrated form |

Everything not listed is declared **stable by design** — in particular
`section5_robustness.md` (no row touches it) and the §8.3 first/second
limitations except the additive sentences named above.

## 5. Execution discipline

- The Phase 4 integration pass consumes this document top-down: adopt v2
  map in `thesis_master.md` (G5), then G-rows, then the track rows whose
  branches have resolved. Until Phase 4, no chapter file changes — arms
  report into `output/` and ADRs only.
- Every ADR-gated row cites its governing contract (ADR 0020 for D-rows,
  ADR 0018/0022 for B-rows, ADR 0021 for T-rows); the new ADR for a row
  quotes the branch language from §3 verbatim and may tighten it, never
  loosen it.
- Splice rows route to Codex with verbatim-match oracles (the ADR 0016
  §7.3-replacement pattern); ADR-gated rows are drafted by the best
  available seat and reviewed by the human before Codex splices.
- New figures append from Fig. 10 (master rule); Arm 2 gap-extension and
  Arm 3 trajectory figures reserve 10–13 now to avoid renumbering later.
- One coherence rule for the defense: after Phase 4, §7.1 (the frozen
  prediction) must still read as pre-result text — it is quoted evidence
  of ex-ante commitment, and "fixing" its tense after the verdict would
  destroy exactly what makes it valuable.
