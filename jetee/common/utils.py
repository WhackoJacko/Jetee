import re


def remove_special_characters(word):
    pattern = re.compile(u'[^\w]')
    word = pattern.sub(u'_', word)
    return word