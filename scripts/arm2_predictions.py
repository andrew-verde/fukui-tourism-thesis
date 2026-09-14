#!/usr/bin/env python3
"""Frozen Arm 2 predictions and secondary reports.

Production execution accepts only ``GuardedArm2Data`` from
``arm2_quarantine.load_guarded_arm2_data``.  SCM weights and the friction
ranking are loaded frozen inputs; this module has no fitting function.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from arm2_quarantine import (  # noqa: E402
    assert_guarded_arm2_data,
    GuardedArm2Data,
    FrozenScmArtifacts,
    MIN_UNSEEN_MONTHS,
    SEEN_END_YM,
    UNSEEN_START_YM,
    frozen_gap_matrix,
    load_frozen_scm_artifacts,
    load_guarded_arm2_data,
)
from hokuriku_did_event_study import (  # noqa: E402
    AGE_COL,
    DATE_COL,
    GENDER_COL,
    NOTO_PATTERN,
    OUTCOMES,
    PREF_COL,
    RESIDENCE_COL,
    SITE_COL,
    TREATMENT_DATE,
    _age_band,
    run_specifications,
)
from src.official_fukui.ftas import (  # noqa: E402
    load_japanese_codebook,
    normalize_ftas_survey,
    tag_ftas_dataframe,
)

SEED = 202601
N_PARTITIONS = 100_000
PSEUDO_DURABLE_SIZE = 2
PSEUDO_TRANSIENT_SIZE = 4
P1_ALPHA = 0.05
P2_CONFIRMED_RHO = 0.48
RMSPE_FIT_MULT = 5.0
S3_RATIO_FLOOR = 2.0
FTAS_SEEN_END_YM = "2026-06"
JTA_CONFIRMED_SEEN_END_YEAR = 2024
JTA_PRELIMINARY_SEEN_YEAR = 2025
JTA_UNSEEN_CONFIRMED_START_YEAR = 2025

DURABLE_CODES = (18210, 18322)
TRANSIENT_CODES = (18208, 18201, 18202, 18207)
HIGH_CONFIDENCE_CODES = (
    18201, 18202, 18204, 18205, 18207, 18208, 18210,
    18322, 18404, 18423, 18481, 18483, 18501,
)
S1_SPECS = ("baseline", "drop_jan_mar_2024_and_noto")
S1_OUTCOMES = ("nps", "transport_satisfaction")
VISITOR_OTHER_MODES = (
    "transport_to_fukui_private_car",
    "transport_to_fukui_rental_car",
    "transport_to_fukui_local_train",
    "transport_to_fukui_airplane",
    "transport_to_fukui_tour_bus",
)
SHINKANSEN_MODE = "transport_to_fukui_shinkansen"

FRICTION_CSV = ROOT / "data" / "causal" / "arm2_frozen_friction_ranking.csv"
METADATA_JSON = ROOT / "data" / "causal" / "arm2_frozen_scm_metadata.json"
EXPECTED_FRICTION_SHA256 = (
    "1f2d14802960821078d42452417e5d48cc1474797ebcee8036e388fa886e09dc"
)
CODEBOOK = ROOT / "config" / "official_japanese_friction_codebook.yaml"
SEEN_PANEL = ROOT / "output" / "national_stats" / "japan_kanko_stat_panel.csv"
OUT_DIR = ROOT / "output" / "arm2_prediction"
EXPECTED_SEEN_PANEL_SHA256 = (
    "3f0d4ecd8d1d13c59a571024ef967f58e4cffd648656def559d24400bda8e9e5"
)


@dataclass(frozen=True)
class PrimaryResult:
    p1: dict
    p2: dict


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_frozen_friction_ranking() -> pd.DataFrame:
    """Load the 13-unit seen predictor; never estimate it from new FTAS waves."""
    metadata = json.loads(METADATA_JSON.read_text())
    if metadata["friction_ranking_sha256"] != EXPECTED_FRICTION_SHA256:
        raise AssertionError("frozen transport_access metadata moved")
    if _sha256(FRICTION_CSV) != EXPECTED_FRICTION_SHA256:
        raise AssertionError("frozen transport_access ranking checksum mismatch")
    ranking = pd.read_csv(FRICTION_CSV).sort_values("area_code")
    if tuple(ranking["area_code"].astype(int)) != tuple(
        sorted(HIGH_CONFIDENCE_CODES)
    ):
        raise AssertionError("P2 predictor must contain exactly the frozen 13")
    return ranking


def _unit_mean_gaps(
    mobile: pd.DataFrame,
    frozen: FrozenScmArtifacts,
    role: str,
    codes: list[int],
    months: list[int],
    guarded_data: GuardedArm2Data | None = None,
) -> pd.Series:
    gaps = frozen_gap_matrix(
        mobile,
        frozen,
        role,
        codes,
        months,
        guarded_data=guarded_data,
    )
    return gaps.groupby("area_code")["gap_log"].mean()


def draw_p1_null(
    placebo_mean_gaps: np.ndarray,
    *,
    seed: int = SEED,
    draws: int = N_PARTITIONS,
) -> np.ndarray:
    """Frozen 2/4 without-replacement set-difference null."""
    values = np.asarray(placebo_mean_gaps, dtype=float)
    if values.size < PSEUDO_DURABLE_SIZE + PSEUDO_TRANSIENT_SIZE:
        raise ValueError("P1 gated pool needs at least six placebo donors")
    rng = np.random.default_rng(seed)
    null = np.empty(draws, dtype=float)
    for index in range(draws):
        selected = rng.choice(
            values.size,
            size=PSEUDO_DURABLE_SIZE + PSEUDO_TRANSIENT_SIZE,
            replace=False,
        )
        null[index] = (
            values[selected[:PSEUDO_DURABLE_SIZE]].mean()
            - values[selected[PSEUDO_DURABLE_SIZE:]].mean()
        )
    return null


def classify_p1(
    durable_mean_gaps: pd.Series,
    transient_mean_gaps: pd.Series,
    p_value: float,
) -> str:
    observed = float(durable_mean_gaps.mean() - transient_mean_gaps.mean())
    signs_hold = bool((durable_mean_gaps > 0).all() and observed > 0)
    if not signs_hold:
        return "falsified"
    return "confirmed" if p_value <= P1_ALPHA else "directional-only"


def classify_p2(rho: float) -> str:
    if rho >= P2_CONFIRMED_RHO:
        return "confirmed"
    if rho > 0:
        return "directional-only"
    return "falsified"


def assemble_headline_verdict(p1_status: str, p2_status: str) -> str:
    """Both co-primaries are required for the confirmation headline."""
    allowed = {"confirmed", "directional-only", "falsified"}
    if p1_status not in allowed or p2_status not in allowed:
        raise ValueError("unknown primary prediction status")
    if p1_status == p2_status == "confirmed":
        return "prediction confirmed"
    if "falsified" in {p1_status, p2_status}:
        return "prediction falsified"
    if "confirmed" in {p1_status, p2_status}:
        return "partial support"
    return "directional-only"


def _assemble_primary_results(
    treated: pd.Series,
    placebo: pd.Series,
    frozen: FrozenScmArtifacts,
    friction: pd.DataFrame,
) -> PrimaryResult:
    """Inference on already-computed mean gaps; performs no outcome reads."""
    durable = treated.loc[list(DURABLE_CODES)]
    transient = treated.loc[list(TRANSIENT_CODES)]
    observed = float(durable.mean() - transient.mean())

    fits = frozen.fits[frozen.fits["unit_role"] == "placebo"]
    gate_results = {}
    for anchor, column in (
        ("max", "retained_max_gate"),
        ("min", "retained_min_gate"),
    ):
        gated_codes = fits.loc[fits[column], "area_code"].astype(int).tolist()
        null = draw_p1_null(placebo.loc[gated_codes].to_numpy())
        p_value = float(
            (1 + np.sum(null >= observed)) / (1 + N_PARTITIONS)
        )
        gate_results[anchor] = {
            "p_value_one_sided": p_value,
            "n_gated_placebos": len(gated_codes),
        }

    p1 = {
        "status": classify_p1(durable, transient, gate_results["max"]["p_value_one_sided"]),
        "durable_mean_gaps": {
            str(code): float(value) for code, value in durable.items()
        },
        "transient_mean_gaps": {
            str(code): float(value) for code, value in transient.items()
        },
        "observed_durable_minus_transient": observed,
        "primary_max_anchor": gate_results["max"],
        "sensitivity_min_anchor": gate_results["min"],
        "seed": SEED,
        "partitions": N_PARTITIONS,
        "partition_sizes": [PSEUDO_DURABLE_SIZE, PSEUDO_TRANSIENT_SIZE],
        "sidedness": "one-sided",
        "alpha": P1_ALPHA,
    }

    aligned = (
        friction.set_index("area_code")
        .join(treated.rename("unseen_mean_gap"), how="inner")
        .loc[list(HIGH_CONFIDENCE_CODES)]
    )
    rho = float(spearmanr(
        aligned["transport_access"], aligned["unseen_mean_gap"]
    ).statistic)
    if not np.isfinite(rho):
        raise ValueError("P2 Spearman rho is undefined")
    p2 = {
        "status": classify_p2(rho),
        "rho": rho,
        "n": len(aligned),
        "confirmed_threshold": P2_CONFIRMED_RHO,
        "direction": "positive",
    }
    return PrimaryResult(p1=p1, p2=p2)


def _compute_primary_metrics(data: GuardedArm2Data) -> PrimaryResult:
    """Production engine: rerun guard, then and only then compute gaps."""
    assert_guarded_arm2_data(data)
    mobile = data.unseen_mobile
    frozen = data.frozen_scm
    months = sorted(mobile["ym"].astype(int).unique().tolist())
    if (
        len(months) < MIN_UNSEEN_MONTHS
        or months[0] != UNSEEN_START_YM
    ):
        raise ValueError("primary test requires at least six months from 2026-01")
    treated = _unit_mean_gaps(
        mobile,
        frozen,
        "high_confidence",
        list(HIGH_CONFIDENCE_CODES),
        months,
        guarded_data=data,
    )
    fits = frozen.fits[frozen.fits["unit_role"] == "placebo"]
    placebo = _unit_mean_gaps(
        mobile,
        frozen,
        "placebo",
        fits["area_code"].astype(int).tolist(),
        months,
        guarded_data=data,
    )
    return _assemble_primary_results(
        treated,
        placebo,
        frozen,
        load_frozen_friction_ranking(),
    )


def compute_guarded_primaries(data: GuardedArm2Data) -> PrimaryResult:
    """The only production entry point to an unseen-window gap computation."""
    return _compute_primary_metrics(data)


def prepare_s1_full_extended_sample(raw: pd.DataFrame) -> pd.DataFrame:
    """Prepare the Chapter 3 full-sample DiD without any new-waves-only path."""
    required = {
        PREF_COL, DATE_COL, SITE_COL, RESIDENCE_COL, GENDER_COL, AGE_COL,
        *OUTCOMES.values(),
    }
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"S1 merged survey missing columns: {sorted(missing)}")
    df = raw.copy()
    df["prefecture"] = df[PREF_COL].map({"福井": "Fukui", "石川": "Ishikawa"})
    df = df.dropna(subset=["prefecture"])
    df["response_date"] = pd.to_datetime(df[DATE_COL], errors="coerce")
    df = df.dropna(subset=["response_date"])
    if (
        df["response_date"].min() > pd.Timestamp("2023-12-31")
        or df["response_date"].max() <= pd.Timestamp("2026-06-30")
    ):
        raise ValueError("S1 requires all seen waves plus waves after 2026-06")
    df["transport_satisfaction"] = pd.to_numeric(
        df["交通の満足度"], errors="coerce"
    )
    df["product_service_sat"] = pd.to_numeric(
        df["満足度（商品・サービス）"], errors="coerce"
    )
    df["nps"] = pd.to_numeric(df["おすすめ度"], errors="coerce").where(
        lambda values: values.between(0, 10)
    )
    revisit_map = {
        "また行きたい（1年以内）": 5,
        "また行きたい（１年以内）": 5,
        "機会があれば行きたい": 4,
        "どちらともいえない": 3,
        "あまり行きたいと思わない": 2,
        "行きたくない": 1,
    }
    df["revisit_intent"] = df["再訪意向"].map(revisit_map)
    df["month"] = df["response_date"].dt.to_period("M").astype(str)
    df["post"] = (df["response_date"] >= TREATMENT_DATE).astype(int)
    df["treated"] = (df["prefecture"] == "Fukui").astype(int)
    df["cluster"] = df["prefecture"] + "_" + df["month"]
    home_pref = {"Fukui": "福井県", "Ishikawa": "石川県"}
    df["local_resident"] = (
        df[RESIDENCE_COL].astype(str).str.strip()
        == df["prefecture"].map(home_pref)
    ).astype(int)
    df["gender"] = df[GENDER_COL].astype(str).str.strip().where(
        df[GENDER_COL].astype(str).str.strip().isin(["男", "女"]),
        "other_or_na",
    )
    df["age_band"] = df[AGE_COL].apply(_age_band).fillna("unknown")
    df["noto_site"] = df[SITE_COL].astype(str).str.contains(
        NOTO_PATTERN, na=False, regex=True
    )
    return df


def assess_s1(estimates: pd.DataFrame) -> dict:
    """Apply ADR 0025's met / discordant / middle bands."""
    selected = estimates[
        estimates["spec"].isin(S1_SPECS)
        & estimates["outcome"].isin(S1_OUTCOMES)
    ].copy()
    expected = {(spec, outcome) for spec in S1_SPECS for outcome in S1_OUTCOMES}
    actual = set(zip(selected["spec"], selected["outcome"]))
    if actual != expected:
        raise ValueError("S1 requires NPS and transport satisfaction in both frozen specs")
    discordant = (
        (selected["estimate"] < 0)
        & (selected["ci_high"] < 0)
    ).any()
    if discordant:
        status = "discordant"
    elif (selected["estimate"] >= 0).all():
        status = "prediction met"
    else:
        status = "not confirmed, not discordant"
    return {
        "status": status,
        "analysis_status": "exploratory",
        "secondary_only": True,
        "specifications": list(S1_SPECS),
        "estimates": selected.to_dict(orient="records"),
    }


def build_s2_descriptive_report(jta: pd.DataFrame) -> dict:
    """Return descriptive Fukui event-study inputs; ADR 0020 freezes no cutoff."""
    required = {"pref_code", "year", "month", "total_stays", "vintage"}
    if missing := required - set(jta.columns):
        raise ValueError(f"S2 JTA panel missing columns: {sorted(missing)}")
    fukui = jta[jta["pref_code"].astype(str).str.zfill(2) == "18"].copy()
    fukui["year"] = fukui["year"].astype(int)
    fukui["month"] = fukui["month"].astype(int)
    vintage = fukui["vintage"].astype(str).str.lower()
    for year in range(2018, JTA_CONFIRMED_SEEN_END_YEAR + 1):
        months = set(
            fukui.loc[
                (fukui["year"] == year) & vintage.eq("confirmed"),
                "month",
            ]
        )
        if months != set(range(1, 13)):
            raise ValueError(f"S2 requires complete confirmed JTA year {year}")
    confirmed_2025 = fukui[
        (fukui["year"] == JTA_UNSEEN_CONFIRMED_START_YEAR)
        & vintage.eq("confirmed")
    ]
    if set(confirmed_2025["month"]) != set(range(1, 13)):
        raise ValueError("S2 requires 2025 confirmed values")
    if not (fukui["year"] >= 2026).any():
        raise ValueError("S2 requires at least one 2026 JTA row")
    fukui["ym"] = fukui["year"].astype(int) * 100 + fukui["month"].astype(int)
    series = fukui.sort_values("ym")[
        ["ym", "total_stays", "vintage"]
    ].to_dict(orient="records")
    return {
        "status": "descriptive only",
        "secondary_only": True,
        "gates_nothing": True,
        "series": series,
    }


def assess_s3(ftas_raw: pd.DataFrame) -> dict:
    """Assess unseen FTAS friction using shinkansen versus pooled other modes."""
    normalized = normalize_ftas_survey(ftas_raw)
    codebook = load_japanese_codebook(CODEBOOK)
    tagged = tag_ftas_dataframe(normalized, "friction_source_text", codebook)
    unseen = tagged[tagged["response_year_month"] > FTAS_SEEN_END_YM].copy()
    if unseen.empty:
        raise ValueError("S3 requires FTAS waves after 2026-06")
    modes = (SHINKANSEN_MODE, *VISITOR_OTHER_MODES)
    if missing := set(modes) - set(unseen.columns):
        raise ValueError(f"S3 missing arrival-mode columns: {sorted(missing)}")

    rows = []
    for mode in modes:
        group = unseen[unseen[mode].eq(True)]
        for code in codebook:
            rows.append({
                "mode": mode,
                "friction_code": code,
                "count": int(group[code].sum()),
                "n": len(group),
            })
    counts = pd.DataFrame(rows)
    shinkansen = counts[counts["mode"] == SHINKANSEN_MODE].set_index(
        "friction_code"
    )
    pooled = (
        counts[counts["mode"].isin(VISITOR_OTHER_MODES)]
        .groupby("friction_code")
        .agg(count=("count", "sum"), n=("n", "sum"))
    )
    shinkansen_pct = 100 * shinkansen["count"] / shinkansen["n"]
    pooled_pct = 100 * pooled["count"] / pooled["n"]
    if (
        shinkansen.loc["transport_access", "n"] == 0
        or pooled.loc["transport_access", "n"] == 0
        or pooled_pct["transport_access"] <= 0
    ):
        raise ValueError("S3 pooled-other comparison is not estimable")
    transport_ratio = float(
        shinkansen_pct["transport_access"] / pooled_pct["transport_access"]
    )
    maximum = float(shinkansen_pct.max())
    argmax_codes = sorted(
        shinkansen_pct.index[
            np.isclose(shinkansen_pct.to_numpy(float), maximum, rtol=0, atol=0)
        ].tolist()
    )
    met = (
        "transport_access" in argmax_codes
        and transport_ratio > S3_RATIO_FLOOR
    )
    return {
        "status": "prediction met" if met else "not met",
        "analysis_status": "exploratory",
        "secondary_only": True,
        "argmax_shinkansen_friction": argmax_codes,
        "transport_access_shinkansen_pct": float(
            shinkansen_pct["transport_access"]
        ),
        "transport_access_pooled_other_pct": float(
            pooled_pct["transport_access"]
        ),
        "shinkansen_over_pooled_other_ratio": transport_ratio,
        "ratio_floor_strictly_greater_than": S3_RATIO_FLOOR,
        "denominator": "pooled other arrival modes",
    }


def analyze_guarded(data: GuardedArm2Data) -> dict:
    assert_guarded_arm2_data(data)
    primary = compute_guarded_primaries(data)
    s1_estimates = run_specifications(
        prepare_s1_full_extended_sample(data.merged_raw)
    )
    result = {
        "guard": data.guard_report,
        "analysis_status": "exploratory",
        "confirmatory_claim_permitted": False,
        "protocol_deviation_adr": "0039",
        "headline_verdict_status": "exploratory classification",
        "windows": {
            "mobile_seen_end": SEEN_END_YM,
            "mobile_unseen_start": UNSEEN_START_YM,
            "ftas_seen_end": FTAS_SEEN_END_YM,
            "jta_confirmed_seen_end_year": JTA_CONFIRMED_SEEN_END_YEAR,
            "jta_preliminary_seen_year": JTA_PRELIMINARY_SEEN_YEAR,
            "jta_unseen_confirmed_start_year": (
                JTA_UNSEEN_CONFIRMED_START_YEAR
            ),
        },
        "P1": primary.p1,
        "P2": primary.p2,
        "S1": assess_s1(s1_estimates),
        "S2": build_s2_descriptive_report(data.jta_panel),
        "S3": assess_s3(data.ftas_raw),
    }
    result["headline_verdict"] = assemble_headline_verdict(
        primary.p1["status"], primary.p2["status"]
    )
    result["P1"]["analysis_status"] = "exploratory"
    result["P2"]["analysis_status"] = "exploratory"
    return result


def exercise_seen_mobile_fixture_only() -> dict:
    """Exercise parallel seen-only machinery and discard every result field."""
    if _sha256(SEEN_PANEL) != EXPECTED_SEEN_PANEL_SHA256:
        raise AssertionError("held-out seen fixture panel checksum mismatch")
    panel = pd.read_csv(SEEN_PANEL)
    months = [202507, 202508, 202509, 202510, 202511, 202512]
    fixture_panel = panel[panel["ym"].isin(months)].copy()
    frozen = load_frozen_scm_artifacts()
    treated = _unit_mean_gaps(
        fixture_panel,
        frozen,
        "high_confidence",
        list(HIGH_CONFIDENCE_CODES),
        months,
    )
    fits = frozen.fits[frozen.fits["unit_role"] == "placebo"]
    placebo = _unit_mean_gaps(
        fixture_panel,
        frozen,
        "placebo",
        fits["area_code"].astype(int).tolist(),
        months,
    )
    _assemble_primary_results(
        treated,
        placebo,
        frozen,
        load_frozen_friction_ranking(),
    )
    return {
        "fixture_only": True,
        "source": "held-out slice of seen 2021-01..2025-12 mobile panel",
        "produces_arm2_verdict": False,
        "headline_verdict": None,
        "months_exercised": len(months),
        "partitions_exercised": N_PARTITIONS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    guarded = load_guarded_arm2_data()
    result = analyze_guarded(guarded)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "arm2_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(f"wrote {args.out_dir / 'arm2_results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
