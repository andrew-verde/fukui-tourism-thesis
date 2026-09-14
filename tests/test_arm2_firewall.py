"""Executable Arm 2 quarantine and guard-first sentinels."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
GATEWAY_PATH = ROOT / "scripts" / "arm2_quarantine.py"
PREDICTIONS_PATH = ROOT / "scripts" / "arm2_predictions.py"


def _gateway():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location(
        "arm2_quarantine_firewall_test", GATEWAY_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_loader_refuses_every_path_outside_quarantine(tmp_path) -> None:
    gateway = _gateway()
    with pytest.raises(PermissionError, match="outside quarantine"):
        gateway._assert_quarantined(tmp_path / "city202601.csv")


def test_guard_failure_never_decodes_poisoned_unseen_file(
    tmp_path, monkeypatch
) -> None:
    """Poison-value sentinel: a failed guard must leave it undecoded."""
    gateway = _gateway()
    quarantine = tmp_path / "arm2"
    mobile = quarantine / "mobile"
    mobile.mkdir(parents=True)
    poison = mobile / "city202601.csv"
    poison.write_text("UNSEEN_OUTCOME_SENTINEL_MUST_NOT_BE_DECODED")

    monkeypatch.setattr(gateway, "QUARANTINE_ROOT", quarantine)
    monkeypatch.setattr(gateway, "MOBILE_DIR", mobile)
    decoded_paths = []

    def forbidden_read(path, **_kwargs):
        decoded_paths.append(Path(path))
        raise AssertionError("a post-guard decoder ran before guard passage")

    monkeypatch.setattr(gateway.pd, "read_csv", forbidden_read)
    monkeypatch.setattr(
        gateway, "_load_mobile_vintage_manifest", lambda: {
            "commit": "a" * 40,
            "files": {},
        }
    )
    monkeypatch.setattr(
        gateway, "_load_quarantine_mobile_history", lambda _manifest: pd.DataFrame()
    )
    monkeypatch.setattr(
        gateway, "_load_pinned_mobile_history", lambda: pd.DataFrame()
    )
    monkeypatch.setattr(
        gateway, "load_frozen_scm_artifacts", lambda: object()
    )

    def fail_guard(*_args):
        raise gateway.RevisionGuardError("sentinel guard failure")

    monkeypatch.setattr(gateway, "_run_revision_guard", fail_guard)
    with pytest.raises(gateway.RevisionGuardError, match="sentinel"):
        gateway.load_guarded_arm2_data()
    assert decoded_paths == []


def test_guarded_capability_cannot_be_constructed_or_bypassed() -> None:
    gateway = _gateway()
    with pytest.raises(TypeError, match="quarantine loader"):
        gateway.GuardedArm2Data()
    assert not hasattr(gateway, "_SEAL")
    assert not hasattr(gateway, "is_guarded_arm2_data")
    assert not hasattr(gateway, "_read_quarantine_csv")
    assert not hasattr(gateway, "_load_mobile_unseen")
    assert not hasattr(gateway, "_load_secondary_inputs")

    forged = object.__new__(gateway.GuardedArm2Data)
    object.__setattr__(forged, "guard_report", {"status": "passed"})
    object.__setattr__(forged, "unseen_mobile", pd.DataFrame())
    object.__setattr__(forged, "frozen_scm", object())
    with pytest.raises(TypeError, match="incomplete"):
        gateway.assert_guarded_arm2_data(forged)

    predictions_spec = importlib.util.spec_from_file_location(
        "arm2_predictions_firewall_test", PREDICTIONS_PATH
    )
    assert predictions_spec and predictions_spec.loader
    predictions = importlib.util.module_from_spec(predictions_spec)
    sys.modules[predictions_spec.name] = predictions
    predictions_spec.loader.exec_module(predictions)
    with pytest.raises(TypeError, match="GuardedArm2Data"):
        predictions.analyze_guarded(pd.DataFrame())
    with pytest.raises(TypeError, match="GuardedArm2Data"):
        predictions.compute_guarded_primaries(pd.DataFrame())
    with pytest.raises(TypeError, match="GuardedArm2Data"):
        predictions._compute_primary_metrics(pd.DataFrame())
    with pytest.raises(TypeError, match="GuardedArm2Data"):
        predictions.compute_guarded_primaries(forged)


def test_no_other_script_has_a_quarantine_filesystem_path() -> None:
    offenders = []
    for path in (ROOT / "scripts").glob("*.py"):
        if path == GATEWAY_PATH:
            continue
        source = path.read_text()
        if "data/quarantine/arm2" in source or "QUARANTINE_ROOT" in source:
            offenders.append(path.name)
    assert offenders == []


def test_guard_call_is_textually_before_closed_unseen_decoders() -> None:
    source = GATEWAY_PATH.read_text()
    loader = source[source.index("def _build_guarded_loader"):]
    guard_position = loader.index("_run_revision_guard(")
    assert guard_position < loader.index(
        "pd.read_csv(_assert_quarantined(path)"
    )


def test_unseen_window_must_start_202601_and_be_contiguous() -> None:
    gateway = _gateway()
    gateway._validate_unseen_months(
        [202601, 202602, 202603, 202604, 202605, 202606]
    )
    with pytest.raises(ValueError, match="contiguous from 2026-01"):
        gateway._validate_unseen_months(
            [202602, 202603, 202604, 202605, 202606, 202607]
        )
    with pytest.raises(ValueError, match="contiguous from 2026-01"):
        gateway._validate_unseen_months(
            [202601, 202602, 202604, 202605, 202606, 202607]
        )


def test_mobile_manifest_rejects_mixed_vintages() -> None:
    gateway = _gateway()
    names = {
        *(f"city{year}.csv" for year in range(2021, 2026)),
        *(f"city20260{month}.csv" for month in range(1, 7)),
    }
    commit = "a" * 40
    manifest = {
        "schema_version": 1,
        "upstream_repo": gateway.MOBILE_UPSTREAM_REPO,
        "commit": commit,
        "files": {
            name: {
                "commit": commit,
                "sha256": "b" * 64,
                "git_blob": "d" * 40,
            }
            for name in names
        },
    }
    gateway._validate_mobile_vintage_manifest(manifest, names)
    manifest["files"]["city2025.csv"]["commit"] = "c" * 40
    with pytest.raises(ValueError, match="mixed-vintage"):
        gateway._validate_mobile_vintage_manifest(manifest, names)


def test_manifest_blob_ids_must_match_declared_git_tree(
    tmp_path, monkeypatch
) -> None:
    gateway = _gateway()
    repository = tmp_path / "repository"
    (repository / ".git").mkdir(parents=True)
    monkeypatch.setattr(gateway, "MOBILE_REPOSITORY", repository)
    names = {
        *(f"city{year}.csv" for year in range(2021, 2026)),
        *(f"city20260{month}.csv" for month in range(1, 7)),
    }
    commit = "a" * 40
    manifest = {
        "commit": commit,
        "files": {
            name: {"git_blob": "b" * 40} for name in names
        },
    }

    def fake_git(*args):
        if args[:3] == ("remote", "get-url", "origin"):
            return gateway.MOBILE_UPSTREAM_REPO
        if args[:2] == ("rev-parse", "HEAD"):
            return commit
        if args[0] == "ls-tree":
            return "\n".join(
                f"100644 blob {'c' * 40}\tdata/{name}"
                for name in sorted(names)
            )
        raise AssertionError(args)

    monkeypatch.setattr(gateway, "_git_output", fake_git)
    with pytest.raises(ValueError, match="blob differs"):
        gateway._verify_mobile_repository_identity(manifest)


def test_gap_application_rejects_missing_outcomes() -> None:
    gateway = _gateway()
    panel = pd.DataFrame({
        "地域コード": [1, 1, 2, 2],
        "ym": [202501, 202502, 202501, 202502],
        "人数": [10.0, float("nan"), 8.0, 9.0],
    })
    weights = pd.DataFrame({
        "unit_role": ["high_confidence"],
        "area_code": [1],
        "donor_code": [2],
        "weight": [1.0],
    })
    frozen = gateway.FrozenScmArtifacts(weights=weights, fits=pd.DataFrame())
    with pytest.raises(ValueError, match="non-finite"):
        gateway.frozen_gap_matrix(
            panel, frozen, "high_confidence", [1], [202501, 202502]
        )


def test_post_2025_gap_is_bound_to_exact_guarded_inputs(
    monkeypatch,
) -> None:
    gateway = _gateway()
    months = [202601, 202602, 202603, 202604, 202605, 202606]
    panel = pd.DataFrame({
        "地域コード": [1] * 6 + [2] * 6,
        "ym": months * 2,
        "人数": [10.0] * 6 + [9.0] * 6,
    })
    weights = pd.DataFrame({
        "unit_role": ["high_confidence"],
        "area_code": [1],
        "donor_code": [2],
        "weight": [1.0],
    })
    frozen = gateway.FrozenScmArtifacts(weights=weights, fits=pd.DataFrame())
    guarded = object.__new__(gateway.GuardedArm2Data)
    object.__setattr__(guarded, "unseen_mobile", panel)
    object.__setattr__(guarded, "frozen_scm", frozen)
    monkeypatch.setattr(gateway, "assert_guarded_arm2_data", lambda _data: None)
    with pytest.raises(ValueError, match="bound to the exact guarded panel"):
        gateway.frozen_gap_matrix(
            panel.copy(),
            frozen,
            "high_confidence",
            [1],
            months,
            guarded_data=guarded,
        )


def test_guard_revalidation_rejects_in_memory_unseen_mutation(
    monkeypatch,
) -> None:
    gateway = _gateway()
    months = [202601, 202602, 202603, 202604, 202605, 202606]
    bound = pd.DataFrame({
        "地域コード": [1] * 6,
        "ym": months,
        "人数": [10.0] * 6,
    })
    mutated = bound.copy()
    mutated.loc[0, "人数"] = 999.0
    frozen = gateway.FrozenScmArtifacts(
        weights=pd.DataFrame(), fits=pd.DataFrame()
    )
    data = object.__new__(gateway.GuardedArm2Data)
    for name, value in {
        "revised_seen_mobile": pd.DataFrame(),
        "unseen_mobile": mutated,
        "guard_report": {
            "status": "passed",
            "mobile_vintage_commit": "a" * 40,
        },
        "frozen_scm": frozen,
    }.items():
        object.__setattr__(data, name, value)

    manifest = {
        "commit": "a" * 40,
        "files": {
            f"city20260{month}": {} for month in range(1, 7)
        },
    }
    manifest["files"] = {
        f"{name}.csv": entry for name, entry in manifest["files"].items()
    }
    monkeypatch.setattr(
        gateway, "_load_pinned_mobile_history", lambda: pd.DataFrame()
    )
    monkeypatch.setattr(
        gateway, "load_frozen_scm_artifacts", lambda: frozen
    )
    monkeypatch.setattr(
        gateway, "_run_revision_guard", lambda *_args: {"status": "passed"}
    )
    monkeypatch.setattr(
        gateway, "_load_mobile_vintage_manifest", lambda: manifest
    )
    monkeypatch.setattr(
        gateway,
        "_load_quarantine_mobile_history",
        lambda _manifest: pd.DataFrame(),
    )
    monkeypatch.setattr(
        gateway, "_verify_mobile_manifest_digest", lambda *_args: None
    )
    monkeypatch.setattr(
        gateway, "_assert_quarantined", lambda path: path
    )
    monkeypatch.setattr(gateway.pd, "read_csv", lambda *_args, **_kwargs: pd.DataFrame())

    def fake_normalize(_frame, source):
        month = int(Path(source).stem[-6:])
        return bound[bound["ym"] == month].copy()

    monkeypatch.setattr(gateway, "_normalize_mobile", fake_normalize)
    with pytest.raises(AssertionError, match="guarded unseen-panel binding"):
        gateway.assert_guarded_arm2_data(data)


def test_post_event_nan_cannot_pass_revision_guard() -> None:
    gateway = _gateway()
    pinned = gateway._load_pinned_mobile_history()
    revised = pinned.copy()
    revised.loc[
        (revised["地域コード"] == 18201) & (revised["ym"] == 202512),
        "人数",
    ] = float("nan")
    with pytest.raises(gateway.RevisionGuardError, match="non-finite"):
        gateway._run_revision_guard(
            revised,
            pinned,
            gateway.load_frozen_scm_artifacts(),
        )


def test_s1_suffix_must_be_new_nondeduplicated_rows() -> None:
    gateway = _gateway()
    column = gateway.MERGED_RESPONSE_DATE_COLUMN
    reference = pd.DataFrame({
        column: ["2026-06-01", "2026-06-29"],
        "value": [1, 2],
    })
    valid = pd.concat([
        reference,
        pd.DataFrame({column: ["2026-07-01"], "value": [3]}),
    ], ignore_index=True)
    checked = gateway._validate_2026_merged_extension(reference, valid)
    assert checked.equals(valid)

    reordered = pd.concat([
        pd.DataFrame({column: ["2026-07-02"], "value": [4]}),
        reference.iloc[::-1],
        pd.DataFrame({column: ["2026-07-01"], "value": [3]}),
    ], ignore_index=True)
    checked = gateway._validate_2026_merged_extension(reference, reordered)
    assert checked[column].tolist() == [
        "2026-06-01",
        "2026-06-29",
        "2026-07-02",
        "2026-07-01",
    ]

    revised_history = pd.concat([
        reference.assign(value=[1, 99]),
        pd.DataFrame({column: ["2026-07-01"], "value": [3]}),
    ], ignore_index=True)
    checked = gateway._validate_2026_merged_extension(reference, revised_history)
    assert checked.equals(valid)

    backfilled = pd.concat([
        reference,
        pd.DataFrame({
            column: ["2026-06-28", "2026-07-01"],
            "value": [30, 3],
        }),
    ], ignore_index=True)
    checked = gateway._validate_2026_merged_extension(reference, backfilled)
    assert checked.equals(valid)

    seam = pd.concat([
        reference,
        pd.DataFrame({
            column: ["2026-06-30", "2026-07-01"],
            "value": [30, 3],
        }),
    ], ignore_index=True)
    checked = gateway._validate_2026_merged_extension(reference, seam)
    assert checked[column].tolist() == [
        "2026-06-01",
        "2026-06-29",
        "2026-07-01",
    ]

    duplicated_suffix = pd.DataFrame({
        column: ["2026-07-01", "2026-07-01"],
        "value": [3, 3],
    })
    duplicate = pd.concat([reference, duplicated_suffix], ignore_index=True)
    with pytest.raises(ValueError, match="duplicates"):
        gateway._validate_2026_merged_extension(reference, duplicate)

    invalid_date = pd.concat([
        reference,
        pd.DataFrame({column: ["not-a-date"], "value": [3]}),
    ], ignore_index=True)
    with pytest.raises(ValueError, match="invalid response date"):
        gateway._validate_2026_merged_extension(reference, invalid_date)
