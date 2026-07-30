import hashlib
import importlib
import json

import pandas as pd
import pytest


@pytest.fixture
def gov_modules(tmp_path, monkeypatch):
    monkeypatch.delenv("ESTAT_APP_ID", raising=False)
    monkeypatch.delenv("MLIT_DATA_APP_ID", raising=False)
    dotenv = importlib.import_module("dotenv")
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: False)
    monkeypatch.chdir(tmp_path)
    fetch_gov_sources = importlib.import_module("scripts.fetch_gov_sources")
    fetch_estat_data = importlib.import_module("scripts.fetch_estat_data")
    return fetch_gov_sources, fetch_estat_data


def estat_payload(values):
    return {
        "GET_STATS_DATA": {
            "STATISTICAL_DATA": {
                "CLASS_INF": {
                    "CLASS_OBJ": {
                        "@id": "cat01",
                        "CLASS": [
                            {"@code": "a", "$": "Alpha"},
                            {"@code": "b", "@name": "Beta"},
                        ],
                    }
                },
                "DATA_INF": {"VALUE": values},
            }
        }
    }


def test_pref_pair_normalizes_supported_metadata_shapes(gov_modules):
    fetch_gov_sources, _ = gov_modules
    assert fetch_gov_sources._pref_pair({"DPF:prefecture_code": ["1", "18"]}) == ("01", "18")
    assert fetch_gov_sources._pref_pair({"DPF:prefecture_code": "1 to 18"}) == ("01", "18")
    assert fetch_gov_sources._pref_pair({"DPF:prefecture_code": ["18"]}) is None
    assert fetch_gov_sources._pref_pair({"DPF:prefecture_code": ["1", "2", "3"]}) is None
    assert fetch_gov_sources._pref_pair({"prefecture_code": ["7", "8"]}) == ("07", "08")
    assert fetch_gov_sources._pref_pair({"DPF:prefecture_code": ["18000", "18-"]}) == ("18000", "18")


def test_pref_names_uses_names_only_at_origin_destination_arity(gov_modules):
    fetch_gov_sources, _ = gov_modules
    assert fetch_gov_sources._pref_names({"DPF:prefecture_name": ["A", "B"]}, "01", "18") == ("A", "B")
    assert fetch_gov_sources._pref_names({"DPF:prefecture_name": " A, B "}, "01", "18") == ("A", "B")
    assert fetch_gov_sources._pref_names({"DPF:prefecture_name": ["A"]}, "01", "18") == ("01", "18")


def test_estat_rows_normalizes_shapes_labels_and_numeric_values(gov_modules):
    fetch_gov_sources, _ = gov_modules
    rows = fetch_gov_sources._estat_rows(
        estat_payload(
            [
                {"@area": "01000", "@tab": "category", "@time": "202401", "@cat01": "a", "@unit": "people", "$": "1,234"},
                {"@tab": "fallback", "@time": "202402", "@cat01": "unknown", "$": "-"},
                {"@area": "01000", "@time": "202403", "@cat01": "b", "$": ""},
                {"@area": "01000", "@time": "202404", "@cat01": "a", "$": None},
                {"@area": "01000", "@time": "202405", "@cat01": "a", "$": "not numeric"},
            ]
        ),
        "table-1",
    )

    expected = [
        {"stat_id": "table-1", "area": "01000", "time": "202401", "cat": "tab=category|cat01=Alpha", "value": 1234.0, "unit": "people"},
        {"stat_id": "table-1", "area": "fallback", "time": "202402", "cat": "cat01=unknown", "value": None, "unit": ""},
        {"stat_id": "table-1", "area": "01000", "time": "202403", "cat": "cat01=Beta", "value": None, "unit": ""},
        {"stat_id": "table-1", "area": "01000", "time": "202404", "cat": "cat01=Alpha", "value": None, "unit": ""},
        {"stat_id": "table-1", "area": "01000", "time": "202405", "cat": "cat01=Alpha", "value": None, "unit": ""},
    ]
    for row, expected_row in zip(rows, expected, strict=True):
        assert set(row) == set(fetch_gov_sources.ESTAT_COLUMNS)
        for key, expected_value in expected_row.items():
            if expected_value is None:
                assert pd.isna(row[key])
            else:
                assert row[key] == expected_value


def test_estat_rows_normalizes_bare_value_dict(gov_modules):
    fetch_gov_sources, _ = gov_modules
    rows = fetch_gov_sources._estat_rows(
        estat_payload({"@area": "01", "@time": "2024", "@cat01": "a", "$": "2"}),
        "table-2",
    )
    assert rows == [{"stat_id": "table-2", "area": "01", "time": "2024", "cat": "cat01=Alpha", "value": 2.0, "unit": ""}]


def test_sha256_file_reads_more_than_one_chunk(tmp_path, gov_modules):
    fetch_gov_sources, _ = gov_modules
    content = (b"government-data" * 100_000) + b"end"
    path = tmp_path / "large.bin"
    path.write_bytes(content)
    assert fetch_gov_sources.sha256_file(path) == hashlib.sha256(content).hexdigest()


def test_fetch_jta_overnight_uses_guest_nights_and_inclusive_dates(
    tmp_path, monkeypatch, gov_modules
):
    fetch_gov_sources, _ = gov_modules
    source = tmp_path / "accommodation.csv"
    pd.DataFrame(
        {
            "year": [2023, 2024, 2024, 2024],
            "month": [12, 1, 2, 3],
            "pref_code": [18, 1, 18, 18],
            "pref_name": ["Fukui", "Hokkaido", "Fukui", "Fukui"],
            "total_stays": [5.0, 10.0, None, 30.0],
            "foreign_stays_10plus": [50.0, 101.0, 202.0, 303.0],
            "vintage": ["v0", "v1", "v1", "v2"],
        }
    ).to_csv(source, index=False)
    monkeypatch.setattr(fetch_gov_sources, "ACCOMMODATION_PATH", source)

    frame = fetch_gov_sources.fetch_jta_overnight("2024-01", "2024-02")

    assert frame.index.tolist() == [0, 1]
    assert frame.date.tolist() == ["2024-01-01", "2024-02-01"]
    assert frame.geo_id.tolist() == ["pref_01", "pref_18"]
    assert frame.geo_level.tolist() == ["prefecture", "prefecture"]
    assert frame.pref_code.tolist() == [1, 18]
    assert frame.vintage.tolist() == ["v1", "v1"]
    assert frame.coverage_flag.tolist() == ["ok", "missing"]
    assert frame.jta_guest_nights.iloc[0] == 10.0
    assert pd.isna(frame.jta_guest_nights.iloc[1])
    assert frame.jta_foreign_guest_nights.tolist() == [101.0, 202.0]
    assert "2023-12-01" not in frame.date.tolist()
    assert "2024-03-01" not in frame.date.tolist()
    assert "jta_guest_nights" in frame and not any("guest" in column and column != "jta_guest_nights" and column != "jta_foreign_guest_nights" for column in frame)


def test_update_manifest_merges_gov_sources_without_losing_other_keys(
    tmp_path, monkeypatch, gov_modules
):
    fetch_gov_sources, _ = gov_modules
    monkeypatch.setattr(fetch_gov_sources, "ROOT", tmp_path)
    manifest_path = tmp_path / "data" / "nonsurvey" / "data_manifest.json"

    fetch_gov_sources._update_manifest(tmp_path / "one.parquet", "one", {"rows": 1})
    assert json.loads(manifest_path.read_text(encoding="utf-8")) == {"gov_sources": {"one": {"rows": 1}}}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["unrelated"] = {"keep": True}
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    fetch_gov_sources._update_manifest(tmp_path / "two.parquet", "two", {"rows": 2})

    assert json.loads(manifest_path.read_text(encoding="utf-8")) == {
        "unrelated": {"keep": True}, "gov_sources": {"one": {"rows": 1}, "two": {"rows": 2}}
    }


def test_discover_tables_normalizes_table_and_checks_status(monkeypatch, gov_modules):
    _, fetch_estat_data = gov_modules
    calls = []

    def api_get(endpoint, params, timeout):
        calls.append((endpoint, params, timeout))
        return {"GET_STATS_LIST": {"RESULT": {"STATUS": 0}, "DATALIST_INF": {"TABLE_INF": {"@id": "t1"}}}}

    monkeypatch.setattr(fetch_estat_data, "_api_get", api_get)
    assert fetch_estat_data.discover_tables("app", "survey", 12) == [{"@id": "t1"}]
    assert calls == [("getStatsList", {"appId": "app", "statsCode": "survey", "limit": 1000}, 12)]

    monkeypatch.setattr(fetch_estat_data, "_api_get", lambda *args: {"GET_STATS_LIST": {"RESULT": {"STATUS": 1}}})
    with pytest.raises(RuntimeError, match="getStatsList status=1"):
        fetch_estat_data.discover_tables("app", "survey", 12)


def test_fetch_table_pages_and_only_sets_area_filter_when_needed(monkeypatch, gov_modules):
    _, fetch_estat_data = gov_modules
    calls = []
    payloads = [
        {"GET_STATS_DATA": {"RESULT": {"STATUS": 0}, "STATISTICAL_DATA": {"RESULT_INF": {"NEXT_KEY": "42"}}}},
        {"GET_STATS_DATA": {"RESULT": {"STATUS": 0}, "STATISTICAL_DATA": {"RESULT_INF": {}}}},
    ]

    def api_get(endpoint, params, timeout):
        calls.append((endpoint, params, timeout))
        return payloads.pop(0)

    monkeypatch.setattr(fetch_estat_data, "_api_get", api_get)
    pages = fetch_estat_data.fetch_table("app", "table", ["01", "18"], 9)
    assert len(pages) == 2
    assert [call[0] for call in calls] == ["getStatsData", "getStatsData"]
    assert [call[1]["appId"] for call in calls] == ["app", "app"]
    assert [call[1]["statsDataId"] for call in calls] == ["table", "table"]
    assert [call[1]["limit"] for call in calls] == [
        fetch_estat_data.PAGE_LIMIT,
        fetch_estat_data.PAGE_LIMIT,
    ]
    assert [call[1]["startPosition"] for call in calls] == [1, 42]
    assert [call[1]["cdArea"] for call in calls] == ["01,18", "01,18"]
    assert [call[2] for call in calls] == [9, 9]

    no_area_calls = []
    monkeypatch.setattr(fetch_estat_data, "_api_get", lambda endpoint, params, timeout: no_area_calls.append(params) or {"GET_STATS_DATA": {"RESULT": {"STATUS": 0}}})
    fetch_estat_data.fetch_table("app", "table", [], 9)
    assert "cdArea" not in no_area_calls[0]


def test_fetch_table_raises_on_nonzero_status(monkeypatch, gov_modules):
    _, fetch_estat_data = gov_modules
    monkeypatch.setattr(fetch_estat_data, "_api_get", lambda *args: {"GET_STATS_DATA": {"RESULT": {"STATUS": 2}}})
    with pytest.raises(RuntimeError, match="getStatsData status=2"):
        fetch_estat_data.fetch_table("app", "table", [], 1)
