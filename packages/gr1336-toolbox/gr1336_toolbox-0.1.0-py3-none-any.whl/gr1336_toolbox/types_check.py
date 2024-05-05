from pathlib import Path
from numpy import ndarray
from typing import Any


def _int(entry: Any, check_string: bool = False) -> bool:
    """Checks if a number is a valid integer.

    Args:
        entry (Any): The item to be check if is a valid integer
        check_string (bool, optional): To check strings to see if its a possible number. Defaults to False.

    Returns:
        bool: True if its a True integer otherwise False.
    """
    if check_string and _str(entry):
        return entry.isdigit()
    return isinstance(entry, int)


def _float(entry: Any, check_string: bool = False) -> bool:
    """
    Checks if the entry provided is a valid float. It can check if a string can be converted to float if check_string is True.

    Args:
        entry (Any): The value to be checked.
        check_string (bool, optional): If True, it will check if the value can be converted to float.

    Returns:
        bool: If True, means that is a valid float otherwise false.
    """
    # I'm not much certain
    if check_string and _str(entry):
        # While in most cases '.' is the decimal separator,
        # in some rare cases ',' is used as decimal separator.
        separator = [",", "."] if "." in str(1.1) else [".", ","]
        entry.replace(separator[0], separator[1])
        try:
            float(entry)
            return True
        except:
            return False
    return isinstance(entry, float)


def _number(entry: Any, check_string: bool = False) -> bool:
    """Check if the entry is a number (being either a int or float). It also check if in case its a string (and check_string is True) if its a valid number if converted.

    Args:
        entry (Any): The value to be checked.
        check_string (bool, optional): If True will consider strings to possible be non-converted numbers. Defaults to False.

    Returns:
        bool: True if the value is either a float or a integer, otherwise False.
    """
    return _int(entry, check_string) or _float(entry, check_string)


def _numpy(entry: Any, allow_empty: bool = True) -> bool:
    return isinstance(entry, ndarray) and (
        allow_empty or bool(len(entry.flatten().tolist()))
    )


def _str(
    entry: Any,
    allow_empty: bool = False,
) -> bool:
    """Check if a value is a string or Path item,
    and (if allow_empty is False) checks if the string is empty or not(removing white spaces)
    """
    return isinstance(entry, (str, Path)) and (allow_empty or bool(str(entry).strip()))


def _array(entry: Any, allow_empty: bool = False):
    """Checks if the entry is either a list or tuple, it also check if its empty if allow_empty is False.

    Args:
        entry (Any): Value to be analised.
        allow_empty (bool, optional): If True will allow empty arrays to be returned as True. Defaults to False.

    Returns:
        bool: If True the value is a valid (non-empty if allow_empty is False else it returns true just for being a list or tuple).
    """
    return isinstance(entry, (list, tuple)) and (allow_empty or bool(entry))


def _dict(entry: Any, allow_empty: bool = False) -> bool:
    """Check if the provided entry is a valid dictionary and if it has content or not (if allow_empty is False).

    Args:
        entry (Any): The value to be checked if its True.
        allow_empty (bool, optional): If True it allow empty dictionaries to be evaluated, otherwise it requires it to be a dictionary and have at least some content there. Defaults to False.

    Returns:
        bool: True if valid dictionary and (if allow_empty is False) if it has some content in it.
    """
    return isinstance(entry, dict) and (allow_empty or bool(entry))


def _compare(arg1: Any | None, arg2: Any) -> Any:
    """
    arg1 if its not None or arg2.

    Useful to allow a different aproach than 'or' operator in strings, for example:

    Consider that the arguments as:
    ```py
    arg1 = 0
    arg2 = 3
    ```
    If using or operator directly the following would happen:

    ```python
    results = arg1 or arg2
    # results = arg2 (3)
    ```
    It checks for Falsely data in the first item, but sometimes that value would be valid even if falsely like: `0`, `""`, `[]`, `{}`, `()` and `False`.

    So, it was made to check if the first value is None or non-None if None it uses the arg2, otherwise it returns the arg1 even if falsely.

    example:
    ```
    from gr1336_toolbox import _compare
    results = _compare(arg1, arg2)
    # results = arg1 (0)
    ```

    """
    return arg1 if arg1 is not None else arg2


def _path(entry: str | Path) -> bool:
    """Checks if `entry` is an existent path"""
    return Path(entry).exists() if _str(entry) else False
