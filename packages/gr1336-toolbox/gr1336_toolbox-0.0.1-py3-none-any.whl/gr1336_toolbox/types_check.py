from typing import Any, Callable
from pathlib import Path
from numpy import ndarray


def _int(entry: Any, check_string: bool = False):
    if check_string and _str(entry):
        try:
            int(entry)
            return True
        except:
            pass
    return isinstance(entry, int)


def _float(entry: Any, check_string: bool = False):
    if check_string and _str(entry):
        try:
            float(entry)
            return True
        except:
            pass
    return isinstance(entry, float)


def _number(entry: Any, check_string: bool = False):
    return any((_int(entry, check_string), _float(entry, check_string)))


def _numpy(entry: Any, allow_empty:bool=True) -> bool:
    return isinstance(entry, ndarray) and (allow_empty or (len(entry.flatten().tolist())))


def _str(
    entry: Any,
    allow_empty: bool = False,
) -> bool:
    if isinstance(entry, (str, Path)):
        entry = str(entry)
        if allow_empty:
            return bool(entry)
        return bool(entry.strip())
    return False


def _array(entry: Any, allow_empty: bool = False):
    if allow_empty or not isinstance(entry, (list, tuple)):
        return isinstance(entry, (list, tuple))
    return bool(entry)


def _dict(entry: Any, allow_empty: bool = False):
    if allow_empty or not isinstance(entry, dict):
        return isinstance(entry, dict)
    return bool(entry)


def _compare(arg1: Any | None, arg2: Any) -> Any:
    """
    arg1 if its not None or arg2.
    It considers fasely values from the first arg.
    Falsely are usualy: (0, "", {}, False, [])
    """
    return arg1 if arg1 is not None else arg2


def _path(entry) -> bool:
    if _str(entry):
        return Path(entry).exists()
    return False
