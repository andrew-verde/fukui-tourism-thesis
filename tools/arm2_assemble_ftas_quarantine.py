#!/usr/bin/env python3
"""Assemble the Arm 2 FTAS quarantine from local operator-supplied files.

This tool performs only byte-level checks. The authoritative row-level
prefix, backfill, and duplicate validation for ``merged_survey_2026.csv``
remains ``scripts/arm2_quarantine.py``'s
``_validate_2026_merged_extension()``, which runs later inside the frozen
gateway. The 2026 byte-prefix check here is only a cheap early abort.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import arm2_quarantine

OFFICIAL_SOURCES = arm2_quarantine.ROOT / "config" / "official_fukui_sources.yaml"


class ToolError(RuntimeError):
    """Raised when the FTAS quarantine cannot be assembled safely."""


def _git_output(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _byte_length(path: Path) -> int:
    return path.stat().st_size


def _load_ftas_source_config() -> dict[str, str]:
    config = yaml.safe_load(OFFICIAL_SOURCES.read_text(encoding="utf-8"))
    try:
        source = config["sources"]["ftas_survey_all"]
    except KeyError as exc:
        raise ToolError("missing ftas_survey_all source configuration") from exc
    required = {"upstream_repo", "source_path", "filename"}
    missing = sorted(required - set(source))
    if missing:
        raise ToolError(
            "ftas_survey_all source configuration is incomplete: "
            + ", ".join(missing)
        )
    return {
        "upstream_repo": str(source["upstream_repo"]),
        "source_path": str(source["source_path"]),
        "filename": str(source["filename"]),
    }


def _discover_ftas_source_file(
    source_repository: Path,
    source_config: dict[str, str],
) -> tuple[str, Path]:
    origin = _git_output(source_repository, "remote", "get-url", "origin")
    if origin.removesuffix(".git") != (
        source_config["upstream_repo"].removesuffix(".git")
    ):
        raise ToolError(
            "source checkout origin does not match the protected FTAS upstream"
        )

    dirty = _git_output(
        source_repository, "status", "--porcelain", "--untracked-files=all"
    )
    if dirty:
        raise ToolError("source checkout HEAD is dirty")

    commit = _git_output(source_repository, "rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ToolError("source checkout HEAD must resolve to a full commit SHA")

    source_path = source_repository / source_config["source_path"]
    if not source_path.is_file():
        raise ToolError(f"missing FTAS source file: {source_path}")

    tree_line = _git_output(
        source_repository, "ls-tree", "-r", commit, "--", source_config["source_path"]
    )
    if not tree_line:
        raise ToolError("required FTAS source file does not resolve from HEAD")
    blob = tree_line.split("\t", 1)[0].split()[2]
    working_blob = _git_output(source_repository, "hash-object", str(source_path))
    if working_blob != blob:
        raise ToolError("FTAS source working file differs from the declared HEAD tree")

    return commit, source_path


def _ensure_empty_target() -> None:
    if arm2_quarantine.FTAS_DIR.exists():
        existing = sorted(path.name for path in arm2_quarantine.FTAS_DIR.iterdir())
        if existing:
            joined = ", ".join(existing)
            raise ToolError(
                f"target FTAS quarantine directory must be empty; found: {joined}"
            )
    arm2_quarantine.FTAS_DIR.mkdir(parents=True, exist_ok=True)


def _verify_pinned_merged_wave(year: int) -> Path:
    path = arm2_quarantine.PINNED_MERGED_DIR / f"merged_survey_{year}.csv"
    if not path.is_file():
        raise FileNotFoundError(f"missing pinned seen merged reference: {path}")
    expected = arm2_quarantine.EXPECTED_SEEN_MERGED_SHA256[year]
    actual = _sha256(path)
    if actual != expected:
        raise ToolError(f"pinned seen merged reference checksum mismatch: {year}")
    return path


def _verify_2026_prefix(reference_path: Path, extended_path: Path) -> None:
    """Reject vintage-mixing before the gateway's row-level extension checks."""
    reference_size = _byte_length(reference_path)
    extended_size = _byte_length(extended_path)
    if extended_size <= reference_size:
        raise ToolError("2026 merged extension must be strictly longer than pinned")
    with reference_path.open("rb") as reference, extended_path.open("rb") as extended:
        while True:
            chunk = reference.read(1024 * 1024)
            if not chunk:
                break
            if extended.read(len(chunk)) != chunk:
                raise ToolError(
                    "2026 merged extension rewrites the frozen seen prefix; "
                    "stop for human decision"
                )


def _copy_file(source_path: Path, destination_path: Path) -> dict[str, int | str]:
    shutil.copyfile(source_path, destination_path)
    return {
        "sha256": _sha256(destination_path),
        "byte_length": _byte_length(destination_path),
    }


def _copy_ftas_survey_file(
    source_path: Path,
    destination_name: str,
) -> dict[str, int | str]:
    destination_path = arm2_quarantine.FTAS_DIR / destination_name
    return _copy_file(source_path, destination_path)


def _copy_pinned_merged_waves() -> dict[str, dict[str, int | str]]:
    copied = {}
    for year in range(2023, 2026):
        source_path = _verify_pinned_merged_wave(year)
        destination_path = arm2_quarantine.FTAS_DIR / source_path.name
        copied[source_path.name] = _copy_file(source_path, destination_path)
    return copied


def _copy_extended_2026_wave(
    extended_2026_path: Path,
) -> tuple[str, dict[str, int | str]]:
    if not extended_2026_path.is_file():
        raise FileNotFoundError(
            f"missing operator-supplied 2026 merged wave: {extended_2026_path}"
        )
    reference_path = _verify_pinned_merged_wave(2026)
    _verify_2026_prefix(reference_path, extended_2026_path)
    destination_name = "merged_survey_2026.csv"
    destination_path = arm2_quarantine.FTAS_DIR / destination_name
    metadata = _copy_file(extended_2026_path, destination_path)
    return destination_name, metadata


def _write_manifest(
    ftas_commit: str,
    ftas_filename: str,
    ftas_metadata: dict[str, int | str],
    merged_metadata: dict[str, dict[str, int | str]],
    merged_2026_filename: str,
    merged_2026_metadata: dict[str, int | str],
) -> tuple[str, dict[str, dict[str, int | str] | str]]:
    manifest = {
        "schema_version": 1,
        "ftas_upstream_commit": ftas_commit,
        "files": {
            ftas_filename: {
                "source": "operator-supplied",
                **ftas_metadata,
            },
            **{
                name: {
                    "source": "pinned",
                    **metadata,
                }
                for name, metadata in merged_metadata.items()
            },
            merged_2026_filename: {
                "source": "operator-supplied",
                **merged_2026_metadata,
            },
        },
    }
    manifest_name = "assembly_manifest.json"
    manifest_path = arm2_quarantine.FTAS_DIR / manifest_name
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_name, {
        "source": "tooling-provenance",
        "sha256": _sha256(manifest_path),
        "byte_length": _byte_length(manifest_path),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Populate the Arm 2 FTAS quarantine from an existing FTAS checkout "
            "and an operator-supplied 2026 merged wave file."
        )
    )
    parser.add_argument(
        "ftas_checkout",
        type=Path,
        help="Path to a clean local checkout of the FTAS upstream repository.",
    )
    parser.add_argument(
        "extended_2026_wave",
        type=Path,
        help="Path to the operator-supplied extended merged_survey_2026.csv file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    source_repository = args.ftas_checkout.resolve()
    extended_2026_path = args.extended_2026_wave.resolve()

    try:
        source_config = _load_ftas_source_config()
        ftas_commit, ftas_source_path = _discover_ftas_source_file(
            source_repository, source_config
        )
        _ensure_empty_target()
        ftas_filename = source_config["filename"]
        ftas_metadata = _copy_ftas_survey_file(
            ftas_source_path,
            ftas_filename,
        )
        merged_metadata = _copy_pinned_merged_waves()
        merged_2026_filename, merged_2026_metadata = _copy_extended_2026_wave(
            extended_2026_path
        )
        manifest_name, manifest_metadata = _write_manifest(
            ftas_commit,
            ftas_filename,
            ftas_metadata,
            merged_metadata,
            merged_2026_filename,
            merged_2026_metadata,
        )
    except (
        ToolError,
        FileNotFoundError,
        OSError,
        subprocess.CalledProcessError,
        ValueError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"commit: {ftas_commit}")
    print(f"{ftas_filename} {ftas_metadata['sha256']}")
    for year in range(2023, 2026):
        name = f"merged_survey_{year}.csv"
        print(f"{name} {merged_metadata[name]['sha256']}")
    print(f"{merged_2026_filename} {merged_2026_metadata['sha256']}")
    print(f"{manifest_name} {manifest_metadata['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
