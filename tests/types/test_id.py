"""Unit tests for JMAP Identifier type."""
import string

import pytest

from python_jmap.types.id import ID


def test_id_creation() -> None:
    """It returns the same string as passed in."""
    _id = ID("test_id")
    assert _id == "test_id"


def test_id_generation() -> None:
    """It returns a safe, valid ID if nothing is passed in."""
    _id = ID()
    assert ID.is_safe(_id)


def test_id_invalid_length() -> None:
    """It raises a ValueError if the string is too short or too long."""
    with pytest.raises(ValueError):
        ID("")

    with pytest.raises(ValueError):
        ID("a" * 256)


def test_id_invalid_characters() -> None:
    """It raises a ValueError if the string contains invalid characters."""
    with pytest.raises(ValueError):
        ID("test@id")


def test_generate_length() -> None:
    """It generates a safe, valid identifier of the provided length."""
    _id = ID.generate(10)
    assert len(_id) == 10


def test_generate_contents() -> None:
    """It generates a safe, valid identifier that only contains legal characters."""
    _id = ID.generate(10)

    for char in _id:
        assert char in (string.ascii_letters + string.digits + "_-")


def test_generate_uniqueness() -> None:
    """It generates a safe, valid identifier with sufficient entropy."""
    ids = {ID.generate(10) for _ in range(1000)}
    assert len(ids) == 1000


def test_is_safe() -> None:
    """It returns True if the valid is a safe, valid identifier."""
    # Safe ID: does not start with dash or digit, does not contain only digits,
    # does not contain "NIL", and does not differ only in case
    assert ID.is_safe("abc123") is True

    # Unsafe ID: starts with a digit
    assert ID.is_safe("1abc123") is False

    # Unsafe ID: starts with a dash
    assert ID.is_safe("-abc123") is False

    # Unsafe ID: contains only digits
    assert ID.is_safe("123456") is False

    # Unsafe ID: contains the sequence "NIL"
    assert ID.is_safe("abcNIL123") is False

    # Unsafe ID: differs only by case
    assert ID.is_safe("abc") is False
    assert ID.is_safe("ABC") is False


def test_validate_logs_warning_for_unsafe_id() -> None:
    """It logs a warning if the identifier is not safe."""
    unsafe_id = "abc"  # All lower case, no digit, hyphen or underscore

    with pytest.warns(UserWarning):
        ID.validate(unsafe_id)
