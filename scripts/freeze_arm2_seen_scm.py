#!/usr/bin/env python3
"""Freeze Arm 2 SCM inputs from the pinned, SEEN 2021-01..2025-12 panel.

This is a pre-registration build tool, not an Arm 2 analysis runner.  It
refuses any month after 2025-12.  Production Arm 2 code loads its outputs and
contains no weight-fitting path.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_causal_arm_summary import (  # noqa: E402
    EVENT_YM,
    HOKURIKU_PREFS,
    fw_scm_sparse,
)

SEEN_END_YM = 202512
TARGET_ITERATIONS = 1000
PLACEBO_ITERATIONS = 400
RMSPE_FIT_MULT = 5.0
GOOD_FIT_RMSPE = 0.15
POSITIVE_WEIGHT_TOL = 0.0

HIGH_CONFIDENCE_CODES = (
    18201, 18202, 18204, 18205, 18207, 18208, 18210,
    18322, 18404, 18423, 18481, 18483, 18501,
)
P1_CODES = (18210, 18322, 18208, 18201, 18202, 18207)

RAW_DIR = ROOT / "output" / "national_stats" / "japan_kanko_stat" / "raw"
CONFIG = ROOT / "config" / "national_data_sources.yaml"
WEIGHTS_CSV = ROOT / "data" / "causal" / "arm2_frozen_scm_weights.csv"
FITS_CSV = ROOT / "data" / "causal" / "arm2_frozen_scm_fits.csv"
METADATA_JSON = ROOT / "data" / "causal" / "arm2_frozen_scm_metadata.json"
FRICTION_SOURCE_CSV = (
    ROOT / "output" / "synthesis" / "synthesis_regime_friction_map.csv"
)
FRICTION_CSV = ROOT / "data" / "causal" / "arm2_frozen_friction_ranking.csv"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_seen_panel() -> pd.DataFrame:
    """Load checksum-pinned local files, refusing non-seen months."""
    config = yaml.safe_load(CONFIG.read_text())["japan_kanko_stat"]
    expected = {item["path"].split("/")[-1]: item for item in config["files"]}
    expected_names = [f"city{year}.csv" for year in range(2021, 2026)]
    if sorted(expected) != expected_names:
        raise AssertionError("Arm 2 freezer requires exactly city2021.csv..city2025.csv")

    frames = []
    for name in expected_names:
        path = RAW_DIR / name
        if not path.is_file():
            raise FileNotFoundError(f"missing pinned seen input: {path}")
        if _sha256(path) != expected[name]["sha256"]:
            raise AssertionError(f"pinned seen checksum mismatch: {name}")
        frame = pd.read_csv(path, encoding="utf-8-sig")
        if len(frame) != expected[name]["rows"]:
            raise AssertionError(f"pinned seen row-count mismatch: {name}")
        frames.append(frame)

    panel = pd.concat(frames, ignore_index=True)
    panel = panel[
        (panel["地域区分"] == "市区町村")
        & (panel["データ区分"] == "観光来訪者数")
    ].copy()
    panel["ym"] = (
        pd.to_numeric(panel["年"]).astype(int) * 100
        + pd.to_numeric(panel["月"]).astype(int)
    )
    for column in ("都道府県コード", "地域コード", "人数"):
        panel[column] = pd.to_numeric(panel[column])
    if panel["ym"].max() > SEEN_END_YM:
        raise AssertionError("SEEN-ONLY FIREWALL: freezer refuses months after 2025-12")
    if panel["ym"].min() != 202101 or panel["ym"].max() != SEEN_END_YM:
        raise AssertionError("seen panel boundary must be 2021-01..2025-12")
    return panel


def build_frozen_artifacts(
    panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit Direction D weights once, using only months through 2024-02."""
    wide = panel.pivot(index="地域コード", columns="ym", values="人数")
    pref_of = (
        panel.drop_duplicates("地域コード")
        .set_index("地域コード")["都道府県コード"]
        .to_dict()
    )
    full = wide.dropna(axis=0, how="any").copy()
    codes = full.index.to_numpy(int)
    donor_codes = codes[
        ~np.isin(np.array([pref_of[code] for code in codes]), HOKURIKU_PREFS)
    ]
    months = sorted(int(month) for month in full.columns)
    pre_months = [month for month in months if month < EVENT_YM]
    if pre_months[-1] != 202402:
        raise AssertionError("SCM fitting must end at 2024-02")
    if not set(HIGH_CONFIDENCE_CODES).issubset(full.index):
        raise AssertionError("13 high-confidence municipalities lack full coverage")

    donor_pre = np.log(full.loc[donor_codes, pre_months].to_numpy(float))
    weight_rows: list[dict] = []
    fit_rows: list[dict] = []

    for code in HIGH_CONFIDENCE_CODES:
        actual = np.log(full.loc[code, pre_months].to_numpy(float))
        weights = fw_scm_sparse(
            donor_pre.T, actual, iters=TARGET_ITERATIONS
        )
        gap = actual - weights @ donor_pre
        fit_rows.append({
            "unit_role": "high_confidence",
            "area_code": int(code),
            "pre_rmspe": float(np.sqrt(np.mean(gap ** 2))),
            "retained_max_gate": False,
            "retained_min_gate": False,
        })
        for donor_code, weight in zip(donor_codes, weights):
            if weight > POSITIVE_WEIGHT_TOL:
                weight_rows.append({
                    "unit_role": "high_confidence",
                    "area_code": int(code),
                    "donor_code": int(donor_code),
                    "weight": float(weight),
                })

    placebo_rmspe: dict[int, float] = {}
    for index, code in enumerate(donor_codes):
        keep = np.ones(len(donor_codes), dtype=bool)
        keep[index] = False
        weights = fw_scm_sparse(
            donor_pre[keep].T,
            donor_pre[index],
            iters=PLACEBO_ITERATIONS,
        )
        gap = donor_pre[index] - weights @ donor_pre[keep]
        placebo_rmspe[int(code)] = float(np.sqrt(np.mean(gap ** 2)))
        for donor_code, weight in zip(donor_codes[keep], weights):
            if weight > POSITIVE_WEIGHT_TOL:
                weight_rows.append({
                    "unit_role": "placebo",
                    "area_code": int(code),
                    "donor_code": int(donor_code),
                    "weight": float(weight),
                })

    target_rmspe = {
        int(row["area_code"]): float(row["pre_rmspe"])
        for row in fit_rows
    }
    max_gate = RMSPE_FIT_MULT * max(target_rmspe[code] for code in P1_CODES)
    min_gate = RMSPE_FIT_MULT * min(target_rmspe[code] for code in P1_CODES)
    if any(
        target_rmspe[code] > GOOD_FIT_RMSPE
        for code in HIGH_CONFIDENCE_CODES
    ):
        raise AssertionError("high-confidence target exceeds pre_rmspe <= 0.15")
    for code in donor_codes:
        rmspe = placebo_rmspe[int(code)]
        fit_rows.append({
            "unit_role": "placebo",
            "area_code": int(code),
            "pre_rmspe": rmspe,
            "retained_max_gate": bool(rmspe <= max_gate),
            "retained_min_gate": bool(rmspe <= min_gate),
        })

    weights = pd.DataFrame(weight_rows).sort_values(
        ["unit_role", "area_code", "donor_code"]
    ).reset_index(drop=True)
    fits = pd.DataFrame(fit_rows).sort_values(
        ["unit_role", "area_code"]
    ).reset_index(drop=True)
    return weights, fits


def main() -> int:
    panel = load_seen_panel()
    weights, fits = build_frozen_artifacts(panel)
    friction_source = pd.read_csv(FRICTION_SOURCE_CSV)
    friction = (
        friction_source.loc[
            friction_source["regime_confidence"].eq("high"),
            ["area_code", "transport_access"],
        ]
        .sort_values("area_code")
        .reset_index(drop=True)
    )
    if tuple(friction["area_code"].astype(int)) != tuple(sorted(HIGH_CONFIDENCE_CODES)):
        raise AssertionError("frozen friction ranking must contain exactly the 13 units")
    friction["friction_rank"] = friction["transport_access"].rank(
        method="average", ascending=True
    )
    WEIGHTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    weights.to_csv(WEIGHTS_CSV, index=False, float_format="%.17g")
    fits.to_csv(FITS_CSV, index=False, float_format="%.17g")
    friction.to_csv(FRICTION_CSV, index=False, float_format="%.17g")
    metadata = {
        "purpose": "Arm 2 frozen SCM inputs built from seen data only; not a result",
        "seen_window": [202101, SEEN_END_YM],
        "fit_window": [202101, 202402],
        "event_ym": EVENT_YM,
        "target_iterations": TARGET_ITERATIONS,
        "placebo_iterations": PLACEBO_ITERATIONS,
        "rmspe_fit_mult": RMSPE_FIT_MULT,
        "good_fit_rmspe": GOOD_FIT_RMSPE,
        "n_high_confidence": len(HIGH_CONFIDENCE_CODES),
        "n_placebo_units": int((fits["unit_role"] == "placebo").sum()),
        "weights_sha256": _sha256(WEIGHTS_CSV),
        "fits_sha256": _sha256(FITS_CSV),
        "friction_ranking_sha256": _sha256(FRICTION_CSV),
    }
    METADATA_JSON.write_text(json.dumps(metadata, indent=2) + "\n")
    print(
        "wrote seen-only frozen SCM artifacts "
        f"({len(weights)} positive weights; no Arm 2 result)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
