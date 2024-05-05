"""A Python helper script to load a set of mods from a local mods-list."""

from collections.abc import Sequence

__all__: Sequence[str] = (
    "run",
    "restore_custom_formatted_tables_from_all_files",
    "remove_custom_formatted_tables_from_all_files",
    "remove_custom_formatted_tables_from_file",
    "RemoveCustomFormattedTables",
)
__version__ = "v1.0.4"


from rcft_pymarkdown.console import run
from rcft_pymarkdown.context_manager import RemoveCustomFormattedTables
from rcft_pymarkdown.remove_custom_formatted_tables import (
    remove_custom_formatted_tables_from_all_files,
    remove_custom_formatted_tables_from_file,
)
from rcft_pymarkdown.restore_custom_formatted_tables import (
    restore_custom_formatted_tables_from_all_files,
)
