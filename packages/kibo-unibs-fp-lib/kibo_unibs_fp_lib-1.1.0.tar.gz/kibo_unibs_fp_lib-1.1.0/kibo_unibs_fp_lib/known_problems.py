"""Module for the KnownProblems class"""


class KnownProblems:
    """
    This class has the implementation of some of the usual problems that you always forget and need
    to go watch the solution on StackOverflow even though you know you've already solved them.
    """

    _CONSTRUCTOR_ERROR: str = "This class is not instantiable!"
    _VALUES_ERROR: str = "Too few arguments were passed!"

    def __init__(self) -> None:
        """Prevents the instantiation of this class.

        Raises
        ------
        - NotImplementedError
        """
        raise NotImplementedError(KnownProblems._CONSTRUCTOR_ERROR)

    @staticmethod
    def _mcd(a: int, b: int) -> int:
        """Finds the MCD (Maximum Common Divider) between two integers.

        Params
        ------
        - a -> The first number to calculate the MCD.
        - b -> The second number to calculate the MCD.

        Returns
        -------
        An integer representing the MCD.
        """
        while a != 0 and b != 0:
            if a > b:
                a %= b
            else:
                b %= a

        return b if a == 0 else a

    @staticmethod
    def mcd(values: list[int]) -> int:
        """Finds the MCD (Maximum Common Divider) between a list of integers.

        Params
        ------
        - values -> The values used to find the MCD.

        Returns
        -------
        An integer representing the MCD between all the values.

        Raises
        ------
        - ValueError -> If less than two values are given.
        """
        if not values or len(values) < 2:
            raise ValueError(KnownProblems._VALUES_ERROR)

        mcd: int = values[0]

        for value in values[1:]:
            mcd = KnownProblems._mcd(mcd, value)

        return mcd

    @staticmethod
    def _mcm(a: int, b: int) -> int:
        """Finds the MCM (Minimum Common Multiplier) between two numbers.

        Params
        ------
        - a -> The first number to calculate the MCM.
        - b -> The second number to calculate the MCM.

        Returns
        -------
        An integer representing the MCM.
        """
        mcd: int = KnownProblems._mcd(a, b)

        return (a * b) // mcd

    @staticmethod
    def mcm(values: list[int]) -> int:
        """Finds the MCM (Minimum Common Multiplier) between a list of integers.

        Params
        ------
        - values -> The values used to find the MCM.

        Returns
        -------
        An integer representing the MCM between all the values.

        Raises
        ------
        - ValueError -> If less than two values are given.
        """
        if not values or len(values) < 2:
            raise ValueError(KnownProblems._VALUES_ERROR)

        mcm: int = values[0]

        for value in values[1:]:
            mcm = KnownProblems._mcm(mcm, value)

        return mcm

    @staticmethod
    def count_integer_digits(n: int) -> int:
        """Counts the number of digits of an integer.

        Params
        ------
        - n -> The number to calculate the digits.

        Returns
        -------
        An integer representing the number of digits of n.
        """
        return len(str(abs(n)))

    @staticmethod
    def count_decimal_digits(n: float) -> int:
        """Counts the number of decimal digits in a float.

        Params
        ------
        - n -> The number to calculate the decimal digits.

        Returns
        -------
        An integer representing the number of decimal digits of n.
        """
        splitted_number: list[str] = str(abs(n)).split(".")

        if len(splitted_number) < 2:
            return 0

        return len(splitted_number[1])
