#!/usr/bin/env python3
"""Build the data bundle for the non-survey SEM simulation webapp."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

SITE_LABELS = {
    "tojinbo": ("Tojinbo", "persons/day", "cam_person_total"),
    "fukui_station_east": ("Fukui Station East", "persons/day", "cam_person_total"),
    "rainbow_line_lot1": ("Rainbow Line", "vehicles/day", "cam_plate_vehicles"),
}

AREA_LABELS = {
    "awara_onsen": "Awara Onsen",
    "fukui_station": "Fukui Station",
    "obama": "Obama",
    "echizen_coast": "Echizen Coast",
    "mikatagoko": "Mikatagoko",
}

SITE_AREA_LINK = {
    "tojinbo": "awara_onsen",
    "fukui_station_east": "fukui_station",
    "rainbow_line_lot1": "mikatagoko",
}


def weekend_mask(dates: pd.Series) -> pd.Series:
    return pd.to_datetime(dates).dt.dayofweek >= 5


def site_baselines(site: pd.DataFrame) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for site_id, (label, metric, col) in SITE_LABELS.items():
        g = site[site["geo_id"] == site_id].copy()
        values = pd.to_numeric(g[col], errors="coerce").dropna()
        wknd = weekend_mask(g["date"])
        weekend = pd.to_numeric(g.loc[wknd, col], errors="coerce").dropna()
        weekday = pd.to_numeric(g.loc[~wknd, col], errors="coerce").dropna()
        out[site_id] = {
            "label": label,
            "median_daily": float(values.median()),
            "p95_daily": float(values.quantile(0.95)),
            "weekend_mean": float(weekend.mean()),
            "weekday_mean": float(weekday.mean()),
            "wk_wd_ratio": float(weekend.mean() / weekday.mean()),
            "peakiness": float(values.quantile(0.95) / values.median()),
            "out_of_pref": None,
            "metric": metric,
        }
        if "cam_plate_share_out_of_pref" in g:
            share = pd.to_numeric(g["cam_plate_share_out_of_pref"], errors="coerce").dropna()
            if not share.empty:
                out[site_id]["out_of_pref"] = float(share.mean())
    return out


def area_baselines(area: pd.DataFrame) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for area_id, label in AREA_LABELS.items():
        g = area[area["geo_id"] == area_id].copy()
        wknd = weekend_mask(g["date"])
        occ_weekend = float(pd.to_numeric(g.loc[wknd, "rsv_occ_proxy"], errors="coerce").mean())
        occ_weekday = float(pd.to_numeric(g.loc[~wknd, "rsv_occ_proxy"], errors="coerce").mean())
        adr = pd.to_numeric(g["rsv_adr_proxy"], errors="coerce").replace([float("inf"), -float("inf")], pd.NA)
        out[area_id] = {
            "label": label,
            "occ_weekend": occ_weekend,
            "occ_weekday": occ_weekday,
            "gap_pp": float((occ_weekend - occ_weekday) * 100),
            "stays_mean": float(pd.to_numeric(g["rsv_n_stay"], errors="coerce").mean()),
            "adr": float(adr.dropna().mean()),
            "capacity": float(pd.to_numeric(g["hotel_capacity_rooms"], errors="coerce").dropna().iloc[0]),
        }
    return out


def sem_block(path: Path) -> dict[str, object]:
    coeffs = json.loads(path.read_text(encoding="utf-8"))
    intent_path = next(p for p in coeffs["paths"] if p["from"] == "intent" and p["to"] == "demand")
    anchor = coeffs["observed_elasticities"]["awara_weekly_directions_to_stays_loglog"]
    return {
        "intent_to_demand": intent_path["std"],
        "loadings": {row["indicator"]: row["std"] for row in coeffs["loadings"]},
        "anchor_elasticity": anchor,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", default=Path("data/nonsurvey"), type=Path)
    parser.add_argument("--sem", default=Path("output/sem/nonsurvey/coefficients.json"), type=Path)
    args = parser.parse_args()

    site = pd.read_parquet(args.panel / "panel_site_daily.parquet")
    area = pd.read_parquet(args.panel / "panel_area_daily.parquet")
    coeffs = json.loads(args.sem.read_text(encoding="utf-8"))
    data = {
        "sites": site_baselines(site),
        "areas": area_baselines(area),
        "sem": sem_block(args.sem),
        "site_area_link": SITE_AREA_LINK,
        "meta": {
            "fit": coeffs["fit"],
            "n_obs": coeffs["n_obs"],
            "n_sites": coeffs["n_sites"],
        },
    }

    out = Path(__file__).resolve().parent / "data" / "webapp_data.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"APP DATA wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
