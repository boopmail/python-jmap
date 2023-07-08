"""Unit tests for JMAP Identifier type."""
import string

import pytest

from python_jmap.types.id import ID


def test_id_creation() -> None:
    """It returns the same string as passed in."""
    _id = ID("test_id")
    assert _id == "test_id"


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


def test_generate_safe_id_length() -> None:
    """It generates a safe, valid identifier of the provided length."""
    _id = ID.generate_safe_id(10)
    assert len(_id) == 10


def test_generate_safe_id_contents() -> None:
    """It generates a safe, valid identifier that only contains legal characters."""
    _id = ID.generate_safe_id(10)

    for char in _id:
        assert char in (string.ascii_letters + string.digits + "_-")


def test_generate_safe_id_uniqueness() -> None:
    """It generates a safe, valid identifier with sufficient entropy."""
    ids = {ID.generate_safe_id(10) for _ in range(1000)}
    assert len(ids) == 1000


def test_is_safe_id() -> None:
    """It returns True if the valid is a safe, valid identifier."""
    # W0212:protected-access
    assert not ID._is_safe_id("123abc")
    assert not ID._is_safe_id("-abc123")
    assert not ID._is_safe_id("123456")
    assert not ID._is_safe_id("abcNIL123")
    assert not ID._is_safe_id("abc")
    assert ID._is_safe_id("abc123")
