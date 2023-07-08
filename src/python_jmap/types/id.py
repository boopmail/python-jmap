"""JMAP Identifier type."""
import re
import secrets
import string
from typing import Type


class ID(str):
    """JMAP Identifier type.

    Example:
    >>> id = ID("test_id")
    >>> print(id)
    test_id
    """

    def __new__(cls: Type["ID"], identifier: str) -> "ID":
        """Creates a new instance of the ID class.

        Args:
            identifier (str): A string to be used as the ID.

        Returns:
            ID: A new ID instance with the identifier transformed to uppercase.

        Raises:
            ValueError: If the identifier is not between 1 and 255 characters in length,
                        or if it contains characters other than alphanumeric, hyphen, and underscore.
        """
        cls._validate(identifier)
        return str.__new__(cls, identifier)

    @staticmethod
    def _validate(identifier: str) -> None:
        """Validate the identifier.

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

        # Match only the allowed characters
        if not re.match(r"^[A-Za-z0-9_-]*$", identifier):
            raise ValueError(
                "Identifier contains invalid characters. Only alphanumeric, hyphen, and underscore are allowed."
            )

    @staticmethod
    def _is_safe_id(id_str: str) -> bool:
        """Check if the ID is safe.

        A safe ID does not start with a dash or digit, does not contain only digits,
        does not contain the sequence "NIL", and does not have differing only in case.

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
            or id_str.lower() in {id_str, id_str.upper()}
        )

    @staticmethod
    def generate_safe_id(length: int = 255) -> "ID":
        """Generate a safe ID.

        A safe ID starts with an alphabetical character, contains only alphanumeric, hyphen,
        and underscore characters, does not contain only digits, and does not contain the
        sequence "NIL".

        Args:
            length (int, optional): The length of the ID to generate. Must be between 2 and 255. Defaults to 255.

        Returns:
            ID: A new ID instance that meets the criteria for a safe ID.

        Raises:
            ValueError: If the requested length is not between 2 and 255 characters.
        """
        if length < 2 or length > 255:
            raise ValueError("Length must be between 2 and 255 characters")

        # Create a list of allowed characters
        allowed_characters = string.ascii_letters + string.digits + "_-"

        # Generate a random ID, avoiding IDs that are not safe
        while True:
            id_str = secrets.choice(string.ascii_letters) + "".join(
                secrets.choice(allowed_characters) for _ in range(length - 1)
            )
            if ID._is_safe_id(id_str):
                break

        return ID(id_str)
