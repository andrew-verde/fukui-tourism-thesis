#!/usr/bin/env python3
"""Sole filesystem gateway for Arm 2 unseen data.

The gateway has no caller-supplied paths.  It first reads only the revised
2021-01..2025-12 history from ``data/quarantine/arm2/mobile``, runs the
vintage-revision guard, and only then decodes any unseen outcome file.
Nothing outside this module may read from the quarantine root.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
QUARANTINE_ROOT = ROOT / "data" / "quarantine" / "arm2"
MOBILE_DIR = QUARANTINE_ROOT / "mobile"
MOBILE_VINTAGE_MANIFEST = MOBILE_DIR / "vintage_manifest.json"
MOBILE_REPOSITORY = MOBILE_DIR / "repository"
MOBILE_DATA_DIR = MOBILE_REPOSITORY / "data"
FTAS_DIR = QUARANTINE_ROOT / "ftas"
JTA_DIR = QUARANTINE_ROOT / "jta"
PINNED_MERGED_DIR = ROOT / "output" / "hokuriku_merged" / "raw"
PINNED_MOBILE_DIR = (
    ROOT / "output" / "national_stats" / "japan_kanko_stat" / "raw"
)
NATIONAL_CONFIG = ROOT / "config" / "national_data_sources.yaml"
WEIGHTS_CSV = ROOT / "data" / "causal" / "arm2_frozen_scm_weights.csv"
FITS_CSV = ROOT / "data" / "causal" / "arm2_frozen_scm_fits.csv"
METADATA_JSON = ROOT / "data" / "causal" / "arm2_frozen_scm_metadata.json"
EXPECTED_WEIGHTS_SHA256 = (
    "824761cd7412a738764f4fc206bccd57f479283e0ad0eb85db0620c59a9bfaa3"
)
EXPECTED_FITS_SHA256 = (
    "5a6fbbdefd1632abdf514293cd6b97d1fd53452ee319fd455efcab253f950147"
)
EXPECTED_SEEN_MERGED_SHA256 = {
    2023: "298393e0dd050f9540ea8ecb026b179e066a610f45f84d65ab67af61edf7ae45",
    2024: "dc06d1c5479b06b9b1c539937bcce8c77a8d1078790d4bb04677df4c40c64bbd",
    2025: "d59e85f5ed5aca3801362da852f9e371ebe8aba32c2c4db8d377b07d5987729f",
    2026: "2cc19c71e789fda90fb162e5e5552551e784d3bb3bf823f7fadf66f90bec4202",
}

SEEN_START_YM = 202101
SEEN_END_YM = 202512
UNSEEN_START_YM = 202601
EVENT_YM = 202403
MIN_UNSEEN_MONTHS = 6
REVISION_RMS_RELATIVE_LIMIT = 0.02
RMSPE_FIT_MULT = 5.0
GOOD_FIT_RMSPE = 0.15

HIGH_CONFIDENCE_CODES = (
    18201, 18202, 18204, 18205, 18207, 18208, 18210,
    18322, 18404, 18423, 18481, 18483, 18501,
)
P1_CODES = (18210, 18322, 18208, 18201, 18202, 18207)
MOBILE_COLUMNS = (
    "年", "月", "地域区分", "データ区分", "都道府県コード",
    "都道府県名", "地域コード", "地域名称", "人数",
)
MERGED_RESPONSE_DATE_COLUMN = "アンケート回答日"
FTAS_SEEN_END_DATE = pd.Timestamp("2026-06-30")
MOBILE_UPSTREAM_REPO = "https://github.com/code4fukui/japan-kanko-stat"
class RevisionGuardError(RuntimeError):
    """The load must stop before any unseen outcome is decoded."""


@dataclass(frozen=True)
class FrozenScmArtifacts:
    weights: pd.DataFrame
    fits: pd.DataFrame


@dataclass(frozen=True, init=False)
class GuardedArm2Data:
    """Capability object obtainable only after the revision guard passes."""

    revised_seen_mobile: pd.DataFrame
    unseen_mobile: pd.DataFrame
    ftas_raw: pd.DataFrame
    merged_raw: pd.DataFrame
    jta_panel: pd.DataFrame
    guard_report: dict
    frozen_scm: FrozenScmArtifacts

    def __init__(self, **_kwargs) -> None:
        raise TypeError("GuardedArm2Data is created only by the quarantine loader")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_quarantined(path: Path) -> Path:
    root = QUARANTINE_ROOT.resolve()
    resolved = path.resolve()
    if resolved != root and root not in resolved.parents:
        raise PermissionError(f"Arm 2 unseen path is outside quarantine: {path}")
    return resolved


def _read_quarantine_history_csv(path: Path) -> pd.DataFrame:
    """Read only one of the five explicitly seen historical siblings."""
    allowed = {
        MOBILE_DATA_DIR / f"city{year}.csv" for year in range(2021, 2026)
    }
    if path not in allowed:
        raise PermissionError("pre-guard reader accepts only city2021..city2025")
    if path.is_symlink():
        raise PermissionError("pre-guard historical siblings may not be symlinks")
    return pd.read_csv(
        _assert_quarantined(path),
        encoding="utf-8-sig",
    )


def _normalize_mobile(frame: pd.DataFrame, source: str) -> pd.DataFrame:
    if tuple(frame.columns) != MOBILE_COLUMNS:
        raise ValueError(f"{source}: unexpected mobile-panel schema")
    data = frame[
        (frame["地域区分"] == "市区町村")
        & (frame["データ区分"] == "観光来訪者数")
    ].copy()
    for column in ("年", "月", "都道府県コード", "地域コード", "人数"):
        data[column] = pd.to_numeric(data[column], errors="raise")
    numeric = data[
        ["年", "月", "都道府県コード", "地域コード", "人数"]
    ].to_numpy(float)
    if not np.isfinite(numeric).all():
        raise ValueError(f"{source}: mobile numeric fields must be finite")
    data["ym"] = data["年"].astype(int) * 100 + data["月"].astype(int)
    data["地域コード"] = data["地域コード"].astype(int)
    if data.duplicated(["地域コード", "ym"]).any():
        raise ValueError(f"{source}: duplicate municipality-month rows")
    if (data["人数"] <= 0).any():
        raise ValueError(f"{source}: SCM log outcomes must be positive")
    return data.sort_values(["地域コード", "ym"]).reset_index(drop=True)


def _validate_mobile_vintage_manifest(
    manifest: dict,
    actual_names: set[str],
) -> None:
    if manifest.get("schema_version") != 1:
        raise ValueError("mobile vintage manifest schema_version must be 1")
    if manifest.get("upstream_repo") != MOBILE_UPSTREAM_REPO:
        raise ValueError("mobile vintage manifest has wrong upstream repository")
    commit = str(manifest.get("commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("mobile vintage manifest requires a full commit SHA")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("mobile vintage manifest files must be an object")
    expected_history = {f"city{year}.csv" for year in range(2021, 2026)}
    monthly = {
        name for name in files
        if re.fullmatch(r"city20\d{4}\.csv", name)
    }
    if set(files) != expected_history | monthly:
        raise ValueError("mobile vintage manifest contains unexpected filenames")
    if set(files) != actual_names:
        raise ValueError("mobile vintage manifest and directory filenames differ")
    months = sorted(int(name[4:10]) for name in monthly)
    _validate_unseen_months(months)
    for name, entry in files.items():
        if not isinstance(entry, dict) or entry.get("commit") != commit:
            raise ValueError(f"{name}: mixed-vintage commit in mobile manifest")
        if not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", ""))):
            raise ValueError(f"{name}: invalid sha256 in mobile manifest")
        if not re.fullmatch(r"[0-9a-f]{40}", str(entry.get("git_blob", ""))):
            raise ValueError(f"{name}: invalid Git blob ID in mobile manifest")


def _git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(MOBILE_REPOSITORY), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _verify_mobile_repository_identity(manifest: dict) -> None:
    if not (MOBILE_REPOSITORY / ".git").is_dir():
        raise FileNotFoundError("quarantine mobile repository checkout is missing")
    origin = _git_output("remote", "get-url", "origin").removesuffix(".git")
    if origin != MOBILE_UPSTREAM_REPO.removesuffix(".git"):
        raise ValueError("quarantine mobile checkout has wrong origin")
    if _git_output("rev-parse", "HEAD") != manifest["commit"]:
        raise ValueError("quarantine mobile checkout HEAD differs from manifest")
    tree = _git_output(
        "ls-tree", "-r", manifest["commit"], "--", "data"
    ).splitlines()
    tree_blobs = {}
    for line in tree:
        if not line:
            continue
        metadata, path = line.split("\t", 1)
        blob = metadata.split()[2]
        name = Path(path).name
        if name in manifest["files"]:
            tree_blobs[name] = blob
    if set(tree_blobs) != set(manifest["files"]):
        raise ValueError("manifest filenames differ from declared commit tree")
    for name, entry in manifest["files"].items():
        if entry["git_blob"] != tree_blobs[name]:
            raise ValueError(f"{name}: manifest blob differs from commit tree")


def _load_mobile_vintage_manifest() -> dict:
    if not MOBILE_VINTAGE_MANIFEST.is_file():
        raise FileNotFoundError(
            f"missing quarantine provenance manifest: {MOBILE_VINTAGE_MANIFEST}"
        )
    manifest = json.loads(
        _assert_quarantined(MOBILE_VINTAGE_MANIFEST).read_text()
    )
    history_names = {f"city{year}.csv" for year in range(2021, 2026)}
    actual_names = {
        path.name
        for path in MOBILE_DATA_DIR.glob("city*.csv")
        if path.is_file()
        and (
            path.name in history_names
            or (
                re.fullmatch(r"city20\d{4}\.csv", path.name)
                and int(path.stem[4:]) >= UNSEEN_START_YM
            )
        )
    }
    _validate_mobile_vintage_manifest(manifest, actual_names)
    _verify_mobile_repository_identity(manifest)
    return manifest


def _verify_mobile_manifest_digest(
    path: Path,
    manifest: dict,
) -> None:
    expected = manifest["files"][path.name]["sha256"]
    if _sha256(_assert_quarantined(path)) != expected:
        raise AssertionError(f"{path.name}: mobile vintage digest mismatch")
    blob = _git_output("hash-object", str(_assert_quarantined(path)))
    if blob != manifest["files"][path.name]["git_blob"]:
        raise AssertionError(f"{path.name}: working file differs from commit blob")


def _load_quarantine_mobile_history(manifest: dict) -> pd.DataFrame:
    frames = []
    for year in range(2021, 2026):
        path = MOBILE_DATA_DIR / f"city{year}.csv"
        if not path.is_file():
            raise FileNotFoundError(f"missing quarantined revised history: {path}")
        _verify_mobile_manifest_digest(path, manifest)
        frame = _normalize_mobile(
            _read_quarantine_history_csv(path), path.name
        )
        if set(frame["ym"].unique()) != {
            year * 100 + month for month in range(1, 13)
        }:
            raise ValueError(f"{path.name}: expected all 12 months of {year}")
        frames.append(frame)
    history = pd.concat(frames, ignore_index=True)
    if history["ym"].min() != SEEN_START_YM or history["ym"].max() != SEEN_END_YM:
        raise ValueError("revised history boundary must be 2021-01..2025-12")
    return history


def _load_pinned_mobile_history() -> pd.DataFrame:
    config = yaml.safe_load(NATIONAL_CONFIG.read_text())["japan_kanko_stat"]
    expected = {Path(item["path"]).name: item for item in config["files"]}
    frames = []
    for year in range(2021, 2026):
        name = f"city{year}.csv"
        path = PINNED_MOBILE_DIR / name
        if not path.is_file():
            raise FileNotFoundError(
                f"missing pinned seen reference {path}; fetch only commit "
                f"{config['commit']}"
            )
        if _sha256(path) != expected[name]["sha256"]:
            raise AssertionError(f"pinned seen reference checksum mismatch: {name}")
        frames.append(_normalize_mobile(
            pd.read_csv(path, encoding="utf-8-sig"), name
        ))
    return pd.concat(frames, ignore_index=True)


def load_frozen_scm_artifacts() -> FrozenScmArtifacts:
    metadata = json.loads(METADATA_JSON.read_text())
    if metadata["weights_sha256"] != EXPECTED_WEIGHTS_SHA256:
        raise AssertionError("frozen Arm 2 weight metadata moved")
    if metadata["fits_sha256"] != EXPECTED_FITS_SHA256:
        raise AssertionError("frozen Arm 2 fit metadata moved")
    if _sha256(WEIGHTS_CSV) != EXPECTED_WEIGHTS_SHA256:
        raise AssertionError("frozen Arm 2 weight artifact checksum mismatch")
    if _sha256(FITS_CSV) != EXPECTED_FITS_SHA256:
        raise AssertionError("frozen Arm 2 fit artifact checksum mismatch")
    weights = pd.read_csv(WEIGHTS_CSV)
    fits = pd.read_csv(FITS_CSV)
    if set(fits.loc[fits["unit_role"] == "high_confidence", "area_code"]) != set(
        HIGH_CONFIDENCE_CODES
    ):
        raise AssertionError("frozen SCM artifact has wrong 13-unit population")
    high = fits[fits["unit_role"] == "high_confidence"]
    if (high["pre_rmspe"] > GOOD_FIT_RMSPE).any():
        raise AssertionError("frozen high-confidence unit exceeds pre_rmspe <= 0.15")
    return FrozenScmArtifacts(weights=weights, fits=fits)


def frozen_gap_matrix(
    panel: pd.DataFrame,
    frozen: FrozenScmArtifacts,
    unit_role: str,
    unit_codes: tuple[int, ...] | list[int],
    months: list[int],
    guarded_data: GuardedArm2Data | None = None,
) -> pd.DataFrame:
    """Apply loaded weights; this function cannot fit or alter weights."""
    if any(month >= UNSEEN_START_YM for month in months):
        assert_guarded_arm2_data(guarded_data)
        guarded_months = sorted(
            guarded_data.unseen_mobile["ym"].astype(int).unique().tolist()
        )
        if (
            panel is not guarded_data.unseen_mobile
            or frozen is not guarded_data.frozen_scm
            or months != guarded_months
        ):
            raise ValueError(
                "post-2025 gaps are bound to the exact guarded panel, "
                "frozen artifacts, and complete month sequence"
            )
    wide = panel.pivot(index="地域コード", columns="ym", values="人数")
    missing_months = set(months) - set(wide.columns)
    if missing_months:
        raise ValueError(f"mobile panel lacks months: {sorted(missing_months)}")
    rows = []
    role_weights = frozen.weights[frozen.weights["unit_role"] == unit_role]
    for code in unit_codes:
        weights = role_weights[role_weights["area_code"] == code]
        if weights.empty:
            raise ValueError(f"no frozen {unit_role} weights for {code}")
        donor_codes = weights["donor_code"].astype(int).to_numpy()
        if code not in wide.index or not set(donor_codes).issubset(wide.index):
            raise ValueError(f"incomplete outcome coverage for frozen unit {code}")
        actual_values = wide.loc[code, months].to_numpy(float)
        donor_values = wide.loc[donor_codes, months].to_numpy(float)
        weight_values = weights["weight"].to_numpy(float)
        if (
            not np.isfinite(actual_values).all()
            or not np.isfinite(donor_values).all()
            or not np.isfinite(weight_values).all()
            or (actual_values <= 0).any()
            or (donor_values <= 0).any()
        ):
            raise ValueError(f"non-finite, missing, or non-positive input for {code}")
        if not np.isclose(weight_values.sum(), 1.0, rtol=0, atol=1e-12):
            raise ValueError(f"frozen weights do not sum to one for {code}")
        actual = np.log(actual_values)
        synthetic = weight_values @ np.log(donor_values)
        rows.extend({
            "area_code": int(code),
            "ym": int(month),
            "gap_log": float(gap),
        } for month, gap in zip(months, actual - synthetic))
    return pd.DataFrame(rows)


def _run_revision_guard(
    revised: pd.DataFrame,
    pinned: pd.DataFrame,
    frozen: FrozenScmArtifacts,
) -> dict:
    months = list(range(202101, 202113))
    months += list(range(202201, 202213))
    months += list(range(202301, 202313))
    months += list(range(202401, 202413))
    months += list(range(202501, 202513))
    revised_wide = revised.pivot(index="地域コード", columns="ym", values="人数")
    pinned_wide = pinned.pivot(index="地域コード", columns="ym", values="人数")

    revisions = {}
    for code in HIGH_CONFIDENCE_CODES:
        if code not in revised_wide.index or code not in pinned_wide.index:
            raise RevisionGuardError(f"confirmatory municipality missing: {code}")
        new = revised_wide.loc[code, months].to_numpy(float)
        old = pinned_wide.loc[code, months].to_numpy(float)
        if (
            not np.isfinite(new).all()
            or not np.isfinite(old).all()
            or (old <= 0).any()
        ):
            raise RevisionGuardError(
                f"{code}: non-finite or non-positive revision input"
            )
        rms_relative = float(np.sqrt(np.mean(((new - old) / old) ** 2)))
        if not np.isfinite(rms_relative):
            raise RevisionGuardError(f"{code}: non-finite RMS relative revision")
        revisions[str(code)] = rms_relative
        if rms_relative > REVISION_RMS_RELATIVE_LIMIT:
            raise RevisionGuardError(
                f"{code}: RMS relative revision {rms_relative:.6f} exceeds 0.02"
            )

    pre_months = [month for month in months if month < EVENT_YM]
    p1_gaps = frozen_gap_matrix(
        revised, frozen, "high_confidence", list(P1_CODES), pre_months
    )
    target_rmspe = (
        p1_gaps.groupby("area_code")["gap_log"]
        .apply(lambda values: float(np.sqrt(np.mean(values.to_numpy() ** 2))))
    )
    max_limit = RMSPE_FIT_MULT * float(target_rmspe.max())
    min_limit = RMSPE_FIT_MULT * float(target_rmspe.min())

    placebo_fits = frozen.fits[frozen.fits["unit_role"] == "placebo"]
    retained_max = tuple(
        placebo_fits.loc[placebo_fits["retained_max_gate"], "area_code"].astype(int)
    )
    retained_min = tuple(
        placebo_fits.loc[placebo_fits["retained_min_gate"], "area_code"].astype(int)
    )
    retained_union = tuple(sorted(set(retained_max) | set(retained_min)))
    placebo_gaps = frozen_gap_matrix(
        revised, frozen, "placebo", list(retained_union), pre_months
    )
    revised_rmspe = (
        placebo_gaps.groupby("area_code")["gap_log"]
        .apply(lambda values: float(np.sqrt(np.mean(values.to_numpy() ** 2))))
    )
    exited_max = [code for code in retained_max if revised_rmspe[code] > max_limit]
    exited_min = [code for code in retained_min if revised_rmspe[code] > min_limit]
    if exited_max or exited_min:
        raise RevisionGuardError(
            "retained donor exited frozen fit gate; stop for deviation ADR "
            f"(max={exited_max[:5]}, min={exited_min[:5]})"
        )
    return {
        "status": "passed",
        "checked_before_unseen_read": True,
        "confirmatory_codes": list(HIGH_CONFIDENCE_CODES),
        "rms_relative_limit": REVISION_RMS_RELATIVE_LIMIT,
        "rms_relative_revisions": revisions,
        "retained_max_gate_count": len(retained_max),
        "retained_min_gate_count": len(retained_min),
    }


def _month_sequence(start: int, end: int) -> list[int]:
    months = []
    year, month = divmod(start, 100)
    while year * 100 + month <= end:
        months.append(year * 100 + month)
        month += 1
        if month == 13:
            year += 1
            month = 1
    return months


def _validate_unseen_months(months: list[int]) -> None:
    if (
        len(months) < MIN_UNSEEN_MONTHS
        or months[0] != UNSEEN_START_YM
        or months != _month_sequence(UNSEEN_START_YM, months[-1])
    ):
        raise ValueError(
            "unseen mobile window must be contiguous from 2026-01 "
            "and contain at least six months"
        )


def _validate_2026_merged_extension(
    reference: pd.DataFrame,
    extended: pd.DataFrame,
) -> pd.DataFrame:
    if list(extended.columns) != list(reference.columns):
        raise ValueError("2026 merged wave schema differs from seen vintage")
    if MERGED_RESPONSE_DATE_COLUMN not in extended.columns:
        raise ValueError("2026 merged source lacks response date")

    # The committed file is the sole seen-population authority. Upstream
    # revises its rebuilt history, so use the current file only to select rows
    # strictly beyond the frozen date boundary (ADR 0038).
    response_dates = pd.to_datetime(
        extended[MERGED_RESPONSE_DATE_COLUMN], errors="coerce"
    )
    if response_dates.isna().any():
        raise ValueError("2026 merged source contains an invalid response date")
    unseen_suffix = extended.loc[
        response_dates > FTAS_SEEN_END_DATE
    ].copy()
    if unseen_suffix.empty:
        raise ValueError("2026 merged wave has no rows after 2026-06")
    suffix_hashes = pd.util.hash_pandas_object(unseen_suffix, index=False)
    if suffix_hashes.duplicated().any():
        raise ValueError("2026 merged post-boundary rows contain duplicates")
    return pd.concat([reference, unseen_suffix], ignore_index=True)


def _build_guarded_loader():
    """Close over every post-guard decoder."""

    def load() -> GuardedArm2Data:
        manifest = _load_mobile_vintage_manifest()
        revised_seen = _load_quarantine_mobile_history(manifest)
        pinned_seen = _load_pinned_mobile_history()
        frozen = load_frozen_scm_artifacts()
        guard_report = _run_revision_guard(revised_seen, pinned_seen, frozen)

        # All code below is closed inside the passing-guard path. There is no
        # importable post-guard decoder or alternate filesystem path.
        paths = [
            MOBILE_DATA_DIR / name
            for name in sorted(manifest["files"])
            if re.fullmatch(r"city20\d{4}\.csv", name)
        ]
        frames = []
        for path in paths:
            filename_ym = int(path.stem.removeprefix("city"))
            if filename_ym < UNSEEN_START_YM:
                raise ValueError(
                    f"unexpected monthly file before unseen boundary: {path.name}"
                )
            _verify_mobile_manifest_digest(path, manifest)
            frame = _normalize_mobile(
                pd.read_csv(_assert_quarantined(path), encoding="utf-8-sig"),
                path.name,
            )
            if set(frame["ym"].unique()) != {filename_ym}:
                raise ValueError(f"{path.name}: rows do not match filename month")
            frames.append(frame)
        if not frames:
            raise FileNotFoundError("no quarantined unseen mobile files")
        unseen_mobile = pd.concat(frames, ignore_index=True)
        months = sorted(unseen_mobile["ym"].astype(int).unique().tolist())
        _validate_unseen_months(months)

        ftas_path = FTAS_DIR / "ftas_survey_all.csv"
        required_merged = [
            FTAS_DIR / f"merged_survey_{year}.csv"
            for year in range(2023, 2027)
        ]
        merged_paths = sorted(FTAS_DIR.glob("merged_survey_*.csv"))
        jta_path = JTA_DIR / "jta_accommodation_panel.csv"
        if (
            not ftas_path.is_file()
            or not all(path.is_file() for path in required_merged)
            or not jta_path.is_file()
        ):
            raise FileNotFoundError(
                "quarantine requires FTAS full survey, full merged 2023-2026 "
                "survey waves, and normalized JTA accommodation panel"
            )
        ftas = pd.read_csv(
            _assert_quarantined(ftas_path), dtype=str, low_memory=False
        )
        merged_frames = []
        for path in merged_paths:
            year = int(path.stem.rsplit("_", 1)[-1])
            if year not in EXPECTED_SEEN_MERGED_SHA256:
                raise ValueError(f"unexpected merged-survey year: {year}")
            reference_path = PINNED_MERGED_DIR / path.name
            if (
                not reference_path.is_file()
                or _sha256(reference_path) != EXPECTED_SEEN_MERGED_SHA256[year]
            ):
                raise AssertionError(f"pinned seen merged reference moved: {year}")
            reference = pd.read_csv(reference_path, low_memory=False)
            extended = pd.read_csv(_assert_quarantined(path), low_memory=False)
            if year < 2026:
                if _sha256(path) != EXPECTED_SEEN_MERGED_SHA256[year]:
                    raise AssertionError(f"seen merged wave changed: {year}")
            else:
                extended = _validate_2026_merged_extension(
                    reference, extended
                )
            merged_frames.append(extended)
        merged = pd.concat(merged_frames, ignore_index=True)
        jta = pd.read_csv(_assert_quarantined(jta_path))

        data = object.__new__(GuardedArm2Data)
        values = {
            "revised_seen_mobile": revised_seen,
            "unseen_mobile": unseen_mobile,
            "ftas_raw": ftas,
            "merged_raw": merged,
            "jta_panel": jta,
            "guard_report": guard_report,
            "frozen_scm": frozen,
        }
        guard_report["mobile_vintage_commit"] = manifest["commit"]
        for name, value in values.items():
            object.__setattr__(data, name, value)
        return data

    return load


load_guarded_arm2_data = _build_guarded_loader()


def assert_guarded_arm2_data(data: object) -> None:
    """Mechanically rerun the revision guard before any post-2025 gap."""
    if not isinstance(data, GuardedArm2Data):
        raise TypeError("post-2025 computation requires GuardedArm2Data")
    required = (
        "revised_seen_mobile",
        "unseen_mobile",
        "guard_report",
        "frozen_scm",
    )
    if any(not hasattr(data, name) for name in required):
        raise TypeError("incomplete GuardedArm2Data capability")
    if (
        not isinstance(data.unseen_mobile, pd.DataFrame)
        or "ym" not in data.unseen_mobile.columns
    ):
        raise TypeError("incomplete GuardedArm2Data unseen panel")
    months = sorted(
        data.unseen_mobile["ym"].astype(int).unique().tolist()
    )
    _validate_unseen_months(months)
    pinned = _load_pinned_mobile_history()
    frozen = load_frozen_scm_artifacts()
    rerun = _run_revision_guard(data.revised_seen_mobile, pinned, frozen)
    if rerun.get("status") != "passed" or data.guard_report.get("status") != "passed":
        raise RevisionGuardError("revision guard revalidation is not passing")
    if data.frozen_scm is not frozen:
        # Artifact identity need not match, but content must be the same frozen
        # checksummed frames loaded above.
        pd.testing.assert_frame_equal(data.frozen_scm.weights, frozen.weights)
        pd.testing.assert_frame_equal(data.frozen_scm.fits, frozen.fits)

    manifest = _load_mobile_vintage_manifest()
    if data.guard_report.get("mobile_vintage_commit") != manifest["commit"]:
        raise RevisionGuardError("guarded mobile commit differs from checkout")
    bound_seen = _load_quarantine_mobile_history(manifest)
    pd.testing.assert_frame_equal(
        data.revised_seen_mobile.reset_index(drop=True),
        bound_seen.reset_index(drop=True),
        check_dtype=False,
        obj="guarded revised-history binding",
    )
    bound_frames = []
    for name in sorted(manifest["files"]):
        if not re.fullmatch(r"city20\d{4}\.csv", name):
            continue
        path = MOBILE_DATA_DIR / name
        _verify_mobile_manifest_digest(path, manifest)
        bound_frames.append(_normalize_mobile(
            pd.read_csv(_assert_quarantined(path), encoding="utf-8-sig"),
            name,
        ))
    bound_unseen = pd.concat(bound_frames, ignore_index=True)
    bound_months = sorted(bound_unseen["ym"].astype(int).unique().tolist())
    _validate_unseen_months(bound_months)
    pd.testing.assert_frame_equal(
        data.unseen_mobile.reset_index(drop=True),
        bound_unseen.reset_index(drop=True),
        check_dtype=False,
        obj="guarded unseen-panel binding",
    )
