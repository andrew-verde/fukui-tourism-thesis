#!/usr/bin/env python3
"""Awara occupancy: frozen forward prediction test at a 30-day horizon.

Executes ADR 0040. This script is committed BEFORE the unseen pull and must not be edited
after it; edits are visible in git history and any edit voids the confirmatory status.

Modes:
  --guard-only   run the vintage-revision guard on the seen window and stop (no unseen read)
  --evaluate     guard, then the single evaluation of P1, P2, S1-S3

Frozen quantities (all fixed pre-pull, see ADR 0040 "Frozen inputs"):
  capacity denominator = 576 rooms, NOT recomputed from a fresh latest_hotel.csv. The
    upstream capacity is a moving sum over latest_hotel.csv; recomputing it would rescale
    the outcome and silently invalidate the frozen coefficients.
  trend origin         = 2023-10-01, the first night of the seen panel.
  coefficients         = data/frozen/awara_frozen_model_coefficients.csv (M3)
                         data/frozen/awara_frozen_m1_coefficients.csv (M1, S2 comparator)
"""
import argparse, hashlib, json, os, sys
import numpy as np, pandas as pd, jpholiday
from scipy import stats

CAP_FROZEN   = 576.0
TREND_ORIGIN = pd.Timestamp("2023-10-01")
SEEN_END     = pd.Timestamp("2026-07-08")
SEEN_START   = pd.Timestamp("2023-10-01")
HORIZON      = 30
FLAG_THR     = 0.60
MIN_UNSEEN   = 60
GUARD_RMS    = 0.02      # RMS relative revision of rsv_occ_proxy on the seen window
GUARD_MAXPP  = 0.01      # max single seen night absolute difference, 1 percentage point
ALPHA        = 0.05
S1_MAE_CEIL  = 0.090     # 9.0 pp
S3_GAP_FLOOR = 0.15      # 15 pp peak-vs-midweek gap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def load_quarantine(qdir):
    """Fresh pull: booking curve (predictors) + reservation sums (outcome). Capacity frozen."""
    bc = pd.read_csv(os.path.join(qdir, "booking_curve.csv"))
    bc.columns = [c.strip() for c in bc.columns]
    bc = bc.rename(columns={"target_date": "date"})
    bc["date"] = pd.to_datetime(bc["date"])
    rs = pd.read_csv(os.path.join(qdir, "latest_rsv_sum.csv"))
    rs.columns = [c.strip() for c in rs.columns]
    rs = rs.rename(columns={"date_visit": "date", "n_room": "rsv_n_room"})
    rs["date"] = pd.to_datetime(rs["date"])
    rs["rsv_occ_proxy"] = rs["rsv_n_room"] / CAP_FROZEN
    return bc.merge(rs[["date", "rsv_occ_proxy"]], on="date", how="inner").sort_values("date").reset_index(drop=True)


def features(d):
    d = d.copy()
    d["dow"] = d.date.dt.dayofweek
    d["month"] = d.date.dt.month
    d["is_hol"] = d.date.map(lambda x: jpholiday.is_holiday(x.date()))
    d["eve_hol"] = (d.date + pd.Timedelta(days=1)).map(lambda x: jpholiday.is_holiday(x.date())).values & ~d.is_hol.values
    d["trend"] = (d.date - TREND_ORIGIN).dt.days / 365.25
    occ = d.set_index("date").rsv_occ_proxy
    d["occ_lag364"] = occ.reindex(d.date - pd.Timedelta(days=364)).values
    for k in (30, 60, 90):
        col = f"ago_{k}days"
        assert col in d.columns, f"missing {col}"
        d[f"l_ago{k}"] = np.log(d[col].replace(0, np.nan))
    d["pickup_60_30"] = d.l_ago30 - d.l_ago60
    d["pickup_90_60"] = d.l_ago60 - d.l_ago90
    # horizon assertion: no sub-30-day state may enter any prediction
    for c in d.columns:
        if c.startswith("ago_") and int(c.replace("ago_", "").replace("days", "")) < HORIZON:
            assert c not in DESIGN_TERMS_SOURCE, f"{c} is inside the horizon"
    return d


DESIGN_TERMS_SOURCE = {"l_ago30", "l_ago60", "l_ago90", "pickup_60_30", "pickup_90_60",
                       "trend", "occ_lag364", "dow", "is_hol", "eve_hol", "month"}


def design(d, terms):
    """Build the design matrix manually from frozen term names.

    Manual construction rather than a patsy formula so that reference levels cannot drift
    between the fitting session and this one; every frozen term must be reproduced exactly
    or the run aborts.
    """
    X = pd.DataFrame(index=d.index)
    for t in terms:
        if t == "Intercept":
            X[t] = 1.0
        elif t.startswith("C(dow)[T."):
            X[t] = (d.dow == int(t.split("T.")[1].rstrip("]"))).astype(float)
        elif t.startswith("C(month)[T."):
            X[t] = (d.month == int(t.split("T.")[1].rstrip("]"))).astype(float)
        elif t == "C(is_hol)[T.True]":
            X[t] = d.is_hol.astype(float)
        elif t == "C(eve_hol)[T.True]":
            X[t] = d.eve_hol.astype(float)
        elif t in d.columns:
            X[t] = d[t].astype(float)
        else:
            raise RuntimeError(f"frozen term not reproducible: {t}")
    return X


def predict(d, coef_path):
    c = pd.read_csv(coef_path).set_index("term").coef
    return design(d, list(c.index)).values @ c.values


def eligible_unseen(d, pull_date):
    """Nights that are genuinely unseen outcomes.

    Excludes the forward-filled tail: upstream repeats the on-hand count at every horizon
    for stay nights after the pull, so a flat curve is a booking snapshot, not an outcome.
    """
    ago = [c for c in d.columns if c.startswith("ago_")]
    flat = d[ago].nunique(axis=1) <= 1
    ok = ((d.date > SEEN_END) & (d.date < pull_date) & (~flat)
          & d[["l_ago30", "l_ago60", "l_ago90", "occ_lag364", "rsv_occ_proxy"]].notna().all(axis=1))
    return d[ok].copy(), {"flat_curve_excluded": int((flat & (d.date > SEEN_END)).sum()),
                          "post_pull_total": int((d.date > SEEN_END).sum())}


def guard(fresh, committed):
    f = fresh[(fresh.date >= SEEN_START) & (fresh.date <= SEEN_END)].set_index("date").rsv_occ_proxy
    c = committed[(committed.date >= SEEN_START) & (committed.date <= SEEN_END)].set_index("date").rsv_occ_proxy
    j = pd.concat([f.rename("fresh"), c.rename("committed")], axis=1).dropna()
    rel = ((j.fresh - j.committed) / j.committed.replace(0, np.nan)).dropna()
    absd = (j.fresh - j.committed).abs()
    rms = float(np.sqrt((rel ** 2).mean())) if len(rel) else float("nan")
    mx = float(absd.max()) if len(absd) else float("nan")
    return {"n_seen_nights_compared": int(len(j)),
            "n_seen_nights_committed": int(len(c)), "n_seen_nights_fresh": int(len(f)),
            "rms_relative_revision": rms, "rms_limit": GUARD_RMS,
            "max_abs_night_diff": mx, "max_abs_limit": GUARD_MAXPP,
            "worst_night": str(absd.idxmax().date()) if len(absd) else None,
            "status": "passed" if (rms <= GUARD_RMS and mx <= GUARD_MAXPP) else "BREACHED"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quarantine", required=True)
    ap.add_argument("--pull-date", required=True)
    ap.add_argument("--guard-only", action="store_true")
    ap.add_argument("--out", default=os.path.join(REPO, "output", "awara_forward"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    pull_date = pd.Timestamp(a.pull_date)

    res = {"adr": "0040", "executed_utc": pd.Timestamp.utcnow().isoformat(),
           "pull_date": str(pull_date.date()), "capacity_frozen": CAP_FROZEN,
           "trend_origin": str(TREND_ORIGIN.date()),
           "quarantine_checksums": {f: sha256(os.path.join(a.quarantine, f))
                                    for f in sorted(os.listdir(a.quarantine)) if f.endswith(".csv")}}

    fresh = features(load_quarantine(a.quarantine))
    bc = pd.read_parquet(os.path.join(REPO, "data/nonsurvey/booking_curve_awara.parquet"))
    ar = pd.read_parquet(os.path.join(REPO, "data/nonsurvey/panel_area_daily.parquet"))
    ar["date"] = pd.to_datetime(ar.date)
    committed = ar[ar.geo_id == "awara_onsen"][["date", "rsv_occ_proxy"]]

    res["guard"] = guard(fresh, committed)
    if res["guard"]["status"] != "passed":
        res["verdict"] = "STOPPED at vintage guard — log a deviation ADR per 0040"
        json.dump(res, open(os.path.join(a.out, "awara_forward_results.json"), "w"), indent=2)
        print(json.dumps(res["guard"], indent=2)); print("\nSTOPPED:", res["verdict"]); return 2
    if a.guard_only:
        json.dump(res, open(os.path.join(a.out, "awara_forward_guard.json"), "w"), indent=2)
        print(json.dumps(res["guard"], indent=2)); print("\nguard-only: stopping before unseen read"); return 0

    te, excl = eligible_unseen(fresh, pull_date)
    res["unseen"] = {**excl, "n_eligible": int(len(te)), "minimum_required": MIN_UNSEEN,
                     "date_min": str(te.date.min().date()) if len(te) else None,
                     "date_max": str(te.date.max().date()) if len(te) else None}
    if len(te) < MIN_UNSEEN:
        res["verdict"] = f"WAITING — {len(te)} eligible unseen nights, minimum {MIN_UNSEEN}"
        json.dump(res, open(os.path.join(a.out, "awara_forward_results.json"), "w"), indent=2)
        print(json.dumps(res["unseen"], indent=2)); print("\n" + res["verdict"]); return 0

    y = te.rsv_occ_proxy.values
    p3 = predict(te, os.path.join(REPO, "data/frozen/awara_frozen_model_coefficients.csv"))
    p1c = predict(te, os.path.join(REPO, "data/frozen/awara_frozen_m1_coefficients.csv"))
    p0 = te.occ_lag364.values
    e3, e0, e1 = np.abs(y - p3), np.abs(y - p0), np.abs(y - p1c)

    # P1 - frozen M3 beats the naive seasonal rule
    w = stats.wilcoxon(e3, e0, alternative="less")
    res["P1"] = {"mae_M3": float(e3.mean()), "mae_M0_naive": float(e0.mean()),
                 "median_abs_err_M3": float(np.median(e3)), "median_abs_err_M0": float(np.median(e0)),
                 "wilcoxon_stat": float(w.statistic), "p_one_sided": float(w.pvalue), "alpha": ALPHA,
                 "status": ("falsified" if e3.mean() >= e0.mean()
                            else "confirmed" if w.pvalue <= ALPHA else "directional-only")}
    # P2 - soft nights identifiable at the horizon
    flag = p3 < FLAG_THR
    act = y < FLAG_THR
    base = float(act.mean())
    hits, n_flag = int((flag & act).sum()), int(flag.sum())
    prec = hits / n_flag if n_flag else float("nan")
    bino = stats.binomtest(hits, n_flag, base, alternative="greater").pvalue if n_flag else float("nan")
    res["P2"] = {"n_flagged": n_flag, "hits": hits, "precision": prec,
                 "recall": float((flag & act).sum() / act.sum()) if act.sum() else float("nan"),
                 "unseen_base_rate": base, "p_one_sided": float(bino), "alpha": ALPHA,
                 "status": ("falsified" if not (prec > base)
                            else "confirmed" if bino <= ALPHA else "directional-only")}
    res["headline_verdict"] = ("prediction confirmed"
                               if res["P1"]["status"] == "confirmed" and res["P2"]["status"] == "confirmed"
                               else "prediction falsified"
                               if "falsified" in (res["P1"]["status"], res["P2"]["status"])
                               else "partial support")
    # Secondaries - reported, never headline
    peak = te.date.dt.dayofweek.isin([4, 5]) | te.is_hol | te.eve_hol
    res["S1_no_accuracy_collapse"] = {"mae_M3": float(e3.mean()), "ceiling": S1_MAE_CEIL,
                                      "status": "held" if e3.mean() <= S1_MAE_CEIL else "exceeded",
                                      "secondary_only": True}
    w2 = stats.wilcoxon(e3, e1, alternative="less")
    res["S2_state_beats_calendar"] = {"mae_M3": float(e3.mean()), "mae_M1_calendar_only": float(e1.mean()),
                                      "p_one_sided": float(w2.pvalue),
                                      "status": "replicated" if (e3.mean() < e1.mean() and w2.pvalue <= ALPHA) else "not replicated",
                                      "secondary_only": True}
    gap = float(y[peak.values].mean() - y[~peak.values].mean()) if peak.any() and (~peak).any() else float("nan")
    res["S3_demand_gap_persists"] = {"peak_minus_midweek": gap, "floor": S3_GAP_FLOOR,
                                     "n_peak": int(peak.sum()), "n_midweek": int((~peak).sum()),
                                     "status": "persists" if gap >= S3_GAP_FLOOR else "eroded",
                                     "secondary_only": True}
    pd.DataFrame({"date": te.date.dt.date, "actual": y, "pred_M3_frozen": p3,
                  "pred_M0_naive": p0, "pred_M1_calendar": p1c,
                  "flagged_soft": flag, "actually_soft": act}).to_csv(
        os.path.join(a.out, "awara_forward_predictions.csv"), index=False)
    json.dump(res, open(os.path.join(a.out, "awara_forward_results.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in res.items() if k != "quarantine_checksums"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
