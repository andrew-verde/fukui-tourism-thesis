"""Frozen scientific-contract oracles for Arm 2 (seen data only)."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS = ROOT / "scripts" / "arm2_predictions.py"
QUARANTINE = ROOT / "scripts" / "arm2_quarantine.py"


def _load(path: Path, name: str):
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def producer():
    return _load(PREDICTIONS, "arm2_predictions_test")


@pytest.fixture(scope="module")
def gateway():
    return _load(QUARANTINE, "arm2_quarantine_test")


def test_frozen_windows_populations_thresholds_and_sidedness(
    producer, gateway
) -> None:
    assert gateway.SEEN_START_YM == 202101
    assert gateway.SEEN_END_YM == 202512
    assert gateway.UNSEEN_START_YM == 202601
    assert gateway.EVENT_YM == 202403
    assert gateway.MIN_UNSEEN_MONTHS == 6
    assert gateway.REVISION_RMS_RELATIVE_LIMIT == 0.02
    assert gateway.RMSPE_FIT_MULT == 5.0
    assert gateway.GOOD_FIT_RMSPE == 0.15
    assert producer.FTAS_SEEN_END_YM == "2026-06"
    assert producer.JTA_CONFIRMED_SEEN_END_YEAR == 2024
    assert producer.JTA_PRELIMINARY_SEEN_YEAR == 2025
    assert producer.JTA_UNSEEN_CONFIRMED_START_YEAR == 2025
    assert producer.DURABLE_CODES == (18210, 18322)
    assert producer.TRANSIENT_CODES == (18208, 18201, 18202, 18207)
    assert producer.HIGH_CONFIDENCE_CODES == (
        18201, 18202, 18204, 18205, 18207, 18208, 18210,
        18322, 18404, 18423, 18481, 18483, 18501,
    )
    assert producer.P1_ALPHA == 0.05
    assert producer.P2_CONFIRMED_RHO == 0.48
    assert producer.S3_RATIO_FLOOR == 2.0
    assert producer.S1_SPECS == (
        "baseline",
        "drop_jan_mar_2024_and_noto",
    )
    assert producer.S1_OUTCOMES == ("nps", "transport_satisfaction")
    assert "0.826" not in PREDICTIONS.read_text()
    assert "10.74" not in PREDICTIONS.read_text()


def test_p1_partition_oracle_and_seeded_without_replacement(producer) -> None:
    assert producer.SEED == 202601
    assert producer.N_PARTITIONS == 100_000
    assert producer.PSEUDO_DURABLE_SIZE == 2
    assert producer.PSEUDO_TRANSIENT_SIZE == 4
    assert "replace=False" in PREDICTIONS.read_text()
    values = np.arange(8, dtype=float)
    first = producer.draw_p1_null(values, seed=202601, draws=20)
    second = producer.draw_p1_null(values, seed=202601, draws=20)
    assert np.array_equal(first, second)
    assert len(first) == 20


def test_max_gate_is_primary_and_min_gate_is_sensitivity(producer) -> None:
    source = PREDICTIONS.read_text()
    assert '("max", "retained_max_gate")' in source
    assert '("min", "retained_min_gate")' in source
    assert '"primary_max_anchor": gate_results["max"]' in source
    assert '"sensitivity_min_anchor": gate_results["min"]' in source
    assert "(1 + np.sum(null >= observed)) / (1 + N_PARTITIONS)" in source
    frozen = producer.load_frozen_scm_artifacts()
    fits = frozen.fits
    high = fits.set_index(["unit_role", "area_code"])
    p1_rmspe = [
        high.loc[("high_confidence", code), "pre_rmspe"]
        for code in (*producer.DURABLE_CODES, *producer.TRANSIENT_CODES)
    ]
    placebos = fits[fits["unit_role"] == "placebo"]
    assert np.array_equal(
        placebos["retained_max_gate"].to_numpy(),
        (
            placebos["pre_rmspe"]
            <= producer.RMSPE_FIT_MULT * max(p1_rmspe)
        ).to_numpy(),
    )
    assert np.array_equal(
        placebos["retained_min_gate"].to_numpy(),
        (
            placebos["pre_rmspe"]
            <= producer.RMSPE_FIT_MULT * min(p1_rmspe)
        ).to_numpy(),
    )


def test_frozen_weights_are_loaded_and_never_refit_in_production(
    producer, gateway
) -> None:
    source = PREDICTIONS.read_text()
    quarantine_source = QUARANTINE.read_text()
    assert "load_frozen_scm_artifacts" in source
    assert "fw_scm_sparse" not in source
    assert "fit_convex_weights" not in source
    assert "fw_scm_sparse" not in quarantine_source
    assert gateway.EXPECTED_WEIGHTS_SHA256 == (
        "824761cd7412a738764f4fc206bccd57f479283e0ad0eb85db0620c59a9bfaa3"
    )
    assert gateway.EXPECTED_FITS_SHA256 == (
        "5a6fbbdefd1632abdf514293cd6b97d1fd53452ee319fd455efcab253f950147"
    )
    assert producer.EXPECTED_FRICTION_SHA256 == (
        "1f2d14802960821078d42452417e5d48cc1474797ebcee8036e388fa886e09dc"
    )
    frozen = producer.load_frozen_scm_artifacts()
    high = frozen.fits[frozen.fits["unit_role"] == "high_confidence"]
    assert set(high["area_code"]) == set(producer.HIGH_CONFIDENCE_CODES)
    assert (high["pre_rmspe"] <= 0.15).all()
    sums = (
        frozen.weights.groupby(["unit_role", "area_code"])["weight"].sum()
    )
    assert np.allclose(sums.to_numpy(), 1.0, atol=1e-12, rtol=0)


def test_prediction_trichotomies_are_verbatim(producer) -> None:
    durable_positive = pd.Series([0.2, 0.1], index=producer.DURABLE_CODES)
    transient_lower = pd.Series(
        [0.0, 0.0, 0.0, 0.0], index=producer.TRANSIENT_CODES
    )
    assert producer.classify_p1(
        durable_positive, transient_lower, 0.05
    ) == "confirmed"
    assert producer.classify_p1(
        durable_positive, transient_lower, 0.0500001
    ) == "directional-only"
    assert producer.classify_p1(
        pd.Series([0.0, 0.1], index=producer.DURABLE_CODES),
        transient_lower,
        0.001,
    ) == "falsified"
    assert producer.classify_p1(
        durable_positive,
        pd.Series([0.3, 0.3, 0.3, 0.3], index=producer.TRANSIENT_CODES),
        0.001,
    ) == "falsified"

    assert producer.classify_p2(0.48) == "confirmed"
    assert producer.classify_p2(0.479999) == "directional-only"
    assert producer.classify_p2(np.nextafter(0.0, 1.0)) == "directional-only"
    assert producer.classify_p2(0.0) == "falsified"
    assert producer.classify_p2(-0.1) == "falsified"


def test_headline_requires_both_primaries(producer) -> None:
    assert producer.assemble_headline_verdict(
        "confirmed", "confirmed"
    ) == "prediction confirmed"
    assert producer.assemble_headline_verdict(
        "confirmed", "directional-only"
    ) == "partial support"
    assert producer.assemble_headline_verdict(
        "directional-only", "confirmed"
    ) == "partial support"
    assert producer.assemble_headline_verdict(
        "directional-only", "directional-only"
    ) == "directional-only"
    assert producer.assemble_headline_verdict(
        "confirmed", "falsified"
    ) == "prediction falsified"


def test_s1_bands_and_s3_pooled_other_contract(producer) -> None:
    rows = []
    for spec in producer.S1_SPECS:
        for outcome in producer.S1_OUTCOMES:
            rows.append({
                "spec": spec,
                "outcome": outcome,
                "estimate": 0.0,
                "ci_low": -0.1,
                "ci_high": 0.1,
            })
    estimates = pd.DataFrame(rows)
    assert producer.assess_s1(estimates)["status"] == "prediction met"
    estimates.loc[0, ["estimate", "ci_low", "ci_high"]] = [-0.01, -0.1, 0.1]
    assert producer.assess_s1(estimates)["status"] == (
        "not confirmed, not discordant"
    )
    estimates.loc[0, ["estimate", "ci_low", "ci_high"]] = [-0.01, -0.1, -0.001]
    assert producer.assess_s1(estimates)["status"] == "discordant"

    assert producer.VISITOR_OTHER_MODES == (
        "transport_to_fukui_private_car",
        "transport_to_fukui_rental_car",
        "transport_to_fukui_local_train",
        "transport_to_fukui_airplane",
        "transport_to_fukui_tour_bus",
    )
    assert producer.SHINKANSEN_MODE not in producer.VISITOR_OTHER_MODES
    seen = pd.read_csv(
        ROOT / "output" / "synthesis" / "synthesis_mode_friction.csv"
    ).set_index("friction_code").loc["transport_access"]
    assert seen["shinkansen_pct"] == 7.09
    assert seen["other_arrival_pooled_pct"] == 1.7711661764394693
    assert seen["shk_over_other_ratio"] == 4.0030123058542415


def test_s2_requires_confirmed_2025_and_2026_rows(producer) -> None:
    rows = []
    for year in range(2018, 2026):
        for month in range(1, 13):
            rows.append({
                "pref_code": "18",
                "year": year,
                "month": month,
                "total_stays": 1.0,
                "vintage": "confirmed",
            })
    rows.append({
        "pref_code": "18",
        "year": 2026,
        "month": 1,
        "total_stays": 1.0,
        "vintage": "preliminary",
    })
    fixture = pd.DataFrame(rows)
    report = producer.build_s2_descriptive_report(fixture)
    assert report["status"] == "descriptive only"
    with pytest.raises(ValueError, match="2025 confirmed"):
        producer.build_s2_descriptive_report(
            fixture[fixture["year"] != 2025]
        )
    with pytest.raises(ValueError, match="2026"):
        producer.build_s2_descriptive_report(
            fixture[fixture["year"] != 2026]
        )


def test_source_pins_have_not_moved_from_adr_0032() -> None:
    national = yaml.safe_load(
        (ROOT / "config" / "national_data_sources.yaml").read_text()
    )
    assert national["japan_kanko_stat"]["commit"] == (
        "dfb906975b63adcaef20a3e7a35f2a10ab22ada5"
    )
    official = yaml.safe_load(
        (ROOT / "config" / "official_fukui_sources.yaml").read_text()
    )
    for name in ("ftas_survey_all", "ftas_survey_counts", "ftas_area_master"):
        assert official["sources"][name]["commit"] == (
            "5857c311acc5782eb44d85f06d95e6a2e6af4509"
        )
    combined = json.dumps([national, official])
    assert "6d8dccf1514262c1d13acb3e00072f6dc5b55ae9" not in combined
    assert "22a95f3f2e941077ba1c557c5d4fca23fcc05e09" not in combined


def test_s1_seen_wave_freeze_is_complete(gateway) -> None:
    assert gateway.EXPECTED_SEEN_MERGED_SHA256 == {
        2023: "298393e0dd050f9540ea8ecb026b179e066a610f45f84d65ab67af61edf7ae45",
        2024: "dc06d1c5479b06b9b1c539937bcce8c77a8d1078790d4bb04677df4c40c64bbd",
        2025: "d59e85f5ed5aca3801362da852f9e371ebe8aba32c2c4db8d377b07d5987729f",
        2026: "2cc19c71e789fda90fb162e5e5552551e784d3bb3bf823f7fadf66f90bec4202",
    }
    for year, expected in gateway.EXPECTED_SEEN_MERGED_SHA256.items():
        path = gateway.PINNED_MERGED_DIR / f"merged_survey_{year}.csv"
        assert gateway._sha256(path) == expected


def test_seen_fixture_runs_end_to_end_but_returns_no_result(producer) -> None:
    report = producer.exercise_seen_mobile_fixture_only()
    assert report == {
        "fixture_only": True,
        "source": "held-out slice of seen 2021-01..2025-12 mobile panel",
        "produces_arm2_verdict": False,
        "headline_verdict": None,
        "months_exercised": 6,
        "partitions_exercised": 100_000,
    }
