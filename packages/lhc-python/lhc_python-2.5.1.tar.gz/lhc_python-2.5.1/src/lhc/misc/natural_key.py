import re

NATURAL_KEY_REGX = re.compile('(\d+)')


def natural_key(item):
    return [int(part) if part.isdigit() else part for part in NATURAL_KEY_REGX.split(item)]
