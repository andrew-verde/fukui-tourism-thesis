"""Direct-bus grocery round trips on the two Ono circular routes.

All calculations use seconds from the start of a GTFS service day. Repeated
stops retain their sequence positions, so a circular trip is not collapsed.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from statistics import median
from zipfile import ZipFile

from fetch_sources import verify_sources

ROOT = Path(__file__).resolve().parent


def seconds(value: str) -> int:
    h, m, s = map(int, value.split(":"))
    if h < 0 or not 0 <= m < 60 or not 0 <= s < 60:
        raise ValueError(f"Invalid GTFS time: {value}")
    return h * 3600 + m * 60 + s


def clock(value: int) -> str:
    return f"{value // 3600:02d}:{value % 3600 // 60:02d}:{value % 60:02d}"


def active_services(calendar: list[dict], exceptions: list[dict], day: date) -> set[str]:
    stamp = day.strftime("%Y%m%d")
    weekday = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][day.weekday()]
    active = {r["service_id"] for r in calendar
              if r["start_date"] <= stamp <= r["end_date"] and r[weekday] == "1"}
    for row in exceptions:
        if row["date"] == stamp:
            if row["exception_type"] == "1":
                active.add(row["service_id"])
            elif row["exception_type"] == "2":
                active.discard(row["service_id"])
            else:
                raise ValueError("Unknown calendar exception type")
    return active


@dataclass(frozen=True)
class Call:
    stop: str
    sequence: int
    arrival: int
    departure: int
    pickup: bool = True
    dropoff: bool = True


@dataclass(frozen=True)
class Trip:
    id: str
    route: str
    service: str
    calls: tuple[Call, ...]


@dataclass(frozen=True)
class Ride:
    trip: str
    route: str
    board: Call
    alight: Call


class Feed:
    def __init__(self, path: Path, route_ids: set[str]):
        with ZipFile(path) as archive:
            def read(name: str) -> list[dict]:
                if name not in archive.namelist():
                    return []
                return list(csv.DictReader(io.StringIO(archive.read(name).decode("utf-8-sig"))))
            self.info = read("feed_info.txt")[0]
            self.stops = {r["stop_id"]: r for r in read("stops.txt")}
            self.routes = {r["route_id"]: r for r in read("routes.txt") if r["route_id"] in route_ids}
            self.calendar = read("calendar.txt")
            self.exceptions = read("calendar_dates.txt")
            trips = {r["trip_id"]: r for r in read("trips.txt") if r["route_id"] in route_ids}
            if set(self.routes) != route_ids or not trips:
                raise ValueError("Selected routes are absent or have no trips")
            if any(r["trip_id"] in trips for r in read("frequencies.txt")):
                raise ValueError("Frequency-based trips are outside this prototype")
            calls: dict[str, list[Call]] = defaultdict(list)
            for row in read("stop_times.txt"):
                if row["trip_id"] not in trips:
                    continue
                pickup, dropoff = row.get("pickup_type") or "0", row.get("drop_off_type") or "0"
                if pickup not in {"0", "1"} or dropoff not in {"0", "1"}:
                    raise ValueError("On-demand boarding is outside this prototype")
                if row["stop_id"] not in self.stops:
                    raise ValueError("Unknown stop")
                calls[row["trip_id"]].append(Call(
                    row["stop_id"], int(row["stop_sequence"]), seconds(row["arrival_time"]),
                    seconds(row["departure_time"]), pickup == "0", dropoff == "0"))
            self.trips = []
            for tid, row in trips.items():
                ordered = tuple(sorted(calls[tid], key=lambda c: c.sequence))
                if len(ordered) < 2 or len({c.sequence for c in ordered}) != len(ordered):
                    raise ValueError(f"Missing or duplicate stop sequences: {tid}")
                if any(c.arrival > c.departure for c in ordered) or any(
                    a.departure > b.arrival for a, b in zip(ordered, ordered[1:])
                ):
                    raise ValueError(f"Non-monotone trip times: {tid}")
                self.trips.append(Trip(tid, row["route_id"], row["service_id"], ordered))

    def on(self, day: date, shifts: dict[str, int] | None = None) -> list[Trip]:
        stamp = day.strftime("%Y%m%d")
        if not self.info["feed_start_date"] <= stamp <= self.info["feed_end_date"]:
            raise ValueError(f"Date outside feed validity: {day}")
        services = active_services(self.calendar, self.exceptions, day)
        selected = []
        for trip in self.trips:
            if trip.service in services:
                shift = (shifts or {}).get(trip.route, 0) * 60
                if any(c.arrival + shift < 0 for c in trip.calls):
                    raise ValueError("Retiming crosses the start of the service day")
                selected.append(replace(trip, calls=tuple(replace(
                    c, arrival=c.arrival + shift, departure=c.departure + shift) for c in trip.calls)))
        return selected

    def stop_ids(self, name: str) -> set[str]:
        served = {c.stop for t in self.trips for c in t.calls}
        ids = {sid for sid, row in self.stops.items() if row["stop_name"] == name and sid in served}
        if not ids:
            raise ValueError(f"No selected-route stop matches {name!r}")
        return ids


def rides(trips: list[Trip], origins: set[str], destinations: set[str]) -> list[Ride]:
    result = []
    for trip in trips:
        for i, board in enumerate(trip.calls):
            if board.stop in origins and board.pickup:
                for alight in trip.calls[i + 1:]:
                    if alight.stop in destinations and alight.dropoff:
                        result.append(Ride(trip.id, trip.route, board, alight))
    return sorted(result, key=lambda r: (r.board.departure, r.alight.arrival, r.trip))


def round_trip(outward: list[Ride], inward: list[Ride], ready: int, opens: int, closes: int,
               shopping: int, walk: int, buffer: int, origin_access: int, return_by: int) -> dict:
    """Choose earliest return to the origin area, including waiting from ready time.

Walking and boarding allowances are scenario assumptions, not measured paths.
Waiting before store opening is permitted. No transfers occur within a leg.
"""
    best = None
    had_bus = False
    had_shop = False
    for out in outward:
        if out.board.departure < ready + origin_access + buffer:
            continue
        had_bus = True
        start = max(out.alight.arrival + walk, opens)
        end = start + shopping
        if end > closes:
            continue
        had_shop = True
        for back in inward:
            if back.board.departure < end + walk + buffer:
                continue
            finish = back.alight.arrival + origin_access
            if finish > return_by:
                continue
            key = (finish, out.board.departure, back.board.departure, out.trip, back.trip)
            if best is None or key < best[0]:
                best = (key, out, back, start, end)
    if best is None:
        reason = "no_outbound_bus" if not had_bus else "store_window" if not had_shop else "no_return_by_deadline"
        return {"feasible": False, "reason": reason}
    key, out, back, start, end = best
    finish = key[0]
    return {
        "feasible": True, "reason": "", "out_trip": out.trip, "out_route": out.route,
        "out_board_stop": out.board.stop, "out_board_sequence": out.board.sequence,
        "out_departure": clock(out.board.departure), "out_alight_stop": out.alight.stop,
        "out_alight_sequence": out.alight.sequence, "out_arrival": clock(out.alight.arrival),
        "shopping_start": clock(start), "shopping_end": clock(end),
        "back_trip": back.trip, "back_route": back.route, "back_board_stop": back.board.stop,
        "back_board_sequence": back.board.sequence, "back_departure": clock(back.board.departure),
        "back_alight_stop": back.alight.stop, "back_alight_sequence": back.alight.sequence,
        "back_arrival": clock(back.alight.arrival), "origin_return": clock(finish),
        "elapsed_minutes": (finish - ready) / 60,
        "initial_wait_minutes": (out.board.departure - ready - origin_access) / 60,
        "store_open_wait_minutes": (start - out.alight.arrival - walk) / 60,
        "return_wait_minutes": (back.board.departure - end - walk) / 60,
        "bus_minutes": (out.alight.arrival - out.board.departure + back.alight.arrival - back.board.departure) / 60,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(study: dict, feed: Feed) -> list[dict]:
    results = []
    for scenario in study["scenarios"]:
        for stamp in study["dates"]:
            day = date.fromisoformat(stamp)
            trips = feed.on(day, scenario["route_shift_minutes"])
            for origin in study["origin_names"]:
                origin_ids = feed.stop_ids(origin)
                for store in study["destinations"]:
                    store_ids = feed.stop_ids(store["stop_name"])
                    outward = rides(trips, origin_ids, store_ids)
                    inward = rides(trips, store_ids, origin_ids)
                    for ready in range(seconds(study["ready_start"]), seconds(study["ready_end"]) + 1,
                                       study["ready_step_minutes"] * 60):
                        row = {"scenario": scenario["id"], "date": stamp, "origin": origin,
                               "destination": store["id"], "ready": clock(ready)}
                        if day.strftime("%m-%d") in store["closed_month_days"]:
                            trip = {"feasible": False, "reason": "store_closed"}
                        else:
                            trip = round_trip(outward, inward, ready, seconds(store["opens"]),
                                              seconds(store["closes"]), scenario["shopping_minutes"] * 60,
                                              scenario["store_walk_minutes"] * 60,
                                              scenario["boarding_buffer_minutes"] * 60,
                                              study["origin_access_minutes"] * 60, seconds(study["return_by"]))
                        row.update(trip)
                        row["within_budget"] = trip["feasible"] and trip["elapsed_minutes"] <= study["elapsed_budget_minutes"]
                        results.append(row)
    return results


def summarize(rows: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["scenario"], row["date"]].append(row)
    result = []
    for (scenario, day), group in groups.items():
        times = [r["elapsed_minutes"] for r in group if r["feasible"]]
        result.append({"scenario": scenario, "date": day, "origin_store_ready_cases": len(group),
                       "feasible_cases": len(times), "within_budget_cases": sum(r["within_budget"] for r in group),
                       "median_elapsed_minutes_feasible_only": median(times) if times else None,
                       "max_elapsed_minutes_feasible_only": max(times) if times else None})
    return result


def best_store(rows: list[dict]) -> list[dict]:
    """One case per origin and ready time, allowing either selected store."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["scenario"], row["date"], row["origin"], row["ready"]].append(row)
    result = []
    for group in groups.values():
        selected = dict(min(group, key=lambda r: (not r["feasible"], r.get("elapsed_minutes", float("inf")), r["destination"])))
        if not selected["feasible"]:
            selected.update(destination="", reason="no_selected_store_round_trip")
        result.append(selected)
    return result


def compare(rows: list[dict]) -> list[dict]:
    key = lambda r: (r["date"], r["origin"], r["destination"], r["ready"])
    baseline = {key(r): r for r in rows if r["scenario"] == "baseline"}
    comparisons = []
    for row in rows:
        if row["scenario"] == "baseline":
            continue
        old = baseline[key(row)]
        comparisons.append({k: row[k] for k in ["scenario", "date", "origin", "destination", "ready"]} | {
            "baseline_feasible": old["feasible"], "scenario_feasible": row["feasible"],
            "baseline_within_budget": old["within_budget"], "scenario_within_budget": row["within_budget"],
            "elapsed_change_minutes": row["elapsed_minutes"] - old["elapsed_minutes"]
            if row["feasible"] and old["feasible"] else None})
    return comparisons


def main() -> None:
    hashes = verify_sources()
    study = json.loads((ROOT / "study.json").read_text())
    feed = Feed(ROOT / study["feed"], set(study["route_ids"]))
    output = ROOT / "results"
    output.mkdir(exist_ok=True)
    rows = run(study, feed)
    any_store = best_store(rows)
    write_csv(output / "journeys.csv", rows)
    write_csv(output / "summary.csv", summarize(rows))
    write_csv(output / "any_store_journeys.csv", any_store)
    write_csv(output / "any_store_summary.csv", summarize(any_store))
    write_csv(output / "comparisons.csv", compare(rows))
    selected_names = set(study["origin_names"]) | {s["stop_name"] for s in study["destinations"]}
    selected_ids = set().union(*(feed.stop_ids(n) for n in selected_names))
    write_csv(output / "stops.csv", [feed.stops[sid] for sid in sorted(selected_ids)])
    audit = {
        "status": "exploratory computation; no population or causal interpretation",
        "sources": hashes,
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "study_sha256": hashlib.sha256((ROOT / "study.json").read_bytes()).hexdigest(),
        "feed_info": feed.info, "selected_routes": list(feed.routes.values()),
        "selected_trip_patterns": len(feed.trips),
        "active_trip_counts": {day: dict(Counter(t.route for t in feed.on(date.fromisoformat(day)))) for day in study["dates"]},
        "trips_with_repeated_stop_ids": sum(len({c.stop for c in t.calls}) < len(t.calls) for t in feed.trips),
        "origin_count": len(study["origin_names"]), "destination_count": len(study["destinations"]),
        "journey_rows": len(rows),
        "limitations": ["Direct buses only; no transfer or walking-only alternatives",
                        "Origins are named stop areas, not homes or population samples",
                        "Origin access and store walking times are unmeasured assumptions",
                        "Retiming is hypothetical; no vehicle or driver scheduling data",
                        "Scheduled service only; no delays, capacity, fares or pedestrian barriers modeled"]}
    (output / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summarize(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
