"""project_generation.py: Contains the functions for generating a project."""

from pathlib import Path

from ..generation.folder_generation import generate_folder_structure
from ..generation.template_rendering import render_template
from ..logs.setup_logging import setup_logging

project_logger = setup_logging()


def dict_to_tree(file_structure: dict, indent: int = 0, prefix: str = "") -> str:
    """
    Convert a dictionary to a tree structure.

    Parameters
    ----------
    file_structure : dict
        The dictionary to convert.
    indent : int, optional
        The indentation level, by default 0.
    prefix : str, optional
        The prefix to add to each line, by default "". Used internally.

    Returns
    -------
    str
        The tree structure as a string.

    Examples
    --------
    >>> file_structure = {
    ...     "folder1": {
    ...         "file1": None,
    ...         "file2": None,
    ...     },
    ...     "folder2": {
    ...         "file3": None,
    ...     },
    ... }
    >>> dict_to_tree(file_structure)
    '├── folder1\n│   ├── file1\n│   └── file2\n└── folder2\n    └── file3\n'

    Notes
    -----
    This function converts a dictionary to a tree structure, with each key
    representing a folder or file name.
    """
    if not file_structure:
        return ""

    keys = list(file_structure.keys())
    last_index = len(keys) - 1
    structure_str = ""

    for index, key in enumerate(keys):
        if index == last_index:
            joint = "└── "
            extension = "    "
        else:
            joint = "├── "
            extension = "│   "

        structure_str += f"{prefix}{joint}{key}\n"

        if isinstance(file_structure[key], dict):
            sub_prefix = prefix + extension
            structure_str += dict_to_tree(file_structure[key], indent + 1, sub_prefix)

    return structure_str


def strip_to_folder_structure(full_structure: dict) -> dict:
    """
    Strip a full structure dictionary to just the folder paths.

    Parameters
    ----------
    full_structure : dict
        The full structure dictionary.

    Returns
    -------
    dict
        The folder structure dictionary.

    Examples
    --------
    >>> full_structure = {
    ...     "folder1": {
    ...         "file1": None,
    ...         "file2": None,
    ...     },
    ...     "folder2": {
    ...         "file3": None,
    ...     },
    ... }
    >>> strip_to_folder_structure(full_structure)
    {'folder1': {}, 'folder2': {}}

    Notes
    -----
    This function strips a full structure dictionary to just the folder paths.
    """
    folder_structure = {}
    for key, value in full_structure.items():
        if isinstance(value, dict):
            nested_folders = strip_to_folder_structure(value)
            if nested_folders:
                folder_structure[key] = nested_folders
            elif not nested_folders:
                folder_structure[key] = {}
        elif isinstance(value, list):
            folder_structure[key] = {}

    return folder_structure


def strip_to_files(full_structure: dict, base_path: str = "") -> list[tuple[str, str]]:
    """
    Strip a full structure dictionary to just the file paths.

    Parameters
    ----------
    full_structure : dict
        The full structure dictionary.
    base_path : str, optional
        The base path for the files, by default "". Used internally.

    Returns
    -------
    list[tuple[str, str]]
        The file paths as a list of tuples.

    Examples
    --------
    >>> full_structure = {
    ...     "folder1": {
    ...         "file1": None,
    ...         "file2": None,
    ...     },
    ...     "folder2": {
    ...         "file3": None,
    ...     },
    ... }
    >>> strip_to_files(full_structure)
    [('file1', 'folder1'), ('file2', 'folder1'), ('file3', 'folder2')]

    Notes
    -----
    This function strips a full structure dictionary to just the file paths.
    """
    files_list = []
    for key, value in full_structure.items():
        current_path = f"{base_path}/{key}".strip("/")
        if isinstance(value, dict):
            nested_files = strip_to_files(value, current_path)
            files_list.extend(nested_files)
        elif value is None:
            files_list.append((key, current_path))

    return files_list


def generate_project(project_details: dict[str, str]) -> None:
    """
    Generate a project.

    Parameters
    ----------
    project_details : dict[str, str]
        The project details.

    Examples
    --------
    >>> project_details = {
    ...     "project_name": "MyProject",
    ...     "project_location": "C:/Users/user/Documents/Projects",
    ... }
    >>> generate_project(project_details)

    Notes
    -----
    This function generates a project based on the provided details.
    """
    project_name = project_details["project_name"]
    project_location = project_details["project_location"]

    full_structure = {
        ".github": {
            "workflows": {
                "continuous_integration.yml": None,
                "todo_to_issue.yml": None,
            },
        },
        ".vscode": {
            "extensions.json": None,
        },
        "docs": {},
        "scripts": {"release.sh"},
        "source": {
            project_name: {
                "config": {
                    "__init__.py": None,
                    "constants.py": None,
                    "paths.py": None,
                },
                "interface": {
                    "__init__.py": None,
                    "command_line.py": None,
                },
                "logs": {
                    "__init__.py": None,
                    "setup_logging.py": None,
                },
                "main.py": None,
                "py.typed": None,
                "VERSION": None,
            },
        },
        "tests": {},
        ".gitignore": None,
        ".pre-commit-config.yaml": None,
        "CHANGELOG.md": None,
        "conf.py": None,
        "CONTRIBUTING.md": None,
        "index.rst": None,
        "LICENSE": None,
        "pyproject.toml": None,
        "README.md": None,
        "requirements-dev.txt": None,
        "requirements.txt": None,
        "tox.ini": None,
    }

    project_logger.info(f"Generating project: {project_name}")
    project_logger.info(f"{project_name}\n{dict_to_tree(full_structure)}")

    folder_structure = strip_to_folder_structure(full_structure)
    file_structure = strip_to_files(full_structure)

    project_logger.debug(f"Folder structure:\n{folder_structure}")
    project_logger.debug(f"File structure:\n{file_structure}")

    generate_folder_structure(folder_structure, Path(project_location))

    for file_name, file_path in file_structure:
        render_template(file_name + ".j2", Path(project_location) / file_path, project_details)
