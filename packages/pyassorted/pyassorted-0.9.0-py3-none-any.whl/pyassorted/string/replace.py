import re
from enum import Enum
from typing import Dict, Text


class Bracket(Enum):
    NoBracket = 0
    Parenthesis = 1
    CurlyBrackets = 2
    SquareBrackets = 3


def multiple_replace(
    d: Dict[Text, Text], text: Text, wrapped_by: Bracket = Bracket.NoBracket
) -> Text:
    """Replace 'd' keys with 'd' values in 'text' string.

    Parameters
    ----------
    d : Dict[Text, Text]
        Dictionary with keys to be replaced by values.
    text : Text
        Text to be replaced.
    wrapped_by : Bracket, optional
        If specified, the keys will be wrapped by the specified bracket type.
        If not specified, the keys will be replaced without any wrapping.
        The default is Bracket.NoBracket.

    Returns
    -------
    Text
        Text with replaced keys.

    Raises
    ------
    ValueError
        If 'wrapped_by' is not a valid Bracket type.

    Examples
    --------
    >>> d = {"var1": "Hello", "var2": "World"}
    >>> text = "var1 var2"
    >>> multiple_replace(d, text)
    'Hello World'
    """

    if wrapped_by is Bracket.NoBracket:
        regex = re.compile(r"%s" % "|".join(map(re.escape, d.keys())))
    elif wrapped_by is Bracket.Parenthesis:
        regex = re.compile(r"\(\s*(%s)\s*\)" % "|".join(map(re.escape, d.keys())))
    elif wrapped_by is Bracket.SquareBrackets:
        regex = re.compile(r"\[\s*(%s)\s*\]" % "|".join(map(re.escape, d.keys())))
    elif wrapped_by is Bracket.CurlyBrackets:
        regex = re.compile(r"{\s*(%s)\s*}" % "|".join(map(re.escape, d.keys())))
    else:
        raise ValueError(f"Invalid Bracket type: {wrapped_by}")

    if wrapped_by is Bracket.Parenthesis:
        return regex.sub(lambda mo: d[mo.group().strip("() \t\n\r")], text)
    if wrapped_by is Bracket.SquareBrackets:
        return regex.sub(lambda mo: d[mo.group().strip("[] \t\n\r")], text)
    else:
        return regex.sub(lambda mo: d[mo.group().strip("{} \t\n\r")], text)


def limit_consecutive_newlines(text: Text, max_newlines: int = 2) -> Text:
    """Limit consecutive newlines in a string.

    Parameters
    ----------
    text : Text
        Input text with newlines.
    max_newlines : int, optional
        Maximum number of consecutive newlines allowed. The default is 2.

    Returns
    -------
    Text
        Text with limited consecutive newlines.

    Examples
    --------
    >>> text = "Hello\n\n\n\n\nWorld"
    >>> limit_consecutive_newlines(text)
    'Hello\n\nWorld'
    """

    # Creating a regex pattern to match more than `max_newlines` newlines
    pattern = r"\n{" + str(max_newlines + 1) + ",}"
    # Replace found patterns with `max_newlines` amount of newline characters
    return re.sub(pattern, "\n" * max_newlines, text)
