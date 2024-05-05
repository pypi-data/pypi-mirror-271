"""Custom context manager to remove custom-formatted tables only inside the context."""

from collections.abc import Sequence

__all__: Sequence[str] = ("RemoveCustomFormattedTables",)


from types import TracebackType

from rcft_pymarkdown import (
    remove_custom_formatted_tables,
    restore_custom_formatted_tables,
)


class RemoveCustomFormattedTables:
    """Context manager to remove custom-formatted tables only inside the context."""

    def __enter__(self) -> None:
        """Remove custom-formatted tables before entering the context."""
        remove_custom_formatted_tables.remove_custom_formatted_tables_from_all_files()

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:  # noqa: E501
        """Restore Markdown files back to their original state."""
        restore_custom_formatted_tables.restore_custom_formatted_tables_from_all_files()
