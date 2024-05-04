import tempfile
from pathlib import Path
from typing import Optional, Text, Union


def create_dummy_file(size_mb, filepath: Optional[Text] = None) -> Union[Text, Path]:
    """Creates a temporary file with the specified size in MB.

    Parameters
    ----------
    size_mb: int
        Size of the file in MB.

    Returns
    -------
    str
        The path to the temporary file.
    """

    # Calculate the number of bytes
    size_bytes = int(size_mb * 1024 * 1024)
    dummy_bytes = b"\0" * size_bytes

    if not filepath:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(dummy_bytes)
            return f.name

    else:
        # Create a file at the specified path
        with open(filepath, "wb") as f:
            f.write(dummy_bytes)
            return filepath
