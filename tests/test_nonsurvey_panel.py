import json
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import build_nonsurvey_panel as builder
from scripts import sem_nonsurvey as sem

EXPECTED_CODE4FUKUI_REPOS = {
    "fukui-kanko-people-flow-data",
    "fukui-kanko-reservation",
    "fukui-station-kanko-reservation",
    "echizen-coast-kanko-reservation",
    "obama-kanko-reservation",
    "mikatagoko-kanko-reservation",
    "fukui-kanko-trend-data",
}


def write_panel_inputs(artifact_dir: Path) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    site = pd.DataFrame(
        {
            "date": ["2024-03-15", "2024-03-16"],
            "geo_id": ["tojinbo", "fukui_station_east"],
            "value": [1, 2],
        }
    )
    area = pd.DataFrame(
        {
            "date": ["2024-03-16", "2024-03-17"],
            "geo_id": ["awara_onsen", "fukui_station"],
            "value": [3, 4],
        }
    )
    booking = pd.DataFrame({"stay_date": ["2024-03-16"], "lead_days": [7]})
    site.to_parquet(artifact_dir / builder.PANEL_FILES["panel_site_daily"], index=False)
    area.to_parquet(artifact_dir / builder.PANEL_FILES["panel_area_daily"], index=False)
    booking.to_parquet(artifact_dir / builder.PANEL_FILES["booking_curve_awara"], index=False)
    (artifact_dir / "data_manifest.json").write_text(
        json.dumps(
            {
                "sources": {repo: {"commit": f"{repo}-commit"} for repo in EXPECTED_CODE4FUKUI_REPOS},
                "notes": ["staged fixture"],
            }
        ),
        encoding="utf-8",
    )


def write_linked_panel_inputs(panel_dir: Path, site: pd.DataFrame, area: pd.DataFrame) -> None:
    panel_dir.mkdir()
    site.to_parquet(panel_dir / "panel_site_daily.parquet", index=False)
    area.to_parquet(panel_dir / "panel_area_daily.parquet", index=False)


def test_add_contract_columns_break_boundary_and_copy():
    original = pd.DataFrame(
        {
            "date": ["2024-03-15", "2024-03-16", "2024-03-17"],
            "value": [1, 2, 3],
        }
    )

    result = builder.add_contract_columns(original)

    assert result["post_shinkansen"].tolist() == [0, 1, 1]
    assert "post_shinkansen" not in original.columns
    assert result is not original


def test_add_contract_columns_preserves_existing_values():
    original = pd.DataFrame(
        {
            "date": ["2024-03-15", "2024-03-17"],
            "post_shinkansen": [1, 0],
        }
    )

    result = builder.add_contract_columns(original)

    assert result["post_shinkansen"].tolist() == [1, 0]
    assert result is not original


def test_find_artifact_dir_accepts_flat_layout(tmp_path):
    write_panel_inputs(tmp_path)

    assert builder.find_artifact_dir(tmp_path) == tmp_path


def test_find_artifact_dir_accepts_nested_layout(tmp_path):
    panel_dir = tmp_path / "panel"
    write_panel_inputs(panel_dir)

    assert builder.find_artifact_dir(tmp_path) == panel_dir


def test_find_artifact_dir_rejects_partial_layout(tmp_path):
    (tmp_path / builder.PANEL_FILES["panel_site_daily"]).touch()

    with pytest.raises(FileNotFoundError) as exc_info:
        builder.find_artifact_dir(tmp_path)

    message = str(exc_info.value)
    for artifact in builder.PANEL_FILES.values():
        assert artifact in message


def test_write_parquet_round_trip_and_metadata(tmp_path):
    frame = pd.DataFrame(
        {"date": ["2024-03-15", "2024-03-16"], "value": [1.5, 2.5]}
    )
    src = tmp_path / "source.parquet"
    dst = tmp_path / "output.parquet"
    frame.to_parquet(src, index=False)

    metadata = builder.write_parquet(src, dst, add_post=True)

    expected = frame.assign(post_shinkansen=[0, 1])
    pd.testing.assert_frame_equal(pd.read_parquet(dst), expected)
    assert metadata["rows"] == len(frame)
    assert metadata["sha256"] == builder.sha256_file(dst)


def test_write_parquet_without_post_column(tmp_path):
    frame = pd.DataFrame({"stay_date": ["2024-03-16"], "lead_days": [4]})
    src = tmp_path / "source.parquet"
    dst = tmp_path / "output.parquet"
    frame.to_parquet(src, index=False)

    builder.write_parquet(src, dst, add_post=False)

    result = pd.read_parquet(dst)
    pd.testing.assert_frame_equal(result, frame)
    assert "post_shinkansen" not in result.columns


def test_write_manifest_with_complete_sources_adds_no_note(tmp_path):
    artifact_dir = tmp_path / "artifacts"
    out_dir = tmp_path / "out"
    artifact_dir.mkdir()
    out_dir.mkdir()
    assert builder.CODE4FUKUI_REPOS == EXPECTED_CODE4FUKUI_REPOS
    source_manifest = {
        "sources": {repo: {"commit": repo} for repo in EXPECTED_CODE4FUKUI_REPOS},
        "notes": ["existing note"],
    }
    (artifact_dir / "data_manifest.json").write_text(
        json.dumps(source_manifest), encoding="utf-8"
    )

    builder.write_manifest(artifact_dir, out_dir, {"panel": {"rows": 2}})

    result = json.loads((out_dir / "data_manifest.json").read_text(encoding="utf-8"))
    assert result["notes"] == ["existing note"]
    assert result["sources"] == source_manifest["sources"]
    assert result["outputs"] == {"panel": {"rows": 2}}
    assert all("absent from manifest" not in note for note in result["notes"])


def test_write_manifest_names_only_missing_repo_and_preserves_content(tmp_path):
    artifact_dir = tmp_path / "artifacts"
    out_dir = tmp_path / "out"
    artifact_dir.mkdir()
    out_dir.mkdir()
    missing_repo = "obama-kanko-reservation"
    sources = {
        repo: {"commit": f"{repo}-commit"}
        for repo in EXPECTED_CODE4FUKUI_REPOS
        if repo != missing_repo
    }
    (artifact_dir / "data_manifest.json").write_text(
        json.dumps({"sources": sources, "notes": ["keep me"]}), encoding="utf-8"
    )

    builder.write_manifest(artifact_dir, out_dir, {})

    result = json.loads((out_dir / "data_manifest.json").read_text(encoding="utf-8"))
    assert result["sources"] == sources
    assert result["notes"][0] == "keep me"
    assert result["notes"][1] == (
        "Expected pinned Code4Fukui repos absent from manifest: " + missing_repo
    )


def test_write_manifest_without_source_manifest(tmp_path):
    artifact_dir = tmp_path / "artifacts"
    out_dir = tmp_path / "out"
    artifact_dir.mkdir()
    out_dir.mkdir()
    outputs = {"panel_site_daily": {"rows": 3}}

    builder.write_manifest(artifact_dir, out_dir, outputs)

    result = json.loads((out_dir / "data_manifest.json").read_text(encoding="utf-8"))
    assert result["outputs"] == outputs
    assert result["sources"] == {}


@pytest.mark.parametrize("with_gov_panel", [False, True])
def test_main_builds_staged_panels_and_conditionally_adds_gov_panel(
    tmp_path, monkeypatch, with_gov_panel
):
    raw_dir = tmp_path / "raw"
    artifact_dir = raw_dir / "panel"
    out_dir = tmp_path / "out"
    gov_dir = tmp_path / "gov"
    write_panel_inputs(artifact_dir)
    gov_dir.mkdir()
    if with_gov_panel:
        pd.DataFrame(
            {"date": ["2024-03-15", "2024-03-16"], "overnight_stays": [10, 20]}
        ).to_parquet(gov_dir / "jta_overnight.parquet", index=False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_nonsurvey_panel.py",
            "--raw-dir",
            str(raw_dir),
            "--out",
            str(out_dir),
            "--gov-dir",
            str(gov_dir),
        ],
    )

    assert builder.main() == 0

    for name in builder.PANEL_FILES.values():
        assert (out_dir / name).exists()
    assert (out_dir / "data_manifest.json").exists()
    assert "post_shinkansen" in pd.read_parquet(
        out_dir / builder.PANEL_FILES["panel_site_daily"]
    ).columns
    assert "post_shinkansen" in pd.read_parquet(
        out_dir / builder.PANEL_FILES["panel_area_daily"]
    ).columns
    assert "post_shinkansen" not in pd.read_parquet(
        out_dir / builder.PANEL_FILES["booking_curve_awara"]
    ).columns
    monthly = out_dir / "panel_pref_monthly.parquet"
    assert monthly.exists() is with_gov_panel
    manifest = json.loads((out_dir / "data_manifest.json").read_text(encoding="utf-8"))
    assert ("panel_pref_monthly" in manifest["outputs"]) is with_gov_panel


def test_reference_is_frozen_coefficient_contract():
    assert sem.REFERENCE == {
        "model": "nonsurvey_extended_sem_v1",
        "n_obs": 1602,
        "n_sites": 4,
        "fit": {
            "chi2": 67.9009137406868,
            "CFI": 0.9860337604105707,
            "TLI": 0.9650844010264266,
            "RMSEA": 0.09989134770409785,
            "AIC": 21.915229820548454,
        },
        "paths": [
            {
                "from": "intent",
                "to": "demand",
                "std": 0.17337153649094222,
                "p": 5.9530202856095116e-05,
            }
        ],
        "loadings": [
            {
                "latent": "intent",
                "indicator": "trend_directions_lz",
                "std": 0.7899045558718679,
            },
            {
                "latent": "intent",
                "indicator": "trend_search_views_lz",
                "std": 0.597908750523608,
            },
            {
                "latent": "demand",
                "indicator": "cam_load_lz",
                "std": 0.38412886448619493,
            },
            {
                "latent": "demand",
                "indicator": "rsv_n_stay_lz",
                "std": 0.9618242446618926,
            },
            {
                "latent": "demand",
                "indicator": "rsv_n_reserve_lz",
                "std": 0.9909176864930526,
            },
        ],
        "observed_elasticities": {
            "directions_to_stays_loglog": {
                "beta": 0.01496765241574735,
                "pearson_logs": 0.012584134115182367,
                "note": "1% rise in GBP directions ~ beta% change in stays (pooled daily across sites with national trend broadcast is attenuated; NOT used as anchor)",
            },
            "footfall_to_stays_loglog": {
                "beta": 0.5188793516442793,
                "pearson_logs": 0.8545440439265284,
            },
            "awara_weekly_directions_to_stays_loglog": {
                "beta": 0.12641991596033017,
                "pearson_logs": 0.47896307517258246,
                "n_weeks": 111,
                "note": "DEFENSIBLE ANCHOR: within-Awara weekly elasticity; a 1pct rise in GBP directions associates with ~0.13pct change in stays. Used to bound the intent->demand path in the simulation.",
            },
        },
    }
    elasticities = sem.REFERENCE["observed_elasticities"]
    assert "DEFENSIBLE ANCHOR" in elasticities[
        "awara_weekly_directions_to_stays_loglog"
    ]["note"]
    assert "NOT used as anchor" in elasticities["directions_to_stays_loglog"]["note"]


def test_site_area_link_is_frozen():
    assert sem.SITE_AREA_LINK == {
        "tojinbo": "awara_onsen",
        "fukui_station_east": "fukui_station",
        "rainbow_line_lot1": "mikatagoko",
        "rainbow_line_lot2": "mikatagoko",
    }


def test_linked_panel_inner_joins_dates_and_areas_with_suffixes(tmp_path):
    site = pd.DataFrame(
        {
            "date": ["2024-01-01"] * 4,
            "geo_id": [
                "tojinbo",
                "fukui_station_east",
                "rainbow_line_lot1",
                "unmapped_site",
            ],
            "overlap": [10, 20, 30, 40],
        }
    )
    area = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "geo_id": ["awara_onsen", "fukui_station"],
            "overlap": [100, 200],
        }
    )
    write_linked_panel_inputs(tmp_path / "panels", site, area)

    result = sem.linked_panel(tmp_path / "panels")

    assert len(result) == 1
    assert result.loc[0, "geo_id_site"] == "tojinbo"
    assert result.loc[0, "geo_id_area"] == "awara_onsen"
    assert result.loc[0, "overlap_site"] == 10
    assert result.loc[0, "overlap_area"] == 100


def test_complete_case_count_coalesces_footfall_and_requires_inputs(tmp_path):
    site = pd.DataFrame(
        {
            "date": [f"2024-01-{day:02d}" for day in range(1, 7)],
            "geo_id": ["tojinbo"] * 6,
            "trend_directions": [None, 1.0, 1.0, 1.0, 1.0, 1.0],
            "trend_search_views": [1.0, None, 1.0, 1.0, 1.0, 1.0],
            "cam_person_total": [1.0, 1.0, 1.0, 1.0, 1.0, None],
            "cam_plate_vehicles": [None, None, None, None, None, 2.0],
        }
    )
    area = pd.DataFrame(
        {
            "date": [f"2024-01-{day:02d}" for day in range(1, 7)],
            "geo_id": ["awara_onsen"] * 6,
            "trend_directions": [10.0] * 6,
            "trend_search_views": [10.0] * 6,
            "rsv_n_stay": [1.0, 1.0, None, 1.0, 1.0, 1.0],
            "rsv_n_reserve": [1.0, 1.0, 1.0, None, 1.0, 1.0],
        }
    )
    write_linked_panel_inputs(tmp_path / "panels", site, area)

    assert sem.complete_case_count(tmp_path / "panels") == 2
