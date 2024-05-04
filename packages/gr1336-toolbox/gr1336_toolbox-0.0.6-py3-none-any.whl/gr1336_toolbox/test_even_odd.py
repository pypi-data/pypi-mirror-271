import sys
from time import sleep

from textblob import TextBlob


def split_quotations(text: str):
    results = []
    current = ""
    quotations = text.count('"')
    if quotations > 0:
        for char in text:
            if char == "\n":
                results.append("\n")
            elif char == '"':
                if not current:
                    current = char
                elif current.count('"') % 2 == 0:
                    results.append(current)
                    current = char
                else:
                    current += char
                    results.append(current)
                    current = ""
            else:
                current += char
    else:
        return [text]
    if current and current.count('"') == 0:
        results.append(current)
    return results


def text_spliter(text: str):
    text: list[str] = [x for x in text.replace("\n\n\n", "\n\n").splitlines()]
    preprocess = split_quotations("\n".join(text))
    response = []
    for entry in preprocess:
        if entry.find('"') == -1:
            if entry == "\n":
                response.append(entry)
            else:
                response.extend([x for x in TextBlob(entry).raw_sentences])
        else:
            response.append(entry)

    if len(response) > 1:
        last_text: str = response[-1]
        if last_text.find('"') != -1:
            pass
        elif not last_text.endswith((".", "!", "?")):
            response.pop()
    return response


def split_sentences(text):
    blob = TextBlob(text).raw_sentences
    joined_sentences = []

    # Check if a quotation is not completed and join sentences accordingly
    inquote = False
    for i, sentence in enumerate(blob):
        num_quotes = sentence.count('"')
        if num_quotes % 2 != 0:
            inquote = True
        if inquote:
            if i + 1 < len(blob):
                next_sentence = blob[i + 1]
                sentence += " " + next_sentence
                inquote = False
        joined_sentences.append(sentence)
    if len(joined_sentences) > 1:
        if not joined_sentences[-1].endswith((".", "?", "!", '"')):
            joined_sentences.pop()
    return joined_sentences


[
    "Alexander looked at the knights, his eyes filled with determination.",
    '"I\'m not a traitor," he said, his voice shaking.',
    "Killbride's eyes twinkled with amusement and 3.33 he cocked his head to one side.",
    '"No? Then what were you doing last night, my lord?',
    "Then what were you doing last night, my lord?",
    'Or should I say, what you failed to do." Alexander frowned, knowing he had indeed done nothing.',
    "Alexander frowned, knowing he had indeed done nothing.",
    '"Keep silent!"',
    "Snivel cried, stamping his foot on the ground.",
    "\"You'll get us all killed. I think Lord Kilbride's taking a rather... unconventional approach.\"",
    "I think Lord Kilbride's taking a rather... unconventional approach.\" Lady Yennen gasped in surprise and frowned at her cousin.",
    "Lady Yennen gasped in surprise and frowned at her cousin.",
    '"Snivel, that\'s not like you."',
]

text__ = """Alexander looked at the knights, his eyes filled with determination. "I'm not a traitor," he said, his voice shaking. 

Killbride's eyes twinkled with amusement and 3.33 he cocked his head to one side. "No? Then what were you doing last night, my lord? Or should I say, what you failed to do."

Alexander frowned, knowing he had indeed done nothing. "Keep silent!" Snivel cried, stamping his foot on the ground. "You'll get us all killed. I think Lord Kilbride's taking a rather... unconventional approach."

Lady Yennen gasped in surprise and frowned at her cousin."Snivel, that's not like you."

Snivel pointed at Alexander"""

# tx = text_spliter(text__)
# tx = [x for x in TextBlob(text__).raw_sentences]
tx = split_sentences(text__)
print(tx)
f_text = ""
# for _res in tx:
#     if len(f_text) > 1 and f_text[-2:] != "\n":
#         f_text += " "  + _res
#     else:
#         f_text += _res
print()
print()
print(" ".join(tx))


____ = [
    "Alexander looked at the knights, his eyes filled with determination.",
    '"I\'m not a traitor,"',
    "\n",
    "\n",
    "he said, his voice shaking.Killbride's eyes twinkled with amusement and he cocked his head to one side.",
    '"No? Then what were you doing last night, my lord? Or should I say, what you failed to do."',
    "\n",
    "\n",
    "Alexander frowned, knowing he had indeed done nothing.",
    '"Keep silent!"',
    "Snivel cried, stamping his foot on the ground.",
    "\"You'll get us all killed. I think Lord Kilbride's taking a rather... unconventional approach.\"",
    "\n",
    "\n",
    "Lady Yennen gasped in surprise and frowned at her cousin.",
    '"Snivel, that\'s not like you."',
    "\n",
    "\n",
]

# print(list(text__))
