# ADR 0027: Scope boundary for the non-survey behavioral evidence engine

Date: 2026-07-09
Status: accepted

## Context

The thesis reframe adds a non-survey panel, an extended SEM, an opportunity
scan, and a simulation app. These are observational. There is a real risk that
a reader, or a future refactor, treats a correlation or a simulated scenario as
a measured causal intervention effect.

## Decision

The non-survey evidence engine identifies, prioritizes, and effect-bounds
physical-intervention opportunities. It does NOT estimate causal intervention
effects. Specifically:

1. **The Shinkansen natural experiment is estimated only from the multi-year arrivals/accommodation series** (existing repo scripts), NOT from the new reservation panels — those start Oct 2023 and have no seasonally comparable pre-extension window. A naive pre/post on the new panels is a documented seasonal artifact (`opportunity_signals.json` -> `S5_shinkansen_NOT_identifiable_here`).
2. **The SEM structural path (0.17) is associational.** It justifies the path's existence, sign, and rough magnitude; it is not a causal effect of intent on demand.
3. **Simulation outputs are scenarios.** They propagate a hypothetical physical change through fitted path coefficients and one observed elasticity anchor (Awara weekly directions->stays, beta ~= 0.13). Every output is visibly labeled a scenario pending field validation.
4. **The causal claim requires the pre-registered field trial** (nudge-pilot app + power calculation, already in the repo), which becomes the explicit Arm 2/3 future work.

## Consequences

- The thesis is defensible today with data in hand: the contribution is the
  evidence engine plus opportunity identification, not a completed experiment.
- The untestable field trial becomes a pre-registered next step rather than a
  missing result.
- The thesis cannot claim a proven intervention effect. Reviewers must
  understand the current result as observational prioritization and scenario
  bounding pending field validation.

## Rejected Alternatives

- **Treat the reservation-panel Shinkansen break as causal evidence.** Rejected
  because the panels start in October 2023 and have no seasonally comparable
  pre-extension window.
- **Present the SEM path as an effect estimate.** Rejected because the fitted
  path is associational and pooled across heterogeneous sites.
- **Hide scenario caveats in prose only.** Rejected because the webapp is a
  decision surface; the scenario label must be visible wherever simulated
  outputs appear.
