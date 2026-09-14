# ADR 0037: Reconcile the frozen FTAS population by row identity

Date: 2026-09-14
Status: superseded by ADR 0038 on 2026-09-14

## Context

The Arm 2 FTAS assembler required the current `merged_survey_2026.csv` to
start with the committed June 2026 file byte for byte. The first authorized
production attempt showed that the upstream merge pipeline rebuilds the file
rather than appending bytes. The current file failed the prefix guard, and a
metadata-only audit found that every archived daily release checked from
2026-06-12 onward also failed it. The audit compared file sizes, hashes, and
byte prefixes only. It did not decode or inspect any outcome row, and the Arm
2 production entry point did not run.

The byte-prefix rule therefore cannot admit a real post-June upstream
release. It is stricter than the scientific boundary it was meant to protect:
the committed respondents and their values must remain unchanged, but their
physical row positions carry no meaning.

## Decision

The gateway will reconcile the committed June population against the current
file by exact row identity across every column, without assuming row order.
Each committed row must occur in the current file with the same values and
multiplicity. A missing or changed committed row stops the run. Rows left
after that match are candidate additions. Their response dates must not
precede 2026-06-30, exact duplicate additions stop the run, the 2026-06-30
seam is excluded, and only rows after 2026-06-30 enter the unseen FTAS
window.

The assembler may copy a larger operator-supplied file into quarantine after
checksum-pinning it. The frozen gateway remains the authority that decodes
the file and performs the identity, date, and duplicate checks. It constructs
the analytical 2026 wave as the committed frozen population followed by the
validated post-June additions. The raw upstream file remains separate and
unchanged.

This changes the input plumbing for S1 and S3, so they are reported as
exploratory secondary checks. It does not change P1 or P2. Their mobile data,
frozen weights, predictions, thresholds, and inference remain exactly as
accepted in ADR 0020, so the Arm 2 headline verdict remains confirmatory. S2
and its ADR 0036 disclosure are also unchanged.

## Rejected alternatives

- Treat the rebuilt file as an append. This would silently mix revised and
  frozen respondents.
- Manufacture a byte-prefix file without validating row identity. This would
  make the original guard appear to pass without establishing its premise.
- Skip the FTAS checks inside the existing production entry point. That would
  change the frozen report contract and leave an unexplained missing leg.
- Demote P1 and P2. The discovered incompatibility is confined to the FTAS
  secondary inputs and does not touch either primary analysis.
