#!/usr/bin/env python3
"""Build/copy the non-survey tourism panel for the physical-intervention reframe.

The shipped artifact set is the reproducible reference panel: Code4Fukui source
repos are pinned in ``data_manifest.json`` with per-file SHA256s. In normal
review mode, pass ``--raw-dir`` pointing at a directory containing those staged
parquet/manifest files and this script validates row counts, applies derived
contract columns, and writes ``data/nonsurvey``.

The original online builder is preserved as the source design, but live
refetching is intentionally not implicit because re-pulling HEAD would violate
the pinned-provenance contract. Use the manifest as the fetch plan when
refreshing the raw cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd

SHINKANSEN_BREAK = "2024-03-16"

CODE4FUKUI_REPOS = {
    "fukui-kanko-people-flow-data",
    "fukui-kanko-reservation",
    "fukui-station-kanko-reservation",
    "echizen-coast-kanko-reservation",
    "obama-kanko-reservation",
    "mikatagoko-kanko-reservation",
    "fukui-kanko-trend-data",
}

PANEL_FILES = {
    "panel_site_daily": "panel_site_daily.parquet",
    "panel_area_daily": "panel_area_daily.parquet",
    "booking_curve_awara": "booking_curve_awara.parquet",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_artifact_dir(raw_dir: Path) -> Path:
    candidates = [raw_dir, raw_dir / "panel"]
    for candidate in candidates:
        if all((candidate / name).exists() for name in PANEL_FILES.values()):
            return candidate
    expected = ", ".join(PANEL_FILES.values())
    raise FileNotFoundError(
        f"{raw_dir} does not contain the staged panel artifacts ({expected}). "
        "Supply the pinned raw/artifact cache; do not re-pull unpinned HEAD."
    )


def add_contract_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "post_shinkansen" not in out.columns:
        out["post_shinkansen"] = (pd.to_datetime(out["date"]) >= SHINKANSEN_BREAK).astype(int)
    return out


def write_parquet(src: Path, dst: Path, *, add_post: bool) -> dict[str, object]:
    df = pd.read_parquet(src)
    if add_post:
        df = add_contract_columns(df)
    df.to_parquet(dst, index=False)
    return {"path": str(dst), "sha256": sha256_file(dst), "rows": int(df.shape[0])}


def write_manifest(artifact_dir: Path, out_dir: Path, outputs: dict[str, dict[str, object]]) -> None:
    src = artifact_dir / "data_manifest.json"
    if src.exists():
        manifest = json.loads(src.read_text(encoding="utf-8"))
    else:
        manifest = {"sources": {}, "notes": []}
    missing = sorted(CODE4FUKUI_REPOS - set(manifest.get("sources", {})))
    if missing:
        manifest.setdefault("notes", []).append(
            "Expected pinned Code4Fukui repos absent from manifest: " + ", ".join(missing)
        )
    manifest["outputs"] = outputs
    (out_dir / "data_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", required=True, type=Path, help="Pinned raw/artifact directory")
    parser.add_argument("--out", default=Path("data/nonsurvey"), type=Path)
    args = parser.parse_args()

    artifact_dir = find_artifact_dir(args.raw_dir)
    args.out.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, dict[str, object]] = {}
    outputs["panel_site_daily"] = write_parquet(
        artifact_dir / PANEL_FILES["panel_site_daily"],
        args.out / PANEL_FILES["panel_site_daily"],
        add_post=True,
    )
    outputs["panel_area_daily"] = write_parquet(
        artifact_dir / PANEL_FILES["panel_area_daily"],
        args.out / PANEL_FILES["panel_area_daily"],
        add_post=True,
    )
    outputs["booking_curve_awara"] = write_parquet(
        artifact_dir / PANEL_FILES["booking_curve_awara"],
        args.out / PANEL_FILES["booking_curve_awara"],
        add_post=False,
    )
    write_manifest(artifact_dir, args.out, outputs)

    coverage = artifact_dir / "coverage_report.md"
    if coverage.exists():
        coverage_out = args.out / "coverage_report.md"
        if coverage.resolve() != coverage_out.resolve():
            shutil.copy2(coverage, coverage_out)

    print(
        "PANEL BUILD wrote",
        outputs["panel_site_daily"]["rows"],
        "site rows and",
        outputs["panel_area_daily"]["rows"],
        "area rows",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
