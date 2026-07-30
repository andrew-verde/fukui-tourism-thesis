#!/usr/bin/env python3
"""Run the frozen Arm 3 Kanazawa prefecture-level SCM battery.

The source workbook extends beyond Arm 3's confirmatory window.  This module
therefore reads the XLSX worksheet XML directly: outcome cells after 2019-12
are rejected by column position before their contents are decoded.  A later
``DataFrame.query`` or post-load filter is deliberately not used as the
firewall.

Outputs are written below ``output/arm3_kanazawa/causal_robustness``.  The
seven checksum-pinned annual confirmed releases are parsed directly and the
required vintage cross-check runs before any sensitivity result is computed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import openpyxl
import pandas as pd
import xlrd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = (
    ROOT / "output" / "national_stats" / "raw"
    / "jta_accommodation_timeseries.xlsx"
)
OUT_DIR = ROOT / "output" / "arm3_kanazawa" / "causal_robustness"
RAW_DIR = ROOT / "output" / "national_stats" / "raw"
ANCHOR_DIR = ROOT / "output" / "arm3_kanazawa"

# Frozen by docs/thesis/arm3_kanazawa_design.md §§2, 4, and 5.
EVENT_YM = 201503
INTIME_EVENT_YM = 201403
PANEL_CAP_YM = 201912
PRIMARY_PRE_START_YM = 201201
SENSITIVITY_PRE_START_YM = 201101
PRE_END_YM = 201502
INTIME_PRE_END_YM = 201402
POST_END_YM = 201912
OPENING_MONTHS = (201503, 201504)
LATE_START_YM = 201801
LATE_END_YM = 201912
FIRST_12_POST_MONTHS = tuple(
    year * 100 + month
    for year, month in (
        (2015, 3), (2015, 4), (2015, 5), (2015, 6), (2015, 7),
        (2015, 8), (2015, 9), (2015, 10), (2015, 11), (2015, 12),
        (2016, 1), (2016, 2),
    )
)
MASK_2018_MONTHS = (201806, 201807, 201808, 201809)
MASK_HAGIBIS_PRIMARY_MONTHS = (201910,)
MASK_HAGIBIS_RECOVERY_MONTHS = (201910, 201911, 201912)
HAGIBIS_MASKS = {
    "event": MASK_HAGIBIS_PRIMARY_MONTHS,
    "recovery": MASK_HAGIBIS_RECOVERY_MONTHS,
}

TREATED_CODES = ("17", "16")
TREATED_NAMES = {"17": "Ishikawa", "16": "Toyama"}
PRIMARY_EXCLUDED_CODES = (
    "01", "02", "03", "04", "07", "15", "16", "17", "20", "33",
    "34", "38", "43",
)
STRICT_EXTRA_EXCLUDED_CODES = (
    "05", "06", "08", "12", "21", "26", "27", "28", "29", "31",
    "32", "35", "39", "44",
)
ALL_PREF_CODES = tuple(f"{code:02d}" for code in range(1, 48))
PRIMARY_DONOR_CODES = tuple(
    code for code in ALL_PREF_CODES if code not in PRIMARY_EXCLUDED_CODES
)
STRICT_DONOR_CODES = tuple(
    code for code in PRIMARY_DONOR_CODES
    if code not in STRICT_EXTRA_EXCLUDED_CODES
)
GOOD_FIT_RMSPE = 0.15
RMSPE_FIT_MULT = 5.0
POSITIVE_WEIGHT_TOL = 1e-6

SHEET_OUTCOMES = {
    "旧1-2": "total_stays",
    "旧2-2": "japanese_stays",
    "旧3-2": "foreign_stays",
}
PREF_NAMES_JA = (
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県",
    "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
    "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県",
    "沖縄県",
)
PREF_NAME_TO_CODE = dict(zip(PREF_NAMES_JA, ALL_PREF_CODES))
ANNUAL_RELEASES = {
    2011: (
        "jta_accommodation_2011_confirmed.xls",
        "d47b5caec1da4a2f986cee89636483283d1b4375c5a76f849ce0d32d4d681a1f",
    ),
    2012: (
        "jta_accommodation_2012_confirmed.xls",
        "3ece2333d8dd3014e95b9687a9609da9843ed02dafe56928ef9a8faccd1386fe",
    ),
    2013: (
        "jta_accommodation_2013_confirmed.xls",
        "fec002e6c1cac48de968fbafee57be6d5f043b53c20e389ced8e721dd0695882",
    ),
    2014: (
        "jta_accommodation_2014_confirmed.xls",
        "1546ef4319cc7c1bc6a6868ab849789187faa7d205908877473c5f765578307a",
    ),
    2015: (
        "jta_accommodation_2015_confirmed.xlsx",
        "d03b0b35d219e7cedd644f83badb214644c703f71eb924c15a0a241b28f50f13",
    ),
    2016: (
        "jta_accommodation_2016_confirmed.xlsx",
        "efeef94ea5a549e636c578d18af1a48fc4b982bfa0061ae734003f919d969ed4",
    ),
    2017: (
        "jta_accommodation_2017_confirmed.xlsx",
        "6ace13525563fd28ff02dc3cadbd7a39fd0c7056db30df1dd9cdbc73254b5ca2",
    ),
}
PREF_RE = re.compile(r"^(?P<code>\d{2})(?P<name>.+)$")
CELL_RE = re.compile(r"^(?P<column>[A-Z]+)(?P<row>\d+)$")
XML_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {
    "r": "http://schemas.openxmlformats.org/package/2006/relationships"
}
OFFICE_REL = (
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
)

EXPECTED_ARTIFACT_SHA256 = {
    "figures/fig1_scm_trajectories.png": (
        "bd72d7aa40aac89fbdea4c98e90964c3fb723ac88e53caf853e21fad7a98a657"
    ),
    "figures/fig2_gap_trajectories.png": (
        "6664ea09f8e55e83795b1dfeb9016a23ee14faf1e7ec8719512119873cdbaddd"
    ),
    "figures/fig3_placebo_distributions.png": (
        "8b4493618855c5edc1bf7a6558c23bd3f40974a554e633f822f23ca28bdd675e"
    ),
    "figures/fig4_v3_anchor_indices.png": (
        "d4634635464241e7bed5c7040b56788da0a4fc3d71e3dcc6d03d01dee3db34dd"
    ),
    "intime_placebo.csv": (
        "3570e8a032891813393d30a8e4ed3b112082213f018de77d102114f1ac21063e"
    ),
    "leave_one_out.csv": (
        "151319a8ef4f444953db2087fa5b4a6c62b2c9395fa83ef05751f37d039ad230"
    ),
    "metrics.json": (
        "8af45d7d583bf9687f00dae3aed437ddebd74d4c01202314720be21bc2992f44"
    ),
    "placebo_distributions.csv": (
        "5f826b5e06df609969cca075ac1c3fcb2fb2e329853e7b72f9283c96446f3749"
    ),
    "scm_weights.csv": (
        "94701d0c6bc987416326997a1069d10309b57e15453a6e39a9d9e071bf87c83b"
    ),
    "specification_summary.csv": (
        "820283199be89ae5335d22dc6df514a6b47fb1c2ad31851aa72285833113ed0b"
    ),
    "target_gap_trajectories.csv": (
        "ba40112813a45a89af5d2b14a07fcd35a18a5bdef770b3f2f32118e1b40f517f"
    ),
    "v3_anchor_indices.csv": (
        "03034000eac9db3710a3b0abd6b56d92c762d8e122853d1483d96c317b321858"
    ),
}


class FrozenDesignContradiction(RuntimeError):
    """Raised when accepted Arm 3 constants cannot all hold simultaneously."""


@dataclass(frozen=True)
class Specification:
    name: str
    outcome: str
    donor_codes: tuple[str, ...]
    pre_start_ym: int
    late_mask: tuple[int, ...] = ()
    hagibis_mask: str = "event"


BASE_SPECS = (
    Specification(
        "primary", "total_stays", PRIMARY_DONOR_CODES, PRIMARY_PRE_START_YM,
    ),
    Specification(
        "pre_50_months", "total_stays", PRIMARY_DONOR_CODES,
        SENSITIVITY_PRE_START_YM,
    ),
    Specification(
        "strict_donors", "total_stays", STRICT_DONOR_CODES,
        PRIMARY_PRE_START_YM,
    ),
    Specification(
        "mask_2018_06_09", "total_stays", PRIMARY_DONOR_CODES,
        PRIMARY_PRE_START_YM, MASK_2018_MONTHS,
    ),
    Specification(
        "japanese_only", "japanese_stays", PRIMARY_DONOR_CODES,
        PRIMARY_PRE_START_YM,
    ),
    Specification(
        "foreign_only", "foreign_stays", PRIMARY_DONOR_CODES,
        PRIMARY_PRE_START_YM,
    ),
)


def _specifications() -> tuple[Specification, ...]:
    """Apply each of ADR 0030's two Hagibis readings to the full battery."""
    specs = []
    for mask_name, hagibis_months in HAGIBIS_MASKS.items():
        for base in BASE_SPECS:
            name = (
                base.name if mask_name == "event"
                else f"{base.name}_hagibis_recovery"
            )
            specs.append(
                Specification(
                    name=name,
                    outcome=base.outcome,
                    donor_codes=base.donor_codes,
                    pre_start_ym=base.pre_start_ym,
                    late_mask=base.late_mask + hagibis_months,
                    hagibis_mask=mask_name,
                )
            )
    return tuple(specs)


SPECS = _specifications()


def _column_number(label: str) -> int:
    number = 0
    for char in label:
        number = number * 26 + ord(char) - ord("A") + 1
    return number


def _cell_position(reference: str) -> tuple[int, int]:
    match = CELL_RE.fullmatch(reference)
    if not match:
        raise ValueError(f"invalid XLSX cell reference: {reference!r}")
    return _column_number(match.group("column")), int(match.group("row"))


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(
            text.text or ""
            for text in (
                item.findall("./m:t", XML_NS)
                + item.findall("./m:r/m:t", XML_NS)
            )
        )
        for item in root.findall("m:si", XML_NS)
    ]


def _sheet_paths(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(
        archive.read("xl/_rels/workbook.xml.rels")
    )
    targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in relationships.findall("r:Relationship", REL_NS)
    }
    paths = {}
    for sheet in workbook.findall(".//m:sheet", XML_NS):
        target = targets[sheet.attrib[OFFICE_REL]]
        paths[sheet.attrib["name"]] = (
            target if target.startswith("xl/") else f"xl/{target}"
        )
    return paths


def _decode_cell(cell: ET.Element, shared: list[str]) -> object:
    """Decode one admitted XLSX cell.

    Callers must apply the date-column firewall before entering this function.
    """
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(
            text.text or "" for text in cell.findall(".//m:t", XML_NS)
        )
    value_node = cell.find("m:v", XML_NS)
    if value_node is None or value_node.text is None:
        return None
    if cell_type == "s":
        return shared[int(value_node.text)]
    if cell_type in {"str", "e"}:
        return value_node.text
    return float(value_node.text)


def _month_sequence(start_ym: int, end_ym: int) -> tuple[int, ...]:
    months = []
    year, month = divmod(start_ym, 100)
    while year * 100 + month <= end_ym:
        months.append(year * 100 + month)
        month += 1
        if month == 13:
            year += 1
            month = 1
    return tuple(months)


def validate_frozen_design() -> None:
    """Reject drift from the accepted design and ADR 0030 corrections."""
    checks = (
        ("primary pre-window", PRIMARY_PRE_START_YM, PRE_END_YM, 38),
        (
            "sensitivity pre-window",
            SENSITIVITY_PRE_START_YM,
            PRE_END_YM,
            50,
        ),
        ("confirmatory post-window", EVENT_YM, POST_END_YM, 58),
        ("late window", LATE_START_YM, LATE_END_YM, 24),
    )
    for label, start, end, expected in checks:
        actual = len(_month_sequence(start, end))
        if actual != expected:
            raise FrozenDesignContradiction(
                f"{label} {start}..{end} contains {actual} months, "
                f"not the accepted {expected}"
            )
    if HAGIBIS_MASKS != {
        "event": (201910,),
        "recovery": (201910, 201911, 201912),
    }:
        raise FrozenDesignContradiction("ADR 0030 Hagibis masks drifted")


def _parse_timeseries_sheet(
    archive: zipfile.ZipFile,
    path: str,
    shared: list[str],
    cap_ym: int,
) -> tuple[dict[str, str], dict[str, list[float]]]:
    """Decode labels plus outcome cells through ``cap_ym`` only."""
    if cap_ym > PANEL_CAP_YM:
        raise ValueError(
            f"Arm 3 load cap {cap_ym} exceeds frozen boundary {PANEL_CAP_YM}"
        )
    if cap_ym < 201101:
        raise ValueError("Arm 3 workbook series begins at 201101")
    months = _month_sequence(201101, cap_ym)
    first_data_column = 2  # B = 2011-01
    max_data_column = first_data_column + len(months) - 1
    labels: dict[str, str] = {}
    values: dict[str, list[float]] = {}
    header_months: dict[int, str] = {}

    with archive.open(path) as stream:
        for _, cell in ET.iterparse(stream, events=("end",)):
            if cell.tag != f"{{{XML_NS['m']}}}c":
                continue
            column, row = _cell_position(cell.attrib["r"])

            # Structural firewall: never call _decode_cell on an outcome cell
            # outside the admitted date columns.
            if row >= 5 and column > max_data_column:
                cell.clear()
                continue
            if row == 4 and first_data_column <= column <= max_data_column:
                header_months[column] = str(_decode_cell(cell, shared))
            elif row >= 5 and column == 1:
                label = _decode_cell(cell, shared)
                if isinstance(label, str):
                    match = PREF_RE.fullmatch(label.replace(" ", "").replace("　", ""))
                    if match and match.group("code") in ALL_PREF_CODES:
                        labels[match.group("code")] = match.group("name")
            elif (
                row >= 5
                and first_data_column <= column <= max_data_column
            ):
                row_label_cell = None
                # Data rows are fixed by the official sheet: national row 5,
                # prefectures 01..47 in rows 6..52.
                pref_index = row - 5
                if 1 <= pref_index <= 47:
                    row_label_cell = f"{pref_index:02d}"
                if row_label_cell is not None:
                    decoded = _decode_cell(cell, shared)
                    if decoded is None:
                        raise ValueError(
                            f"missing value at {cell.attrib['r']} in {path}"
                        )
                    values.setdefault(row_label_cell, []).append(float(decoded))
            cell.clear()

    expected_headers = {
        first_data_column + index: f"{ym % 100}月"
        for index, ym in enumerate(months)
    }
    if header_months != expected_headers:
        raise ValueError(f"month-axis drift in {path}")
    if set(labels) != set(ALL_PREF_CODES):
        raise ValueError(f"prefecture-label drift in {path}")
    if set(values) != set(ALL_PREF_CODES):
        raise ValueError(f"prefecture-value rows drift in {path}")
    bad_lengths = {
        code: len(series)
        for code, series in values.items()
        if len(series) != len(months)
    }
    if bad_lengths:
        raise ValueError(f"incomplete admitted series in {path}: {bad_lengths}")
    return labels, values


def load_prefecture_panel(
    workbook: Path = WORKBOOK, cap_ym: int = PANEL_CAP_YM
) -> pd.DataFrame:
    """Load the 47-prefecture monthly panel without decoding post-cap outcomes."""
    with zipfile.ZipFile(workbook) as archive:
        shared = _shared_strings(archive)
        paths = _sheet_paths(archive)
        missing = set(SHEET_OUTCOMES) - set(paths)
        if missing:
            raise ValueError(f"required 推移表 sheets missing: {sorted(missing)}")
        parsed = {
            outcome: _parse_timeseries_sheet(
                archive, paths[sheet], shared, cap_ym
            )
            for sheet, outcome in SHEET_OUTCOMES.items()
        }

    months = _month_sequence(201101, cap_ym)
    canonical_labels = parsed["total_stays"][0]
    for outcome, (labels, _) in parsed.items():
        if labels != canonical_labels:
            raise ValueError(f"prefecture labels disagree for {outcome}")
    rows = []
    for code in ALL_PREF_CODES:
        for index, ym in enumerate(months):
            row = {
                "pref_code": code,
                "pref_name": canonical_labels[code],
                "ym": ym,
            }
            for outcome, (_, values) in parsed.items():
                value = values[code][index]
                if not np.isfinite(value) or value <= 0:
                    raise ValueError(
                        f"{outcome} must be positive at {code}/{ym}: {value}"
                    )
                row[outcome] = value
            rows.append(row)
    panel = pd.DataFrame(rows)
    if panel["ym"].max() > PANEL_CAP_YM:
        raise AssertionError("post-2019 value escaped the load-time firewall")
    if panel.duplicated(["pref_code", "ym"]).any():
        raise ValueError("duplicate prefecture-month keys")
    return panel


def _normalize_prefecture_label(value: object) -> str:
    label = str(value).replace(" ", "").replace("　", "")
    return re.sub(r"^\d{2}", "", label)


def _annual_sheet_rows(
    workbook: object, sheet_name: str, legacy_xls: bool
) -> list[tuple[object, ...]]:
    if legacy_xls:
        sheet = workbook.sheet_by_name(sheet_name)
        return [
            tuple(sheet.cell_value(row, column) for column in range(sheet.ncols))
            for row in range(sheet.nrows)
        ]
    sheet = workbook[sheet_name]
    return [tuple(row) for row in sheet.iter_rows(values_only=True)]


def _annual_month_rows(
    rows: list[tuple[object, ...]], year: int, month: int, source: Path
) -> list[dict[str, object]]:
    """Parse all-establishment stays from one confirmed-release Table 4."""
    if len(rows) < 54 or "延べ宿泊者数" not in str(rows[0][0]):
        raise ValueError(f"annual release title drift in {source.name}")
    header = rows[3]
    normalized = [
        str(value).replace("\n", "").replace(" ", "").replace("　", "")
        for value in header
    ]
    total_columns = [
        index for index, value in enumerate(normalized)
        if value.startswith("延べ宿泊者数")
    ]
    foreign_columns = [
        index for index, value in enumerate(normalized)
        if value.startswith("うち外国人延べ宿泊者数")
    ]
    if len(total_columns) != 1 or len(foreign_columns) != 1:
        raise ValueError(f"annual release outcome-header drift in {source.name}")
    total_column = total_columns[0]
    foreign_column = foreign_columns[0]

    parsed = []
    seen_codes = set()
    for row in rows:
        if not row:
            continue
        pref_name = _normalize_prefecture_label(row[0])
        code = PREF_NAME_TO_CODE.get(pref_name)
        if code is None:
            continue
        if code in seen_codes:
            raise ValueError(
                f"duplicate prefecture {code} in {source.name}/{year}-{month:02d}"
            )
        seen_codes.add(code)
        total = float(row[total_column])
        foreign = float(row[foreign_column])
        japanese = total - foreign
        if (
            not np.isfinite([total, japanese, foreign]).all()
            or total <= 0
            or japanese < 0
            or foreign < 0
        ):
            raise ValueError(
                f"invalid annual stays at {source.name}/{code}/{year}{month:02d}"
            )
        parsed.append(
            {
                "pref_code": code,
                "ym": year * 100 + month,
                "total_stays": total,
                "japanese_stays": japanese,
                "foreign_stays": foreign,
            }
        )
    if seen_codes != set(ALL_PREF_CODES):
        raise ValueError(
            f"annual release prefecture drift in {source.name}/{year}-{month:02d}"
        )
    return parsed


def load_annual_release_panel(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Parse and checksum-verify the seven confirmed annual releases."""
    records = []
    for year, (filename, expected_sha256) in ANNUAL_RELEASES.items():
        source = raw_dir / filename
        actual_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise ValueError(
                f"annual release SHA-256 mismatch for {filename}: "
                f"expected {expected_sha256}, got {actual_sha256}"
            )
        legacy_xls = source.suffix == ".xls"
        workbook = (
            xlrd.open_workbook(source, on_demand=True)
            if legacy_xls
            else openpyxl.load_workbook(
                source, read_only=True, data_only=True
            )
        )
        try:
            for month in range(1, 13):
                rows = _annual_sheet_rows(
                    workbook, f"第4表({month}月)", legacy_xls
                )
                records.extend(
                    _annual_month_rows(rows, year, month, source)
                )
        finally:
            workbook.release_resources() if legacy_xls else workbook.close()

    panel = pd.DataFrame(records)
    if len(panel) != 7 * 12 * 47:
        raise ValueError(f"annual release panel has {len(panel)} rows, not 3948")
    if panel.duplicated(["pref_code", "ym"]).any():
        raise ValueError("duplicate prefecture-month keys in annual releases")
    if (
        panel["ym"].min() != 201101
        or panel["ym"].max() != 201712
        or panel["pref_code"].nunique() != 47
    ):
        raise ValueError("annual release coverage drift")
    return panel.sort_values(["pref_code", "ym"]).reset_index(drop=True)


def fw_scm_sparse(
    A: np.ndarray, b: np.ndarray, iters: int = 1000, tol: float = 1e-9
) -> np.ndarray:
    """Direction D's deterministic Frank-Wolfe simplex solver, verbatim."""
    n = A.shape[1]
    err = np.array([np.mean((A[:, j] - b) ** 2) for j in range(n)])
    w = np.zeros(n)
    w[np.argmin(err)] = 1.0
    r = A @ w - b
    for _ in range(iters):
        grad = A.T @ r
        j = np.argmin(grad)
        direction = A[:, j] - A @ w
        denom = direction @ direction
        if denom < tol:
            break
        gamma = np.clip(-(r @ direction) / denom, 0.0, 1.0)
        if gamma < tol:
            break
        w *= 1 - gamma
        w[j] += gamma
        r = r + gamma * direction
    return w


def _wide(panel: pd.DataFrame, outcome: str) -> pd.DataFrame:
    return panel.pivot(index="pref_code", columns="ym", values=outcome)


def _indices(months: list[int], start: int, end: int) -> list[int]:
    return [index for index, ym in enumerate(months) if start <= ym <= end]


def _fit(
    wide: pd.DataFrame,
    target_code: str,
    donor_codes: tuple[str, ...],
    months: list[int],
    pre_start_ym: int,
    pre_end_ym: int,
    iters: int = 1000,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    pre_idx = _indices(months, pre_start_ym, pre_end_ym)
    if not pre_idx or months[max(pre_idx)] >= EVENT_YM:
        raise AssertionError("SCM weights must be fit only on pre-event months")
    donor_all = np.log(wide.loc[list(donor_codes), months].to_numpy(float))
    actual = np.log(wide.loc[target_code, months].to_numpy(float))
    weights = fw_scm_sparse(
        donor_all[:, pre_idx].T, actual[pre_idx], iters=iters
    )
    synthetic = weights @ donor_all
    return weights, actual, synthetic, pre_idx


def _placebos(
    wide: pd.DataFrame,
    donor_codes: tuple[str, ...],
    months: list[int],
    pre_start_ym: int,
    pre_end_ym: int,
    opening_months: tuple[int, ...],
    late_months: list[int],
) -> pd.DataFrame:
    pre_idx = _indices(months, pre_start_ym, pre_end_ym)
    open_idx = [months.index(ym) for ym in opening_months]
    late_idx = [months.index(ym) for ym in late_months]
    donor_all = np.log(wide.loc[list(donor_codes), months].to_numpy(float))
    rows = []
    for index, code in enumerate(donor_codes):
        keep = np.ones(len(donor_codes), dtype=bool)
        keep[index] = False
        weights = fw_scm_sparse(
            donor_all[keep][:, pre_idx].T,
            donor_all[index, pre_idx],
            iters=400,
        )
        gap = donor_all[index] - weights @ donor_all[keep]
        rows.append(
            {
                "placebo_code": code,
                "pre_rmspe": float(np.sqrt(np.mean(gap[pre_idx] ** 2))),
                "opening_gap_log": float(np.mean(gap[open_idx])),
                "late_gap_log": float(np.mean(gap[late_idx])),
            }
        )
    return pd.DataFrame(rows)


def _p_values(null: np.ndarray, treated: float) -> tuple[float, float]:
    one_sided = (1 + np.sum(null >= treated)) / (1 + len(null))
    two_sided = (
        1 + np.sum(np.abs(null) >= abs(treated))
    ) / (1 + len(null))
    return float(one_sided), float(two_sided)


def _run_spec(
    panel: pd.DataFrame, spec: Specification
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    wide = _wide(panel, spec.outcome)
    months = sorted(int(ym) for ym in wide.columns)
    pre_idx = _indices(months, spec.pre_start_ym, PRE_END_YM)
    post_idx = _indices(months, EVENT_YM, POST_END_YM)
    opening_idx = [months.index(ym) for ym in OPENING_MONTHS]
    first12_idx = [months.index(ym) for ym in FIRST_12_POST_MONTHS]
    late_months = [
        ym for ym in months
        if LATE_START_YM <= ym <= LATE_END_YM and ym not in spec.late_mask
    ]
    late_idx = [months.index(ym) for ym in late_months]
    placebos = _placebos(
        wide, spec.donor_codes, months, spec.pre_start_ym, PRE_END_YM,
        OPENING_MONTHS, late_months,
    )
    placebos.insert(0, "hagibis_mask", spec.hagibis_mask)
    placebos.insert(0, "specification", spec.name)
    summaries = []
    weight_rows = []
    gap_rows = []
    loo_rows = []
    for target_code in TREATED_CODES:
        weights, actual, synthetic, fit_idx = _fit(
            wide, target_code, spec.donor_codes, months, spec.pre_start_ym,
            PRE_END_YM,
        )
        if fit_idx != pre_idx:
            raise AssertionError("declared and fitted pre-windows differ")
        gap = actual - synthetic
        pre_rmspe = float(np.sqrt(np.mean(gap[pre_idx] ** 2)))
        opening_gap = float(np.mean(gap[opening_idx]))
        late_gap = float(np.mean(gap[late_idx]))
        first12_gap = float(np.mean(gap[first12_idx]))
        keep = placebos["pre_rmspe"].to_numpy() <= (
            RMSPE_FIT_MULT * pre_rmspe
        )
        opening_p1, opening_p2 = _p_values(
            placebos.loc[keep, "opening_gap_log"].to_numpy(), opening_gap
        )
        late_p1, late_p2 = _p_values(
            placebos.loc[keep, "late_gap_log"].to_numpy(), late_gap
        )
        n_kept = int(keep.sum())
        summaries.append(
            {
                "specification": spec.name,
                "hagibis_mask": spec.hagibis_mask,
                "outcome": spec.outcome,
                "target_code": target_code,
                "target": TREATED_NAMES[target_code],
                "pre_start_ym": spec.pre_start_ym,
                "pre_end_ym": PRE_END_YM,
                "n_pre_months": len(pre_idx),
                "n_donors": len(spec.donor_codes),
                "pre_rmspe": pre_rmspe,
                "good_fit": pre_rmspe <= GOOD_FIT_RMSPE,
                "opening_gap_log": opening_gap,
                "opening_pct": 100 * (np.exp(opening_gap) - 1),
                "opening_p_1s": opening_p1,
                "opening_p_2s": opening_p2,
                "post_mean_gap_log": float(np.mean(gap[post_idx])),
                "late_gap_log": late_gap,
                "late_pct": 100 * (np.exp(late_gap) - 1),
                "late_p_1s": late_p1,
                "late_p_2s": late_p2,
                "first12_gap_log": first12_gap,
                "decay_ratio": late_gap / first12_gap,
                "n_placebos_kept": n_kept,
                "p_floor": 1 / (n_kept + 1),
                "directional_only_floor": n_kept < 19,
                "late_months_used": len(late_idx),
            }
        )
        for donor_code, weight in zip(spec.donor_codes, weights):
            weight_rows.append(
                {
                    "specification": spec.name,
                    "hagibis_mask": spec.hagibis_mask,
                    "target_code": target_code,
                    "donor_code": donor_code,
                    "weight": float(weight),
                    "positive_weight": bool(weight > POSITIVE_WEIGHT_TOL),
                }
            )
        if spec.name == "primary":
            gap_rows.extend(
                {
                    "target_code": target_code,
                    "target": TREATED_NAMES[target_code],
                    "ym": ym,
                    "actual_log": float(actual[index]),
                    "synthetic_log": float(synthetic[index]),
                    "gap_log": float(gap[index]),
                }
                for index, ym in enumerate(months)
            )
        if spec.name in {"primary", "primary_hagibis_recovery"}:
            positive = np.flatnonzero(weights > POSITIVE_WEIGHT_TOL)
            loo_rows.append(
                {
                    "specification": spec.name,
                    "hagibis_mask": spec.hagibis_mask,
                    "target_code": target_code,
                    "target": TREATED_NAMES[target_code],
                    "dropped_donor_code": "(none: baseline)",
                    "dropped_weight": np.nan,
                    "opening_gap_log": opening_gap,
                    "opening_pct": 100 * (np.exp(opening_gap) - 1),
                    "late_gap_log": late_gap,
                    "late_pct": 100 * (np.exp(late_gap) - 1),
                }
            )
            for donor_index in positive:
                donor_keep = np.ones(len(spec.donor_codes), dtype=bool)
                donor_keep[donor_index] = False
                reduced_codes = tuple(
                    code for index, code in enumerate(spec.donor_codes)
                    if donor_keep[index]
                )
                _, loo_actual, loo_synthetic, _ = _fit(
                    wide, target_code, reduced_codes, months,
                    spec.pre_start_ym, PRE_END_YM,
                )
                loo_gap = loo_actual - loo_synthetic
                loo_opening = float(np.mean(loo_gap[opening_idx]))
                loo_late = float(np.mean(loo_gap[late_idx]))
                loo_rows.append(
                    {
                        "specification": spec.name,
                        "hagibis_mask": spec.hagibis_mask,
                        "target_code": target_code,
                        "target": TREATED_NAMES[target_code],
                        "dropped_donor_code": spec.donor_codes[donor_index],
                        "dropped_weight": float(weights[donor_index]),
                        "opening_gap_log": loo_opening,
                        "opening_pct": 100 * (np.exp(loo_opening) - 1),
                        "late_gap_log": loo_late,
                        "late_pct": 100 * (np.exp(loo_late) - 1),
                    }
                )
    return (
        pd.DataFrame(summaries),
        pd.DataFrame(weight_rows),
        pd.DataFrame(gap_rows),
        pd.DataFrame(loo_rows),
        placebos,
    )


def _run_intime(panel: pd.DataFrame) -> pd.DataFrame:
    wide = _wide(panel, "total_stays")
    months = sorted(int(ym) for ym in wide.columns)
    fake_opening = (201403, 201404)
    fake_open_idx = [months.index(ym) for ym in fake_opening]
    placebos = _placebos(
        wide,
        PRIMARY_DONOR_CODES,
        months,
        PRIMARY_PRE_START_YM,
        INTIME_PRE_END_YM,
        fake_opening,
        list(fake_opening),
    )
    rows = []
    for target_code in TREATED_CODES:
        _, actual, synthetic, pre_idx = _fit(
            wide,
            target_code,
            PRIMARY_DONOR_CODES,
            months,
            PRIMARY_PRE_START_YM,
            INTIME_PRE_END_YM,
        )
        gap = actual - synthetic
        pre_rmspe = float(np.sqrt(np.mean(gap[pre_idx] ** 2)))
        fake_gap = float(np.mean(gap[fake_open_idx]))
        keep = placebos["pre_rmspe"].to_numpy() <= (
            RMSPE_FIT_MULT * pre_rmspe
        )
        p1, p2 = _p_values(
            placebos.loc[keep, "opening_gap_log"].to_numpy(), fake_gap
        )
        rows.append(
            {
                "target_code": target_code,
                "target": TREATED_NAMES[target_code],
                "event_ym": INTIME_EVENT_YM,
                "pre_start_ym": PRIMARY_PRE_START_YM,
                "pre_end_ym": INTIME_PRE_END_YM,
                "n_pre_months": len(pre_idx),
                "pre_rmspe": pre_rmspe,
                "backdated_opening_gap_log": fake_gap,
                "backdated_opening_pct": 100 * (np.exp(fake_gap) - 1),
                "p_backdated_opening_1s": p1,
                "p_backdated_opening_2s": p2,
                "n_placebos_kept": int(keep.sum()),
            }
        )
    return pd.DataFrame(rows)


def verify_vintage_crosscheck(
    canonical_panel: pd.DataFrame,
    positive_weight_codes: tuple[str, ...],
    annual_panel: pd.DataFrame,
) -> None:
    """Require byte-level numeric agreement with corrected 2011–2017 annuals.

    ``annual_panel`` is the tidy output expected from the annual-release
    parser: the same key and outcome columns as ``load_prefecture_panel``.
    The frozen oracle interval is 2012-01..2016-12 and covers both treated
    units plus every positive-weight donor from the primary fits.
    """
    required = {
        "pref_code", "ym", "total_stays", "japanese_stays", "foreign_stays"
    }
    if not required.issubset(annual_panel.columns):
        raise ValueError(
            f"annual vintage panel missing columns: "
            f"{sorted(required - set(annual_panel.columns))}"
        )
    codes = tuple(sorted(set(TREATED_CODES) | set(positive_weight_codes)))
    columns = ["pref_code", "ym", "total_stays", "japanese_stays", "foreign_stays"]
    canonical = canonical_panel.loc[
        canonical_panel["pref_code"].isin(codes)
        & canonical_panel["ym"].between(201201, 201612),
        columns,
    ].copy()
    annual = annual_panel.loc[
        annual_panel["pref_code"].astype(str).str.zfill(2).isin(codes)
        & annual_panel["ym"].between(201201, 201612),
        columns,
    ].copy()
    annual["pref_code"] = annual["pref_code"].astype(str).str.zfill(2)
    merged = canonical.merge(
        annual,
        on=["pref_code", "ym"],
        how="outer",
        validate="one_to_one",
        suffixes=("_canonical", "_annual"),
        indicator=True,
    )
    if not (merged["_merge"] == "both").all():
        raise AssertionError("annual vintage oracle key mismatch")
    for outcome in ("total_stays", "japanese_stays", "foreign_stays"):
        if not np.array_equal(
            merged[f"{outcome}_canonical"].to_numpy(),
            merged[f"{outcome}_annual"].to_numpy(),
        ):
            mismatch = merged.loc[
                merged[f"{outcome}_canonical"]
                != merged[f"{outcome}_annual"],
                ["pref_code", "ym"],
            ].iloc[0]
            raise AssertionError(
                f"annual vintage mismatch for {outcome} at "
                f"{mismatch.pref_code}/{int(mismatch.ym)}"
            )


VintageChecker = Callable[
    [pd.DataFrame, tuple[str, ...], pd.DataFrame], None
]


def load_v3_anchor_data(
    anchor_dir: Path = ANCHOR_DIR,
) -> tuple[pd.DataFrame, dict[str, dict[str, object]]]:
    """Load ADR 0030's two descriptive V3 anchor series."""
    sources = {
        "kanazawa_lodging_guests": (
            anchor_dir / "kanazawa_lodging_guests_monthly.csv"
        ),
        "kanazawa_19_facility_visits": (
            anchor_dir / "kanazawa_19_facility_visits_monthly.csv"
        ),
    }
    indexed = []
    metrics = {}
    for label, path in sources.items():
        frame = pd.read_csv(path)
        if (
            len(frame) != 72
            or frame["ym"].min() != 201401
            or frame["ym"].max() != 201912
            or frame["ym"].duplicated().any()
        ):
            raise ValueError(f"V3 anchor coverage drift in {path.name}")
        frame = frame[["ym", "year", "month", "value", "unit"]].copy()
        if (frame["value"] <= 0).any():
            raise ValueError(f"nonpositive V3 anchor value in {path.name}")
        frame.insert(0, "anchor_series", label)
        baseline = frame.loc[frame["year"] == 2014].set_index("month")["value"]
        frame["same_month_2014_index"] = (
            frame["value"] / frame["month"].map(baseline) * 100
        )
        indexed.append(frame)

        opening = frame["ym"].isin(OPENING_MONTHS)
        opening_baseline = (
            (frame["year"] == 2014)
            & frame["month"].isin([ym % 100 for ym in OPENING_MONTHS])
        )
        annual_2014 = float(frame.loc[frame["year"] == 2014, "value"].sum())
        annual_2015 = float(frame.loc[frame["year"] == 2015, "value"].sum())
        annual_2019 = float(frame.loc[frame["year"] == 2019, "value"].sum())
        late_annual_mean = float(
            frame.loc[frame["year"].isin([2018, 2019])]
            .groupby("year")["value"]
            .sum()
            .mean()
        )
        opening_change = 100 * (
            frame.loc[opening, "value"].sum()
            / frame.loc[opening_baseline, "value"].sum()
            - 1
        )
        late_change = 100 * (late_annual_mean / annual_2014 - 1)
        metrics[label] = {
            "unit": str(frame["unit"].iloc[0]),
            "opening_2015_vs_same_months_2014_pct": float(opening_change),
            "annual_2015_vs_2014_pct": float(
                100 * (annual_2015 / annual_2014 - 1)
            ),
            "late_2018_2019_mean_vs_2014_pct": float(late_change),
            "annual_2019_vs_2014_pct": float(
                100 * (annual_2019 / annual_2014 - 1)
            ),
            "surge_positive": bool(opening_change > 0),
            "persistence_positive": bool(late_change > 0),
        }
    return pd.concat(indexed, ignore_index=True), metrics


def _criterion_pass(row: pd.Series, gap: str, p_value: str) -> bool:
    return bool(
        row[gap] > 0
        and row[p_value] <= 0.05
        and not row["directional_only_floor"]
    )


def _directional_contrast(
    ishikawa: pd.Series, toyama: pd.Series
) -> bool:
    return bool(
        ishikawa["decay_ratio"] > toyama["decay_ratio"]
        and ishikawa["late_gap_log"] > toyama["late_gap_log"]
    )


def build_battery(
    panel: pd.DataFrame,
    annual_panel: pd.DataFrame,
    v3_anchor: tuple[pd.DataFrame, dict[str, dict[str, object]]],
    vintage_checker: VintageChecker = verify_vintage_crosscheck,
) -> dict[str, pd.DataFrame | dict]:
    """Run primary, falsification, and declared sensitivity analyses."""
    validate_frozen_design()
    primary_result = _run_spec(panel, SPECS[0])
    primary_summary, primary_weights = primary_result[:2]
    positive_codes = tuple(
        sorted(
            primary_weights.loc[
                primary_weights["positive_weight"], "donor_code"
            ].unique()
        )
    )
    # The source-vintage gate precedes all non-primary sensitivity work.
    vintage_checker(panel, positive_codes, annual_panel)

    runs = [primary_result]
    runs.extend(_run_spec(panel, spec) for spec in SPECS[1:])
    summaries = [run[0] for run in runs]
    weights = [run[1] for run in runs]
    primary_gaps = [run[2] for run in runs if not run[2].empty]
    leave_one_out = [run[3] for run in runs if not run[3].empty]
    placebo_distributions = [run[4] for run in runs]
    summary = pd.concat(summaries, ignore_index=True)
    all_weights = pd.concat(weights, ignore_index=True)
    gaps = pd.concat(primary_gaps, ignore_index=True)
    loo = pd.concat(leave_one_out, ignore_index=True)
    placebos = pd.concat(placebo_distributions, ignore_index=True)
    intime = _run_intime(panel)
    v3_indices, v3_series_metrics = v3_anchor

    primary = primary_summary.copy()
    recovery = summary.loc[
        summary["specification"] == "primary_hagibis_recovery"
    ].copy()
    ishikawa = primary.loc[primary["target_code"] == "17"].iloc[0]
    toyama = primary.loc[primary["target_code"] == "16"].iloc[0]
    recovery_ishikawa = recovery.loc[
        recovery["target_code"] == "17"
    ].iloc[0]
    recovery_toyama = recovery.loc[
        recovery["target_code"] == "16"
    ].iloc[0]
    ishikawa_loo = loo.loc[
        (loo["target_code"] == "17")
        & (loo["specification"] == "primary")
        & (loo["dropped_donor_code"] != "(none: baseline)")
    ]
    ishikawa_intime = intime.loc[intime["target_code"] == "17"].iloc[0]
    v1a = _criterion_pass(ishikawa, "opening_gap_log", "opening_p_1s")
    v1b = bool(ishikawa_intime["p_backdated_opening_1s"] > 0.10)
    v1c = bool(ishikawa_loo["opening_gap_log"].min() > 0)
    v2a = _criterion_pass(ishikawa, "late_gap_log", "late_p_1s")
    v2a_recovery = _criterion_pass(
        recovery_ishikawa, "late_gap_log", "late_p_1s"
    )
    v2b = _directional_contrast(ishikawa, toyama)
    v2b_recovery = _directional_contrast(
        recovery_ishikawa, recovery_toyama
    )
    v3_met = all(
        item["surge_positive"] and item["persistence_positive"]
        for item in v3_series_metrics.values()
    )

    def result_record(row: pd.Series) -> dict[str, object]:
        excluded = {"specification", "outcome", "target_code", "target"}
        record = {}
        for key, value in row.items():
            if key in excluded:
                continue
            if isinstance(value, (bool, np.bool_)):
                record[key] = bool(value)
            elif isinstance(value, (int, np.integer)):
                record[key] = int(value)
            elif isinstance(value, (float, np.floating)):
                record[key] = float(value)
            else:
                record[key] = value
        return record

    metrics = {
        "design": {
            "event_ym": EVENT_YM,
            "intime_event_ym": INTIME_EVENT_YM,
            "panel_cap_ym": PANEL_CAP_YM,
            "primary_pre_window": "2012-01..2015-02",
            "sensitivity_pre_window": "2011-01..2015-02",
            "post_window": "2015-03..2019-12",
            "opening_window": "2015-03..2015-04",
            "late_window": "2018-01..2019-12",
            "good_fit_rmspe": GOOD_FIT_RMSPE,
            "rmspe_fit_mult": RMSPE_FIT_MULT,
            "primary_donors": list(PRIMARY_DONOR_CODES),
            "strict_donors": list(STRICT_DONOR_CODES),
            "mask_2018_months": list(MASK_2018_MONTHS),
            "hagibis_masks": {
                key: list(value) for key, value in HAGIBIS_MASKS.items()
            },
            "specification_count": len(SPECS),
        },
        "vintage_crosscheck": {
            "status": "passed",
            "window": "2012-01..2016-12",
            "treated_and_positive_weight_donors": (
                len(set(TREATED_CODES) | set(positive_codes))
            ),
            "outcome_cells_compared": (
                len(set(TREATED_CODES) | set(positive_codes)) * 60 * 3
            ),
        },
        "positive_weight_donors_primary": list(positive_codes),
        "primary": {
            row["target"].lower(): result_record(pd.Series(row))
            for row in primary.to_dict("records")
        },
        "sensitivities": [
            {
                "specification": row["specification"],
                "target": row["target"],
                **result_record(pd.Series(row)),
            }
            for row in summary.loc[
                summary["specification"] != "primary"
            ].to_dict("records")
        ],
        "success_criteria": {
            "V1a": {
                "met": v1a,
                "opening_gap_log": float(ishikawa["opening_gap_log"]),
                "opening_pct": float(ishikawa["opening_pct"]),
                "p_1s": float(ishikawa["opening_p_1s"]),
                "p_2s": float(ishikawa["opening_p_2s"]),
                "pre_rmspe": float(ishikawa["pre_rmspe"]),
                "good_fit": bool(ishikawa["good_fit"]),
                "directional_only_floor": bool(
                    ishikawa["directional_only_floor"]
                ),
            },
            "V1b": {
                "met": v1b,
                "backdated_opening_gap_log": float(
                    ishikawa_intime["backdated_opening_gap_log"]
                ),
                "backdated_opening_pct": float(
                    ishikawa_intime["backdated_opening_pct"]
                ),
                "p_1s": float(
                    ishikawa_intime["p_backdated_opening_1s"]
                ),
                "p_2s": float(
                    ishikawa_intime["p_backdated_opening_2s"]
                ),
            },
            "V1c": {
                "met": v1c,
                "opening_gap_log_range": [
                    float(ishikawa_loo["opening_gap_log"].min()),
                    float(ishikawa_loo["opening_gap_log"].max()),
                ],
                "opening_pct_range": [
                    float(ishikawa_loo["opening_pct"].min()),
                    float(ishikawa_loo["opening_pct"].max()),
                ],
                "leave_one_out_fits": len(ishikawa_loo),
            },
            "V2a": {
                "met": v2a,
                "late_gap_log": float(ishikawa["late_gap_log"]),
                "late_pct": float(ishikawa["late_pct"]),
                "p_1s": float(ishikawa["late_p_1s"]),
                "p_2s": float(ishikawa["late_p_2s"]),
                "directional_only_floor": bool(
                    ishikawa["directional_only_floor"]
                ),
            },
            "V2b": {
                "met": v2b,
                "ishikawa_decay_ratio": float(ishikawa["decay_ratio"]),
                "toyama_decay_ratio": float(toyama["decay_ratio"]),
                "ishikawa_late_gap_log": float(ishikawa["late_gap_log"]),
                "toyama_late_gap_log": float(toyama["late_gap_log"]),
            },
            "V3": {
                "outcome": (
                    "met_descriptively"
                    if v3_met else "not_met_descriptively"
                ),
                "series": v3_series_metrics,
                "confirmatory": False,
            },
        },
        "tiers": {
            "V1": {
                "outcome": "pass" if all((v1a, v1b, v1c)) else "fail",
                "components": {"V1a": v1a, "V1b": v1b, "V1c": v1c},
            },
            "V2": {
                "outcome": "pass" if all((v2a, v2b)) else "fail",
                "components": {"V2a": v2a, "V2b": v2b},
            },
            "V3": {
                "outcome": (
                    "met_descriptively"
                    if v3_met else "not_met_descriptively"
                ),
                "confirmatory": False,
            },
        },
        "hagibis_comparison": {
            "primary_event_mask": {
                "months": list(MASK_HAGIBIS_PRIMARY_MONTHS),
                "V2a": v2a,
                "V2b": v2b,
                "ishikawa_late_gap_log": float(ishikawa["late_gap_log"]),
                "ishikawa_late_pct": float(ishikawa["late_pct"]),
                "ishikawa_late_p_1s": float(ishikawa["late_p_1s"]),
            },
            "sensitivity_recovery_mask": {
                "months": list(MASK_HAGIBIS_RECOVERY_MONTHS),
                "V2a": v2a_recovery,
                "V2b": v2b_recovery,
                "ishikawa_late_gap_log": float(
                    recovery_ishikawa["late_gap_log"]
                ),
                "ishikawa_late_pct": float(
                    recovery_ishikawa["late_pct"]
                ),
                "ishikawa_late_p_1s": float(
                    recovery_ishikawa["late_p_1s"]
                ),
            },
            "V2a_disagreement": bool(v2a != v2a_recovery),
        },
    }
    return {
        "summary": summary,
        "weights": all_weights,
        "primary_gaps": gaps,
        "intime": intime,
        "leave_one_out": loo,
        "placebo_distributions": placebos,
        "v3_anchor_indices": v3_indices,
        "metrics": metrics,
    }


def write_outputs(
    results: dict[str, pd.DataFrame | dict], out_dir: Path = OUT_DIR
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    filenames = {
        "summary": "specification_summary.csv",
        "weights": "scm_weights.csv",
        "primary_gaps": "target_gap_trajectories.csv",
        "intime": "intime_placebo.csv",
        "leave_one_out": "leave_one_out.csv",
        "placebo_distributions": "placebo_distributions.csv",
        "v3_anchor_indices": "v3_anchor_indices.csv",
    }
    for key, filename in filenames.items():
        frame = results[key]
        assert isinstance(frame, pd.DataFrame)
        frame.to_csv(out_dir / filename, index=False, lineterminator="\n")
    metrics = results["metrics"]
    assert isinstance(metrics, dict)
    (out_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_figures(results, out_dir / "figures")


def write_figures(
    results: dict[str, pd.DataFrame | dict], figure_dir: Path
) -> None:
    """Write deterministic, result-only Arm 3 figures."""
    os.environ["MPLCONFIGDIR"] = str(
        Path(tempfile.gettempdir()) / "arm3-kanazawa-matplotlib"
    )
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    figure_dir.mkdir(parents=True, exist_ok=True)
    save_options = {
        "dpi": 160,
        "facecolor": "white",
        "metadata": {"Software": "Matplotlib"},
    }
    gaps = results["primary_gaps"]
    summary = results["summary"]
    placebos = results["placebo_distributions"]
    anchors = results["v3_anchor_indices"]
    assert isinstance(gaps, pd.DataFrame)
    assert isinstance(summary, pd.DataFrame)
    assert isinstance(placebos, pd.DataFrame)
    assert isinstance(anchors, pd.DataFrame)

    dates = pd.to_datetime(gaps["ym"].astype(str), format="%Y%m")
    fig, axes = plt.subplots(2, 1, figsize=(8.5, 6), sharex=True)
    for axis, target in zip(axes, ("Ishikawa", "Toyama")):
        frame = gaps.loc[gaps["target"] == target]
        target_dates = dates.loc[frame.index]
        axis.plot(target_dates, frame["actual_log"], label=target, linewidth=1.3)
        axis.plot(
            target_dates,
            frame["synthetic_log"],
            label=f"Synthetic {target}",
            linewidth=1.3,
        )
        axis.axvline(
            pd.Timestamp("2015-03-01"),
            color="black",
            linestyle="--",
            linewidth=0.9,
        )
        axis.set_ylabel("log(stays)")
        axis.legend(frameon=False, ncol=2)
    axes[0].set_title("Arm 3 treated and synthetic trajectories")
    fig.tight_layout()
    fig.savefig(
        figure_dir / "fig1_scm_trajectories.png", **save_options
    )
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(8.5, 3.8))
    for target in ("Ishikawa", "Toyama"):
        frame = gaps.loc[gaps["target"] == target]
        target_dates = dates.loc[frame.index]
        axis.plot(
            target_dates,
            100 * (np.exp(frame["gap_log"]) - 1),
            label=target,
            linewidth=1.2,
        )
    axis.axhline(0, color="0.4", linewidth=0.8)
    axis.axvline(
        pd.Timestamp("2015-03-01"),
        color="black",
        linestyle="--",
        linewidth=0.9,
    )
    axis.set(
        title="Arm 3 treated-minus-synthetic gaps",
        ylabel="gap (%)",
        xlabel="month",
    )
    axis.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(
        figure_dir / "fig2_gap_trajectories.png", **save_options
    )
    plt.close(fig)

    primary_placebos = placebos.loc[
        placebos["specification"] == "primary"
    ]
    ishikawa = summary.loc[
        (summary["specification"] == "primary")
        & (summary["target_code"] == "17")
    ].iloc[0]
    kept = primary_placebos.loc[
        primary_placebos["pre_rmspe"]
        <= RMSPE_FIT_MULT * ishikawa["pre_rmspe"]
    ]
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.6))
    for axis, column, treated, title in (
        (
            axes[0],
            "opening_gap_log",
            ishikawa["opening_gap_log"],
            "Opening-window placebo null",
        ),
        (
            axes[1],
            "late_gap_log",
            ishikawa["late_gap_log"],
            "Late-window placebo null",
        ),
    ):
        axis.hist(kept[column], bins=12, color="#8fb9d0", edgecolor="white")
        axis.axvline(treated, color="#b53a3a", linewidth=1.5, label="Ishikawa")
        axis.axvline(0, color="0.4", linewidth=0.8)
        axis.set(title=title, xlabel="mean gap (log points)", ylabel="placebos")
        axis.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(
        figure_dir / "fig3_placebo_distributions.png", **save_options
    )
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(8.5, 6), sharex=True)
    labels = {
        "kanazawa_lodging_guests": "Kanazawa lodging guests",
        "kanazawa_19_facility_visits": "Kanazawa 19-facility visits",
    }
    for axis, series in zip(axes, labels):
        frame = anchors.loc[anchors["anchor_series"] == series]
        anchor_dates = pd.to_datetime(frame["ym"].astype(str), format="%Y%m")
        axis.plot(
            anchor_dates,
            frame["same_month_2014_index"],
            linewidth=1.2,
            label=labels[series],
        )
        axis.axhline(100, color="0.4", linewidth=0.8)
        axis.axvline(
            pd.Timestamp("2015-03-01"),
            color="black",
            linestyle="--",
            linewidth=0.9,
        )
        axis.set_ylabel("same-month 2014 = 100")
        axis.legend(frameon=False)
    axes[0].set_title("V3 descriptive Kanazawa anchor series")
    fig.tight_layout()
    fig.savefig(
        figure_dir / "fig4_v3_anchor_indices.png", **save_options
    )
    plt.close(fig)


def artifact_hashes(out_dir: Path = OUT_DIR) -> dict[str, str]:
    return {
        path.relative_to(out_dir).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(out_dir.rglob("*"))
        if path.is_file() and path.suffix in {".csv", ".json", ".png"}
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", type=Path, default=WORKBOOK)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--anchor-dir", type=Path, default=ANCHOR_DIR)
    args = parser.parse_args()

    validate_frozen_design()
    panel = load_prefecture_panel(args.workbook)
    annual = load_annual_release_panel(args.raw_dir)
    v3_anchor = load_v3_anchor_data(args.anchor_dir)
    results = build_battery(
        panel,
        annual_panel=annual,
        v3_anchor=v3_anchor,
    )
    write_outputs(results, args.out_dir)
    hashes = artifact_hashes(args.out_dir)
    if EXPECTED_ARTIFACT_SHA256 and hashes != EXPECTED_ARTIFACT_SHA256:
        raise AssertionError(
            "Arm 3 result artifacts differ from byte-exact SHA-256 oracles"
        )
    print(
        f"wrote Arm 3 battery to {args.out_dir}; "
        f"sha256={json.dumps(hashes, sort_keys=True)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
