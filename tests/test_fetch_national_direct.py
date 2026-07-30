import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scripts.fetch_national_direct as fetch_direct
from scripts.fetch_national_direct import _expected_sha256, _select_sources


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "national_data_sources.yaml"

EXPECTED_ARM3_PINS = {
    "jta_accommodation_2011_confirmed": (
        "d47b5caec1da4a2f986cee89636483283d1b4375c5a76f849ce0d32d4d681a1f"
    ),
    "jta_accommodation_2012_confirmed": (
        "3ece2333d8dd3014e95b9687a9609da9843ed02dafe56928ef9a8faccd1386fe"
    ),
    "jta_accommodation_2013_confirmed": (
        "fec002e6c1cac48de968fbafee57be6d5f043b53c20e389ced8e721dd0695882"
    ),
    "jta_accommodation_2014_confirmed": (
        "1546ef4319cc7c1bc6a6868ab849789187faa7d205908877473c5f765578307a"
    ),
    "jta_accommodation_2015_confirmed": (
        "d03b0b35d219e7cedd644f83badb214644c703f71eb924c15a0a241b28f50f13"
    ),
    "jta_accommodation_2016_confirmed": (
        "efeef94ea5a549e636c578d18af1a48fc4b982bfa0061ae734003f919d969ed4"
    ),
    "jta_accommodation_2017_confirmed": (
        "6ace13525563fd28ff02dc3cadbd7a39fd0c7056db30df1dd9cdbc73254b5ca2"
    ),
}
EXPECTED_TIMESERIES_PIN = (
    "c866c06362cbe88ac5241280857427337b9ace71ce6ac42f69394f124fc644bb"
)


def test_arm3_annual_vintages_have_exact_lowercase_sha256_pins():
    direct = yaml.safe_load(CONFIG.read_text())["direct"]
    actual = {key: direct[key]["sha256"] for key in EXPECTED_ARM3_PINS}

    assert actual == EXPECTED_ARM3_PINS
    assert all(re.fullmatch(r"[0-9a-f]{64}", digest) for digest in actual.values())


def test_arm3_canonical_timeseries_has_exact_sha256_pin():
    direct = yaml.safe_load(CONFIG.read_text())["direct"]

    assert (
        direct["jta_accommodation_timeseries"]["sha256"]
        == EXPECTED_TIMESERIES_PIN
    )


def test_source_selection_excludes_unrelated_direct_sources():
    sources = {
        "jta_accommodation_2011_confirmed": {"filename": "2011.xls"},
        "jta_accommodation_2017_confirmed": {"filename": "2017.xlsx"},
        "unrelated_later_source": {"filename": "later.xlsx"},
    }

    selected = _select_sources(
        sources,
        [
            "jta_accommodation_2011_confirmed",
            "jta_accommodation_2017_confirmed",
        ],
    )

    assert list(selected) == [
        "jta_accommodation_2011_confirmed",
        "jta_accommodation_2017_confirmed",
    ]
    assert _select_sources(sources, None) is sources


def test_sha256_mismatch_does_not_accept_download(tmp_path, monkeypatch):
    config = tmp_path / "sources.yaml"
    config.write_text(
        yaml.safe_dump(
            {
                "direct": {
                    "pinned": {
                        "url": "https://example.invalid/pinned.xlsx",
                        "filename": "pinned.xlsx",
                        "sha256": "a" * 64,
                    }
                }
            }
        )
    )
    raw_dir = tmp_path / "raw"
    manifest = tmp_path / "manifest.json"
    payload = b"not the pinned bytes"

    monkeypatch.setattr(fetch_direct, "RAW_DIR", raw_dir)
    monkeypatch.setattr(fetch_direct, "MANIFEST_PATH", manifest)
    monkeypatch.setattr(fetch_direct, "_download", lambda url, timeout: payload)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "fetch_national_direct.py",
            "--config",
            str(config),
            "--source",
            "pinned",
        ],
    )

    assert fetch_direct.main() == 1
    assert not (raw_dir / "pinned.xlsx").exists()
    entry = json.loads(manifest.read_text())["sources"]["pinned"]
    assert entry["expected_sha256"] == "a" * 64
    assert entry["actual_sha256"] == hashlib.sha256(payload).hexdigest()
    assert "SHA256 mismatch" in entry["error"]


def test_expected_sha256_rejects_non_lowercase_or_short_pins():
    for invalid in ["unknown", "A" * 64]:
        try:
            _expected_sha256("bad", {"sha256": invalid})
        except ValueError as exc:
            assert "64-character lowercase digest" in str(exc)
        else:
            raise AssertionError("invalid sha256 pin was accepted")
