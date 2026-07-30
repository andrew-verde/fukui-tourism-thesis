from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL_NAMES = (
    "arm2_assemble_quarantine.py",
    "arm2_rehearsal.py",
)


def test_arm2_rehearsal_source_guardrails(tmp_path) -> None:
    copied_sources = {}
    for name in TOOL_NAMES:
        source = (ROOT / "tools" / name).read_text(encoding="utf-8")
        target = tmp_path / name
        target.write_text(source, encoding="utf-8")
        copied_sources[name] = source

    rehearsal = copied_sources["arm2_rehearsal.py"]
    assert "load_guarded_arm2_data" not in rehearsal
    assert "analyze_guarded" not in rehearsal
    assert "compute_guarded_primaries" not in rehearsal
    assert "_run_revision_guard(" in rehearsal

    for source in copied_sources.values():
        assert "data/quarantine/arm2" not in source
        assert "QUARANTINE_ROOT" not in source

    guard_suffix = rehearsal[rehearsal.index("_run_revision_guard("):]
    assert re.search(r"city20\d{4}", guard_suffix) is None
