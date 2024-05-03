"""Module used for customizing the output to the terminal.

This module provides:
- The class AnsiFontColors.
- The class AnsiFontWeights.
- The class AnsiFontDecorations.
- The constant RESET for resetting the previously given customization.
"""

# Standard Libraries
from enum import StrEnum

RESET: str = "\u001b[0m"


class AnsiFontWeights(StrEnum):
    """Used for accessing a list of font weight customization for writing in the terminal."""

    BOLD = "\u001b[1m"
    LIGHT = "\u001b[2m"
    ITALIC = "\u001b[3m"


class AnsiFontDecorations(StrEnum):
    """Used for accessing a list of font decoration customization for writing in the terminal."""

    UNDERLINE = "\u001b[4m"
    HIDE = "\u001b[8m"
    STRIKETHROUGH = "\u001b[9m"
    DOUBLE_UNDERLINE = "\u001b[21m"
    OVERLINE = "\u001b[53m"


class AnsiFontColors:
    """Used for accessing a list of color customization for writing in the terminal.

    Only the standard 8 colors for back and foreground are implemented as constants, plus the code
    for clearing the terminal and inverting back and foreground. For more color customization see
    the specified methods.
    """

    _VALUE_ERROR: str = (
        f"Only values from {AnsiFontWeights.BOLD}0{RESET} to \
            {AnsiFontWeights.BOLD}255{RESET} are allowed!"
    )

    INVERT: str = "\u001b[7m"
    BLACK: str = "\u001b[30m"
    RED: str = "\u001b[31m"
    GREEN: str = "\u001b[32m"
    YELLOW: str = "\u001b[33m"
    BLUE: str = "\u001b[34m"
    PURPLE: str = "\u001b[35m"
    CYAN: str = "\u001b[36m"
    WHITE: str = "\u001b[37m"
    BLACK_BACKGROUND: str = "\u001b[40m"
    RED_BACKGROUND: str = "\u001b[41m"
    GREEN_BACKGROUND: str = "\u001b[42m"
    YELLOW_BACKGROUND: str = "\u001b[43m"
    BLUE_BACKGROUND: str = "\u001b[44m"
    PURPLE_BACKGROUND: str = "\u001b[45m"
    CYAN_BACKGROUND: str = "\u001b[46m"
    WHITE_BACKGROUND: str = "\u001b[47m"
    CLEAR: str = "\u001b[H\u001b[2J"

    @staticmethod
    def eight_bit_color(n: int, apply_to_background: bool = False) -> str:
        """For a better understanding look here
        https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit.

        The general rules are:
        - Only numbers from 0 to 255 are allowed.
        - 0 to 7 are the standard colors, already provided as constants.
        - 8 to 15 are the brighter variants of the standard colors.
        - 16 to 231 are a LOT of shades of the aforementioned standard colors.
        - 232 to 255 are the grayscale colors.

        Params
        ------
        - n -> An integer representing the 8-bit color.
        - apply_to_background -> If the color should be applied to the background or the
        foreground, defaulted to False.

        Returns
        -------
        A string with the ansi code for coloring the back or foreground of the terminal.
        """
        if n < 0 or n > 255:
            raise ValueError(AnsiFontColors._VALUE_ERROR)

        sgr: str = "48" if apply_to_background else "38"

        return f"\u001b[{sgr};5;{n}m"

    @staticmethod
    def twenty_four_bit_color(
        red: int, green: int, blue: int, apply_to_background: bool = False
    ) -> str:
        """Very similar to its 8-bit counter part but this time using RGB colors.

        Params
        ------
        - red -> The red value of the color from 0 to 255.
        - blue -> The blue value of the color from 0 to 255.
        - green -> The green value of the color from 0 to 255.
        - apply_to_background -> If the color should be applied to the background or the
        foreground, defaulted to False.

        Returns
        -------
        A string with the ansi code for coloring the back or foreground of the terminal.
        """
        red_error: bool = red < 0 or red > 255
        blue_error: bool = blue < 0 or blue > 255
        green_error: bool = green < 0 or green > 255
        if red_error or blue_error or green_error:
            raise ValueError(AnsiFontColors._VALUE_ERROR)

        sgr: str = "48" if apply_to_background else "38"

        return f"\u001b[{sgr};2;{red};{green};{blue}m"
