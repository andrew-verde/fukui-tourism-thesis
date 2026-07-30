#!/usr/bin/env python3
"""Assemble the Arm 2 mobile quarantine from an existing upstream checkout."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import arm2_quarantine


class ToolError(RuntimeError):
    """Raised when the mobile quarantine cannot be assembled safely."""


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


def _expected_history_names() -> list[str]:
    return [f"city{year}.csv" for year in range(2021, 2026)]


def _monthly_name(ym: int) -> str:
    return f"city{ym}.csv"


def _discover_source_inventory(
    source_repository: Path,
) -> tuple[str, list[str], list[int], dict[str, str], dict[str, str]]:
    source_data_dir = source_repository / "data"
    if not source_data_dir.is_dir():
        raise ToolError(f"missing source data directory: {source_data_dir}")

    origin = _git_output(source_repository, "remote", "get-url", "origin")
    if origin.removesuffix(".git") != (
        arm2_quarantine.MOBILE_UPSTREAM_REPO.removesuffix(".git")
    ):
        raise ToolError(
            "source checkout origin does not match the protected upstream"
        )

    dirty = _git_output(
        source_repository, "status", "--porcelain", "--untracked-files=all"
    )
    if dirty:
        raise ToolError("source checkout HEAD is dirty")

    commit = _git_output(source_repository, "rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ToolError("source checkout HEAD must resolve to a full commit SHA")

    history_names = _expected_history_names()
    for name in history_names:
        path = source_data_dir / name
        if not path.is_file():
            raise ToolError(f"missing historical mobile file: {path}")

    monthly_months = sorted(
        int(path.stem.removeprefix("city"))
        for path in source_data_dir.glob("city*.csv")
        if path.is_file()
        and re.fullmatch(r"city20\d{4}\.csv", path.name)
        and int(path.stem.removeprefix("city")) >= arm2_quarantine.UNSEEN_START_YM
    )
    arm2_quarantine._validate_unseen_months(monthly_months)
    monthly_names = [_monthly_name(month) for month in monthly_months]
    file_names = history_names + monthly_names

    tree_lines = _git_output(
        source_repository, "ls-tree", "-r", commit, "--", "data"
    ).splitlines()
    tree_blobs = {}
    for line in tree_lines:
        if not line:
            continue
        metadata, path = line.split("\t", 1)
        name = Path(path).name
        if name in file_names:
            tree_blobs[name] = metadata.split()[2]
    if set(tree_blobs) != set(file_names):
        raise ToolError(
            "required mobile files do not all resolve from one upstream commit"
        )

    digests = {}
    for name in file_names:
        path = source_data_dir / name
        working_blob = _git_output(source_repository, "hash-object", str(path))
        if working_blob != tree_blobs[name]:
            raise ToolError(
                f"{name}: working file differs from the declared HEAD tree"
            )
        digests[name] = _sha256(path)

    return commit, file_names, monthly_months, tree_blobs, digests


def _ensure_empty_target() -> None:
    if arm2_quarantine.MOBILE_DIR.exists():
        existing = sorted(path.name for path in arm2_quarantine.MOBILE_DIR.iterdir())
        if existing:
            joined = ", ".join(existing)
            raise ToolError(
                f"target mobile quarantine directory must be empty; found: {joined}"
            )
    arm2_quarantine.MOBILE_DIR.mkdir(parents=True, exist_ok=True)


def _copy_checkout(source_repository: Path) -> None:
    shutil.copytree(source_repository, arm2_quarantine.MOBILE_REPOSITORY)


def _write_manifest(
    commit: str,
    file_names: list[str],
    tree_blobs: dict[str, str],
    digests: dict[str, str],
) -> dict:
    manifest = {
        "schema_version": 1,
        "upstream_repo": arm2_quarantine.MOBILE_UPSTREAM_REPO,
        "commit": commit,
        "files": {
            name: {
                "commit": commit,
                "git_blob": tree_blobs[name],
                "sha256": digests[name],
            }
            for name in file_names
        },
    }
    arm2_quarantine.MOBILE_VINTAGE_MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def _validate_assembled_manifest(file_names: list[str]) -> dict:
    manifest = arm2_quarantine._load_mobile_vintage_manifest()
    for name in file_names:
        arm2_quarantine._verify_mobile_manifest_digest(
            arm2_quarantine.MOBILE_DATA_DIR / name,
            manifest,
        )
    return manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Populate the Arm 2 mobile quarantine from an already-cloned "
            "upstream checkout."
        )
    )
    parser.add_argument(
        "source_checkout",
        type=Path,
        help="Path to a clean local checkout of the mobile upstream repository.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    source_repository = args.source_checkout.resolve()

    try:
        commit, file_names, monthly_months, tree_blobs, digests = (
            _discover_source_inventory(source_repository)
        )
        _ensure_empty_target()
        _copy_checkout(source_repository)
        _write_manifest(commit, file_names, tree_blobs, digests)
        _validate_assembled_manifest(file_names)
    except (
        ToolError,
        FileNotFoundError,
        OSError,
        subprocess.CalledProcessError,
        ValueError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    history_count = len(_expected_history_names())
    unseen_count = len(monthly_months)
    unseen_names = ", ".join(_monthly_name(month) for month in monthly_months)
    print(f"commit: {commit}")
    print(f"file count: {len(file_names)}")
    print(f"historical files: {history_count}")
    print(f"unseen monthly files: {unseen_count}")
    print(f"unseen months: {unseen_names}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
