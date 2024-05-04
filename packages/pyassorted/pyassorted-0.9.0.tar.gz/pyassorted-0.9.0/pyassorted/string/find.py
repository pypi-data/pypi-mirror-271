import re
from typing import List, Text


def find_placeholders(
    text: Text, *, open_delim: Text = "{", close_delim: Text = "}"
) -> List[Text]:
    """Find placeholders in a string.

    Parameters
    ----------
    text : Text
        Input string to find placeholders.
    open_delim : Text, optional
        Opening delim for placeholders. The default is "{".
    close_delim : Text, optional
        Closing delim for placeholders. The default is "}".

    Returns
    -------
    List[Text]
        List of placeholder names found in the input string.
    """

    # Escaping delims if necessary for regex usage
    open_delim = re.escape(open_delim)
    close_delim = re.escape(close_delim)

    # Regex pattern to find valid placeholder names
    pattern = rf"{open_delim}([a-zA-Z_][a-zA-Z0-9_-]*){close_delim}"
    return re.findall(pattern, text)


def extract_code_blocks(text: Text, language: Text) -> List[Text]:
    """Extract code blocks for specified languages from a text.

    Parameters
    ----------
    text : str
        The input text from which to extract code blocks.
    language : str
        The language specifier immediately after the opening marker, e.g., "json", "yml", "go".

    Returns
    -------
    List[str]
        A list of extracted code blocks without the markers.

    Examples
    --------
    >>> extract_code_blocks("Here is a code block: ```json{\"key\": \"value\"}``` end", "json")
    ['{"key": "value"}']
    """

    # Pattern to find blocks that start with ```<language>\n and end with ```
    pattern = rf"```{language.strip()}\n(.*?)(?=```)"
    return re.findall(pattern, text, flags=re.DOTALL)
