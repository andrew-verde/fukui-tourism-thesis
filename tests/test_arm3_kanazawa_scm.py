"""Executable data-firewall, vintage, battery, and artifact oracles for Arm 3."""

from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "scripts" / "arm3_kanazawa_scm.py"
RESULT_DIR = ROOT / "output" / "arm3_kanazawa" / "causal_robustness"


def _producer():
    spec = importlib.util.spec_from_file_location(
        "arm3_kanazawa_scm_test", PRODUCER
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_annual_release_parser_and_full_vintage_oracle() -> None:
    producer = _producer()
    annual = producer.load_annual_release_panel()
    canonical = producer.load_prefecture_panel()

    assert len(annual) == 3948
    assert annual["pref_code"].nunique() == 47
    assert annual["ym"].min() == 201101
    assert annual["ym"].max() == 201712
    ishikawa_2013 = annual.loc[
        (annual["pref_code"] == "17") & (annual["ym"] == 201301)
    ].iloc[0]
    assert tuple(
        ishikawa_2013[
            ["total_stays", "japanese_stays", "foreign_stays"]
        ]
    ) == (510540.0, 491910.0, 18630.0)

    columns = [
        "pref_code", "ym", "total_stays", "japanese_stays", "foreign_stays"
    ]
    expected = canonical.loc[
        canonical["ym"].between(201201, 201612), columns
    ].sort_values(["pref_code", "ym"]).reset_index(drop=True)
    actual = annual.loc[
        annual["ym"].between(201201, 201612), columns
    ].sort_values(["pref_code", "ym"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(expected, actual)
    assert len(actual) * 3 == 8460


def test_post_2019_outcome_sentinels_are_never_decoded(tmp_path) -> None:
    producer = _producer()
    sentinel_workbook = tmp_path / "post_2019_sentinels.xlsx"

    with zipfile.ZipFile(producer.WORKBOOK) as source:
        sheet_paths = set(producer._sheet_paths(source)[name] for name in (
            producer.SHEET_OUTCOMES
        ))
        with zipfile.ZipFile(sentinel_workbook, "w") as target:
            for info in source.infolist():
                data = source.read(info.filename)
                if info.filename in sheet_paths:
                    old = b'r="DF6"'
                    position = data.find(old)
                    assert position >= 0
                    value_start = data.find(b"<v>", position) + len(b"<v>")
                    value_end = data.find(b"</v>", value_start)
                    assert value_start > len(b"<v>") and value_end > value_start
                    data = (
                        data[:value_start]
                        + b"POST_2019_SENTINEL"
                        + data[value_end:]
                    )
                target.writestr(info, data)

    panel = producer.load_prefecture_panel(sentinel_workbook)
    assert panel["ym"].max() == 201912
    assert len(panel) == 47 * 108


def test_backdated_placebo_uses_the_backdated_opening_window() -> None:
    producer = _producer()
    result = producer._run_intime(producer.load_prefecture_panel())
    ishikawa = result.loc[result["target_code"] == "17"].iloc[0]

    assert ishikawa["event_ym"] == 201403
    assert ishikawa["n_pre_months"] == 26
    assert np.isclose(
        ishikawa["backdated_opening_gap_log"], -0.024146994029025315
    )
    assert np.isclose(ishikawa["p_backdated_opening_1s"], 18 / 31)
    assert np.isclose(ishikawa["p_backdated_opening_2s"], 22 / 31)


def test_result_semantics_and_byte_exact_artifacts() -> None:
    producer = _producer()
    hashes = producer.artifact_hashes(RESULT_DIR)

    assert producer.EXPECTED_ARTIFACT_SHA256
    assert hashes == producer.EXPECTED_ARTIFACT_SHA256
    metrics = json.loads((RESULT_DIR / "metrics.json").read_text())
    assert metrics["vintage_crosscheck"]["status"] == "passed"
    assert metrics["tiers"] == {
        "V1": {
            "components": {"V1a": False, "V1b": True, "V1c": True},
            "outcome": "fail",
        },
        "V2": {
            "components": {"V2a": False, "V2b": True},
            "outcome": "fail",
        },
        "V3": {
            "confirmatory": False,
            "outcome": "met_descriptively",
        },
    }
    comparison = metrics["hagibis_comparison"]
    assert comparison["V2a_disagreement"] is False
    assert comparison["primary_event_mask"]["V2a"] is False
    assert comparison["sensitivity_recovery_mask"]["V2a"] is False
    assert metrics["success_criteria"]["V1c"]["opening_gap_log_range"][0] > 0

    summary = pd.read_csv(RESULT_DIR / "specification_summary.csv")
    assert len(summary) == 24
    assert set(summary["hagibis_mask"]) == {"event", "recovery"}
    assert summary["n_pre_months"].isin([38, 50]).all()
    trajectories = pd.read_csv(RESULT_DIR / "target_gap_trajectories.csv")
    assert trajectories["ym"].max() == 201912
    assert trajectories["ym"].min() == 201101


def test_result_artifacts_regenerate_byte_exactly(tmp_path) -> None:
    producer = _producer()
    result = subprocess.run(
        [
            sys.executable,
            str(PRODUCER),
            "--out-dir",
            str(tmp_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert producer.artifact_hashes(tmp_path) == (
        producer.EXPECTED_ARTIFACT_SHA256
    )
