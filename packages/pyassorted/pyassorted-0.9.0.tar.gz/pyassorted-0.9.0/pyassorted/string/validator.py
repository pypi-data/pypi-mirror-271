import re
import uuid
from typing import Sequence, Text


def is_valid_filename(filename: Text) -> bool:
    """Checks if a filename is valid."""

    if len(filename) > 255:
        return False

    if re.match(r"^[\w\-. ]+$", filename) is None:
        return False

    return True


def sanitize_filename(filename: Text) -> Text:
    """Sanitize the filename by replacing invalid characters and spaces."""

    filename = re.sub(r'[\\/*?:"<>| ]', "_", filename)
    return filename


def decode_text_bytes(
    text_bytes: bytes,
    encoding_options: Sequence[Text] = ("utf-8", "windows-1252", "iso-8859-1"),
    unified_text: bool = True,
) -> Text:
    for encoding in encoding_options:
        try:
            file_content = text_bytes.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        return Exception(
            f"Could not decode file content with any of the following encodings: {encoding_options}"
        )

    if unified_text is True:
        file_content = file_content.replace("\r\n", "\n")
        file_content = file_content.replace("\r", "\n")
        file_content = "\n".join(
            [line.strip() for line in file_content.split("\n") if line.strip()]
        )
        file_content = file_content.replace("\t", "    ")
        file_content = file_content.replace("\xa0", " ")
        file_content = file_content.strip()
    return file_content


def validate_uuid(uuid_string: Text, version: int = 4) -> bool:
    """Checks if a UUID string is valid."""

    uuid_string = uuid_string.lower()
    try:
        uuid_obj = uuid.UUID(uuid_string, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_string
