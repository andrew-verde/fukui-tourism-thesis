"""Small routing examples plus independent checks against the city timetable PDF."""

import json
import unittest
from datetime import date

from access import ROOT, Call, Feed, Trip, active_services, best_store, rides, round_trip, run, seconds
from fetch_sources import verify_sources


def call(stop, sequence, time, **kwargs):
    return Call(stop, sequence, seconds(time), seconds(time), **kwargs)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.trips = [
            Trip("out", "1", "daily", (call("O", 1, "09:00:00"), call("D", 2, "09:20:00"))),
            Trip("back", "2", "daily", (call("D", 1, "10:10:00"), call("O", 2, "10:30:00"))),
        ]

    def plan(self, **changes):
        params = dict(outward=rides(self.trips, {"O"}, {"D"}), inward=rides(self.trips, {"D"}, {"O"}),
                      ready=seconds("08:55:00"), opens=seconds("09:00:00"), closes=seconds("20:00:00"),
                      shopping=45 * 60, walk=0, buffer=2 * 60, origin_access=0, return_by=seconds("18:00:00"))
        params.update(changes)
        return round_trip(**params)

    def test_complete_round_trip_includes_waiting(self):
        result = self.plan()
        self.assertTrue(result["feasible"])
        self.assertEqual(result["shopping_end"], "10:05:00")
        self.assertEqual(result["origin_return"], "10:30:00")
        self.assertEqual(result["elapsed_minutes"], 95)

    def test_missed_last_return_is_infeasible(self):
        result = self.plan(shopping=51 * 60)
        self.assertFalse(result["feasible"])
        self.assertEqual(result["reason"], "no_return_by_deadline")

    def test_origin_access_and_boarding_allowance_can_miss_bus(self):
        self.assertFalse(self.plan(origin_access=4 * 60)["feasible"])

    def test_store_walk_is_required_in_both_directions(self):
        self.assertFalse(self.plan(walk=3 * 60)["feasible"])

    def test_shopping_must_finish_before_closing(self):
        self.assertEqual(self.plan(closes=seconds("10:00:00"))["reason"], "store_window")

    def test_store_opening_wait_is_counted(self):
        result = self.plan(opens=seconds("09:25:00"), shopping=40 * 60)
        self.assertEqual(result["store_open_wait_minutes"], 5)
        self.assertTrue(result["feasible"])

    def test_return_deadline_includes_origin_access(self):
        self.assertFalse(self.plan(origin_access=60, return_by=seconds("10:30:00"))["feasible"])

    def test_repeated_stop_keeps_later_occurrence(self):
        loop = Trip("loop", "1", "daily", (call("O", 1, "09:00:00"), call("D", 2, "09:20:00"),
                                             call("O", 3, "09:40:00")))
        back = rides([loop], {"D"}, {"O"})
        self.assertEqual(len(back), 1)
        self.assertEqual(back[0].alight.sequence, 3)

    def test_pickup_and_dropoff_restrictions(self):
        trip = Trip("restricted", "1", "daily", (call("O", 1, "09:00:00", pickup=False),
                                                   call("D", 2, "09:20:00")))
        self.assertEqual(rides([trip], {"O"}, {"D"}), [])
        trip = Trip("restricted", "1", "daily", (call("O", 1, "09:00:00"),
                                                   call("D", 2, "09:20:00", dropoff=False)))
        self.assertEqual(rides([trip], {"O"}, {"D"}), [])

    def test_midnight_time_does_not_wrap(self):
        self.assertEqual(seconds("25:10:00"), 90600)
        with self.assertRaises(ValueError):
            seconds("09:61:00")

    def test_calendar_exception_overrides_weekday(self):
        calendar = [{"service_id": "weekday", "start_date": "20260101", "end_date": "20261231",
                     **dict.fromkeys(["monday", "tuesday", "wednesday", "thursday", "friday"], "1"),
                     "saturday": "0", "sunday": "0"}]
        changes = [{"service_id": "weekday", "date": "20260915", "exception_type": "2"},
                   {"service_id": "special", "date": "20260915", "exception_type": "1"}]
        self.assertEqual(active_services(calendar, changes, date(2026, 9, 15)), {"special"})
        self.assertEqual(active_services(calendar, [], date(2026, 9, 19)), set())

    def test_any_store_selects_earliest_return_and_keeps_failed_cases(self):
        base = dict(scenario="baseline", date="2026-09-15", origin="O", ready="09:00:00")
        rows = [base | dict(destination="A", feasible=True, elapsed_minutes=150),
                base | dict(destination="B", feasible=True, elapsed_minutes=90)]
        self.assertEqual(best_store(rows)[0]["destination"], "B")
        rows = [base | dict(destination="A", feasible=False), base | dict(destination="B", feasible=False)]
        self.assertEqual(best_store(rows)[0]["reason"], "no_selected_store_round_trip")


class OnoSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        verify_sources()
        cls.feed = Feed(ROOT / "sources/onoshiei_bus.zip", {"1", "2"})

    def test_pdf_transcribed_times(self):
        """Expected values were read from PDF page 1, not copied from GTFS."""
        checks = json.loads((ROOT / "timetable_checks.json").read_text())["checks"]
        trips = {t.id: t for t in self.feed.trips}
        for row in checks:
            with self.subTest(row=row):
                matching = [c for c in trips[row["trip_id"]].calls if c.stop == row["stop_id"]]
                self.assertTrue(any(getattr(c, row["field"]) == seconds(row["expected"]) for c in matching))

    def test_weekday_weekend_and_new_year_services(self):
        self.assertEqual(len(self.feed.on(date(2026, 9, 15))), 10)
        self.assertEqual(len(self.feed.on(date(2026, 9, 19))), 4)
        self.assertEqual(self.feed.on(date(2027, 1, 1)), [])
        with self.assertRaises(ValueError):
            self.feed.on(date(2027, 4, 1))

    def test_retiming_preserves_trips_running_time_and_stop_sequence(self):
        old = self.feed.on(date(2026, 9, 15))
        new = self.feed.on(date(2026, 9, 15), {"2": 10})
        self.assertEqual(len(old), len(new))
        for before, after in zip(old, new):
            self.assertEqual(before.id, after.id)
            shift = 600 if before.route == "2" else 0
            for a, b in zip(before.calls, after.calls):
                self.assertEqual((a.stop, a.sequence, a.pickup, a.dropoff), (b.stop, b.sequence, b.pickup, b.dropoff))
                self.assertEqual(b.arrival - a.arrival, shift)
                self.assertEqual(b.departure - a.departure, shift)

    def test_every_configured_stop_is_served(self):
        study = json.loads((ROOT / "study.json").read_text())
        for name in study["origin_names"] + [s["stop_name"] for s in study["destinations"]]:
            self.assertTrue(self.feed.stop_ids(name))

    def test_store_closure_is_enforced(self):
        study = json.loads((ROOT / "study.json").read_text())
        study.update(dates=["2027-01-01"], origin_names=study["origin_names"][:1],
                     scenarios=study["scenarios"][:1], ready_end=study["ready_start"])
        result = run(study, self.feed)
        self.assertTrue(all(r["reason"] == "store_closed" and not r["within_budget"] for r in result))


if __name__ == "__main__":
    unittest.main()
