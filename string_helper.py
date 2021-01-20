import re


def remove_special_chars_from_text(text):
    return re.sub('\W+', ' ', text)


def change_whitespaces_to_dash(text):
    return text.replace(' ', '-')
