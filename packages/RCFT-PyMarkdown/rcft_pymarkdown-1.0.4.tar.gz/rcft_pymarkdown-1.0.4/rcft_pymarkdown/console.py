"""Console entry point for RCFT-PyMarkdown."""

from collections.abc import Sequence

__all__: Sequence[str] = ("run",)


import functools
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from subprocess import CompletedProcess
from typing import TYPE_CHECKING, Final, TypeAlias

from rcft_pymarkdown import (
    remove_custom_formatted_tables,
    restore_custom_formatted_tables,
    utils,
)
from rcft_pymarkdown.context_manager import RemoveCustomFormattedTables

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from argparse import _SubParsersAction

    SubParserGroup: TypeAlias = _SubParsersAction[ArgumentParser]


def _run_remove(arg_parser: ArgumentParser) -> int:
    remove_tables_file_exists_error: FileExistsError
    try:
        remove_custom_formatted_tables.remove_custom_formatted_tables_from_all_files()

    except FileExistsError as remove_tables_file_exists_error:
        MANUAL_REMOVE_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
            bool(remove_tables_file_exists_error.args)
            and "already exists" in remove_tables_file_exists_error.args[0]
        )
        if MANUAL_REMOVE_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
            MANUAL_REMOVE_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                f"{remove_tables_file_exists_error.args[0]} "
                f"Use `{arg_parser.prog} --restore` to first restore the files "
                "to their original state."
            )
            raise type(remove_tables_file_exists_error)(
                MANUAL_REMOVE_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE  # noqa: COM812
            ) from remove_tables_file_exists_error

        raise remove_tables_file_exists_error from remove_tables_file_exists_error

    return 0


def _run_restore() -> int:
    restore_custom_formatted_tables.restore_custom_formatted_tables_from_all_files()
    return 0


def _run_scan_all(arg_parser: ArgumentParser) -> int:
    try:
        with RemoveCustomFormattedTables():
            parser_output: CompletedProcess[bytes] = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pymarkdown",
                    "--return-code-scheme",
                    "minimal",
                    "scan",
                    utils.PROJECT_ROOT.resolve(),
                ],
                check=True,
            )

    except FileExistsError as remove_tables_file_exists_error:
        WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
            bool(remove_tables_file_exists_error.args)
            and "already exists" in remove_tables_file_exists_error.args[0]
        )
        if WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
            WITH_PYMARKDOWN_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                f"{remove_tables_file_exists_error.args[0]} "
                f"Use `{arg_parser.prog} --restore` to first restore the files "
                "to their original state."
            )
            raise type(remove_tables_file_exists_error)(
                WITH_PYMARKDOWN_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE  # noqa: COM812
            ) from remove_tables_file_exists_error

        raise remove_tables_file_exists_error from remove_tables_file_exists_error

    return parser_output.returncode


def _set_up_arg_parser() -> ArgumentParser:
    arg_parser: ArgumentParser = ArgumentParser(
        prog="rcft-pymarkdown",
        description="Lint Markdown files after removing custom-formatted tables.",
    )

    action_sub_parser_group: "SubParserGroup" = arg_parser.add_subparsers(
        title="action",
        required=True,
        dest="action",
    )

    remove_action_sub_parser: ArgumentParser = action_sub_parser_group.add_parser(
        "remove",
        help="Manually remove custom formatted tables from all Markdown files.",
    )
    remove_action_sub_parser.set_defaults(
        run_func=functools.partial(_run_remove, arg_parser=arg_parser),
    )

    restore_action_sub_parser: ArgumentParser = action_sub_parser_group.add_parser(
        "restore",
        help="Manually restore custom formatted tables from all Markdown files.",
    )
    restore_action_sub_parser.set_defaults(run_func=_run_restore)

    scan_all_action_sub_parser: ArgumentParser = action_sub_parser_group.add_parser(
        "scan-all",
        help="Lint all Markdown files after removing custom-formatted tables.",
    )
    scan_all_action_sub_parser.set_defaults(
        run_func=functools.partial(_run_scan_all, arg_parser=arg_parser),
    )

    return arg_parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run RCFT-PyMarkdown."""
    arg_parser: ArgumentParser = _set_up_arg_parser()

    parsed_args: Namespace = arg_parser.parse_args(argv)

    return_value: object = parsed_args.run_func()
    if not isinstance(return_value, int):
        INVALID_ACTION_RETURN_TYPE: Final[str] = (
            f"Action {parsed_args.action}'s run_func did not return an integer."
        )
        raise TypeError(INVALID_ACTION_RETURN_TYPE)

    return return_value
