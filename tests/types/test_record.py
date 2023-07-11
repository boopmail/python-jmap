"""Unit tests for JMAP base Record type."""

import pytest

from python_jmap.types.record import Record


class ChildRecord(Record):
    """An example child of Record."""


def test_child_instantiation() -> None:
    """It allows children of Record to be instantiated."""
    record = ChildRecord()
    assert isinstance(record, ChildRecord)


def test_base_instantiation() -> None:
    """It raises a TypeError when trying to instantiate Record directly."""
    with pytest.raises(TypeError):
        Record()
