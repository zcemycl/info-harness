"""Missing diary names are not path escapes."""

from pathlib import Path

import pytest

from tools.diary.resolve_diary_path import resolve_diary_path


def test_unknown_relative_name_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    diary = tmp_path / "data" / "diary"
    diary.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="fdalabels_prostate_cancer_drugs"):
        resolve_diary_path("fdalabels_prostate_cancer_drugs", diary_dir=diary)


def test_parent_path_escapes(tmp_path: Path) -> None:
    diary = tmp_path / "data" / "diary"
    diary.mkdir(parents=True)
    with pytest.raises(ValueError, match="escapes"):
        resolve_diary_path("../secret.txt", diary_dir=diary)
