"""Perform the removal of custom-formatted tables from Markdown files."""

from collections.abc import Sequence

__all__: Sequence[str] = (
    "remove_custom_formatted_tables_from_all_files",
    "remove_custom_formatted_tables_from_file",
)


import re
import shutil
from collections.abc import MutableSequence
from pathlib import Path
from typing import Final, TextIO

from git import PathLike, Repo

from rcft_pymarkdown import utils


def remove_custom_formatted_tables_from_file(original_file_path: Path) -> None:  # noqa: PLR0915
    """Remove custom-formatted tables from given path to a Markdown file."""
    table_lines: MutableSequence[int] = []
    custom_formatted_table_lines: MutableSequence[int] = []

    original_file: TextIO
    with original_file_path.open("r") as original_file:
        line_number: int
        line: str
        for line_number, line in enumerate(original_file, 1):
            if re.match(r"\|(?:( .+)|-+)\|", line):
                table_lines.append(line_number)

                if re.match(r"\| .+<br/>\* .", line):
                    custom_formatted_table_lines.append(line_number)

    if custom_formatted_table_lines and not table_lines:
        INCONSISTENT_TABLE_LINES_MESSAGE: Final[str] = (
            "Found custom-formatted table lines without any normal table lines."
        )
        raise RuntimeError(INCONSISTENT_TABLE_LINES_MESSAGE)

    if not table_lines:
        return

    temp_file_path: Path = shutil.copy2(
        original_file_path,
        original_file_path.parent / f"{original_file_path.name}.original",
    )
    new_file_path = original_file_path
    original_file_path = temp_file_path
    del temp_file_path

    new_file: TextIO
    with original_file_path.open("r") as original_file, new_file_path.open("w") as new_file:
        def write_table_if_not_custom_formatted(write_table_line_number: int, *, is_newline: bool = False) -> None:  # noqa: E501
            write_table_lines: MutableSequence[str] = []
            while write_table_line_number in table_lines or is_newline:
                is_newline = False

                if write_table_line_number in custom_formatted_table_lines:
                    return

                write_table_lines.append(original_file.readline())
                write_table_line_number += 1

            write_table_line: str
            for write_table_line in write_table_lines:
                new_file.write(write_table_line)

        line_number = 1
        at_end_of_original_file: bool = False
        while not at_end_of_original_file:
            current_position: int = original_file.tell()
            line = original_file.readline()
            at_end_of_original_file = not line

            if line:
                if line_number not in table_lines and line != "\n":
                    new_file.write(line)
                elif line == "\n":
                    if line_number + 1 not in table_lines:
                        new_file.write(line)
                    else:
                        original_file.seek(current_position)
                        _ = original_file.readline()
                        original_file.seek(current_position)
                        write_table_if_not_custom_formatted(line_number, is_newline=True)
                else:
                    original_file.seek(current_position)
                    _ = original_file.readline()
                    original_file.seek(current_position)
                    write_table_if_not_custom_formatted(line_number, is_newline=False)

            line_number += 1


def remove_custom_formatted_tables_from_all_files() -> None:
    """Remove all custom-formatted tables within every Markdown file in this repository."""
    file_entry: tuple[str | PathLike, object]
    for file_entry in Repo(utils.PROJECT_ROOT).index.entries:
        file_path: Path = utils.PROJECT_ROOT / file_entry[0]

        if file_path.suffix != ".md":
            continue

        if not file_path.is_file() or not file_path.exists():
            continue

        original_file_path: Path = file_path.parent / f"{file_path.name}.original"
        if original_file_path.exists():
            ORIGINAL_FILE_ALREADY_EXISTS_MESSAGE: str = (
                "Cannot remove custom-formatted tables from Markdown files: "
                f"{original_file_path} already exists."
            )
            raise FileExistsError(ORIGINAL_FILE_ALREADY_EXISTS_MESSAGE)

        remove_custom_formatted_tables_from_file(file_path)
