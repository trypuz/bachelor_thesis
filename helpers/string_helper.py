import re


def remove_extra_whitespaces(text):
    return re.sub(r'\s+', ' ', text)
