"""Module for the PrettyStrings class"""


class PrettyStrings:
    """This class contains various methods to prettify print strings to the terminal."""

    _CONSTRUCTOR_ERROR: str = "This class is not instantiable!"
    _SPACE = " "
    _HORIZONTAL_FRAME = "-"
    _VERTICAL_FRAME = "|"
    _NEW_LINE = "\n"

    def __init__(self) -> None:
        """Prevents the instantiation of this class.

        Raises
        ------
        - NotImplementedError
        """
        raise NotImplementedError(PrettyStrings._CONSTRUCTOR_ERROR)

    @staticmethod
    def frame(
        to_frame: str, frame_length: int, centered: bool, vertical_frame: bool
    ) -> str:
        """Puts the given string in the center or in the beginning of the line surrounded by the
        horizontal frame above and below and, if needed, also the vertical frame before and after.
        It's required to specify a frame length for the horizontal frame.

        Params
        ------
        - to_frame -> The string to put in the frame
        - frame_length -> The length of the horizontal frame.
        - centered -> If the string needs to be centered or not.
        - vertical_frame -> If the vertical frame is needed or not.

        Returns
        -------
        A string containing the framed original string.
        """
        framed: list[str] = []
        horizontal_frame: list[str] = "".join(
            [
                PrettyStrings.repeat_char(
                    PrettyStrings._HORIZONTAL_FRAME, frame_length
                ),
                PrettyStrings._NEW_LINE,
            ]
        )

        framed.append(horizontal_frame)

        if vertical_frame:
            framed.append(PrettyStrings._VERTICAL_FRAME)

        to_append: str
        if centered:
            to_append = (
                PrettyStrings.center(to_frame, frame_length - 2)
                if vertical_frame
                else "".join(
                    [
                        PrettyStrings.center(to_frame, frame_length),
                        PrettyStrings._NEW_LINE,
                    ]
                )
            )
        else:
            to_append = (
                PrettyStrings.column(to_frame, frame_length - 2)
                if vertical_frame
                else "".join(
                    [
                        PrettyStrings.column(to_frame, frame_length),
                        PrettyStrings._NEW_LINE,
                    ]
                )
            )
        framed.append(to_append)

        if vertical_frame:
            framed.append(
                "".join([PrettyStrings._VERTICAL_FRAME, PrettyStrings._NEW_LINE])
            )

        framed.append(horizontal_frame)

        return "".join(framed)

    @staticmethod
    def column(to_columnize: str, width: int) -> str:
        """Puts teh given string at the beginning of the line and adds spaces until the end of it.
        If the string is too long for the width of the line, it will be cut off.

        Params
        ------
        - to_columnize -> The string to put in column.
        - width -> The length of the line.

        Returns
        -------
        A string containing the columned string.
        """
        columned: list[str] = []
        to_columnize_length: int = len(to_columnize)
        chars_to_print: int = min(width, to_columnize_length)

        columned.append(
            to_columnize[:chars_to_print]
            if to_columnize_length > chars_to_print
            else to_columnize
        )

        columned.append(
            PrettyStrings.repeat_char(
                PrettyStrings._SPACE, max(0, width - to_columnize_length)
            )
        )

        return "".join(columned)

    @staticmethod
    def center(to_center: str, width: int) -> str:
        """Puts the given string in the center of the line of the given width. If the string is too
        long it will be cut off.

        Params
        ------
        - to_center -> The string to center.
        - width -> The length of the line where to center the string.

        Returns
        -------
        A string containing the centered string.
        """
        to_center_length: int = len(to_center)

        if to_center_length > width:
            return to_center[:width]

        if to_center_length == width:
            return to_center

        centered: list[str] = []
        whitespaces: int = width - to_center_length
        whitespaces_before: int = whitespaces // 2
        whitespaces_after: int = whitespaces - whitespaces_before

        centered.append(
            PrettyStrings.repeat_char(PrettyStrings._SPACE, whitespaces_before)
        )
        centered.append(to_center)
        centered.append(
            PrettyStrings.repeat_char(PrettyStrings._SPACE, whitespaces_after)
        )

        return "".join(centered)

    @staticmethod
    def repeat_char(char: str, times: int) -> str:
        """Repeats a given character a given number of times.

        Params
        ------
        - char -> The character to repeat.
        - times -> The number of times to repeat the character.

        Returns
        -------
        A string containing the character repeated. If times is less than or equal to 0 an empty
        string will be returned.
        """
        return char * max(0, times)

    @staticmethod
    def isolated_line(to_isolate: str) -> str:
        """Isolates a given string by adding an empty line before and after it.

        Params
        ------
        - to_isolate -> The string to isolate.

        Returns
        -------
        A string containing the isolated string.
        """
        return f"{PrettyStrings._NEW_LINE}{to_isolate}{PrettyStrings._NEW_LINE}"
