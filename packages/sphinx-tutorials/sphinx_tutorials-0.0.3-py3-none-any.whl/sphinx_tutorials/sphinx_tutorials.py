from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sphinx_tutorials.utils.copy import _copy_all_folders, copy_tutorials


def generate(
        docs_path: str | Path,
        tutorials_source_path: str | Path = None,
        tutorials_dest_path: str | Path = None,  # often same as docs
        *,
        style: bool = True,
        overwrite_style: bool = False,
        overwrite_tutorials: bool = False,
        include_suffixes: Iterable[str] = None,
        exclude_prefixes: Iterable[str] = None
) -> None:
    """
    Generates tutorials.

    Parameters
    ----------
    docs_path
    tutorials_source_path
    tutorials_dest_path
    style
    overwrite_style
    overwrite_tutorials
    include_suffixes
    exclude_prefixes

    Returns
    -------

    """
    if tutorials_source_path is not None and tutorials_dest_path is not None:
        copy_tutorials(
            source_path=tutorials_source_path,
            destination_path=tutorials_dest_path,
            overwrite=overwrite_tutorials,
            include_suffixes=include_suffixes,
            exclude_prefixes=exclude_prefixes,
        )

    if style:
        _copy_all_folders(
            source_path=Path(__file__).parent.absolute() / "_docs_files",
            destination_path=Path(docs_path),
            overwrite=overwrite_style,
        )
