from os import makedirs
from os.path import join, dirname, isabs
from io import TextIOWrapper


def file_is_yaml(file: str) -> bool:
    """Check if a file is a YAML file.

    Args:
        file: The file name.

    Returns:
        True if the file is a YAML file, False otherwise.
    """
    return file.endswith((".yaml", ".yml"))


def file_is_json(file: str) -> bool:
    """Check if a file is a JSON file.

    Args:
        file: The file name.

    Returns:
        True if the file is a JSON file, False otherwise.
    """
    return file.endswith(".json")


def safe_open(file_path: str, mode: str) -> TextIOWrapper:
    """Open a file with creating its parent directories if they do not exist.

    Args:
        file_path: The file path.
        mode: The file open mode.

    Returns:
        The opened file.
    """
    makedirs(dirname(file_path), exist_ok=True)
    return open(file_path, mode)


def resolve(cwd: str, path: str) -> str:
    return path if isabs(path) else join(cwd, path)
