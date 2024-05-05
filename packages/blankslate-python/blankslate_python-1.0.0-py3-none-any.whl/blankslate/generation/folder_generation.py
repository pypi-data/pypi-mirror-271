"""folder_generation.py: Contains functions for generating folders."""

import os
from pathlib import Path

from ..logs.setup_logging import setup_logging

folder_logger = setup_logging()


def generate_folder(folder: str, path: Path) -> None:
    """
    Generate a single folder.

    Parameters
    ----------
    folder : str
        The folder to generate.
    path : Path
        The path to generate the folder in.

    Notes
    -----
    This function generates a single folder in the specified path.
    """
    folder_logger.debug(f"Generating folder: {folder}")
    folder_path = path / folder
    os.makedirs(folder_path, exist_ok=True)
    folder_logger.info(f"Folder generated: {folder_path}")


def generate_folders(folders: list[str], path: Path) -> None:
    """
    Generate multiple folders.

    Parameters
    ----------
    folders : list[str]
        The folders to generate.
    path : Path
        The path to generate the folders in.

    Notes
    -----
    This function generates multiple folders in the specified path.
    """
    for folder in folders:
        generate_folder(folder, path)


def generate_folder_structure(folder_structure: dict[str, list[str]], path: Path) -> None:
    """
    Generate a folder structure.

    Parameters
    ----------
    folder_structure : dict[str, list[str]]
        The folder structure to generate.
    path : Path
        The path to generate the folder structure in.

    Examples
    --------
    >>> folder_structure = {
    ...     "folder1": ["subfolder1", "subfolder2"],
    ...     "folder2": ["subfolder3", "subfolder4"],
    ... }
    >>> path = Path("C:/Users/user/Documents/Projects/project")
    >>> generate_folder_structure(folder_structure, path)

    Notes
    -----
    This function generates a folder structure in the specified path.
    """
    if not folder_structure:
        folder_logger.warning("No folder structure to generate.")
        return
    elif not path.exists():
        folder_logger.warning(f"Path does not exist, creating: {path}")
        os.makedirs(path)

    folder_logger.debug(f"Generating folder structure: {folder_structure}")

    for folder, subfolders in folder_structure.items():
        current_path = path / folder
        generate_folder(folder, path)
        if isinstance(subfolders, list):
            folder_logger.debug(f"Generating subfolders: {subfolders}")
            generate_folders(subfolders, current_path)
