#!/usr/bin/env python3
"""Assemble the Arm 2 JTA quarantine from local operator-supplied workbooks.

This tool reuses ``build_accommodation_panel.parse_workbook`` for one
2025-confirmed annual workbook and one or more 2026 monthly preliminary
workbooks, then writes the normalized panel into the Arm 2 quarantine.

The frozen ``build_s2_descriptive_report`` function is called only as a
pre-write contract check. Its return value is intentionally discarded because
it contains the S2 descriptive series, and the assembler must not observe,
print, or persist those outcome values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import arm2_quarantine
from arm2_predictions import build_s2_descriptive_report
from build_accommodation_panel import parse_workbook

SEEN_PANEL_PATH = ROOT / "output" / "national_stats" / "accommodation_panel.csv"
DESTINATION_FILENAME = "jta_accommodation_panel.csv"
MANIFEST_FILENAME = "assembly_manifest.json"
FRAME_BASIS_COLUMN = "frame_basis"
BASE_COLUMNS = (
    "pref_code",
    "pref_name",
    "year",
    "month",
    "total_stays",
    "foreign_stays_10plus",
    "vintage",
)


class ToolError(RuntimeError):
    """Raised when the JTA quarantine cannot be assembled safely."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _byte_length(path: Path) -> int:
    return path.stat().st_size


def _ensure_empty_target() -> None:
    if arm2_quarantine.JTA_DIR.exists():
        existing = sorted(path.name for path in arm2_quarantine.JTA_DIR.iterdir())
        if existing:
            joined = ", ".join(existing)
            raise ToolError(
                f"target JTA quarantine directory must be empty; found: {joined}"
            )
    arm2_quarantine.JTA_DIR.mkdir(parents=True, exist_ok=True)


def _load_seen_panel() -> tuple[pd.DataFrame, list[str], dict[str, int | str]]:
    if not SEEN_PANEL_PATH.is_file():
        raise FileNotFoundError(f"missing committed seen JTA panel: {SEEN_PANEL_PATH}")
    frame = pd.read_csv(
        SEEN_PANEL_PATH,
        dtype={"pref_code": str, "pref_name": str, "vintage": str},
    )
    columns = list(frame.columns)
    if columns != list(BASE_COLUMNS):
        raise ToolError(
            "committed seen JTA panel schema moved; expected "
            + ", ".join(BASE_COLUMNS)
        )
    frame["pref_code"] = frame["pref_code"].astype(str).str.zfill(2)
    frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
    frame["month"] = pd.to_numeric(frame["month"], errors="raise").astype(int)
    metadata = {
        "filename": SEEN_PANEL_PATH.name,
        "sha256": _sha256(SEEN_PANEL_PATH),
        "byte_length": _byte_length(SEEN_PANEL_PATH),
    }
    return frame, columns, metadata


def _parse_source_workbook(
    path: Path,
    *,
    year: int,
    vintage: str,
    require_complete_year: bool,
) -> tuple[pd.DataFrame, dict[str, int | str | list[int]]]:
    if not path.is_file():
        raise FileNotFoundError(f"missing operator-supplied JTA workbook: {path}")
    rows = parse_workbook(path, year, vintage)
    if not rows:
        raise ToolError(f"{path.name}: parsed workbook yielded no rows")
    frame = pd.DataFrame(rows)
    if list(frame.columns) != list(BASE_COLUMNS):
        raise ToolError(f"{path.name}: parsed workbook schema mismatch")
    frame["pref_code"] = frame["pref_code"].astype(str).str.zfill(2)
    frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
    frame["month"] = pd.to_numeric(frame["month"], errors="raise").astype(int)
    actual_years = sorted(frame["year"].unique().tolist())
    if actual_years != [year]:
        raise ToolError(f"{path.name}: expected only year {year}, found {actual_years}")
    actual_vintages = sorted(frame["vintage"].astype(str).str.lower().unique().tolist())
    if actual_vintages != [vintage]:
        raise ToolError(
            f"{path.name}: expected only vintage {vintage}, found {actual_vintages}"
        )
    months = sorted(frame["month"].unique().tolist())
    invalid = [month for month in months if month < 1 or month > 12]
    if invalid:
        raise ToolError(f"{path.name}: workbook yielded invalid months {invalid}")
    if require_complete_year and months != list(range(1, 13)):
        raise ToolError(
            f"{path.name}: confirmed 2025 workbook must provide all 12 months"
        )
    if frame.duplicated(["pref_code", "year", "month", "vintage"]).any():
        raise ToolError(f"{path.name}: duplicate prefecture-month rows")
    metadata = {
        "filename": path.name,
        "sha256": _sha256(path),
        "byte_length": _byte_length(path),
        "year": year,
        "vintage": vintage,
        "months": months,
    }
    return frame, metadata


def _parse_monthly_workbooks(
    paths: list[Path],
) -> tuple[list[pd.DataFrame], list[dict[str, int | str | list[int]]]]:
    frames = []
    metadata = []
    month_sources: dict[int, str] = {}
    for path in paths:
        frame, item = _parse_source_workbook(
            path,
            year=2026,
            vintage="preliminary",
            require_complete_year=False,
        )
        duplicates = [
            month for month in item["months"] if month in month_sources
        ]
        if duplicates:
            detail = ", ".join(
                f"{month} ({month_sources[month]} vs {item['filename']})"
                for month in duplicates
            )
            raise ToolError(
                f"duplicate 2026 months across supplied monthly files: {detail}"
            )
        for month in item["months"]:
            month_sources[month] = str(item["filename"])
        frames.append(frame)
        metadata.append(item)
    return frames, metadata


def _validate_s2_contract(panel: pd.DataFrame) -> None:
    """Call the frozen S2 gate and discard the returned descriptive series."""
    try:
        build_s2_descriptive_report(panel)
    except ValueError as exc:
        raise ToolError(f"S2 pre-write validation failed: {exc}") from exc


def _maybe_add_frame_basis(panel: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    panel_with_basis = panel.copy()
    panel_with_basis[FRAME_BASIS_COLUMN] = panel_with_basis["year"].map(
        lambda year: "employee_count" if int(year) <= 2025 else "room_count"
    )
    try:
        _validate_s2_contract(panel_with_basis)
    except ToolError:
        return panel, False
    return panel_with_basis, True


def _drop_overlapping_seen_rows(
    seen_panel: pd.DataFrame,
    incoming: pd.DataFrame,
) -> pd.DataFrame:
    key_columns = ["pref_code", "year", "month"]
    incoming_keys = set(incoming[key_columns].itertuples(index=False, name=None))
    keep_mask = [
        key not in incoming_keys
        for key in seen_panel[key_columns].itertuples(index=False, name=None)
    ]
    return seen_panel.loc[keep_mask].reset_index(drop=True)


def _assemble_panel(
    seen_panel: pd.DataFrame,
    confirmed_2025: pd.DataFrame,
    monthly_2026: list[pd.DataFrame],
) -> tuple[pd.DataFrame, bool]:
    incoming = pd.concat([confirmed_2025, *monthly_2026], ignore_index=True)
    retained_seen = _drop_overlapping_seen_rows(seen_panel, incoming)
    panel = pd.concat([retained_seen, incoming], ignore_index=True)
    if panel.duplicated(["pref_code", "year", "month"]).any():
        raise ToolError(
            "assembled JTA panel contains duplicate prefecture-month keys"
        )
    _validate_s2_contract(panel)
    return _maybe_add_frame_basis(panel)


def _write_panel(
    panel: pd.DataFrame,
    seen_columns: list[str],
) -> tuple[Path, str, int]:
    output_path = arm2_quarantine.JTA_DIR / DESTINATION_FILENAME
    columns = list(seen_columns)
    if FRAME_BASIS_COLUMN in panel.columns:
        columns.append(FRAME_BASIS_COLUMN)
    panel.loc[:, columns].to_csv(output_path, index=False, lineterminator="\n")
    return output_path, _sha256(output_path), len(panel)


def _write_manifest(
    *,
    seen_metadata: dict[str, int | str],
    source_metadata: list[dict[str, int | str | list[int]]],
    frame_basis_included: bool,
) -> None:
    manifest = {
        "schema_version": 1,
        "seen_panel": seen_metadata,
        "inputs": [
            {
                key: value
                for key, value in item.items()
                if key != "months"
            }
            for item in source_metadata
        ],
        "frame_basis_included": frame_basis_included,
    }
    manifest_path = arm2_quarantine.JTA_DIR / MANIFEST_FILENAME
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _label_set(panel: pd.DataFrame) -> list[tuple[int, str]]:
    return sorted(
        {
            (int(year), str(vintage))
            for year, vintage in panel[["year", "vintage"]].itertuples(
                index=False, name=None
            )
        }
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Populate the Arm 2 JTA quarantine from a 2025 confirmed workbook "
            "and one or more 2026 monthly preliminary workbooks."
        )
    )
    parser.add_argument(
        "--confirmed-2025",
        required=True,
        type=Path,
        help="Path to the operator-supplied 2025 confirmed annual JTA workbook.",
    )
    parser.add_argument(
        "--monthly-2026",
        required=True,
        nargs="+",
        type=Path,
        help="One or more operator-supplied 2026 monthly preliminary workbooks.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        seen_panel, seen_columns, seen_metadata = _load_seen_panel()
        confirmed_2025, confirmed_metadata = _parse_source_workbook(
            args.confirmed_2025.resolve(),
            year=2025,
            vintage="confirmed",
            require_complete_year=True,
        )
        monthly_2026, monthly_metadata = _parse_monthly_workbooks(
            [path.resolve() for path in args.monthly_2026]
        )
        _ensure_empty_target()
        panel, frame_basis_included = _assemble_panel(
            seen_panel,
            confirmed_2025,
            monthly_2026,
        )
        output_path, output_sha, row_count = _write_panel(panel, seen_columns)
        _write_manifest(
            seen_metadata=seen_metadata,
            source_metadata=[confirmed_metadata, *monthly_metadata],
            frame_basis_included=frame_basis_included,
        )
    except (ToolError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for metadata in [seen_metadata, confirmed_metadata, *monthly_metadata]:
        print(f"{metadata['filename']} {metadata['sha256']}")
    labels = _label_set(panel)
    print(f"{output_path} {output_sha} {row_count}")
    print(f"labels: {labels}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
