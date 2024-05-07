# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

import pytest

from dan.ocr.predict.attention import (
    Level,
    parse_delimiters,
    split_text_and_confidences,
)
from dan.utils import EntityType, parse_charset_pattern, parse_tokens_pattern


@pytest.mark.parametrize(
    (
        "text",
        "confidence",
        "level",
        "tokens",
        "split_text",
        "mean_confidences",
        "expected_offsets",
    ),
    [
        # level: char
        (
            "To <kyo>",
            [0.1, 0.2, 0.3, 0.4],
            Level.Char,
            None,
            ["T", "o", " ", "<kyo>"],
            [0.1, 0.2, 0.3, 0.4],
            [0, 0, 0, 0],
        ),
        # level: word
        (
            "Lo ve\nTokyo",
            [0.1, 0.1, 0.2, 0.3, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5],
            Level.Word,
            None,
            ["Lo", "ve", "Tokyo"],
            [0.1, 0.3, 0.5],
            [1, 1, 0],
        ),
        # level: line
        (
            "Love\nTokyo",
            [0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            Level.Line,
            None,
            ["Love", "Tokyo"],
            [0.1, 0.3],
            [1, 0],
        ),
        # level: NER (no end tokens)
        (
            "ⒶLove ⒷTokyo",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5],
            Level.NER,
            [EntityType(start="Ⓐ"), EntityType(start="Ⓑ")],
            ["ⒶLove ", "ⒷTokyo"],
            [0.2, 0.48],
            [0, 0],
        ),
        # level: NER (with end tokens)
        (
            "ⓐLoveⒶ ⓑTokyoⒷ",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7],
            Level.NER,
            [EntityType(start="ⓐ", end="Ⓐ"), EntityType(start="ⓑ", end="Ⓑ")],
            ["ⓐLoveⒶ", "ⓑTokyoⒷ"],
            [0.2, 0.6],
            [1, 0],
        ),
        # level: NER (no end tokens, no space)
        (
            "ⒶLoveⒷTokyo",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4],
            Level.NER,
            [EntityType(start="Ⓐ"), EntityType(start="Ⓑ")],
            ["ⒶLove", "ⒷTokyo"],
            [0.18, 0.38],
            [0, 0],
        ),
        # level: NER (with end tokens, no space)
        (
            "ⓐLoveⒶⓑTokyoⒷ",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6],
            Level.NER,
            [EntityType(start="ⓐ", end="Ⓐ"), EntityType(start="ⓑ", end="Ⓑ")],
            ["ⓐLoveⒶ", "ⓑTokyoⒷ"],
            [0.2, 0.5],
            [0, 0],
        ),
    ],
)
def test_split_text_and_confidences(
    text: str,
    confidence: list[float],
    level: Level,
    tokens: list[EntityType] | None,
    split_text: list[str],
    mean_confidences: list[list[float]],
    expected_offsets: list[int],
):
    # Full charset
    charset = [
        # alphabet
        "T",
        "o",
        "L",
        "v",
        "e",
        "k",
        "y",
        # Entities
        "ⓐ",
        "Ⓐ",
        "ⓑ",
        "Ⓑ",
        # Special
        "<kyo>",
        # Punctuation
        " ",
    ]

    texts, averages, offsets = split_text_and_confidences(
        text=text,
        confidences=confidence,
        level=level,
        char_separators=parse_charset_pattern(charset),
        word_separators=parse_delimiters([" ", "\n"]),
        line_separators=parse_delimiters(["\n"]),
        tokens_separators=parse_tokens_pattern(tokens) if tokens else None,
    )

    assert texts == split_text
    assert averages == mean_confidences
    assert offsets == expected_offsets
