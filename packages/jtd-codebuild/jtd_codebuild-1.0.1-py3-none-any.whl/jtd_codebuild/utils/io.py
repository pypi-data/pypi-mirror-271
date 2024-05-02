import json
from typing import Any
from os import makedirs
from os.path import dirname


def read(file: str) -> str:
    """Read a file.

    Args:
        file: The file name.

    Returns:
        The file content.
    """
    makedirs(dirname(file), exist_ok=True)
    with open(file, "r") as f:
        return f.read()


def write(file: str, data: str) -> None:
    """Write a file.

    Args:
        file: The file name.
        data: The file content.
    """
    makedirs(dirname(file), exist_ok=True)
    with open(file, "w") as f:
        f.write(data)


def read_json(file: str) -> dict[str, Any]:
    """Read a JSON file.

    Args:
        file: The file name.

    Returns:
        The JSON content.
    """
    return json.loads(read(file))


def write_json(file: str, data: dict[str, Any]) -> None:
    """Write a JSON file.

    Args:
        file: The file name.
        data: The JSON content.
    """
    return write(file, json.dumps(data, indent=2))
