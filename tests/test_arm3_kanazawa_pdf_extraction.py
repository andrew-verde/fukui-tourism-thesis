"""Contract tests for Arm 3's page-cited Kanazawa PDF extraction."""

import ast
import csv
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "scripts" / "extract_arm3_kanazawa_pdfs.py"
OUT_DIR = ROOT / "output" / "arm3_kanazawa"

EXPECTED_SOURCE_SHA256 = {
    "kanazawa_tourism_survey_2018.pdf": (
        "778cf580b354a8923b0be2456bc8e201095f0edfb720a75ddcace0f8a1bd3ea7"
    ),
    "kanazawa_tourism_survey_2019.pdf": (
        "d8107ffe851dcbbc9ce1504a95d2403ccffec22a0db1ee99e5a267339b5f7a77"
    ),
}
EXPECTED_OUTPUT_SHA256 = {
    "kanazawa_lodging_guests_monthly.csv": (
        "51b87ff654470291ed5c8ae05df073e081f7974775c3a75784a0aa26bdd44de5"
    ),
    "kanazawa_19_facility_visits_monthly.csv": (
        "512511140f8007c723c68e53238515d5dfea15e525fcef292637bc1a01be40f9"
    ),
    "kenrokuen_visits_monthly.csv": (
        "ae14da453830c8149a20ccc5c8fd6400ef669836b4031cd11b5376eb74d30633"
    ),
    "kanazawa_19_facility_membership.csv": (
        "cf76623463195b6cce4143215dce6e64f821c9255ea371f01cb03859386d9877"
    ),
}
EXPECTED_MANIFEST_SHA256 = (
    "4ff8e2c77d3e3d28ba9f4ecf4691082990fd8f88a66880b9ed2fdc725b17f4d7"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_csv(name: str) -> list[dict[str, str]]:
    with (OUT_DIR / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _producer_hashes() -> dict[str, str]:
    tree = ast.parse(PRODUCER.read_text(encoding="utf-8"))
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name)
                and target.id == "EXPECTED_OUTPUT_SHA256"
                for target in node.targets
            )
        ):
            return ast.literal_eval(node.value)
    raise AssertionError("producer does not define EXPECTED_OUTPUT_SHA256")


def _load_producer():
    spec = importlib.util.spec_from_file_location(
        "extract_arm3_kanazawa_pdfs", PRODUCER
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_pdfs_are_sha256_pinned() -> None:
    raw_dir = OUT_DIR / "raw"
    assert {
        name: _sha256(raw_dir / name) for name in EXPECTED_SOURCE_SHA256
    } == EXPECTED_SOURCE_SHA256


def test_committed_outputs_are_byte_stable_and_manifested() -> None:
    assert _producer_hashes() == {
        "lodging_guests": EXPECTED_OUTPUT_SHA256[
            "kanazawa_lodging_guests_monthly.csv"
        ],
        "facility_aggregate": EXPECTED_OUTPUT_SHA256[
            "kanazawa_19_facility_visits_monthly.csv"
        ],
        "kenrokuen": EXPECTED_OUTPUT_SHA256["kenrokuen_visits_monthly.csv"],
        "facility_membership": EXPECTED_OUTPUT_SHA256[
            "kanazawa_19_facility_membership.csv"
        ],
    }
    actual = {
        name: _sha256(OUT_DIR / name) for name in EXPECTED_OUTPUT_SHA256
    }
    assert actual == EXPECTED_OUTPUT_SHA256

    manifest = json.loads(
        (OUT_DIR / "kanazawa_pdf_provenance.json").read_text(encoding="utf-8")
    )
    assert _sha256(OUT_DIR / "kanazawa_pdf_provenance.json") == (
        EXPECTED_MANIFEST_SHA256
    )
    for key, filename in (
        ("lodging_guests", "kanazawa_lodging_guests_monthly.csv"),
        ("facility_aggregate", "kanazawa_19_facility_visits_monthly.csv"),
        ("kenrokuen", "kenrokuen_visits_monthly.csv"),
        ("facility_membership", "kanazawa_19_facility_membership.csv"),
    ):
        assert manifest["outputs"][key]["sha256"] == actual[filename]


def test_monthly_coverage_units_pages_and_annual_oracles() -> None:
    lodging = _read_csv("kanazawa_lodging_guests_monthly.csv")
    attractions = _read_csv("kanazawa_19_facility_visits_monthly.csv")
    kenrokuen = _read_csv("kenrokuen_visits_monthly.csv")

    assert len(lodging) == 72
    assert [int(lodging[0]["ym"]), int(lodging[-1]["ym"])] == [201401, 201912]
    assert {row["unit"] for row in lodging} == {"persons"}
    assert {int(row["source_pdf_page"]) for row in lodging} == {97, 109}

    assert len(attractions) == 72
    assert [int(attractions[0]["ym"]), int(attractions[-1]["ym"])] == [
        201401,
        201912,
    ]
    assert {row["unit"] for row in attractions} == {"person_visits"}
    assert {int(row["source_pdf_page"]) for row in attractions} == {90, 102}

    assert len(kenrokuen) == 36
    assert [int(kenrokuen[0]["ym"]), int(kenrokuen[-1]["ym"])] == [
        201701,
        201912,
    ]
    assert {int(row["source_pdf_page"]) for row in kenrokuen} == {92, 104}
    assert not any(int(row["ym"]) == 201503 for row in kenrokuen)

    annual = lambda rows, year: sum(  # noqa: E731
        int(row["value"]) for row in rows if int(row["year"]) == year
    )
    assert annual(lodging, 2014) == 2656588
    assert annual(lodging, 2015) == 2816987
    assert annual(lodging, 2019) == 3431493
    assert annual(attractions, 2014) == 5979183
    assert annual(attractions, 2018) == 9048836
    assert annual(attractions, 2019) == 9155285
    assert annual(kenrokuen, 2018) == 2750105


def test_facility_membership_is_stable_but_vintage_revision_is_disclosed() -> None:
    members = _read_csv("kanazawa_19_facility_membership.csv")
    sets = {}
    for row in members:
        sets.setdefault(int(row["source_report_year"]), []).append(
            row["facility_name_ja_normalized"]
        )
    assert len(sets[2018]) == len(sets[2019]) == 19
    assert sets[2018] == sets[2019]
    assert "兼六園" in sets[2018]
    label_rows = [
        row
        for row in members
        if row["facility_name_ja_normalized"] == "金沢蓄音器館"
    ]
    assert [row["facility_name_ja_as_printed"] for row in label_rows] == [
        "金沢蓄音機館",
        "金沢蓄音器館",
    ]

    manifest = json.loads(
        (OUT_DIR / "kanazawa_pdf_provenance.json").read_text(encoding="utf-8")
    )
    issues = {
        item["issue"] for item in manifest["source_ambiguities"]
    }
    assert {
        "lodging_monthly_rows_do_not_sum_to_printed_totals",
        "2018_facility_aggregate_revised",
        "2019_internal_aggregate_month_discrepancy",
        "kenrokuen_opening_window_not_supported",
        "lodging_reporting_universe_changes",
    } <= issues


def test_regeneration_is_deterministic(tmp_path: Path) -> None:
    producer = _load_producer()
    regenerated = producer.build_outputs(
        out_dir=tmp_path,
        raw_dir=OUT_DIR / "raw",
    )
    for key, filename in (
        ("lodging_guests", "kanazawa_lodging_guests_monthly.csv"),
        ("facility_aggregate", "kanazawa_19_facility_visits_monthly.csv"),
        ("kenrokuen", "kenrokuen_visits_monthly.csv"),
        ("facility_membership", "kanazawa_19_facility_membership.csv"),
    ):
        assert regenerated[key].read_bytes() == (OUT_DIR / filename).read_bytes()
    assert regenerated["manifest"].read_bytes() == (
        OUT_DIR / "kanazawa_pdf_provenance.json"
    ).read_bytes()
