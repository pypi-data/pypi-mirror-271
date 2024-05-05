"""Perform the restoration of Markdown files that had custom-formatted tables removed."""

from collections.abc import Sequence

__all__: Sequence[str] = ("restore_custom_formatted_tables_from_all_files",)


from typing import TYPE_CHECKING

from rcft_pymarkdown import utils

if TYPE_CHECKING:
    from pathlib import Path


def restore_custom_formatted_tables_from_all_files() -> None:
    """Return all Markdown files to their original state before linting."""
    file_path: Path
    for file_path in utils.PROJECT_ROOT.rglob("*.md.original"):
        FILE_IS_TEMPORARY_ORIGINAL: bool = (
            len(file_path.suffixes) == 2
            and file_path.suffixes[0] == ".md"
            and file_path.suffixes[1] == ".original"
        )
        if not FILE_IS_TEMPORARY_ORIGINAL:
            continue

        if not file_path.is_file() or not file_path.exists():
            continue

        correct_original_file_path: Path = file_path.parent / file_path.stem
        if correct_original_file_path.exists():
            correct_original_file_path.unlink()

        file_path.rename(file_path.parent / file_path.stem)
