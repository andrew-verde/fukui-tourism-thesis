# Results overview: friction impact and nudge design for Fukui tourism

One-page map of the thesis's quantitative arc. All numbers regenerate from the
Makefile targets named in each section; decisions are recorded in
`docs/adr/`, terminology in `CONTEXT.md`.

## The arc

```
IMPACT          MECHANISM            INTERVENTION
Shinkansen DiD  →  Two-stage SEM  →  Nudge priority ranking → nudge-pilot app
(causal shock)     (transmission)     (evidence-weighted)      (built artifact)
```

## 1. Impact: a transport-friction shock changes outcomes (DiD)

`make hokuriku-did-event-study` compares Fukui (treated) with Ishikawa
(control) around the March 2024 Hokuriku Shinkansen extension. It uses merged
tri-prefecture microdata (n≈104k responses, Apr 2023 to present, CC-BY) and
prefecture-by-month clustered standard errors.

| Outcome | DiD (baseline) | Earthquake-robust* | Verdict |
|---|---|---|---|
| NPS (0 to 10) | +0.55 | +0.65 | robust, grows under robustness |
| Transport satisfaction (1 to 5) | +0.05 | +0.08 | robust |
| Revisit intention (1 to 5) | +0.04 | +0.01 | fragile, do not headline |
| Product/service satisfaction | −0.04 | −0.02 | null, placebo-style check |

*Drops January to March 2024 and Noto-area control sites. The event-study plot
and pre-trend diagnostics are in `output/hokuriku_merged/did_event_study_report.md`.
Pre-trends are imperfect: 6 of 20 pre-coefficients are significant at a large
sample size. Report effect magnitudes against the mixed-sign pre-period range
of ±0.1 to 0.4.

## 2. Mechanism: friction transmits to intention via satisfaction (SEM)

`make sem-ftas` uses deduplicated FTAS respondents. The exposure is
`reported_inconvenience`, which the survey asks of every respondent and does
not condition on writing free text.

- CFA: the three satisfaction items form one latent construct (loadings
  .87/.51/.84).
- Stage 1 (n=16,219; CFI .990, RMSEA .044): friction to satisfaction,
  **β = −0.21**; satisfaction to intention, **β = 0.80**; direct friction to
  intention, β = −0.06. Approximately 73% of friction's damage to visit
  intention is mediated through satisfaction.
- Stage 2 (n=2,565 friction reporters with free text; CFI .91): ranks
  friction-type paths below. Conditioning on reporters avoids coding non-writers as
  friction-free.

## 3. Intervention: evidence-weighted nudge ranking

`make nudge-ranking` calculates priority as path × prevalence ×
(satisfaction to intention).

| # | Friction | SEM path | Prevalence | Priority |
|---|----------|----------|------------|----------|
| 1 | Transport / Access | −0.123 | 20.3% | 0.0200 |
| 2 | Opening Hours / Availability | −0.105 | 4.1% | 0.0034 |
| 3 | Food / Amenities Gap | −0.049 | 4.2% | 0.0017 |

Transport/access has a priority about six times the next category. This aligns
with the DiD result: the observable historical friction-reduction shock, the
Shinkansen extension, was a transport intervention and changed NPS.
`output/sem/nudge_priority_ranking.md` lists intervention candidates by code.
`experiments/nudge-pilot/` is an artifact only. See ADR 0002.

## Supporting layers

- JTA accommodation panel: behavioral companion outcome and descriptive demand context.
- Chinese social-media analysis: exploratory side project only; excluded from thesis inference.
- Statistical integrity: the 2026-06 audit fixes (dedup, text-writer
  denominators, reported_inconvenience recode) are locked in by regression
  tests (`tests/test_statistical_validation_official.py`) and CI.
