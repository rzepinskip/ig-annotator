from typing import List


def split_text_into_sentence(text: str) -> List[str]:
    return [text]


def remove_dots(sentence: str) -> str:
    return sentence.replace(".", "") + "."
