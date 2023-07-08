"""JMAP integer types.

Spec: https://jmap.io/spec-core.html#the-int-and-unsignedint-data-types
"""
from typing import cast


class Int(int):
    """Integer in the range -2^53+1 to 2^53-1.

    Example:
    >>> x = Int(10)
    >>> print(x)
    10
    """

    def __new__(cls, value: int) -> "Int":
        """Creates a new instance of the Int class."""
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (-(2**53) + 1 <= value <= 2**53 - 1):
            raise ValueError(
                "Value not within acceptable range (-2^53+1 <= value <= 2^53-1)"
            )
        return super().__new__(cls, value)


class UnsignedInt(Int):
    """Integer where the value MUST be in the range 0 to 2^53-1.

    Example:
    >>> x = UnsignedInt(10)
    >>> print(x)
    10
    """

    def __new__(cls, value: int) -> "UnsignedInt":
        """Creates a new instance of the UnsignedInt class."""
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (0 <= value <= 2**53 - 1):
            raise ValueError("Value not within acceptable range (0 <= value <= 2^53-1)")
        return cast(UnsignedInt, super().__new__(cls, value))
