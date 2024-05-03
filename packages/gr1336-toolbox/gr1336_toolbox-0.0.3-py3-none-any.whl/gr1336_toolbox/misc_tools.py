import re
import pyperclip
from datetime import datetime
from .types_check import _array, _dict, _numpy
from typing import Any, TypeAlias, Literal, Callable




def np_list(content):
    if _numpy(content):
        return content.flatten().tolist()


def current_time():
    return f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"


def clipboard(text: str):
    """
    Set the clipboard to the given text.
    """
    pyperclip.copy(str(text))


def flatten_list(entry):
    """
    Example:
    ```py
    from grtoolbox.type_tools import flatten_list

    sample = ["test", [[[1]], [2]], 3, [{"last":4}]]
    results = flatten_list(sample)
    # results = ["test", 1, 2, 3, {"last": 4}]
    ```"""
    if _array(entry):
        return [item for sublist in entry for item in flatten_list(sublist)]
    return [entry] if entry is not None else []


def filter_list(entry: list | tuple, types: TypeAlias) -> list:
    if not _array(entry, allow_empty=False):
        return []
    return [x for x in entry if isinstance(x, types)]


def dict_to_list(
    entry: dict[str, Any],
    return_item: Literal["key", "content"] = "content",
) -> list:
    res = []
    assert _dict(entry), "the entry provided is not a valid dictionary. Received: {}".format(entry)
    if return_item == "content":
        return list(entry.values())
    return list(entry.keys())


def try_call(comp: Callable, verbose_exception: bool = False, **kwargs):
    try: return comp(**kwargs)
    except Exception as e:
        if verbose_exception: 
            print(e)


def recursive_replacer(text: str, dic: dict) -> str:
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def atoi(text: str):
    """Credits"""
    text = text.strip()
    return int(text) if text.isdigit() else text.lower()


def natural_keys(text):
    # From oobabooga
    return [atoi(c) for c in re.split(r"(\d+)", text)]
