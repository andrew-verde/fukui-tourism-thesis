"""Figure for ADR 0041: Awara forward prediction test result.

Reads only the committed evaluation outputs. Renders nothing that is not in them.
"""
import pandas as pd, numpy as np, json, matplotlib as mpl, matplotlib.pyplot as plt

R = "output/awara_forward"
p = pd.read_csv(f"{R}/awara_forward_predictions.csv"); p["date"] = pd.to_datetime(p.date)
res = json.load(open(f"{R}/awara_forward_results.json"))
apply_figure_style(sizes=(8, 7, 6))

M3, M0, M1, ALARM = "#1b6ca8", "#d95f02", "#9aa0a6", "#b2182b"
e3 = (p.actual - p.pred_M3_frozen).abs(); e0 = (p.actual - p.pred_M0_naive).abs()
e1 = (p.actual - p.pred_M1_calendar).abs()
assert abs(e3.mean() - res["P1"]["mae_M3"]) < 1e-12
assert abs(e0.mean() - res["P1"]["mae_M0_naive"]) < 1e-12
assert abs(e1.mean() - res["S2_state_beats_calendar"]["mae_M1_calendar_only"]) < 1e-12
n = len(p)
assert n == res["unseen"]["n_eligible"]

fig = plt.figure(figsize=(7.2, 5.4))
gs = fig.add_gridspec(2, 2, hspace=0.52, wspace=0.28)
axa, axb = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
axc, axd = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])

# (a) one MAE per model - lollipop
lab = ["same night\nlast year", "booking state\n+ seasonal lag", "calendar\nonly"]
val = [e0.mean() * 100, e3.mean() * 100, e1.mean() * 100]
col = [M0, M3, M1]
y = np.arange(3)[::-1]
for yi, v, c in zip(y, val, col):
    axa.plot([0, v], [yi, yi], color=c, lw=1.0, alpha=0.55, zorder=1, solid_capstyle="butt")
    axa.plot(v, yi, "o", color=c, ms=6.5, zorder=3)
    axa.annotate(f"{v:.1f}", xy=(v, yi), xytext=(5, 0), textcoords="offset points",
                 va="center", fontsize=6, color=c)
axa.set_yticks(y); axa.set_yticklabels(lab)
axa.set_xlabel("mean absolute error (percentage points)")
axa.set_title("The parameterless rule is the most accurate", loc="left")
axa.set_xlim(0, max(val) * 1.22); axa.margins(y=0.18)
axa.annotate("lower = better", xy=(0.98, -0.30), xycoords="axes fraction",
             fontsize=6, color=META_GREY, ha="right")

# (b) paired per-night error difference
dif = (e3 - e0) * 100
order = np.argsort(dif.values)
axb.bar(np.arange(n), dif.values[order], width=0.9,
        color=[M3 if v > 0 else M0 for v in dif.values[order]], linewidth=0)
axb.axhline(0, color="0.25", lw=0.7)
worse = int((dif > 0).sum())
axb.set_xlabel(f"the {n} unseen nights, sorted by difference")
axb.set_ylabel("error gap (pp)\nmodel minus naive")
axb.set_title("The model is worse on most nights", loc="left")
axb.annotate(f"model worse on {worse}/{n}", xy=(0.03, 0.95), xycoords="axes fraction",
             fontsize=6, color=M3, ha="left", va="top")
axb.set_xticks([]); axb.margins(x=0.02)

# (c) realised vs both predictions
axc.plot(p.date, p.actual * 100, color="0.15", lw=1.1, label="realised", zorder=3)
axc.plot(p.date, p.pred_M0_naive * 100, color=M0, lw=0.9, alpha=0.9, label="same night last year")
axc.plot(p.date, p.pred_M3_frozen * 100, color=M3, lw=0.9, alpha=0.9, label="booking state + lag")
axc.axhline(60, color=ALARM, lw=0.7, ls=(0, (3, 2)), zorder=1,
            label="60% soft-night threshold")
axc.set_ylabel("occupancy proxy (%)")
axc.set_title("Both track the weekly cycle", loc="left")
axc.legend(frameon=False, fontsize=6, loc="lower left", ncol=1, handlelength=1.3)
axc.xaxis.set_major_formatter(mpl.dates.DateFormatter("%d %b"))
axc.xaxis.set_major_locator(mpl.dates.MonthLocator())

# (d) soft-night flagging vs base rate
base = res["P2"]["unseen_base_rate"] * 100
prec = res["P2"]["precision"] * 100
axd.plot([0, base], [1, 1], color=META_GREY, lw=1.0, alpha=0.55, solid_capstyle="butt")
axd.plot(base, 1, "o", color=META_GREY, ms=6.5)
axd.plot([0, prec], [0, 0], color=M3, lw=1.0, alpha=0.55, solid_capstyle="butt")
axd.plot(prec, 0, "o", color=M3, ms=6.5)
axd.annotate(f"{base:.0f}", xy=(base, 1), xytext=(5, 0), textcoords="offset points",
             va="center", fontsize=6, color=META_GREY)
axd.annotate(f"{prec:.0f}", xy=(prec, 0), xytext=(5, 0), textcoords="offset points",
             va="center", fontsize=6, color=M3)
axd.set_yticks([1, 0])
axd.set_yticklabels(["soft nights in\nthe window", "flagged nights\nthat were soft"])
axd.set_xlabel("share of nights below 60% occupancy (%)")
axd.set_title("Flagging works, but flags half the calendar", loc="left")
axd.set_xlim(0, prec * 1.35); axd.margins(y=0.35)
axd.annotate(f"{res['P2']['n_flagged']}/{n} nights flagged, catching all "
             f"{res['P2']['hits']} soft ones\n(p = {res['P2']['p_one_sided']:.3f})",
             xy=(0.03, 0.42), xycoords="axes fraction", fontsize=5.8, color="0.3", va="top")

for ax, L in ((axa, "a"), (axb, "b"), (axc, "c"), (axd, "d")):
    panel_letter(ax, L)
fig.savefig(f"{R}/awara_forward.png", dpi=300, bbox_inches="tight")

r = fig.canvas.get_renderer()
texts = [(t, t.get_window_extent(r)) for t in fig.findobj(mpl.text.Text)
         if t.get_text().strip() and t.get_visible()]
ov = [(a.get_text(), b.get_text()) for i, (a, ba) in enumerate(texts)
      for b, bb in texts[i+1:] if ba.overlaps(bb)]
print("MAE pp  naive", round(val[0], 2), "| model", round(val[1], 2), "| calendar", round(val[2], 2))
print("model worse on", worse, "of", n, "| text-text overlaps:", len(ov))
