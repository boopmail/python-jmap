"""Unit tests for JMAP datetime types."""
from datetime import datetime
from datetime import timezone

import pytest

from python_jmap.types.date import Date
from python_jmap.types.date import UTCDate


def test_date_creation() -> None:
    """It should create a valid Date object from a datetime."""
    d = datetime(2022, 10, 30, 14, 12, 0)
    assert Date(d) == "2022-10-30T14:12:00"  # Removed 'Z'


def test_date_with_microseconds() -> None:
    """It should include fractional seconds in the output when they are non-zero."""
    d = datetime(2022, 10, 30, 14, 12, 0, 500000)
    assert Date(d) == "2022-10-30T14:12:00.500"  # Removed 'Z'


def test_date_with_invalid_input() -> None:
    """It should raise TypeError when created with non-datetime input."""
    with pytest.raises(TypeError):
        Date(23434556567)  # type: ignore


def test_utc_date_creation() -> None:
    """It should create a valid UTCDate object from a UTC datetime."""
    d = datetime(2022, 10, 30, 14, 12, 0, tzinfo=timezone.utc)
    assert UTCDate(d) == "2022-10-30T14:12:00Z"


def test_utc_date_with_non_utc_datetime() -> None:
    """It should raise ValueError when created with a non-UTC datetime."""
    d = datetime(2022, 10, 30, 14, 12, 0)
    with pytest.raises(ValueError):
        UTCDate(d)  # Non-UTC datetime


def test_utc_date_with_invalid_input() -> None:
    """It should raise TypeError when created with non-datetime input."""
    with pytest.raises(TypeError):
        UTCDate(23434556567)  # type: ignore


def test_utc_date_with_microseconds() -> None:
    """It should include fractional seconds in the output when they are non-zero."""
    d = datetime(2022, 10, 30, 14, 12, 0, 500000, tzinfo=timezone.utc)
    assert UTCDate(d) == "2022-10-30T14:12:00.500Z"
