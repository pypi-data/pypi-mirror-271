from .types_check import _str
from textblob import TextBlob

def unescape(elem: str) -> str:
    assert _str(elem, True), "The input should be a valid string."
    return elem.encode().decode("unicode-escape", "ignore")

def blob_split(text: str) -> list[str]:
    return [x for x in TextBlob(text).raw_sentences]

def trimincompletesentence(txt: str) -> str:
    """Idea from KoboldAI"""
    # Cache length of text
    ln = len(txt)
    # Find last instance of punctuation (Borrowed from Clover-Edition by cloveranon)
    lastpunc = max(txt.rfind(". "), txt.rfind("!"), txt.rfind("?"))
    # Is this the end of a quote?
    if lastpunc < ln - 1:
        if txt[lastpunc + 1] == '"':
            lastpunc = lastpunc + 1
    if lastpunc >= 0:
        txt = txt[: lastpunc + 1]
    return txt

def simplify_quotes(txt:str) -> str:
    """Idea from kobold"""
    assert _str(txt, True), f"The input '{txt}' is not a valid string"
    replacements = {
        "“": '"',
        "”": '"',
        "’": "'",
        "‘": "'",
        "`": "'",
    }
    for key, value in replacements.items():
        txt = txt.replace(key, value)
    return txt
