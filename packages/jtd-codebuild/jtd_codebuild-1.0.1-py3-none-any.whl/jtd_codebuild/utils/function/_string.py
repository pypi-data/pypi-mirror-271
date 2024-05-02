from typing import Callable


def replace(old: str, new: str) -> Callable[[str], str]:
    """Return a function that replaces `old` with `new` in a string.

    Args:
        old: The string to replace.
        new: The string to replace with.

    Returns:
        A function that replaces `old` with `new` in a string.
    """

    def replacer(source: str) -> str:
        return source.replace(old, new)

    return replacer
