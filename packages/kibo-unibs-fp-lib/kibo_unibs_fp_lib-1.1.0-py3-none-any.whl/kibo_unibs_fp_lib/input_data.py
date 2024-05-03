"""Module for the InputData class"""

# Internal Libraries
from kibo_unibs_fp_lib.ansi_colors import (
    RESET,
    AnsiFontColors,
    AnsiFontWeights,
    AnsiFontDecorations,
)


class InputData:
    """
    This class can read a specific data type inserted in input by the user, while also allowing to
    make controls on the data inserted and printing errors to the user.
    """

    _CONSTRUCTOR_ERROR: str = "This class is not instantiable!"
    _RED_ERROR: str = f"\n{AnsiFontColors.RED}{AnsiFontWeights.BOLD}Error!{RESET}"

    _ALPHANUMERIC_CHARACTERS_ERROR: str = (
        f"Only {AnsiFontWeights.BOLD}alphanumeric{RESET} characters are allowed.\n"
    )
    _EMPTY_STRING_ERROR: str = (
        f"No {AnsiFontWeights.BOLD}characters{RESET} or only \
            {AnsiFontWeights.BOLD}whitespaces{RESET} were inserted.\n"
    )
    _ALLOWED_CHARACTERS_ERROR: str = "The only allowed characters are: %s\n"
    _YES_ANSWERS: str = "yY"
    _NO_ANSWERS: str = "nN"
    _INTEGER_FORMAT_ERROR: str = (
        f"The inserted data is in an {AnsiFontWeights.BOLD}incorrect{RESET} format. An \
            {AnsiFontDecorations.UNDERLINE}integer{RESET} is required.\n"
    )
    _MINIMUM_ERROR: str = "A value greater than or equal to %.2f is required.\n"
    _MAXIMUM_ERROR: str = "A value less than or equal to %.2f is required.\n"
    _FLOAT_FORMAT_ERROR: str = (
        f"The inserted data is in an {AnsiFontWeights.BOLD}incorrect{RESET} format. A \
            {AnsiFontDecorations.UNDERLINE}float{RESET} is required.\n"
    )

    def __init__(self) -> None:
        """Prevents the instantiation of this class.

        Raises
        ------
        - NotImplementedError
        """
        raise NotImplementedError(InputData._CONSTRUCTOR_ERROR)

    @staticmethod
    def read_string(message: str, alphanumeric: bool = False) -> str:
        """Prints message in the terminal and reads the text inserted by the user. It's also
        possible to select if the inserted text needs to be alphanumeric or not via the
        alphanumeric variable.

        Params
        ------
        - message -> The message to print.
        - alphanumeric -> If the input needs to be alphanumeric or not, defaulted to False.

        Returns
        -------
        A string representing the user input.
        """
        if not alphanumeric:
            return input(message)

        is_alphanumeric: bool = False
        while not is_alphanumeric:
            read: str = input(message)

            is_alphanumeric = read.isalnum()

            if not is_alphanumeric:
                print(InputData._RED_ERROR)
                print(InputData._ALPHANUMERIC_CHARACTERS_ERROR)

        return read

    @staticmethod
    def read_non_empty_string(message: str, alphanumeric: bool = False) -> str:
        """Prints message in the terminal and reads the text inserted by the user, given that it
        isn't empty. It's also possible to select if the inserted text needs to be alphanumeric or
        not via the alphanumeric variable.

        Params
        ------
        - message -> The message to print.
        - alphanumeric -> If the input needs to be alphanumeric or not.

        Returns
        -------
        A string representing the user input.
        """
        is_empty: bool = True

        while is_empty:
            read: str = InputData.read_string(message, alphanumeric).strip()

            is_empty = not read
            if is_empty:
                print(InputData._RED_ERROR)
                print(InputData._EMPTY_STRING_ERROR)

        return read

    @staticmethod
    def read_char(message: str, allowed: str = None) -> str:
        """Read a single character input from the user. It's also possible to give a list, in the
        form of a string, of the possible allowed characters.

        Params
        ------
        - message -> The message to display to the user.
        - allowed -> Contains the allowed characters, defaulted to None.

        Returns
        -------
        The single character input by the user.
        """
        if not allowed:
            return InputData.read_non_empty_string(message, False)[0]

        is_allowed = False

        while not is_allowed:
            read = InputData.read_non_empty_string(message, False)[0]

            if read in allowed:
                is_allowed = True
            else:
                print(InputData._RED_ERROR)
                print(InputData._ALLOWED_CHARACTERS_ERROR % list(allowed))

        return read

    @staticmethod
    def read_yes_or_no(question: str) -> bool:
        """Prompts the user with a question and expects a yes or no response.

        The idea is to give the question the usual unix terminal aspects, where the question is
        followed by square brackets and the two possible answers, the upper case one is the default
        if no answer is given.

        Params
        ------
        - question -> The question to display the user without question mark.

        Returns
        -------
        True if the user respond with 'y' or 'Y', False otherwise.
        """
        question = (
            f"{question}? [{InputData._YES_ANSWERS[1]}/{InputData._NO_ANSWERS[0]}] "
        )
        response = InputData.read_string(question)

        if not response:
            return True

        return response[0] in InputData._YES_ANSWERS

    @staticmethod
    def read_integer(message: str) -> int:
        """Reads an integer input from the user.

        Params
        ------
        - message -> The message to display the user.

        Returns
        -------
        The integer input by the user.
        """
        is_integer: bool = False

        while not is_integer:
            try:
                read: int = int(input(message))
                is_integer = True
            except ValueError:
                print(InputData._RED_ERROR)
                print(InputData._INTEGER_FORMAT_ERROR)

        return read

    @staticmethod
    def read_integer_with_minimum(message: str, min_value: int) -> int:
        """Reads an integer input from the user with a minimum value constraint.

        Params
        ------
        - message -> The message to display the user.
        - min_value -> The minimum allowed value for the input.

        Returns
        -------
        The integer input by the user that is greater than or equal to min_value.
        """
        is_input_out_of_range: bool = True

        while is_input_out_of_range:
            read: int = InputData.read_integer(message)

            if read >= min_value:
                is_input_out_of_range = False
            else:
                print(InputData._RED_ERROR)
                print(InputData._MINIMUM_ERROR % min_value)

        return read

    @staticmethod
    def read_integer_with_maximum(message: str, max_value: int) -> int:
        """Reads an integer input from the user with a maximum value constraint.

        Params
        ------
        - message -> The message to display the user.
        - max_value -> The maximum allowed value for the input.

        Returns
        -------
        The integer input by the user that is less than or equal to max_value.
        """
        is_input_out_of_range: bool = True

        while is_input_out_of_range:
            read: int = InputData.read_integer(message)

            if read <= max_value:
                is_input_out_of_range = False
            else:
                print(InputData._RED_ERROR)
                print(InputData._MAXIMUM_ERROR % max_value)

        return read

    @staticmethod
    def read_integer_between(message: str, min_value: int, max_value: int) -> int:
        """Reads an integer input from the user with a minimum and maximum value constraint.

        Params
        ------
        - message -> The message to display the user.
        - min_value -> The minimum allowed value for the input.
        - max_value -> The maximum allowed value for the input.

        Returns
        -------
        The integer input by the user that is greater than or equal to min_value and less than or
        equal to max_value.
        """
        is_input_out_of_range: bool = True

        while is_input_out_of_range:
            read: int = InputData.read_integer(message)

            if read < min_value:
                print(InputData._RED_ERROR)
                print(InputData._MINIMUM_ERROR % min_value)
            elif read > max_value:
                print(InputData._RED_ERROR)
                print(InputData._MAXIMUM_ERROR % max_value)
            else:
                is_input_out_of_range = False

        return read

    @staticmethod
    def read_float(message: str) -> float:
        """Reads a float input from the user.

        Params
        ------
        - message -> The message to display the user.

        Returns
        -------
        The float input by the user.
        """
        is_float: bool = False

        while not is_float:
            try:
                read = float(input(message))
                is_float = True
            except ValueError:
                print(InputData._RED_ERROR)
                print(InputData._FLOAT_FORMAT_ERROR)

        return read

    @staticmethod
    def read_float_with_minimum(message: str, min_value: float) -> float:
        """Reads a float input from the user with a minimum value constraint.

        Params
        ------
        - message -> The message to display the user.
        - min_value -> The minimum allowed value for the input.

        Returns
        -------
        The float input by the user that is greater than or equal to min_value.
        """
        is_input_out_of_range: bool = True

        while is_input_out_of_range:
            read: float = InputData.read_float(message)

            if read >= min_value:
                is_input_out_of_range = False
            else:
                print(InputData._RED_ERROR)
                print(InputData._MINIMUM_ERROR % min_value)

        return read

    @staticmethod
    def read_float_with_maximum(message: str, max_value: float) -> float:
        """Reads a float input from the user with a maximum value constraint.

        Params
        ------
        - message -> The message to display the user.
        - max_value -> The maximum allowed value for the input.

        Returns
        -------
        The float input by the user that is less than or equal to max_value.
        """
        is_input_out_of_range: bool = True

        while is_input_out_of_range:
            read: float = InputData.read_float(message)

            if read <= max_value:
                is_input_out_of_range = False
            else:
                print(InputData._RED_ERROR)
                print(InputData._MAXIMUM_ERROR % max_value)

        return read

    @staticmethod
    def read_float_between(message: str, min_value: float, max_value: float) -> float:
        """Reads a float input from the user with a minimum and maximum value constraint.

        Params
        ------
        - message -> The message to display the user.
        - min_value -> The minimum allowed value for the input.
        - max_value -> The maximum allowed value for the input.

        Returns
        -------
        The float input by the user that is greater than or equal to min_value and less than or
        equal to max_value.
        """
        is_input_out_of_range: bool = True

        while is_input_out_of_range:
            read: float = InputData.read_float(message)

            if read < min_value:
                print(InputData._RED_ERROR)
                print(InputData._MINIMUM_ERROR % min_value)
            elif read > max_value:
                print(InputData._RED_ERROR)
                print(InputData._MAXIMUM_ERROR % max_value)
            else:
                is_input_out_of_range = False

        return read
