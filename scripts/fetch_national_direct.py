#!/usr/bin/env python3
"""
fetch_national_direct.py — Download direct-URL national supplementary files
(JR West press-release PDFs, 国土数値情報 archives) listed under `direct:` in
config/national_data_sources.yaml.

Writes:
  output/national_stats/raw/*
  output/national_stats/direct_manifest.json

Usage:
    python scripts/fetch_national_direct.py [--force] [--source KEY ...]
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "national_data_sources.yaml"
OUTPUT_DIR = ROOT / "output" / "national_stats"
RAW_DIR = OUTPUT_DIR / "raw"
MANIFEST_PATH = OUTPUT_DIR / "direct_manifest.json"

# JR West serves 403 to default urllib UA.
USER_AGENT = "Mozilla/5.0 (academic-research-fetch; contact: thesis author)"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _download(url: str, timeout: int) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as response:
        return response.read()


def _expected_sha256(key: str, source: dict) -> str | None:
    expected = source.get("sha256")
    if expected is None:
        return None
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError(f"{key}: sha256 must be a 64-character lowercase digest")
    return expected


def _select_sources(sources: dict, selected: list[str] | None) -> dict:
    if not selected:
        return sources
    unknown = sorted(set(selected) - set(sources))
    if unknown:
        raise ValueError(f"unknown direct source(s): {', '.join(unknown)}")
    selected_set = set(selected)
    return {key: source for key, source in sources.items() if key in selected_set}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch direct-URL national data files")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="Path to source YAML")
    parser.add_argument("--timeout", type=int, default=120, help="Download timeout per file")
    parser.add_argument("--force", action="store_true", help="Re-download even when raw file exists")
    parser.add_argument(
        "--source",
        action="append",
        help="Fetch only this direct-source config key (repeatable)",
    )
    args = parser.parse_args()

    with open(args.config) as f:
        sources = yaml.safe_load(f).get("direct", {}) or {}
    try:
        sources = _select_sources(sources, args.source)
        expected_hashes = {
            key: _expected_sha256(key, source) for key, source in sources.items()
        }
    except ValueError as exc:
        parser.error(str(exc))

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "config": str(Path(args.config).resolve()),
        "sources": {},
    }

    failures = 0
    for key, source in sources.items():
        target = RAW_DIR / source["filename"]
        downloaded = False
        if target.exists() and not args.force:
            data = target.read_bytes()
            logger.info("skip (exists): %s", target.name)
        else:
            try:
                data = _download(source["url"], args.timeout)
                downloaded = True
            except Exception as exc:  # noqa: BLE001 — record and continue
                logger.error("failed %s: %s", key, exc)
                manifest["sources"][key] = {"url": source["url"], "error": str(exc)}
                failures += 1
                continue

        actual_sha256 = _sha256(data)
        expected_sha256 = expected_hashes[key]
        if expected_sha256 is not None and actual_sha256 != expected_sha256:
            message = (
                f"SHA256 mismatch: expected {expected_sha256}, got {actual_sha256}"
            )
            logger.error("failed %s: %s", key, message)
            manifest["sources"][key] = {
                "url": source["url"],
                "filename": source["filename"],
                "expected_sha256": expected_sha256,
                "actual_sha256": actual_sha256,
                "error": message,
            }
            failures += 1
            continue

        if downloaded:
            target.write_bytes(data)
            logger.info("downloaded: %s (%d bytes)", target.name, len(data))

        entry = {
            "url": source["url"],
            "filename": source["filename"],
            "description": source.get("description", ""),
            "bytes": len(data),
            "sha256": actual_sha256,
        }
        if expected_sha256 is not None:
            entry["expected_sha256"] = expected_sha256
        manifest["sources"][key] = entry

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    logger.info("manifest written: %s", MANIFEST_PATH)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
