"""JMAP Identifier type."""
import re
import secrets
import string
import warnings
from typing import Optional
from typing import Type


class ID(str):
    """JMAP Identifier type.

    Example:
    >>> id = ID("test_id")
    >>> print(id)
    test_id
    """

    def __new__(cls: Type["ID"], identifier: Optional[str] = None) -> "ID":
        """Creates a new instance of the ID class.

        Args:
            identifier (Optional[str]): A string to be used as the ID.

        Returns:
            ID: A new ID instance with the identifier transformed to uppercase.

        Raises:
            # noqa: DAR402 ValueError
            ValueError: If the identifier is not between 1 and 255 characters in length,
                        or if it contains characters other than alphanumeric, hyphen, and underscore.
        """
        if identifier is None:
            identifier = ID.generate(255)

        cls.validate(identifier)
        return str.__new__(cls, identifier)

    @staticmethod
    def validate(identifier: str) -> None:
        """Validate an identifier.

        The identifier must be between 1 and 255 characters in length and contain only
        alphanumeric, hyphen, and underscore characters.

        Args:
            identifier (str): The identifier to validate.

        Raises:
            ValueError: If the identifier is not valid.
        """
        if not 1 <= len(identifier) <= 255:
            raise ValueError(
                "Identifier must be between 1 and 255 characters in length"
            )

        if not re.match(r"^[A-Za-z0-9_-]*$", identifier):
            raise ValueError(
                "Identifier contains invalid characters. Only alphanumeric, hyphen, and underscore are allowed."
            )

        if not ID.is_safe(identifier):
            warnings.warn(
                "JMAP ID is not safe, to ensure backwards-compatibility your ID should meet the "
                + "criteria outlined in the specification: "
                + "https://jmap.io/spec-core.html#the-id-data-type",
                UserWarning,
                stacklevel=2,
            )

    @staticmethod
    def is_safe(id_str: str) -> bool:
        """Check if the ID is "safe".

        A safe ID does not start with a dash or digit, does not contain only digits,
        does not contain the sequence "NIL", and does not differ only in case.

        Args:
            id_str (str): The ID to check.

        Returns:
            bool: True if the ID is safe, False otherwise.
        """
        return not (
            id_str[0].isdigit()
            or id_str.startswith("-")
            or id_str.isdigit()
            or "NIL" in id_str.upper()
            or not any(char.isdigit() or char in "-_" for char in id_str)
        )

    @staticmethod
    def generate(length: int = 255) -> "ID":
        """Generate a safe ID.

        A safe ID starts with an alphabetical character, contains only alphanumeric, hyphen,
        and underscore characters, does not contain only digits, and does not contain the
        sequence "NIL".

        Args:
            length (int): The length of the ID to generate. Must be between 2 and 255. Defaults to 255.

        Returns:
            ID: A new ID instance that meets the criteria for a safe ID.
        """
        allowed_characters = string.ascii_letters + string.digits + "_-"

        while True:
            id_str = secrets.choice(string.ascii_letters) + "".join(
                secrets.choice(allowed_characters) for _ in range(length - 1)
            )
            if ID.is_safe(id_str):
                break

        return ID(id_str)
