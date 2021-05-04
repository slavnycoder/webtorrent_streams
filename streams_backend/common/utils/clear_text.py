import re

RESTRICTED_CHARACTERS_PATTERN = re.compile(r'[\s\n\r\t]')
WHITESPACE_PATTERN = re.compile(r'[\s]{2,}')


def clean_text(text: str) -> str:
    text = RESTRICTED_CHARACTERS_PATTERN.sub(" ", text)
    text = WHITESPACE_PATTERN.sub(" ", text)
    return text.strip()
