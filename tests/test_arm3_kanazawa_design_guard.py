"""Static contracts for the accepted Arm 3 Kanazawa implementation."""

from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "scripts" / "arm3_kanazawa_scm.py"


def _producer():
    spec = importlib.util.spec_from_file_location(
        "arm3_kanazawa_scm", PRODUCER
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_frozen_arm3_constants_and_donor_pools() -> None:
    producer = _producer()

    assert producer.EVENT_YM == 201503
    assert producer.INTIME_EVENT_YM == 201403
    assert producer.PANEL_CAP_YM == 201912
    assert producer.GOOD_FIT_RMSPE == 0.15
    assert producer.RMSPE_FIT_MULT == 5.0
    assert producer.OPENING_MONTHS == (201503, 201504)
    assert producer.LATE_START_YM == 201801
    assert producer.LATE_END_YM == 201912
    assert producer.PRIMARY_PRE_START_YM == 201201
    assert producer.SENSITIVITY_PRE_START_YM == 201101
    assert producer.PRE_END_YM == 201502
    assert producer.POST_END_YM == 201912
    assert producer.MASK_HAGIBIS_PRIMARY_MONTHS == (201910,)
    assert producer.MASK_HAGIBIS_RECOVERY_MONTHS == (
        201910,
        201911,
        201912,
    )
    assert producer.PRIMARY_EXCLUDED_CODES == (
        "01", "02", "03", "04", "07", "15", "16", "17", "20", "33",
        "34", "38", "43",
    )
    assert producer.STRICT_EXTRA_EXCLUDED_CODES == (
        "05", "06", "08", "12", "21", "26", "27", "28", "29", "31",
        "32", "35", "39", "44",
    )
    assert len(producer.PRIMARY_DONOR_CODES) == 34
    assert len(producer.STRICT_DONOR_CODES) == 20
    assert set(producer.PRIMARY_DONOR_CODES).isdisjoint(
        producer.PRIMARY_EXCLUDED_CODES
    )
    assert set(producer.STRICT_DONOR_CODES).isdisjoint(
        producer.STRICT_EXTRA_EXCLUDED_CODES
    )


def test_corrected_50_month_sensitivity_window_passes_guard() -> None:
    producer = _producer()

    assert len(producer._month_sequence(201201, 201502)) == 38
    assert len(producer._month_sequence(201101, 201502)) == 50
    assert len(producer._month_sequence(201503, 201912)) == 58
    producer.validate_frozen_design()


def test_full_battery_uses_exactly_two_hagibis_masks() -> None:
    producer = _producer()

    assert len(producer.BASE_SPECS) == 6
    assert len(producer.SPECS) == 12
    assert {spec.hagibis_mask for spec in producer.SPECS} == {
        "event",
        "recovery",
    }
    for spec in producer.SPECS:
        hagibis_months = set(spec.late_mask) & {201910, 201911, 201912}
        expected = (
            {201910}
            if spec.hagibis_mask == "event"
            else {201910, 201911, 201912}
        )
        assert hagibis_months == expected
