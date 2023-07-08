"""Unit tests for JMAP integer types."""
import pytest

from python_jmap.types.int import Int
from python_jmap.types.int import UnsignedInt


def test_int_edge_cases() -> None:
    """It should allow integers between -2^53+1 and 2^53-1 (inclusive)."""
    assert Int(-(2**53) + 1) == -(2**53) + 1
    assert Int(2**53 - 1) == 2**53 - 1
    assert Int(0) == 0


def test_int_invalid_values() -> None:
    """It should raise ValueError for numbers outside this range."""
    with pytest.raises(ValueError):
        Int(-(2**53))
    with pytest.raises(ValueError):
        Int(2**53)


def test_int_non_integer_input() -> None:
    """It should raise ValueError for non-integer inputs."""
    with pytest.raises(TypeError):
        Int("test")  # type: ignore


def test_unsigned_int_edge_cases() -> None:
    """It should allow integers between 0 and 2^53-1 (inclusive)."""
    assert UnsignedInt(0) == 0
    assert UnsignedInt(2**53 - 1) == 2**53 - 1


def test_unsigned_int_invalid_values() -> None:
    """It should raise ValueError for numbers outside this range."""
    with pytest.raises(ValueError):
        UnsignedInt(-1)
    with pytest.raises(ValueError):
        UnsignedInt(2**53)


def test_unsigned_int_non_integer_input() -> None:
    """It should raise ValueError for non-integer inputs."""
    with pytest.raises(TypeError):
        UnsignedInt("test")  # type: ignore
