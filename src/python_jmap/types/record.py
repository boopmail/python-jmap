"""JMAP base Record type."""

from typing import Any
from typing import Dict
from typing import List
from typing import Type


class Record:
    """JMAP base Record type."""

    def __new__(
        cls: Type["Record"], *args: List[Any], **kwargs: Dict[str, Any]
    ) -> "Record":
        """Creates a new instance of the Record class."""
        if cls is Record:
            raise TypeError(f"Only children of {cls.__name__!r} may be instantiated.")
        return object.__new__(cls, *args, **kwargs)
