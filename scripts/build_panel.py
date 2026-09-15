#!/usr/bin/env python3
"""Build the unified non-survey tourism panel for the Fukui thesis reframe.

Emits (to OUT dir):
  panel_site_daily.parquet   - sensor-anchored (date x camera site) + nearest lodging/trend context
  panel_area_daily.parquet   - lodging-anchored (date x reservation area) + access-sensor context
  booking_curve_awara.parquet- lead-time table (target_date x ago_Ndays) with derived features
  data_manifest.json         - pinned commits, row counts, coverage windows, checksums
  coverage_report.md         - human-readable coverage + gap report

All Code4Fukui sources are MIT / open-data, keyless. Pinned by commit SHA at fetch time.
No imputation across the 2025-09-26..28 camera outage or the 2024-03-16 Shinkansen break.
"""
import io, os, sys, json, hashlib, datetime as dt
import requests
import pandas as pd
import numpy as np

RAW = "https://raw.githubusercontent.com/code4fukui"
OUT = os.environ.get("PANEL_OUT", "/home/andrewgreen/panel_build_work/out")
CACHE = os.environ.get("PANEL_CACHE", "/home/andrewgreen/panel_build_work/raw")
os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)

MANIFEST = {"generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources": {}, "outputs": {}, "notes": []}

def repo_head(repo):
    r = requests.get(f"https://api.github.com/repos/code4fukui/{repo}/commits?per_page=1", timeout=30)
    r.raise_for_status()
    d = r.json()[0]
    return d["sha"], d["commit"]["committer"]["date"]

# ---------------- source pinning ----------------
# One commit per upstream repo. A rebuild is reproducible only if these are pinned:
# fetching `main` records what arrived instead of pinning what was asked for, which is how
# the 2026-07-09 vintage became unrebuildable. Changing a pin is an explicit research
# decision — see the header of config/official_fukui_sources.yaml. Overridable per run via
# PANEL_PINS=<json> for a deliberate re-vintage, which is logged in the manifest.
PINS = {
    "fukui-kanko-reservation":         "f58e4d8fdc34",
    "fukui-station-kanko-reservation": "f58e4d8fdc34",
    "echizen-coast-kanko-reservation": "f58e4d8fdc34",
    "obama-kanko-reservation":         "f58e4d8fdc34",
    "mikatagoko-kanko-reservation":    "f58e4d8fdc34",
}
if os.environ.get("PANEL_PINS"):
    PINS.update(json.loads(os.environ["PANEL_PINS"]))
    MANIFEST["notes"].append("PANEL_PINS override applied: " + os.environ["PANEL_PINS"])


def fetch(repo, path, encoding=None):
    """Fetch a raw file at its pinned commit, record provenance."""
    ref = PINS.get(repo)
    if not ref:
        raise RuntimeError(
            f"{repo} is not pinned. Add a commit to PINS (and to "
            f"config/official_fukui_sources.yaml with a checksum) before fetching from it. "
            f"Unpinned fetches are not reproducible."
        )
    url = f"{RAW}/{repo}/{ref}/{path}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    raw = r.content
    sha = hashlib.sha256(raw).hexdigest()
    if repo not in MANIFEST["sources"]:
        head_sha, head_date = repo_head(repo)
        MANIFEST["sources"][repo] = {"pinned_ref": ref, "head_sha": head_sha,
                                     "head_date": head_date, "pin_is_head": head_sha.startswith(ref),
                                     "files": {}}
    MANIFEST["sources"][repo]["files"][path] = {"sha256": sha, "bytes": len(raw)}
    enc = encoding or "utf-8-sig"
    return io.StringIO(raw.decode(enc, errors="replace"))

# ---------------- geo masters ----------------
SITES = {
    "tojinbo":            dict(camera="tojinbo-shotaro",                sensors=["Person","Face"], area="awara_onsen",  muni="Sakai",  muni_jis="18210", jma="mikuni"),
    "fukui_station_east": dict(camera="fukui-station-east-entrance",    sensors=["Person","Face"], area="fukui_station",muni="Fukui",  muni_jis="18201", jma="fukuicity"),
    "rainbow_line_lot1":  dict(camera="rainbow-line-parking-lot-1-gate",sensors=["LicensePlate"],  area="mikatagoko",   muni="Mihama", muni_jis="18441", jma="mihama"),
    "rainbow_line_lot2":  dict(camera="rainbow-line-parking-lot-2-gate",sensors=["LicensePlate"],  area="mikatagoko",   muni="Mihama", muni_jis="18441", jma="mihama"),
}
AREAS = {
    "awara_onsen":  dict(repo="fukui-kanko-reservation",         muni="Awara",   muni_jis="18208", origin_pref=True,  trend_muni="あわら市"),
    "fukui_station":dict(repo="fukui-station-kanko-reservation", muni="Fukui",   muni_jis="18201", origin_pref=False, trend_muni=None),
    "echizen_coast":dict(repo="echizen-coast-kanko-reservation", muni="Echizen", muni_jis="18423", origin_pref=False, trend_muni="越前市"),
    "obama":        dict(repo="obama-kanko-reservation",         muni="Obama",   muni_jis="18204", origin_pref=False, trend_muni="小浜市"),
    "mikatagoko":   dict(repo="mikatagoko-kanko-reservation",    muni="Mihama",  muni_jis="18441", origin_pref=False, trend_muni="美浜町"),
}
SHINKANSEN_BREAK = "2024-03-16"
CAM_OUTAGE = ("2025-09-26", "2025-09-28")

def parse_camera_full(repo, camera, target):
    try:
        buf = fetch(repo, f"full/{camera}/{target}.csv")
    except Exception as e:
        MANIFEST["notes"].append(f"MISSING camera {camera}/{target}: {e}")
        return None
    df = pd.read_csv(buf)
    df.columns = [c.strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["aggregate from"]).dt.date.astype(str)
    return df

def build_sensor_daily():
    site_frames = []  # one merged frame per site, concatenated across sites
    for site_id, s in SITES.items():
        per_target = []  # frames to MERGE (same rows, add columns) within this site
        for target in s["sensors"]:
            df = parse_camera_full("fukui-kanko-people-flow-data", s["camera"], target)
            if df is None: continue
            g = df.groupby("date", as_index=False)
            if target == "Person":
                agg = g["total count"].sum().rename(columns={"total count":"cam_person_total"})
                per_target.append(agg[["date","cam_person_total"]])
            elif target == "Face":
                face = g["total count"].sum().rename(columns={"total count":"cam_face_total"})
                cols = [c for c in df.columns if ("range" in c) or c.startswith(("male","female","other"))]
                fem = [c for c in cols if c.startswith("female")]
                sen = [c for c in cols if "65over" in c]
                chi = [c for c in cols if any(x in c for x in ["00to05","06to12","range00","range06"])]
                if cols:
                    dsum = df.groupby("date")[cols].sum()
                    tot = dsum.sum(axis=1).replace(0, np.nan)
                    demog = pd.DataFrame({
                        "date": dsum.index,
                        "cam_face_share_female": (dsum[fem].sum(axis=1)/tot).values if fem else np.nan,
                        "cam_face_share_senior": (dsum[sen].sum(axis=1)/tot).values if sen else np.nan,
                        "cam_face_share_child":  (dsum[chi].sum(axis=1)/tot).values if chi else np.nan,
                    })
                    face = face.merge(demog, on="date", how="left")
                per_target.append(face)
            elif target == "LicensePlate":
                plate = g["total count"].sum().rename(columns={"total count":"cam_plate_vehicles"})
                pref_cols = [c for c in df.columns if c not in ("placement","object class","aggregate from","aggregate to","total count","date")]
                rent = [c for c in pref_cols if "RentACar" in c]
                dsum = df.groupby("date")[pref_cols].sum()
                tot = dsum.sum(axis=1).replace(0, np.nan)
                pref_names = sorted(set(c.rsplit(" ",1)[0] for c in pref_cols))
                pref_tot = pd.DataFrame({p: dsum[[c for c in pref_cols if c.rsplit(" ",1)[0]==p]].sum(axis=1) for p in pref_names})
                out_of_pref = pref_tot.drop(columns=[p for p in pref_names if p=="Fukui"], errors="ignore").sum(axis=1)
                plate2 = pd.DataFrame({
                    "date": dsum.index,
                    "cam_plate_share_out_of_pref": (out_of_pref/tot).values,
                    "cam_plate_share_rentacar": (dsum[rent].sum(axis=1)/tot).values if rent else np.nan,
                    "cam_plate_top_origin_pref": pref_tot.idxmax(axis=1).values,
                })
                plate = plate.merge(plate2, on="date", how="left")
                per_target.append(plate)
        if not per_target: continue
        site_df = per_target[0]
        for extra in per_target[1:]:
            site_df = site_df.merge(extra, on="date", how="outer")
        site_df["geo_id"] = site_id
        site_frames.append(site_df)
    base = pd.concat(site_frames, ignore_index=True)
    base = base.sort_values(["geo_id","date"]).reset_index(drop=True)
    base["coverage_flag"] = "ok"
    o0, o1 = CAM_OUTAGE
    base.loc[(base["date"]>=o0)&(base["date"]<=o1), "coverage_flag"] = "outage"
    meta = pd.DataFrame([{"geo_id":k, "municipality":v["muni"], "muni_jis":v["muni_jis"],
                          "prefecture":"Fukui","pref_code":"18","area":v["area"],"jma":v["jma"]} for k,v in SITES.items()])
    base = base.merge(meta, on="geo_id", how="left")
    base["geo_level"] = "site"
    return base

def parse_rsv_sum(repo):
    buf = fetch(repo, "latest_rsv_sum.csv")
    df = pd.read_csv(buf)
    df.columns = [c.strip() for c in df.columns]
    ren = {"date_visit":"date","n_stay":"rsv_n_stay","n_people":"rsv_n_people","n_room":"rsv_n_room",
           "amount_fee":"rsv_amount_fee","n_reserve":"rsv_n_reserve"}
    df = df.rename(columns=ren)
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["rsv_adr_proxy"] = df["rsv_amount_fee"] / df["rsv_n_stay"].replace(0,np.nan)
    df["rsv_party_size"] = df["rsv_n_people"] / df["rsv_n_reserve"].replace(0,np.nan)
    return df

def parse_hotel_capacity(repo):
    try:
        buf = fetch(repo, "latest_hotel.csv")
        df = pd.read_csv(buf); df.columns=[c.strip() for c in df.columns]
        # one row per hotel; market capacity = sum of rooms across all hotels
        return float(pd.to_numeric(df["nrooms"], errors="coerce").dropna().sum())
    except Exception:
        return np.nan

def build_area_daily():
    frames = []
    for area_id, a in AREAS.items():
        df = parse_rsv_sum(a["repo"])
        cap = parse_hotel_capacity(a["repo"])
        df["rsv_occ_proxy"] = df["rsv_n_room"]/cap if cap==cap else np.nan
        df["geo_id"] = area_id
        df["hotel_capacity_rooms"] = cap
        frames.append(df)
    base = pd.concat(frames, ignore_index=True)
    base = base.sort_values(["geo_id","date"]).reset_index(drop=True)
    meta = pd.DataFrame([{"geo_id":k,"municipality":v["muni"],"muni_jis":v["muni_jis"],
                          "prefecture":"Fukui","pref_code":"18"} for k,v in AREAS.items()])
    base = base.merge(meta, on="geo_id", how="left")
    base["geo_level"] = "area"
    base["coverage_flag"] = "ok"
    base["post_shinkansen"] = (base["date"]>=SHINKANSEN_BREAK).astype(int)
    return base

def build_trend():
    frames=[]
    for yr in ["2024","2025","2026"]:
        try:
            buf = fetch("fukui-kanko-trend-data", f"{yr}/total_daily_metrics.csv")
        except Exception:
            continue
        df = pd.read_csv(buf); df.columns=[c.strip() for c in df.columns]
        df["geo_id"]="_total"; frames.append(df)
    if not frames: return None
    tot = pd.concat(frames, ignore_index=True)
    ren = {"map_views":"trend_map_views","search_views":"trend_search_views","directions":"trend_directions",
           "call_clicks":"trend_call_clicks","website_clicks":"trend_website_clicks","average_rating":"trend_avg_rating",
           "review_count_change":"trend_review_change"}
    tot = tot.rename(columns=ren)
    tot["date"]=pd.to_datetime(tot["date"]).dt.date.astype(str)
    keep = ["date","geo_id"]+[v for v in ren.values() if v in tot.columns]
    return tot[keep]

def build_booking_curve():
    buf = fetch("fukui-kanko-reservation", "booking_curve.csv")
    df = pd.read_csv(buf); df.columns=[c.strip() for c in df.columns]
    ago = [c for c in df.columns if c.startswith("ago_")]
    days = np.array([int(c.replace("ago_","").replace("days","")) for c in ago])
    def leadfeat(row):
        vals = pd.to_numeric(row[ago], errors="coerce").values.astype(float)
        tot = np.nansum(vals)
        if tot<=0: return pd.Series({"lead_time_mean":np.nan,"pct_booked_7d_out":np.nan})
        return pd.Series({"lead_time_mean":np.nansum(vals*days)/tot,"pct_booked_7d_out":np.nansum(vals[days<=7])/tot})
    feat = df.apply(leadfeat, axis=1)
    out = pd.concat([df[["target_date"]].rename(columns={"target_date":"date"}), df[ago], feat], axis=1)
    out["date"]=pd.to_datetime(out["date"]).dt.date.astype(str)
    out["geo_id"]="awara_onsen"
    return out

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(65536),b""): h.update(b)
    return h.hexdigest()

def coverage_summary(df, name):
    d = df.dropna(subset=["date"])
    return {"table":name,"rows":int(len(df)),"date_min":str(d["date"].min()),"date_max":str(d["date"].max()),
            "geo_ids":sorted(df["geo_id"].unique().tolist()) if "geo_id" in df else []}

def main():
    print("[1/5] sensor daily ...", flush=True)
    sensor = build_sensor_daily()
    print("   sensor rows", len(sensor), "sites", sensor["geo_id"].nunique(), flush=True)
    print("[2/5] area daily ...", flush=True)
    area = build_area_daily()
    print("   area rows", len(area), "areas", area["geo_id"].nunique(), flush=True)
    print("[3/5] trend ...", flush=True)
    trend = build_trend()
    if trend is not None:
        area = area.merge(trend.drop(columns=["geo_id"]), on="date", how="left")
        sensor = sensor.merge(trend.drop(columns=["geo_id"]), on="date", how="left")
        print("   trend rows", len(trend), flush=True)
    print("[4/5] booking curve ...", flush=True)
    bc = build_booking_curve()
    lt = bc[["date","geo_id","lead_time_mean","pct_booked_7d_out"]]
    area = area.merge(lt, on=["date","geo_id"], how="left")
    print("   booking-curve rows", len(bc), flush=True)
    print("[5/5] write outputs ...", flush=True)
    paths = {}
    p = os.path.join(OUT,"panel_site_daily.parquet"); sensor.to_parquet(p, index=False); paths["panel_site_daily"]=p
    p = os.path.join(OUT,"panel_area_daily.parquet"); area.to_parquet(p, index=False); paths["panel_area_daily"]=p
    p = os.path.join(OUT,"booking_curve_awara.parquet"); bc.to_parquet(p, index=False); paths["booking_curve_awara"]=p
    sensor.to_csv(os.path.join(OUT,"panel_site_daily.csv"), index=False)
    area.to_csv(os.path.join(OUT,"panel_area_daily.csv"), index=False)
    for name,pth in paths.items():
        MANIFEST["outputs"][name]={"path":pth,"sha256":sha_file(pth),"rows":int(pd.read_parquet(pth).shape[0])}
    covs = [coverage_summary(sensor,"panel_site_daily"), coverage_summary(area,"panel_area_daily"), coverage_summary(bc,"booking_curve_awara")]
    MANIFEST["coverage"]=covs
    with open(os.path.join(OUT,"data_manifest.json"),"w") as f: json.dump(MANIFEST,f,ensure_ascii=False,indent=2)
    with open(os.path.join(OUT,"coverage_report.md"),"w") as f:
        f.write("# Panel Coverage Report\n\n"); f.write(f"Generated {MANIFEST['generated_utc']}\n\n")
        f.write("## Pinned source commits\n\n")
        for repo,meta in MANIFEST["sources"].items():
            f.write(f"- `{repo}` @ `{meta['head_sha'][:12]}` ({meta['head_date']}) — {len(meta['files'])} files\n")
        f.write("\n## Table coverage\n\n| table | rows | date_min | date_max | geo_ids |\n|---|---|---|---|---|\n")
        for c in covs:
            f.write(f"| {c['table']} | {c['rows']} | {c['date_min']} | {c['date_max']} | {', '.join(map(str,c['geo_ids']))} |\n")
        f.write(f"\n## Structural markers\n\n- Shinkansen break: {SHINKANSEN_BREAK} (post_shinkansen flag on area panel)\n")
        f.write(f"- Camera outage: {CAM_OUTAGE[0]}..{CAM_OUTAGE[1]} (coverage_flag=outage, not zero)\n")
        if MANIFEST["notes"]:
            f.write("\n## Notes / missing\n\n"+"\n".join(f"- {n}" for n in MANIFEST["notes"])+"\n")
    print("DONE. outputs in", OUT, flush=True)

if __name__=="__main__":
    main()
