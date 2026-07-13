# SEM Intervention Simulator

Open `index.html` directly in a browser; there is no build step and no external
JavaScript dependency.

Regenerate the data bundle from the non-survey panel and SEM coefficients:

```sh
.venv/bin/python3 experiments/sim-webapp/build_webapp_data.py \
  --panel data/nonsurvey/ \
  --sem output/sem/nonsurvey/coefficients.json
```

The app shows scenarios, not measured intervention effects. Baselines are real
panel values; simulated deltas propagate hypothetical changes through the SEM
path and observed Awara weekly elasticity anchor pending field validation.
