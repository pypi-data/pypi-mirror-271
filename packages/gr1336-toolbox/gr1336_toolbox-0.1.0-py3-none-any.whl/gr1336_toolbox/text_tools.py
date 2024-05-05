import re
from .types_check import _str
from textblob import TextBlob
from .misc_tools import recursive_replacer
from .txt_split_fnc import ProcessSplit


def unescape(elem: str) -> str:
    assert _str(elem, True), "The input should be a valid string."
    return elem.encode().decode("unicode-escape", "ignore")


def blob_split(text: str) -> list[str]:
    return [x for x in TextBlob(text).raw_sentences]


def trimincompletesentence(txt: str) -> str:
    ln = len(txt)
    lastpunc = max(txt.rfind(". "), txt.rfind("!"), txt.rfind("?"))
    if lastpunc < ln - 1:
        if txt[lastpunc + 1] == '"':
            lastpunc = lastpunc + 1
    if lastpunc >= 0:
        txt = txt[: lastpunc + 1]
    return txt


def simplify_quotes(txt: str) -> str:
    assert _str(txt, True), f"The input '{txt}' is not a valid string"
    replacements = {
        "“": '"',
        "”": '"',
        "’": "'",
        "‘": "'",
        "`": "'",
    }
    return recursive_replacer(txt, replacements)


def clear_empty(text: str, clear_empty_lines: bool = True) -> str:
    """A better way to clear multiple empty lines than just using regex for it all.
    For example if you use:
    ```py
    text = "Here is my text.\nIt should only clear empty spaces and           not clear the lines out.\n\n\nThe lines should be preserved!"

    results = re.sub(r"\s+", " ", text)
    # results = "Here is my text. It should only clear empty spaces and not clear the lines out. The lines should be preserved!"
    ```
    As shown in the example above, the lines were all removed even if we just wanted to remove empty spaces.

    This function can also clear empty lines out, with may be useful. Its enabled by default.
    """
    return "\n".join(
        [
            re.sub(r"\s+", " ", x.strip())
            for x in text.splitlines()
            if not clear_empty_lines or x.strip()
        ]
    )


def txtsplit(
    text: str, desired_length=100, max_length=200, simplify_quote: bool = True
) -> list[str]:
    text = clear_empty(text, True)
    if simplify_quote:
        text = simplify_quotes(text)
    processor = ProcessSplit(text, desired_length, max_length)
    return processor.run()
