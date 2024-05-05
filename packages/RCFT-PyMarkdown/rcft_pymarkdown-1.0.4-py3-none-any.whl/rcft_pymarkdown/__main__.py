"""Command-line execution of the `rcft_pymarkdown` package."""

from collections.abc import Sequence

__all__: Sequence[str] = ()


from rcft_pymarkdown import console

if __name__ == "__main__":
    raise SystemExit(console.run())
