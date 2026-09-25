import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def inspect_file(filepath_str):
    """Return basic information about an existing file."""
    # 1: Create a Path object.
    path = Path(filepath_str)

    # 2: If the path is not a file:
    #         Log an ERROR message.
    #         Raise FileNotFoundError (e.g. file not found).
    if not path.is_file():
        logger.error(f"File not found: {filepath_str}")
        raise FileNotFoundError(f"File not found: {filepath_str}")

    # 3: Return a dictionary containing:
    #         name and extension.
    path_info = {
        "name": path.name,
        "extension": path.suffix
    }
    return path_info


def inspect_extension(file_info):
    """Confirm that the file uses a supported text extension."""
    supported_extension = ".txt"

    # 4: If file_info["extension"] does not equal
    #         supported_extension:
    #         Log an ERROR message (e.g. unsupported format).
    #         Raise ValueError.
    if file_info["extension"] not in supported_extension:
        logger.error(f"Unsupported text format: {file_info["extension"]}")
        raise ValueError(f"Unsupported text format: {file_info["extension"]}")
    
    # 5: Return file_info.
    return file_info
