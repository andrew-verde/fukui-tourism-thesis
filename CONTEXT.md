# Domain context

## Thesis question

How did the March 2024 Hokuriku Shinkansen extension affect tourism outcomes
in Fukui, which frictions shape satisfaction and revisit intent, and which
interventions should be prioritized?

## Evidence layers

**Official FTAS layer.** Fukui Tourism Area Survey respondent microdata.
Primary mechanism evidence and SEM input.

**Official comparison layer.** Ishikawa tourism survey data normalized to
shared respondent-level friction indicators.

**Hokuriku impact layer.** Merged Fukui/Ishikawa/Toyama official survey
microdata used for DiD and event-study analysis.

**Accommodation layer.** JTA prefecture-month overnight stays used as
behavioral context.

**Chinese social-media side layer.** Exploratory recommendation-text
analysis. Never thesis inferential evidence.

## Canonical terms

**Friction.** An obstacle reported in official free text or a structured response.

**Friction tag.** Reproducible keyword-based measurement from `src/friction`.
Tag validity is bounded by codebook coverage and manual audit; tag is not
ground truth.

**Respondent.** A deduplicated survey participant. Repeat-response handling must
remain explicit.

**Response row.** A raw survey submission before respondent deduplication.

**Treatment.** Fukui after March 2024 in Shinkansen impact models.

**Control.** Comparison observations specified by each DiD model. Never imply
untreated status beyond model definition.

**Nudge priority.** Intervention score combining SEM path evidence with
official-survey friction prevalence.

## Guardrails

- Keep official datasets separate until an analysis defines a valid join.
- Preserve respondent-level denominators.
- Report effect sizes and uncertainty, not significance alone.
- Do not infer nationality from language.
- Keep exploratory side-project outputs outside thesis causal claims.
