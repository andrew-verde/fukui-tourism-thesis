# ADR 0016: Limitations chapter placement and pre-emptive framing

Date: 2026-07-03
Status: accepted

## Context

Task 2 of the reasoning queue: convert the residual concessions of the
defense memo (ADR 0015, `docs/thesis/defense_memo.md`) into a limitations
section that names each identification threat first, on the thesis's terms —
a prioritized, disarming account rather than a recital. The brief left
placement open: standalone section file, or fold into §7. The existing §7.3
("Consolidated limitations") is a single-paragraph, chapter-by-chapter
recital — accurate but organized by provenance (Chapter 3's caveat, Chapter
5's caveat, …) rather than by threat severity, and it does not perform the
pre-emption the defense posture calls for.

## Decision

1. **Write the limitations as a standalone drop-in,
   `docs/thesis/section_limitations.md`, designed to replace §7.3 verbatim**
   (retaining the 7.3 number). Standalone-first because the chapters are
   under one-task-at-a-time human review: the replacement text can be
   reviewed against the current §7.3 side by side, and splicing it into
   `section7_conclusion.md` is a mechanical edit that routes to Codex with a
   trivial oracle (§7.3 body equals the new file's section body) once
   approved.

2. **Organize by threat reach, not by chapter**: the three identification
   threats first in ADR 0015's feed-forward order — (A) arrival-mode
   composition, (C) one-sided marginal significance, (B) durability
   small-n bridge — followed by the inherited data-layer limits (earthquake
   control, vendor gaps-not-levels, intercept floors, design-not-evidence)
   in one consolidated block.

3. **Each threat follows a fixed rhetorical contract**: state the objection
   in its strongest form first, in the thesis's own voice; give the bounding
   facts (only committed numbers); end with an explicit "what is conceded /
   what is retained" pair. The closing paragraph inverts the usual apology:
   each limit was absorbed into the design that produced it, and the limits'
   function is to discipline what the thesis is *not* entitled to say.

## Consequences

- §7.3's current text is superseded on acceptance; until spliced, the
  thesis carries both, and the splice is a pending mechanical edit (Codex
  seat) — not to be forgotten before submission.
- The limitations section now depends on the defense memo's analysis; edits
  to defense posture (ADR 0015) should propagate here.
- The ordering commits the thesis to presenting the arrival-mode composition
  residual as its most prominent limitation — deliberate, since it attaches
  to the lead result and pre-empts the most likely defense question.
- Word count grows ~5× over the current §7.3; accepted, as the conclusion
  chapter is otherwise short and the pre-emptive function is the point.

## Rejected alternatives

- **Editing `section7_conclusion.md` directly now**: rejected — bypasses the
  agreed pause-for-review rhythm and mixes a reasoning deliverable with a
  mechanical splice that has a cheaper, checkable route.
- **A separate numbered limitations chapter (e.g., §7 Limitations, pushing
  Conclusion to §8)**: rejected — the thesis's chapter arc ends deliberately
  on design-to-field momentum (§7.4); a free-standing limitations chapter
  after Chapter 6 would interrupt the §4→C→B spine, and before §7.4 it
  reads as a wall between conclusion and outlook. The consolidated-section
  convention (already established by the current §7.3) is kept.
- **Keeping the chapter-by-chapter organization**: rejected — provenance
  ordering is a laundry list by construction; threat-reach ordering is what
  makes the section pre-emptive rather than recitative.
