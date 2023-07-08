"""JMAP datetime types.

Spec: https://jmap.io/spec-core.html#the-date-and-utcdate-data-types
"""
from datetime import datetime
from datetime import timezone
from typing import Union
from typing import cast


class Date(str):
    """Helper type for generating JMAP spec-compliant dates.

    The time-secfrac MUST always be omitted if zero, and
    any letters in the string (e.g., “T” and “Z”) MUST be uppercase.
    For example, "2014-10-30T14:12:00+08:00".

    Example:
    >>> d = Date(datetime(2022, 10, 30, 14, 12, 0))
    >>> print(d)
    "2022-10-30T14:12:00"
    >>> d = Date(datetime(2022, 10, 30, 14, 12, 0, 500000))
    >>> print(d)
    "2022-10-30T14:12:00.500"
    """

    def __new__(cls, value: Union[datetime, str]) -> "Date":
        """Creates a new instance of the Date class."""
        if isinstance(value, datetime):
            date_str = value.strftime("%Y-%m-%dT%H:%M:%S")
            if value.microsecond > 0:
                date_str += f".{value.microsecond // 1000:03d}"
        elif isinstance(value, str):
            date_str = value
        else:
            raise TypeError("Value must be a datetime object or a string.")
        return super().__new__(cls, date_str)


class UTCDate(Date):
    """Helper type for generating JMAP spec-compliant UTC dates.

    For example, "2014-10-30T06:12:00Z".

    Example:
    >>> d = UTCDate(datetime(2022, 10, 30, 14, 12, 0, tzinfo=timezone.utc))
    >>> print(d)
    "2022-10-30T14:12:00Z"
    """

    def __new__(cls, value: datetime) -> "UTCDate":
        """Creates a new instance of the UTCDate class."""
        if not isinstance(value, datetime):
            raise TypeError("Value must be a datetime object.")
        if value.tzinfo is not timezone.utc:
            raise ValueError("DateTime object must be in UTC.")
        date_str = value.strftime("%Y-%m-%dT%H:%M:%S")
        if value.microsecond > 0:
            date_str += f".{value.microsecond // 1000:03d}"
        date_str += "Z"
        return cast(UTCDate, super().__new__(cls, date_str))
