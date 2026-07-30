# ADR 0030: Arm 3 implementation corrections — pre-window month count, Hagibis mask scope, V3 anchor series

Date: 2026-07-30
Status: accepted 2026-07-30 (corrects ADR 0021 / `arm3_kanazawa_design.md`; no analytic demotion)

## Context

ADR 0021 was accepted 2026-07-29 and Arm 3 implementation began the same
day. The implementation halted before any causal computation on three
discrepancies between the frozen design and the data actually available.
No outcome data was loaded and no SCM result was produced, so nothing
downstream of these decisions has been contaminated by seeing results.

Full detail: `docs/arm3_implementation_report.md`.

Two of the three are not deviations at all — the design's own language
anticipated them and delegated the resolution to implementation. Only
the first is a correction to frozen text. **None of the three changes an
analytic specification, so no analysis is demoted to exploratory.**

## Decision

### 1. The sensitivity pre-window is 50 months, not 49 (correction)

`arm3_kanazawa_design.md` states the sensitivity pre-window as
`2011-01..2015-02 (49 months)` at lines 90, 150, and 185. The inclusive
span is **50 months**. The count is wrong; the boundaries are right.

Both boundaries are externally determined and are **not** changed:
2011-01 is the earliest consistent post-frame-break month (data audit §1
verdict) and 2015-02 is the month before `EVENT_YM = 201503`. Moving a
boundary to manufacture 49 would discard a month of pre-period for no
substantive reason and would contradict the audit finding.

**Resolution:** correct the three occurrences of "49 months" to "50
months". The primary pre-window `2012-01..2015-02 (38 months)` is
verified correct and is untouched, as is every other constant in the
§4 table.

### 2. Hagibis mask: primary = 2019-10, sensitivity = 2019-10..12

`arm3_kanazawa_design.md:189` masks `2019-10..12` for Typhoon Hagibis and
annotates it "to be date-verified by Codex during implementation — it
postdates the audit's event table". That is a pre-granted license to set
the window from the verification; this ADR records the outcome rather
than amending a frozen decision.

Verification (JMA, `ds.data.jma.go.jp/stats/data/bosai/report/2019/20191012/`):
Hagibis affected Japan **2019-10-10 to 2019-10-13**, landfall 10-12. The
event is contained in October. The written `2019-10..12` window is
therefore over-inclusive as an *event* mask, though defensible as a
*recovery* mask — the design does not say which it intended.

This matters: the mask falls inside the late window `2018-01..2019-12`
(24 months), which carries **V2a**, the durability test supporting the
ADR 0017 durable-where-anchored clause. Masking three months removes
12.5% of that test window; masking one removes 4.2%.

**Resolution:** run both, pre-declared before results exist.

- **Primary:** mask `2019-10` only — the verified event month.
- **Sensitivity:** mask `2019-10..12` — the recovery-window reading, as
  originally written.

V2a's verdict is reported under the primary mask. If the two masks
disagree on V2a, that disagreement is reported as a first-class result,
never resolved by picking the friendlier one. Both are fixed here, in
advance, precisely so that choice cannot be made post hoc.

### 3. V3 anchor uses the 19-facility aggregate

`arm3_kanazawa_design.md:217` specifies the V3 anchor as "Kanazawa
monthly lodging and **Kenrokuen/19-facility** series … on the 2014–2019
windows **the PDFs support**". Extraction found the specified PDFs
support monthly Kenrokuen data only from 2017 — not the 2015 opening
window. The 19-facility aggregate covers the full 2014–2019 span.

The frozen text names the 19-facility series as an alternative and
explicitly bounds the claim to what the PDFs support. This is the
anticipated branch, not a substitution.

**Resolution:** V3 uses Kanazawa monthly lodging (unaffected, full
window) plus the 19-facility aggregate. The Kenrokuen-specific
single-site series is dropped from V3 and its 2017+ availability noted in
the implementation report. No search for an alternative Kenrokuen source
is commissioned.

V3 is "descriptive only, never confirmatory" (`:215`); no V1 or V2
criterion depends on it, and the interpretation contract in §6 is
unchanged.

## Consequences

- Arm 3 is unblocked and may proceed to the full battery.
- No analytic specification changed; no analysis is demoted to
  exploratory. Item 1 is a counting correction, items 2 and 3 are
  resolutions the design delegated to implementation.
- The dual Hagibis mask adds one sensitivity run to the battery and one
  reporting obligation to §6 interpretation.
- V3's anchor claim is slightly broader than single-site (19 facilities
  rather than Kenrokuen alone) and correspondingly less vivid as a
  narrative hook. Accepted: the alternative was an uncommissioned source
  hunt for a layer that cannot affect the verdict.
- All three decisions were made and recorded **before any outcome data
  was loaded or any gap computed**, preserving the pre-specification
  discipline ADR 0021 and ADR 0020 depend on.

## Deviation discipline

Post-acceptance deviations from this ADR require a new ADR and demote
the affected analysis to exploratory, per ADR 0019.
