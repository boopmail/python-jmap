"""JMAP integer types.

Spec: https://jmap.io/spec-core.html#the-int-and-uint-data-types
"""
from typing import cast


class Int(int):
    """Helper type for generating JMAP spec-compliant ints.

    Integer must in the range -2^53+1 to 2^53-1.

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


class UInt(Int):
    """Helper type for generating JMAP spec-compliant uints.

    Integer where the value MUST be in the range 0 to 2^53-1.

    Example:
    >>> x = UInt(10)
    >>> print(x)
    10
    """

    def __new__(cls, value: int) -> "UInt":
        """Creates a new instance of the UInt class."""
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (0 <= value <= 2**53 - 1):
            raise ValueError("Value not within acceptable range (0 <= value <= 2^53-1)")
        return cast(UInt, super().__new__(cls, value))
