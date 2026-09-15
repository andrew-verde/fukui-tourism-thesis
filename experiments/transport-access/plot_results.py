"""Plot computed access times and the selected GTFS stop locations.

Optional dependency: matplotlib. Run access.py first. No basemap is fetched.
"""

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent


def main():
    study = json.loads((ROOT / "study.json").read_text())
    with (ROOT / "results/any_store_journeys.csv").open() as f:
        rows = [r for r in csv.DictReader(f) if r["scenario"] == "baseline"]
    ready = sorted({r["ready"] for r in rows})
    cmap = plt.colormaps["viridis"].copy()
    cmap.set_bad("#dddddd")
    fig, axes = plt.subplots(1, len(study["dates"]), figsize=(13, 6), sharey=True, layout="constrained")
    for ax, day in zip(np.atleast_1d(axes), study["dates"]):
        values = np.full((len(study["origin_names"]), len(ready)), np.nan)
        for row in rows:
            if row["date"] == day and row["feasible"] == "True":
                values[study["origin_names"].index(row["origin"]), ready.index(row["ready"])] = float(row["elapsed_minutes"])
        img = ax.imshow(values, aspect="auto", cmap=cmap, vmin=60, vmax=420)
        ax.set_xticks(range(0, len(ready), 2), [r[:5] for r in ready[::2]], rotation=45)
        ax.set_yticks(range(len(study["origin_names"])), [f"O{i+1}" for i in range(len(study["origin_names"]))])
        ax.set_xlabel("Ready at origin area")
        ax.set_title(day)
    axes[0].set_ylabel("Origin stop area, IDs in origin_key.csv")
    fig.colorbar(img, ax=axes, label="Minutes from ready time to return, including waiting")
    fig.suptitle("Direct-bus round trip to either selected grocery store\n45-minute shop; assumed 5-minute store walks; grey = no return by 18:00", fontsize=12)
    fig.savefig(ROOT / "results/access_matrix.png", dpi=180)
    plt.close(fig)

    with (ROOT / "results/stops.csv").open() as f:
        stops = list(csv.DictReader(f))
    points = {}
    for row in stops:
        points.setdefault(row["stop_name"], []).append((float(row["stop_lon"]), float(row["stop_lat"])))
    fig, ax = plt.subplots(figsize=(7, 7), layout="constrained")
    key = []
    for i, name in enumerate(study["origin_names"]):
        xy = np.mean(points[name], axis=0)
        ax.scatter(*xy, c="#245a80", s=35)
        ax.annotate(f"O{i+1}", xy, xytext=(5, 5), textcoords="offset points")
        key.append({"id": f"O{i+1}", "name": name, "longitude": xy[0], "latitude": xy[1]})
    for store in study["destinations"]:
        xy = np.mean(points[store["stop_name"]], axis=0)
        ax.scatter(*xy, c="#ad3c20", marker="s", s=60)
        ax.annotate(store["id"].removeprefix("kajiso_").title() + " stop", xy,
                    xytext=(5, 10), textcoords="offset points")
    ax.set_aspect(1 / np.cos(np.deg2rad(36)))
    ax.margins(.20)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Selected Ono stop areas\nSquares are grocery bus stops, not surveyed entrances")
    ax.ticklabel_format(useOffset=False)
    fig.savefig(ROOT / "results/study_locations.png", dpi=180)
    plt.close(fig)
    with (ROOT / "results/origin_key.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(key[0]))
        writer.writeheader()
        writer.writerows(key)


if __name__ == "__main__":
    main()
