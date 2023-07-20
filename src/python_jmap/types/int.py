"""JMAP integer types.

Spec: https://jmap.io/spec-core.html#the-int-and-uint-data-types
"""
from typing import Callable
from typing import Iterator
from typing import Type
from typing import TypeVar


def make_ge_validator(minimum: int) -> Callable[[int], int]:
    """Creates a type validated that ensures a value is greater-than-or-equal."""

    def validator(value: int) -> int:
        if value < minimum:
            raise ValueError()
        return value

    return validator


def make_le_validator(maximum: int) -> Callable[[int], int]:
    """Creates a type validated that ensures a value is less-than-or-equal."""

    def validator(value: int) -> int:
        if value > maximum:
            raise ValueError()
        return value

    return validator


_SelfT = TypeVar("_SelfT", bound="RangeInt")


class RangeInt(int):
    """A generic int subclass that allows setting a valid range of values."""

    minimum: int
    maximum: int

    def __new__(cls: Type[_SelfT], value: int) -> _SelfT:
        """A generic int subclass that allows setting a valid range of values."""
        for validator in cls.__get_validators__():
            validator(value)
        return super().__new__(cls, value)

    @classmethod
    def __get_validators__(cls: Type[_SelfT]) -> Iterator[Callable[[int], _SelfT]]:
        """Enumerates validators for this type."""
        # To avoid type: ignore here, you can use classmethod
        # instead or pass `cls` to make_ge_validator too
        yield make_ge_validator(cls.minimum)  # type: ignore
        yield make_le_validator(cls.maximum)  # type: ignore


class Int(RangeInt):
    """Annotated type for generating JMAP spec-compliant ints.

    Integer must in the range -2^53+1 to 2^53-1.

    Example:
    >>> x = Int(10)
    >>> print(x)
    10
    """

    minimum = -(2**53) + 1
    maximum = 2**53 - 1


class UInt(RangeInt):
    """Annotated type for generating JMAP spec-compliant uints.

    Integer where the value MUST be in the range 0 to 2^53-1.

    Example:
    >>> x = UInt(10)
    >>> print(x)
    10
    """

    minimum = 0
    maximum = 2**53 - 1
