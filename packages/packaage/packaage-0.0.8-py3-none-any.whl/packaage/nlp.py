"""NLP related functions"""
from __future__ import absolute_import

import re

from unidecode import unidecode


def clean_text(text: str) -> str:
    """Converts characters to ascii and keeps only letters and numbers.

    Args:
        text (str): The text to be cleaned

    Returns:
        str: The clean text, stripped of any leading of trailing whitespaces
    """
    text = str(text) if text is not None else ''

    return re.sub('[^a-z0-9]+', ' ', unidecode(text.lower())).strip()
