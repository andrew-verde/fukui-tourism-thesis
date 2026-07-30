#!/usr/bin/env python3
"""Seen-only Arm 2 revision-guard rehearsal."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import arm2_quarantine

GUARD_FAILURE_INSTRUCTION = (
    "Stop; write a deviation ADR choosing between re-running the whole "
    "Direction D + Arm 2 chain on the revised vintage, or demoting Arm 2 "
    "to exploratory; mixing vintages is forbidden."
)
NO_UNSEEN_CLOSING = (
    "No unseen outcome value was decoded and the pre-specification option "
    "is unspent."
)


def _build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        description=(
            "Run the Arm 2 revision guard on revised seen mobile history "
            "without decoding any unseen outcome value."
        )
    )


def _seen_months() -> list[int]:
    months = []
    for year in range(2021, 2026):
        months.extend(year * 100 + month for month in range(1, 13))
    return months


def _pre_event_months() -> list[int]:
    return [month for month in _seen_months() if month < arm2_quarantine.EVENT_YM]


def _pivot_mobile(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.pivot(index="地域コード", columns="ym", values="人数")


def _compute_rms_relative_revisions(
    revised_seen: pd.DataFrame,
    pinned_seen: pd.DataFrame,
) -> dict[int, float]:
    months = _seen_months()
    revised_wide = _pivot_mobile(revised_seen)
    pinned_wide = _pivot_mobile(pinned_seen)
    revisions = {}
    for code in arm2_quarantine.HIGH_CONFIDENCE_CODES:
        new = revised_wide.loc[code, months].to_numpy(float)
        old = pinned_wide.loc[code, months].to_numpy(float)
        revisions[int(code)] = float(np.sqrt(np.mean(((new - old) / old) ** 2)))
    return revisions


def _fit_rmspe(
    revised_wide: pd.DataFrame,
    weights: pd.DataFrame,
    code: int,
    months: list[int],
) -> float:
    unit_weights = weights[weights["area_code"] == code]
    donor_codes = unit_weights["donor_code"].astype(int).to_numpy()
    actual = revised_wide.loc[code, months].to_numpy(float)
    donor_values = revised_wide.loc[donor_codes, months].to_numpy(float)
    weight_values = unit_weights["weight"].to_numpy(float)
    if (
        unit_weights.empty
        or not np.isfinite(actual).all()
        or not np.isfinite(donor_values).all()
        or not np.isfinite(weight_values).all()
        or (actual <= 0).any()
        or (donor_values <= 0).any()
        or not np.isclose(weight_values.sum(), 1.0, rtol=0, atol=1e-12)
    ):
        raise ValueError(f"incomplete frozen fit inputs for {code}")
    gaps = np.log(actual) - (weight_values @ np.log(donor_values))
    return float(np.sqrt(np.mean(gaps ** 2)))


def _compute_fit_gate_exits(
    revised_seen: pd.DataFrame,
    frozen: arm2_quarantine.FrozenScmArtifacts,
) -> dict[str, list[int]]:
    revised_wide = _pivot_mobile(revised_seen)
    pre_months = _pre_event_months()

    target_weights = frozen.weights[frozen.weights["unit_role"] == "high_confidence"]
    target_rmspe = {
        int(code): _fit_rmspe(revised_wide, target_weights, int(code), pre_months)
        for code in arm2_quarantine.P1_CODES
    }
    max_limit = arm2_quarantine.RMSPE_FIT_MULT * max(target_rmspe.values())
    min_limit = arm2_quarantine.RMSPE_FIT_MULT * min(target_rmspe.values())

    placebo_fits = frozen.fits[frozen.fits["unit_role"] == "placebo"]
    retained_max = [
        int(code)
        for code in placebo_fits.loc[
            placebo_fits["retained_max_gate"], "area_code"
        ].tolist()
    ]
    retained_min = [
        int(code)
        for code in placebo_fits.loc[
            placebo_fits["retained_min_gate"], "area_code"
        ].tolist()
    ]
    retained_union = sorted(set(retained_max) | set(retained_min))
    placebo_weights = frozen.weights[frozen.weights["unit_role"] == "placebo"]
    revised_rmspe = {
        code: _fit_rmspe(revised_wide, placebo_weights, code, pre_months)
        for code in retained_union
    }
    return {
        "max_gate": [code for code in retained_max if revised_rmspe[code] > max_limit],
        "min_gate": [code for code in retained_min if revised_rmspe[code] > min_limit],
    }


def _print_revision_report(revisions: dict[int, float]) -> None:
    limit = arm2_quarantine.REVISION_RMS_RELATIVE_LIMIT
    print("RMS relative revisions (limit 0.02):")
    for code in arm2_quarantine.HIGH_CONFIDENCE_CODES:
        value = revisions[int(code)]
        status = "pass" if value <= limit else "fail"
        print(f"  {code}: {value:.6f} ({status})")


def _print_fit_gate_report(fit_gate_exits: dict[str, list[int]]) -> None:
    max_gate = ", ".join(str(code) for code in fit_gate_exits["max_gate"]) or "none"
    min_gate = ", ".join(str(code) for code in fit_gate_exits["min_gate"]) or "none"
    print(f"Donor exits max-anchor gate: {max_gate}")
    print(f"Donor exits min-anchor gate: {min_gate}")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parser.parse_args(argv)

    try:
        manifest = arm2_quarantine._load_mobile_vintage_manifest()
        revised_seen = arm2_quarantine._load_quarantine_mobile_history(manifest)
        pinned_seen = arm2_quarantine._load_pinned_mobile_history()
        frozen = arm2_quarantine.load_frozen_scm_artifacts()
        revisions = _compute_rms_relative_revisions(revised_seen, pinned_seen)
        fit_gate_exits = _compute_fit_gate_exits(revised_seen, frozen)
        arm2_quarantine._run_revision_guard(revised_seen, pinned_seen, frozen)
    except arm2_quarantine.RevisionGuardError as exc:
        print("Guard result: fail")
        _print_revision_report(revisions)
        _print_fit_gate_report(fit_gate_exits)
        print(f"Guard detail: {exc}")
        print(GUARD_FAILURE_INSTRUCTION)
        print(NO_UNSEEN_CLOSING)
        return 1
    except (FileNotFoundError, ValueError, AssertionError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print("Guard result: pass")
    _print_revision_report(revisions)
    _print_fit_gate_report(fit_gate_exits)
    print(f"Vintage commit: {manifest['commit']}")
    print(NO_UNSEEN_CLOSING)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
