#!/usr/bin/env python3
"""Build the Arm 3 Kanazawa descriptive-anchor fixtures.

The values below are faithful transcriptions of page-cited tables in the
official 2018 and 2019 Kanazawa City tourism-survey PDFs.  The script verifies
the source-PDF hashes before writing analysis-ready CSV files and a provenance
manifest.  It intentionally does not infer missing Kenrokuen months or combine
point-utilization counts with lodging guests.

Outputs
-------
output/arm3_kanazawa/kanazawa_lodging_guests_monthly.csv
output/arm3_kanazawa/kanazawa_19_facility_visits_monthly.csv
output/arm3_kanazawa/kenrokuen_visits_monthly.csv
output/arm3_kanazawa/kanazawa_19_facility_membership.csv
output/arm3_kanazawa/kanazawa_pdf_provenance.json
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "arm3_kanazawa"
RAW_DIR = OUT_DIR / "raw"

SOURCES = {
    2018: {
        "filename": "kanazawa_tourism_survey_2018.pdf",
        "url": (
            "https://www4.city.kanazawa.lg.jp/material/files/group/32/"
            "houkoku_2018.pdf"
        ),
        "sha256": "778cf580b354a8923b0be2456bc8e201095f0edfb720a75ddcace0f8a1bd3ea7",
        "bytes": 1_989_163,
        "pages": 107,
        "title_ja": "平成30年 金沢市観光調査結果報告書",
    },
    2019: {
        "filename": "kanazawa_tourism_survey_2019.pdf",
        "url": (
            "https://www4.city.kanazawa.lg.jp/material/files/group/32/"
            "houkoku_2019.pdf"
        ),
        "sha256": "d8107ffe851dcbbc9ce1504a95d2403ccffec22a0db1ee99e5a267339b5f7a77",
        "bytes": 5_180_426,
        "pages": 117,
        "title_ja": "2019年 金沢市観光調査結果報告書",
    },
}

# The latest report is used for overlapping monthly observations.  Lodging
# values agree across the two reports for 2015--2018.
LODGING_GUESTS = {
    2014: (
        [176459, 182820, 228061, 230131, 250937, 200665,
         208997, 274973, 234103, 234305, 237791, 197346],
        2018, 97, 96,
    ),
    2015: (
        [164337, 187954, 247035, 240940, 262742, 233475,
         222013, 301251, 242062, 249723, 250455, 215000],
        2019, 109, 108,
    ),
    2016: (
        [198662, 229910, 262249, 254219, 263295, 222298,
         254218, 325711, 278167, 288523, 274064, 233538],
        2019, 109, 108,
    ),
    2017: (
        [210594, 223982, 289052, 272439, 285309, 234003,
         254611, 332231, 279698, 285924, 284956, 240705],
        2019, 109, 108,
    ),
    2018: (
        [210687, 223295, 284570, 281693, 287287, 240408,
         255022, 353279, 306188, 303869, 303843, 254949],
        2019, 109, 108,
    ),
    2019: (
        [218105, 245310, 303779, 315315, 312586, 253069,
         260717, 350660, 297376, 292954, 321319, 260303],
        2019, 109, 108,
    ),
}

# For 2014, the only available source is the 2018 report.  For 2015--2019,
# use the later 2019 report's dedicated 19-facility time-series table.
FACILITY_AGGREGATE = {
    2014: (
        [308403, 309493, 403516, 1062386, 579443, 414995,
         364371, 655362, 449584, 583248, 592497, 255885],
        2018, 90, 89,
    ),
    2015: (
        [278127, 358325, 684942, 1221738, 1031536, 683797,
         604033, 945433, 872324, 895153, 939480, 517698],
        2019, 102, 101,
    ),
    2016: (
        [538271, 583406, 792901, 1300487, 931590, 639879,
         597923, 962892, 819919, 954964, 852707, 516121],
        2019, 102, 101,
    ),
    2017: (
        [516622, 519086, 786665, 1320370, 907449, 609206,
         553917, 971710, 724446, 786363, 841178, 494497],
        2019, 102, 101,
    ),
    2018: (
        [467498, 475792, 815004, 1181118, 880457, 652562,
         601668, 962494, 733436, 815739, 935144, 527924],
        2019, 102, 101,
    ),
    2019: (
        [505274, 610185, 750833, 1370035, 954743, 605096,
         563457, 1004462, 728084, 693088, 914168, 455860],
        2019, 102, 101,
    ),
}

# Monthly Kenrokuen rows are present only for current/prior years in the
# facility-detail tables.  These two PDFs therefore support 2017--2019, not
# the 2015 opening window.
KENROKUEN = {
    2017: (
        [179583, 160703, 227075, 598921, 266233, 167729,
         136578, 244778, 186674, 212078, 264591, 151929],
        2018, 92, 91,
    ),
    2018: (
        [155930, 159540, 254655, 502643, 247475, 176930,
         128644, 237205, 192425, 213809, 319398, 161451],
        2019, 104, 103,
    ),
    2019: (
        [165146, 194824, 208223, 557178, 274007, 166338,
         144091, 235279, 192505, 176765, 293475, 146243],
        2019, 104, 103,
    ),
}

FACILITY_MEMBERS = [
    "兼六園",
    "金沢城公園",
    "金沢21世紀美術館",
    "県立美術館",
    "県立歴史博物館",
    "県立伝統産業工芸館",
    "安江金箔工芸館",
    "中村記念美術館",
    "武家屋敷跡野村家",
    "老舗記念館",
    "前田土佐守家資料館",
    "志摩",
    "泉鏡花記念館",
    "金沢蓄音器館",
    "妙立寺",
    "西茶屋資料館",
    "室生犀星記念館",
    "大野からくり記念館",
    "金沢湯涌夢二館",
]

ANNUAL_TOTALS = {
    "lodging_guests": {
        2014: 2749577,
        2015: 2905204,
        2016: 3084854,
        2017: 3193504,
        2018: 3305090,
        2019: 3431493,
    },
    "facility_aggregate": {
        2014: 5979183,
        2015: 9032586,
        2016: 9491060,
        2017: 9031509,
        2018: 9048836,
        2019: 9155285,
    },
    "kenrokuen": {
        2017: 2796872,
        2018: 2750105,
        2019: 2754074,
    },
}

# The printed annual total beside each monthly row normally equals the sum of
# the 12 printed months.  Two lodging rows are source exceptions.  Preserve
# the monthly cells and fail unless the discrepancy remains exactly as
# documented here; never manufacture a balancing month.
KNOWN_MONTHLY_MINUS_PRINTED_TOTAL = {
    ("lodging_guests", 2014): -92989,
    ("lodging_guests", 2015): -88217,
}

OUTPUT_FILENAMES = {
    "lodging_guests": "kanazawa_lodging_guests_monthly.csv",
    "facility_aggregate": "kanazawa_19_facility_visits_monthly.csv",
    "kenrokuen": "kenrokuen_visits_monthly.csv",
    "facility_membership": "kanazawa_19_facility_membership.csv",
}

# Filled from committed byte-stable outputs.  Tests assert that these stay in
# sync with both this producer and the artifacts.
EXPECTED_OUTPUT_SHA256 = {
    "lodging_guests": (
        "51b87ff654470291ed5c8ae05df073e081f7974775c3a75784a0aa26bdd44de5"
    ),
    "facility_aggregate": (
        "512511140f8007c723c68e53238515d5dfea15e525fcef292637bc1a01be40f9"
    ),
    "kenrokuen": (
        "ae14da453830c8149a20ccc5c8fd6400ef669836b4031cd11b5376eb74d30633"
    ),
    "facility_membership": (
        "cf76623463195b6cce4143215dce6e64f821c9255ea371f01cb03859386d9877"
    ),
}
EXPECTED_MANIFEST_SHA256 = (
    "4ff8e2c77d3e3d28ba9f4ecf4691082990fd8f88a66880b9ed2fdc725b17f4d7"
)


def sha256(path: Path) -> str:
    """Return a file's lowercase SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources(raw_dir: Path = RAW_DIR) -> None:
    """Fail closed if either official source PDF is absent or has drifted."""
    for source in SOURCES.values():
        path = raw_dir / source["filename"]
        if not path.is_file():
            raise FileNotFoundError(f"missing pinned source PDF: {path}")
        actual = sha256(path)
        if actual != source["sha256"]:
            raise ValueError(
                f"source PDF hash mismatch for {path}: "
                f"expected {source['sha256']}, got {actual}"
            )
        if path.stat().st_size != source["bytes"]:
            raise ValueError(f"source PDF byte-size mismatch for {path}")


def _monthly_rows(
    table: dict[int, tuple[list[int], int, int, int]],
    *,
    series: str,
    unit: str,
    source_table_ja: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for year, (values, report_year, pdf_page, printed_page) in table.items():
        if len(values) != 12:
            raise AssertionError(f"{series} {year} does not have 12 months")
        discrepancy = sum(values) - ANNUAL_TOTALS[series][year]
        expected_discrepancy = KNOWN_MONTHLY_MINUS_PRINTED_TOTAL.get(
            (series, year), 0
        )
        if discrepancy != expected_discrepancy:
            raise AssertionError(
                f"{series} {year} monthly-vs-printed-total discrepancy changed: "
                f"got {discrepancy}, expected {expected_discrepancy}"
            )
        source = SOURCES[report_year]
        for month, value in enumerate(values, 1):
            rows.append(
                {
                    "ym": year * 100 + month,
                    "year": year,
                    "month": month,
                    "value": value,
                    "unit": unit,
                    "series": series,
                    "source_report_year": report_year,
                    "source_pdf": source["filename"],
                    "source_pdf_page": pdf_page,
                    "source_printed_page": printed_page,
                    "source_table_ja": source_table_ja,
                }
            )
    return rows


def _write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _membership_rows() -> list[dict[str, object]]:
    rows = []
    for report_year, pdf_page, printed_page in ((2018, 89, 88), (2019, 101, 100)):
        for order, facility in enumerate(FACILITY_MEMBERS, 1):
            as_printed = (
                "金沢蓄音機館"
                if report_year == 2018 and facility == "金沢蓄音器館"
                else facility
            )
            rows.append(
                {
                    "source_report_year": report_year,
                    "facility_order": order,
                    "facility_name_ja_as_printed": as_printed,
                    "facility_name_ja_normalized": facility,
                    "unit": "person_visits",
                    "source_pdf": SOURCES[report_year]["filename"],
                    "source_pdf_page": pdf_page,
                    "source_printed_page": printed_page,
                }
            )
    return rows


def build_outputs(out_dir: Path = OUT_DIR, raw_dir: Path = RAW_DIR) -> dict[str, Path]:
    """Verify the pinned PDFs and write all extraction artifacts."""
    verify_sources(raw_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = {key: out_dir / filename for key, filename in OUTPUT_FILENAMES.items()}
    _write_csv(
        paths["lodging_guests"],
        _monthly_rows(
            LODGING_GUESTS,
            series="lodging_guests",
            unit="persons",
            source_table_ja="月別宿泊客数",
        ),
    )
    _write_csv(
        paths["facility_aggregate"],
        _monthly_rows(
            FACILITY_AGGREGATE,
            series="facility_aggregate",
            unit="person_visits",
            source_table_ja="主要観光施設（19施設計）の月別利用者数の推移",
        ),
    )
    _write_csv(
        paths["kenrokuen"],
        _monthly_rows(
            KENROKUEN,
            series="kenrokuen",
            unit="person_visits",
            source_table_ja="主要観光施設 利用者数集計",
        ),
    )
    _write_csv(paths["facility_membership"], _membership_rows())

    manifest_path = out_dir / "kanazawa_pdf_provenance.json"
    manifest = {
        "schema_version": 1,
        "scope": (
            "Arm 3 descriptive anchor evidence only; these series are not "
            "SCM units or confirmatory causal outcomes."
        ),
        "publisher": "Kanazawa City",
        "publisher_page": (
            "https://www4.city.kanazawa.lg.jp/soshikikarasagasu/"
            "kankoseisakuka/gyomuannai/1/2/30429.html"
        ),
        "page_citation_convention": (
            "source_pdf_page is the 1-indexed physical PDF page; "
            "source_printed_page is the page number printed in the report."
        ),
        "sources": {
            str(year): {
                **source,
                "path": f"output/arm3_kanazawa/raw/{source['filename']}",
            }
            for year, source in SOURCES.items()
        },
        "outputs": {
            key: {
                "path": f"output/arm3_kanazawa/{path.name}",
                "sha256": sha256(path),
                "rows_excluding_header": sum(
                    1 for _ in path.open(encoding="utf-8")
                )
                - 1,
            }
            for key, path in paths.items()
        },
        "extractions": {
            "lodging_guests": {
                "coverage": "2014-01..2019-12",
                "unit": "persons (lodging guests), not person-nights",
                "pages": [
                    {
                        "report_year": 2018,
                        "source_pdf_page": 97,
                        "source_printed_page": 96,
                        "years_used": [2014],
                    },
                    {
                        "report_year": 2019,
                        "source_pdf_page": 109,
                        "source_printed_page": 108,
                        "years_used": [2015, 2016, 2017, 2018, 2019],
                    },
                ],
                "reporting_universe_pages": [
                    {
                        "report_year": 2018,
                        "source_pdf_page": 95,
                        "source_printed_page": 94,
                    },
                    {
                        "report_year": 2019,
                        "source_pdf_page": 107,
                        "source_printed_page": 106,
                    },
                ],
            },
            "facility_aggregate": {
                "coverage": "2014-01..2019-12",
                "unit": "person-visits at 19 points; not unique visitors",
                "pages": [
                    {
                        "report_year": 2018,
                        "source_pdf_page": 90,
                        "source_printed_page": 89,
                        "years_used": [2014],
                    },
                    {
                        "report_year": 2019,
                        "source_pdf_page": 102,
                        "source_printed_page": 101,
                        "years_used": [2015, 2016, 2017, 2018, 2019],
                    },
                ],
            },
            "kenrokuen": {
                "coverage": "2017-01..2019-12",
                "unit": "person-visits at Kenrokuen; not unique visitors",
                "pages": [
                    {
                        "report_year": 2018,
                        "source_pdf_page": 92,
                        "source_printed_page": 91,
                        "years_used": [2017],
                    },
                    {
                        "report_year": 2019,
                        "source_pdf_page": 104,
                        "source_printed_page": 103,
                        "years_used": [2018, 2019],
                    },
                ],
                "unsupported_monthly_years": [2014, 2015, 2016],
            },
            "facility_membership": {
                "coverage": "2018 and 2019 report definitions",
                "unit": "membership definition",
                "pages": [
                    {
                        "report_year": 2018,
                        "source_pdf_page": 89,
                        "source_printed_page": 88,
                    },
                    {
                        "report_year": 2019,
                        "source_pdf_page": 101,
                        "source_printed_page": 100,
                    },
                ],
            },
        },
        "facility_set_review": {
            "result": (
                "No membership change between the 2018 and 2019 report "
                "definitions: the same 19 named facilities appear in the same "
                "order. The 2018 overview spells 金沢蓄音器館 as 金沢蓄音機館; "
                "its detail table and the 2019 report use 金沢蓄音器館, so this "
                "is treated as a label typo rather than a membership change."
            ),
            "member_count_each_report": 19,
            "members_ja": FACILITY_MEMBERS,
        },
        "source_ambiguities": [
            {
                "issue": "lodging_monthly_rows_do_not_sum_to_printed_totals",
                "detail": (
                    "The 12 printed lodging months sum to 2,656,588 for 2014 "
                    "and 2,816,987 for 2015, but the adjacent printed annual "
                    "totals are 2,749,577 and 2,905,204. The discrepancies are "
                    "-92,989 and -88,217. Both reports reproduce the 2015 "
                    "monthly cells and total. The output preserves the printed "
                    "monthly cells and does not force them to balance."
                ),
            },
            {
                "issue": "2018_facility_aggregate_revised",
                "detail": (
                    "The 2018 report, PDF page 90 (printed 89), reports "
                    "9,086,281 visits for 2018. The 2019 report, PDF page 102 "
                    "(printed 101), revises every 2018 month and reports "
                    "9,048,836. Membership is unchanged. The output uses the "
                    "later 2019-report vintage for 2018."
                ),
            },
            {
                "issue": "2019_internal_aggregate_month_discrepancy",
                "detail": (
                    "For 2019 January--June, the dedicated aggregate "
                    "time-series table on PDF page 102 (printed 101) differs "
                    "by +6,+9,+14,+14,-55,+12 from the total rows in the "
                    "facility-detail table on PDF page 104 (printed 103). "
                    "The differences net to zero and both annual totals are "
                    "9,155,285. The output uses the dedicated published "
                    "aggregate time-series table."
                ),
            },
            {
                "issue": "kenrokuen_opening_window_not_supported",
                "detail": (
                    "The reports publish annual Kenrokuen totals back to 2014 "
                    "but monthly Kenrokuen rows only for 2017--2019. They do "
                    "not support a monthly Kenrokuen series for the March 2015 "
                    "opening window."
                ),
            },
            {
                "issue": "lodging_reporting_universe_changes",
                "detail": (
                    "The city reports 112 lodging facilities in 2014 and 345 "
                    "in 2019. The monthly guest series is an evolving "
                    "citywide reporting universe and remains descriptive."
                ),
            },
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {**paths, "manifest": manifest_path}


def main() -> None:
    outputs = build_outputs()
    for path in outputs.values():
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
