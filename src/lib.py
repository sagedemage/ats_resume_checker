"""
Library Module for the Words and Phrases classes
for storing results related to most common terms
"""

from typing import Any


class Words:
    def __init__(
        self, missing_words: list, most_common_words: list[tuple[Any, int]]
    ):
        self.missing = missing_words
        self.most_common = most_common_words


class Phrases:
    def __init__(
        self, missing_phrases: list, most_common_phrases: list[tuple[Any, int]]
    ):
        self.missing = missing_phrases
        self.most_common = most_common_phrases
