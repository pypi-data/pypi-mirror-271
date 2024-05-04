import textwrap


def message(text: str, max_line_length: int = 60) -> str:
    """
    Splits a text so it fits into the maximum line length and formats it
    for showing in the screen.
    """

    lines = textwrap.wrap(text, max_line_length, break_long_words=False)

    return "\n\t> " + "\n\t  ".join(lines) + "\n"
