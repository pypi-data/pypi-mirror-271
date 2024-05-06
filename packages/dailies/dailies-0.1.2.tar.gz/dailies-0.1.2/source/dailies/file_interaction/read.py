"""read.py: Read the game files."""

import os

from ..logs.setup_logging import setup_logging

file_interaction_logger = setup_logging()


def read_file(file: str) -> list[str] | None:
    """
    Read a file.

    Parameters
    ----------
    file : str
        The file to read.

    Returns
    -------
    list[str] | None
        The file contents as a list of strings.
        None if the file does not exist.

    Examples
    --------
    >>> read_file("file.txt")
    ["line 1", "line 2", "line 3"]

    Notes
    -----
    This function reads a file and returns its contents as a list of strings,
    with each string representing a line in the file.
    """
    file_interaction_logger.info(f"Reading file: {file}")
    if not os.path.exists(file):
        file_interaction_logger.error(f"File not found: {file}")
        return None

    with open(file, "r") as f:
        return f.read().splitlines()
