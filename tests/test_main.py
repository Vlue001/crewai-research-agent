from pathlib import Path

import pytest

from main import find_new_reports


@pytest.fixture(autouse=True)
def chdir_to_tmp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _outputs() -> Path:
    return Path("outputs")


def test_returns_new_file():
    _outputs().mkdir()
    before: set[Path] = set(_outputs().glob("*.md"))

    report = _outputs() / "report_20240101_120000_000000.md"
    report.write_text("# Report")

    result = find_new_reports(before)
    assert Path("outputs/report_20240101_120000_000000.md") in result


def test_ignores_preexisting_file():
    _outputs().mkdir()

    old = _outputs() / "old_report.md"
    old.write_text("# Old")
    before = set(_outputs().glob("*.md"))

    new = _outputs() / "new_report.md"
    new.write_text("# New")

    result = find_new_reports(before)
    assert Path("outputs/new_report.md") in result
    assert Path("outputs/old_report.md") not in result


def test_returns_empty_when_no_new_files():
    _outputs().mkdir()

    existing = _outputs() / "existing.md"
    existing.write_text("# Existing")
    before = set(_outputs().glob("*.md"))

    result = find_new_reports(before)
    assert result == []


def test_returns_empty_when_outputs_dir_missing():
    before: set[Path] = set()

    result = find_new_reports(before)
    assert result == []


def test_returns_sorted_list():
    _outputs().mkdir()
    before: set[Path] = set()

    (_outputs() / "b_report.md").write_text("# B")
    (_outputs() / "a_report.md").write_text("# A")

    result = find_new_reports(before)
    assert result == [Path("outputs/a_report.md"), Path("outputs/b_report.md")]
