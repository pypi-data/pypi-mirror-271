import re
import pyperclip
import markdown2
from datetime import datetime
from textblob import TextBlob
from .types import _str
from .txt_split_fnc import ProcessSplit
from markdownify import markdownify as md


def current_time():
    return f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"


def recursive_replacer(text: str, dic: dict) -> str:
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def clipboard(text: str):
    """
    Set the clipboard to the given text.
    """
    pyperclip.copy(text)


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


def remove_special_characters(text: str) -> str:
    """
    Remove special characters from the given text using regular expressions.
    """
    pattern = r"[^A-Za-z0-9\s,.\"'?!()\[\];:]"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def html_to_markdown(html: str) -> str:
    """Converts HTML to Markdown"""
    return md(html)


def markdown_to_html(markdown: str) -> str:
    """Converts Markdown to HTML"""
    return markdown2.markdown(markdown)
