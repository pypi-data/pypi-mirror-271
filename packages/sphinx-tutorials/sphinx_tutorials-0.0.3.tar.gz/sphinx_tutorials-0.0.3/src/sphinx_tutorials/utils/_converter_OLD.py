from __future__ import annotations

from pathlib import Path

from sphinx_tutorials.utils.py_rules import py_to_rst


def generate_rst(
        origin_path: Path,
        target_path: Path,
        force_overwrite: bool = False,
        pkg_name: str = None,
) -> None:
    _convert_py_files(
        origin_path=origin_path,
        target_path=target_path,
        force_overwrite=force_overwrite
    )

    _create_basic_usage_rst(target_path, pkg_name=pkg_name)


def _convert_py_files(
        origin_path: Path,
        target_path: Path,
        force_overwrite: bool = False
) -> None:
    temp: list[Path] = list(origin_path.glob('**/*.py'))

    py_files: list[Path] = []
    for f in temp:
        if (  # skip files or directories starting with '_'
                str(f.relative_to(origin_path)).startswith("_")
                or f.name.startswith('_')
        ):
            continue

        py_files.append(f)

    existing_rst_files = _find_existing_rst_files(
        py_files=py_files,
        target_path=target_path,
    )

    if existing_rst_files and not force_overwrite:
        raise FileExistsError("\n\t" + "\n\t".join(map(str, existing_rst_files)))

    for f in py_files:
        rst_file = target_path / f.relative_to(origin_path).with_suffix('.rst')
        py_to_rst(origin_file_path=f, target_file_path=rst_file)


def _find_existing_rst_files(
        py_files: list[Path],  # where the .py files are
        target_path: Path  # where the .rst should go
) -> list[str | Path]:
    out = []

    for f in py_files:

        rst_file_path = target_path / Path(f.stem).with_suffix('.rst')

        if rst_file_path.exists():
            out.append(rst_file_path)

    return out


# ----------------------------------------------------------------------

def _create_basic_usage_rst(
        target_path: Path,
        *,
        pkg_name: str = None,
) -> None:
    tutorials_rst_path = target_path / 'tutorials.rst'

    # get a list of all the available RST files
    rsts = _create_folder_files_dict(target_path=target_path)

    rst_content = ""
    for title, files in rsts.items():
        # Add a toctree directive for all generated RST files
        rst_content += add_toc_tree(title=title, rst_files=files)

    if pkg_name:
        rst_content = add_show_dependencies(rst_content, pkg_name)

    # Write the content to 'tutorials.rst'
    with tutorials_rst_path.open('w') as rst_file:
        rst_file.write(rst_content)


def add_show_dependencies(rst_content: str, pkg_name: str) -> str:
    rst_content += f"""

.. code-example:: Dependencies Versions in Tutorials
    :collapsible:

    .. ipython:: python

        import {pkg_name}

        {pkg_name}.show_versions()

        """
    return rst_content


def add_toc_tree(title: str | None, rst_files: list) -> str:
    if title is None:
        title = 'Tutorials'

    title = title.replace("_", " ").title().strip()

    toc_str = f"\n{title}\n{'=' * len(title)}\n\n"

    # Add a toctree directive for all generated RST files
    toc_str += """
.. toctree::
   :maxdepth: 1
        """

    for rst_file in rst_files:
        toc_str += f"""
   {rst_file}
            """

    return toc_str


def _create_folder_files_dict(
        target_path: Path,
        exclude_file: str = 'tutorials.rst') -> dict[str | None, list[Path]]:
    rst_files = [
        file.relative_to(target_path)
        for file in target_path.glob('**/*.rst')
        if file.name != exclude_file
    ]

    folder_files_dict = {}

    # todo: instead of separating with - make the subfolders subtitles
    for file in rst_files:
        # Generate the key by joining folder names with " - ",
        # or use 'root' for files at the root level
        folder = " - ".join(file.parts[:-1]) if len(file.parts) > 1 else 'root'
        folder_files_dict.setdefault(folder, []).append(file)

    return folder_files_dict
