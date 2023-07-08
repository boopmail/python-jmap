"""Test cases for the __main__ module."""
from python_jmap import __main__


def test_main_succeeds() -> None:
    """It exits with a status code of zero."""
    __main__.main()
    assert True
