"""Restore missing source snapshots, refusing bytes that differ from the manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent


def verify_sources(root: Path = ROOT) -> dict[str, str]:
    manifest = json.loads((root / "sources/manifest.json").read_text())
    hashes = {}
    for item in manifest["sources"]:
        path = root / "sources" / item["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            raise ValueError(f"Source checksum mismatch: {path}")
        hashes[item["file"]] = digest
    return hashes


def main() -> None:
    manifest = json.loads((ROOT / "sources/manifest.json").read_text())
    for item in manifest["sources"]:
        path = ROOT / "sources" / item["file"]
        if path.exists():
            continue
        with urlopen(item["url"], timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(
                f"Upstream changed: {item['url']}. Restore the archived snapshot; "
                "do not silently update the study's source vintage."
            )
        path.write_bytes(data)
    print(json.dumps(verify_sources(), indent=2))


if __name__ == "__main__":
    main()
