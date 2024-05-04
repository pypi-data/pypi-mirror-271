import random
import string
from typing import Text


def rand_str(
    length: int = 10, chars: Text = string.ascii_letters + string.digits
) -> Text:
    """Generate a random string of fixed length."""

    return "".join(random.choice(chars) for _ in range(length))


def rand_mixed_alpha_number(length: int = 10, upper_case: bool = True) -> Text:
    """Generate a random string of fixed length with alternating alpha and numeric characters."""

    if length < 1:
        raise ValueError("Length must be greater than 0")

    if upper_case is True:
        alpha_chars = string.ascii_uppercase
    else:
        alpha_chars = string.ascii_letters

    out = ""
    for i in range(length):
        if i % 2 == 0:
            out += random.choice(alpha_chars)
        else:
            out += random.choice(string.digits)
    return out
