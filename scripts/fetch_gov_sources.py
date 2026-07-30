#!/usr/bin/env python3
"""Panel-facing adapters for the existing government-data fetch machinery.

JTA's current overnight series is MLIT-Excel-derived guest-nights, not a count
of guests: the e-Stat API survey is frozen at 2016.  FF-DATA remains annual
origin-to-destination data and is deliberately not coerced into monthly panel
grain.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import fetch_estat_data, fetch_ff_data

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "national_data_sources.yaml"
ACCOMMODATION_PATH = ROOT / "output" / "national_stats" / "accommodation_panel.csv"
RAW_ESTAT_DIR = ROOT / "data" / "nonsurvey" / "raw_estat"
RAW_FFDATA_DIR = ROOT / "data" / "nonsurvey" / "gov" / "raw"

ESTAT_COLUMNS = ["stat_id", "area", "time", "cat", "value", "unit"]
FFDATA_COLUMNS = [
    "year", "origin_pref_code", "origin_pref", "dest_pref_code", "dest_pref",
    "transport_mode", "flow_value", "dataset_id", "source",
]
MODE_KEYS = (
    "FFD:all", "FFD:railway", "FFD:bus", "FFD:rental_car", "FFD:other_car",
    "FFD:taxi_n_chauffeur", "FFD:domestic_flight", "FFD:other_transportation",
    "FFD:transportation_unknown",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_jta_overnight(start_ym: str | None = None, end_ym: str | None = None) -> pd.DataFrame:
    """Return MLIT-Excel-derived prefecture-month guest-nights.

    ``jta_guest_nights`` is total overnight guest-nights; the source does not
    publish a separate number-of-guests field. Missing values remain missing.
    """
    source = pd.read_csv(ACCOMMODATION_PATH)
    date = pd.to_datetime(dict(year=source.year, month=source.month, day=1))
    frame = pd.DataFrame({
        "date": date.dt.strftime("%Y-%m-%d"),
        "geo_id": source.pref_code.map(lambda code: f"pref_{int(code):02d}"),
        "geo_level": "prefecture",
        "prefecture": source.pref_name,
        "pref_code": source.pref_code.astype(int),
        "jta_guest_nights": source.total_stays,
        "jta_foreign_guest_nights": source.foreign_stays_10plus,
        "vintage": source.vintage,
        "source_stat_id": "MLIT_JTA_accommodation_survey",
    })
    frame["coverage_flag"] = frame.jta_guest_nights.notna().map({True: "ok", False: "missing"})
    if start_ym:
        frame = frame[frame.date >= f"{start_ym}-01"]
    if end_ym:
        frame = frame[frame.date <= f"{end_ym}-01"]
    return frame.reset_index(drop=True)


def _estat_rows(payload: dict, stat_id: str) -> list[dict[str, object]]:
    data = payload.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {})
    classes = data.get("CLASS_INF", {}).get("CLASS_OBJ", [])
    if isinstance(classes, dict):
        classes = [classes]
    labels: dict[str, dict[str, str]] = {}
    for item in classes:
        ident = item.get("@id", "")
        values = item.get("CLASS", [])
        if isinstance(values, dict):
            values = [values]
        labels[ident] = {str(value.get("@code", "")): str(value.get("$", value.get("@name", ""))) for value in values}
    rows = []
    values = data.get("DATA_INF", {}).get("VALUE", [])
    if isinstance(values, dict):
        values = [values]
    for value in values:
        attrs = {key[1:]: val for key, val in value.items() if key.startswith("@")}
        area_code = attrs.get("area", attrs.get("tab", ""))
        time_code = attrs.get("time", "")
        category = "|".join(
            f"{key}={labels.get(key, {}).get(code, code)}"
            for key, code in attrs.items() if key not in {"area", "time", "unit"}
        )
        raw = value.get("$")
        try:
            numeric = float(str(raw).replace(",", "")) if raw not in (None, "", "-") else float("nan")
        except ValueError:
            numeric = float("nan")
        rows.append({"stat_id": stat_id, "area": area_code, "time": time_code, "cat": category,
                     "value": numeric, "unit": attrs.get("unit", "")})
    return rows


def fetch_estat_generic(
    stats_code: str, dataset: str | None = None, *, refresh: bool = False
) -> pd.DataFrame:
    """Delegate e-Stat discovery and table paging to ``fetch_estat_data``."""
    app_id = os.environ["ESTAT_APP_ID"]
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    datasets = config.get("estat", {})
    if dataset:
        if dataset not in datasets:
            raise ValueError(f"unknown e-Stat dataset: {dataset}")
        spec = datasets[dataset]
        if str(spec["stats_code"]) != str(stats_code):
            raise ValueError(f"dataset {dataset} does not use stats code {stats_code}")
    else:
        spec = next((item for item in datasets.values() if str(item["stats_code"]) == str(stats_code)), {})
    tables = fetch_estat_data.discover_tables(app_id, stats_code, timeout=120)
    RAW_ESTAT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for table in tables:
        stat_id = str(table["@id"])
        path = RAW_ESTAT_DIR / f"{stats_code}_{stat_id}.json"
        if path.exists() and not refresh:
            pages = json.loads(path.read_text(encoding="utf-8"))
        else:
            pages = fetch_estat_data.fetch_table(app_id, stat_id, spec.get("area_codes", []), timeout=120)
            path.write_text(json.dumps(pages, ensure_ascii=False), encoding="utf-8")
        for page in pages:
            rows.extend(_estat_rows(page, stat_id))
    return pd.DataFrame(rows, columns=ESTAT_COLUMNS)


def _pref_pair(metadata: dict) -> tuple[str, str] | None:
    raw = metadata.get("DPF:prefecture_code", metadata.get("prefecture_code", []))
    if isinstance(raw, str):
        raw = re.findall(r"\d+", raw)
    # Records ending in ``~不明`` carry one prefecture code, so they cannot
    # honestly be represented at this table's origin-prefecture ×
    # destination-prefecture grain.
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        return None
    codes = []
    for code in raw:
        digits = re.sub(r"\D", "", str(code))
        codes.append(f"{int(digits):02d}")
    return codes[0], codes[1]


def _pref_names(metadata: dict, origin: str, dest: str) -> tuple[str, str]:
    names = metadata.get("DPF:prefecture_name", metadata.get("prefecture_name", []))
    if isinstance(names, str):
        names = [part.strip() for part in names.split(",")]
    if isinstance(names, (list, tuple)) and len(names) == 2:
        return str(names[0]), str(names[1])
    return origin, dest


def fetch_ffdata(years: list[int] | None = None, *, refresh: bool = False) -> pd.DataFrame:
    """Delegate FF-DATA catalog/search paging to ``fetch_ff_data`` and unpivot modes."""
    app_id = os.environ["MLIT_DATA_APP_ID"]
    spec = (yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {})["ff_data"]
    target_years = years or list(spec["years"])
    RAW_FFDATA_DIR.mkdir(parents=True, exist_ok=True)
    catalog_path = RAW_FFDATA_DIR / "catalog.json"
    if catalog_path.exists() and not refresh:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    else:
        raw = fetch_ff_data._graphql(spec["api_base"], app_id, fetch_ff_data._catalog_query(spec["catalog_id"]), 120)
        catalog_path.write_bytes(raw)
        catalog = json.loads(raw)
    available = {dataset["id"] for entry in catalog.get("data", {}).get("dataCatalog", []) or [] for dataset in entry.get("datasets", []) or []}
    rows = []
    for year in target_years:
        dataset_id = spec.get("dataset_id_template", "ffd_{year}").format(year=year)
        if dataset_id not in available:
            raise ValueError(f"FF-DATA dataset absent from catalog {spec['catalog_id']}: {dataset_id}")
        offset = 0
        total = None
        while total is None or offset < total:
            path = RAW_FFDATA_DIR / f"{dataset_id}_{offset:07d}.json"
            if path.exists() and not refresh:
                payload = json.loads(path.read_text(encoding="utf-8"))
            else:
                raw = fetch_ff_data._graphql(spec["api_base"], app_id, fetch_ff_data._search_query(dataset_id, offset), 120)
                path.write_bytes(raw)
                payload = json.loads(raw)
            search = payload.get("data", {}).get("search", {})
            records = search.get("searchResults", []) or []
            total = int(search.get("totalNumber", 0)) if total is None else total
            if not records and offset < total:
                raise RuntimeError(f"empty FF-DATA page before total for {dataset_id}")
            for record in records:
                metadata = record.get("metadata") or {}
                pair = _pref_pair(metadata)
                if pair is None:
                    continue
                origin_code, dest_code = pair
                origin, dest = _pref_names(metadata, origin_code, dest_code)
                for mode in MODE_KEYS:
                    value = metadata.get(mode)
                    if value in (None, "", "-", "X", "x"):
                        continue
                    rows.append({"year": int(year), "origin_pref_code": origin_code, "origin_pref": origin,
                                 "dest_pref_code": dest_code, "dest_pref": dest, "transport_mode": mode.removeprefix("FFD:"),
                                 "flow_value": float(str(value).replace(",", "")), "dataset_id": dataset_id,
                                 "source": "MLIT Data Platform FF-DATA GraphQL"})
            offset += len(records)
    return pd.DataFrame(rows, columns=FFDATA_COLUMNS)


def _update_manifest(out: Path, name: str, record: dict[str, object]) -> None:
    manifest_path = ROOT / "data" / "nonsurvey" / "data_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    manifest.setdefault("gov_sources", {})[name] = record
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build government context-layer parquet artifacts")
    parser.add_argument("--source", choices=("jta", "ffdata", "generic"), required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "nonsurvey" / "gov")
    parser.add_argument("--stats-code", help="e-Stat survey code (required for generic)")
    parser.add_argument("--refresh", action="store_true", help="refresh cached API JSON")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fetched_utc = datetime.now(timezone.utc).isoformat()
    if args.source == "jta":
        frame, filename, name = fetch_jta_overnight(), "jta_overnight.parquet", "jta_overnight"
        extra = {"origin": "MLIT accommodation survey Excel -> accommodation_panel.csv (e-Stat API 00601020 frozen at 2016; see ADR 0028)", "estat_stats_code": "00601020", "estat_overnight_statsDataId_reference_only": "0003313520"}
    elif args.source == "ffdata":
        frame, filename, name = fetch_ffdata(refresh=args.refresh), "ffdata_od_annual.parquet", "ffdata_od_annual"
        extra = {"origin": "MLIT Data Platform FF-DATA GraphQL (catalog ffd)", "catalog_id": "ffd", "years": list((yaml.safe_load(CONFIG_PATH.read_text()) or {})["ff_data"]["years"])}
    else:
        if not args.stats_code:
            parser.error("--stats-code is required for --source generic")
        frame, filename, name = fetch_estat_generic(args.stats_code, refresh=args.refresh), f"estat_{args.stats_code}.parquet", f"estat_{args.stats_code}"
        extra = {"origin": "e-Stat REST via scripts/fetch_estat_data.py", "estat_stats_code": args.stats_code}
    path = args.out / filename
    frame.to_parquet(path, index=False)
    _update_manifest(path, name, {**extra, "parquet": str(path.resolve().relative_to(ROOT)), "rows": len(frame), "sha256": sha256_file(path), "fetched_utc": fetched_utc})
    print(f"GOV FETCH {name} rows={len(frame)} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
