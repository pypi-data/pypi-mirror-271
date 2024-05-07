# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import pickle
import re
from operator import methodcaller
from typing import NamedTuple

import pytest

from arkindex_export import (
    DatasetElement,
    Element,
    Transcription,
    TranscriptionEntity,
)
from dan.datasets.extract.arkindex import ArkindexExtractor
from dan.datasets.extract.db import get_transcription_entities
from dan.datasets.extract.exceptions import (
    NoTranscriptionError,
    UnknownTokenInText,
)
from dan.datasets.extract.utils import (
    EntityType,
    entities_to_xml,
    normalize_linebreaks,
    normalize_spaces,
)
from dan.utils import parse_tokens
from tests import FIXTURES

EXTRACTION_DATA_PATH = FIXTURES / "extraction"

TWO_SPACES_REGEX = re.compile(r" {2}")
ENTITY_TOKEN_SPACE = re.compile(r"[ⓢ|ⓕ|ⓑ] ")
TWO_SPACES_LM_REGEX = re.compile(r"▁ ▁")

# NamedTuple to mock actual database result
Entity = NamedTuple("Entity", offset=int, length=int, type=str, value=str)

TOKENS = {
    "P": EntityType(start="ⓟ", end="Ⓟ"),
    "D": EntityType(start="ⓓ", end="Ⓓ"),
    "N": EntityType(start="ⓝ", end="Ⓝ"),
    "I": EntityType(start="ⓘ", end="Ⓘ"),
}


def filter_tokens(keys):
    return {key: value for key, value in TOKENS.items() if key in keys}


@pytest.mark.parametrize(
    "text,trimmed",
    (
        ("no_spaces", "no_spaces"),
        (" beginning", "beginning"),
        ("ending ", "ending"),
        (" both ", "both"),
        ("    consecutive", "consecutive"),
        ("\ttab", "tab"),
        ("\t tab", "tab"),
        (" \ttab", "tab"),
        ("no|space", "no|space"),
    ),
)
def test_normalize_spaces(text, trimmed):
    assert normalize_spaces(text) == trimmed


@pytest.mark.parametrize(
    "text,trimmed",
    (
        ("no_linebreaks", "no_linebreaks"),
        ("\nbeginning", "beginning"),
        ("ending\n", "ending"),
        ("\nboth\n", "both"),
        ("\n\n\nconsecutive", "consecutive"),
        ("\rcarriage_return", "carriage_return"),
        ("\r\ncarriage_return+linebreak", "carriage_return+linebreak"),
        ("\n\r\r\n\ncarriage_return+linebreak", "carriage_return+linebreak"),
        ("no|linebreaks", "no|linebreaks"),
    ),
)
def test_normalize_linebreaks(text, trimmed):
    assert normalize_linebreaks(text) == trimmed


def test_process_element_unknown_token_in_text_error(mock_database, tmp_path):
    output = tmp_path / "extraction"
    arkindex_extractor = ArkindexExtractor(output=output)

    # Retrieve a dataset element and update its transcription with an invalid one
    dataset_element = DatasetElement.select().first()
    element = dataset_element.element
    Transcription.update({Transcription.text: "Is this text valid⁇"}).execute()

    with pytest.raises(
        UnknownTokenInText,
        match=re.escape(
            f"Unknown token found in the transcription text of element ({element.id})"
        ),
    ):
        arkindex_extractor.process_element(dataset_element, element)


@pytest.mark.parametrize(
    "load_entities,keep_spaces,transcription_entities_worker_version,expected_subword_language_corpus,subword_vocab_size",
    (
        (
            True,
            True,
            "worker_version_id",
            """▁ ⓢ c a i l l e t ▁ ⓕ m a u r i c e ▁ ⓑ 28. 9.0 6
▁ ⓢ re b ou l ▁ ⓕ j e a n ▁ ⓑ 30. 9.0 2
▁ ⓢ b a re y re ▁ ⓕ j e a n ▁ ⓑ 28. 3 . 1 1
▁ ⓢ r ou s s y ▁ ⓕ j e a n ▁ ⓑ 4 . 1 1 . 1 4
▁ ⓢ m a r i n ▁ ⓕ m a r c e l ▁ ⓑ 1 0 . 8 . 0 6
▁ ⓢ a m i c a l ▁ ⓕ e l o i ▁ ⓑ 1 1 . 1 0 . 0 4
▁ ⓢ b i r o s ▁ ⓕ m a e l ▁ ⓑ 30. 1 0 . 1 0""",
            40,
        ),
        (
            True,
            False,
            "worker_version_id",
            """▁ ⓢ c a i l l e t ▁ ⓕ m a u r i c e ▁ ⓑ 28. 9.0 6
▁ ⓢ re b ou l ▁ ⓕ j e a n ▁ ⓑ 30. 9.0 2
▁ ⓢ b a re y re ▁ ⓕ j e a n ▁ ⓑ 28. 3 . 1 1
▁ ⓢ r ou s s y ▁ ⓕ j e a n ▁ ⓑ 4 . 1 1 . 1 4
▁ ⓢ m a r i n ▁ ⓕ m a r c e l ▁ ⓑ 1 0 . 8 . 0 6
▁ ⓢ a m i c a l ▁ ⓕ e l o i ▁ ⓑ 1 1 . 1 0 . 0 4
▁ ⓢ b i r o s ▁ ⓕ m a e l ▁ ⓑ 30. 1 0 . 1 0""",
            40,
        ),
        (
            False,
            True,
            "worker_version_id",
            """▁ ca i l l e t ▁ ma u r i ce ▁ 28. 9.0 6
▁ re b o u l ▁ j e a n ▁ 30. 9.0 2
▁ b a re y re ▁ j e a n ▁ 28. 3 . 1 1
▁ r o u s s y ▁ j e a n ▁ 4 . 11.1 4
▁ ma r i n ▁ ma r ce l ▁ 10. 8 . 0 6
▁ a m i ca l ▁ el o i ▁ 11.1 0 . 0 4
▁ b i r o s ▁ ma el ▁ 30. 10. 1 0""",
            40,
        ),
        (
            False,
            False,
            "worker_version_id",
            """▁ ca i l l e t ▁ ma u r i ce ▁ 28. 9.0 6
▁ re b o u l ▁ j e a n ▁ 30. 9.0 2
▁ b a re y re ▁ j e a n ▁ 28. 3 . 1 1
▁ r o u s s y ▁ j e a n ▁ 4 . 11.1 4
▁ ma r i n ▁ ma r ce l ▁ 10. 8 . 0 6
▁ a m i ca l ▁ el o i ▁ 11.1 0 . 0 4
▁ b i r o s ▁ ma el ▁ 30. 10. 1 0""",
            40,
        ),
        (
            True,
            True,
            False,
            """▁ ⓢ C a i l l e t ▁ ⓕ M a u r i c e ▁ ⓑ 2 8 . 9 . 0 6
▁ ⓢ R e b o u l ▁ ⓕ J e a n ▁ ⓑ 3 0 . 9 . 0 2
▁ ⓢ B a r e y r e ▁ ⓕ J e a n ▁ ⓑ 2 8 . 3 . 1 1
▁ ⓢ R o u s s y ▁ ⓕ J e a n ▁ ⓑ 4 . 1 1 . 1 4
▁ ⓢ M a r i n ▁ ⓕ M a r c e l ▁ ⓑ 1 0 . 8 . 0 6
▁ ⓢ A m i c a l ▁ ⓕ E l o i ▁ ⓑ 1 1 . 1 0 . 0 4
▁ ⓢ B i r o s ▁ ⓕ M a e l ▁ ⓑ 3 0 . 1 0 . 1 0""",
            40,
        ),
        (
            True,
            True,
            False,
            """▁ ⓢ C a i l l e t ▁ ⓕ M a u ri ce ▁ ⓑ 28. 9.0 6
▁ ⓢ R e b ou l ▁ ⓕ J e a n ▁ ⓑ 30. 9.0 2
▁ ⓢ B a re y re ▁ ⓕ J e a n ▁ ⓑ 28. 3 . 1 1
▁ ⓢ R ou s s y ▁ ⓕ J e a n ▁ ⓑ 4 . 11.1 4
▁ ⓢ Mar i n ▁ ⓕ Mar ce l ▁ ⓑ 10. 8 . 0 6
▁ ⓢ A m ic a l ▁ ⓕ E l o i ▁ ⓑ 11.1 0 . 0 4
▁ ⓢ B i r o s ▁ ⓕ M a e l ▁ ⓑ 30. 10. 10""",
            55,
        ),
        (
            True,
            False,
            False,
            """▁ ⓢ C a i l l e t ▁ ⓕ M a u r i c e ▁ ⓑ 2 8 . 9 . 0 6
▁ ⓢ R e b o u l ▁ ⓕ J e a n ▁ ⓑ 3 0 . 9 . 0 2
▁ ⓢ B a r e y r e ▁ ⓕ J e a n ▁ ⓑ 2 8 . 3 . 1 1
▁ ⓢ R o u s s y ▁ ⓕ J e a n ▁ ⓑ 4 . 1 1 . 1 4
▁ ⓢ M a r i n ▁ ⓕ M a r c e l ▁ ⓑ 1 0 . 8 . 0 6
▁ ⓢ A m i c a l ▁ ⓕ E l o i ▁ ⓑ 1 1 . 1 0 . 0 4
▁ ⓢ B i r o s ▁ ⓕ M a e l ▁ ⓑ 3 0 . 1 0 . 1 0""",
            40,
        ),
        (
            False,
            True,
            False,
            """▁ C a i l l e t ▁ Ma u r i c e ▁ 28. 9.0 6
▁ R e b o u l ▁ J e a n ▁ 30. 9.0 2
▁ B a r e y r e ▁ J e a n ▁ 28. 3 . 1 1
▁ R o u s s y ▁ J e a n ▁ 4 . 1 1 . 1 4
▁ Ma r i n ▁ Ma r c e l ▁ 1 0 . 8 . 0 6
▁ A m i c a l ▁ E l o i ▁ 1 1 . 1 0 . 0 4
▁ B i r o s ▁ Ma e l ▁ 30. 1 0 . 1 0""",
            40,
        ),
        (
            False,
            False,
            False,
            """▁ C a i l l e t ▁ Ma u r i c e ▁ 28. 9.0 6
▁ R e b o u l ▁ J e a n ▁ 30. 9.0 2
▁ B a r e y r e ▁ J e a n ▁ 28. 3 . 1 1
▁ R o u s s y ▁ J e a n ▁ 4 . 1 1 . 1 4
▁ Ma r i n ▁ Ma r c e l ▁ 1 0 . 8 . 0 6
▁ A m i c a l ▁ E l o i ▁ 1 1 . 1 0 . 0 4
▁ B i r o s ▁ Ma e l ▁ 30. 1 0 . 1 0""",
            40,
        ),
    ),
)
def test_extract(
    load_entities,
    keep_spaces,
    transcription_entities_worker_version,
    split_content,
    mock_database,
    expected_subword_language_corpus,
    subword_vocab_size,
    tmp_path,
):
    output = tmp_path / "extraction"
    output.mkdir(parents=True, exist_ok=True)
    (output / "language_model").mkdir(parents=True, exist_ok=True)
    tokens_path = EXTRACTION_DATA_PATH / "tokens.yml"
    tokens = [
        token
        for entity_type in parse_tokens(tokens_path).values()
        for token in [entity_type.start, entity_type.end]
        if token
    ]

    extractor = ArkindexExtractor(
        dataset_ids=["dataset_id"],
        element_type=["text_line"],
        output=output,
        # Keep the whole text
        entity_separators=None,
        tokens=tokens_path if load_entities else None,
        transcription_worker_versions=[transcription_entities_worker_version],
        entity_worker_versions=[transcription_entities_worker_version]
        if load_entities
        else [],
        keep_spaces=keep_spaces,
        subword_vocab_size=subword_vocab_size,
    )
    extractor.run()

    expected_paths = [
        output / "charset.pkl",
        # Language resources
        output / "language_model" / "corpus_characters.txt",
        output / "language_model" / "corpus_subwords.txt",
        output / "language_model" / "corpus_words.txt",
        output / "language_model" / "lexicon_characters.txt",
        output / "language_model" / "lexicon_subwords.txt",
        output / "language_model" / "lexicon_words.txt",
        output / "language_model" / "subword_tokenizer.model",
        output / "language_model" / "subword_tokenizer.vocab",
        output / "language_model" / "tokens.txt",
        output / "split.json",
    ]
    assert sorted(filter(methodcaller("is_file"), output.rglob("*"))) == expected_paths

    # Check "split.json"
    # Transcriptions with worker version are in lowercase
    if transcription_entities_worker_version:
        for split in split_content:
            for element_id in split_content[split]:
                split_content[split][element_id]["text"] = split_content[split][
                    element_id
                ]["text"].lower()

    # If we do not load entities, remove tokens
    if not load_entities:
        token_translations = {ord(token): None for token in tokens}
        for split in split_content:
            for element_id in split_content[split]:
                split_content[split][element_id]["text"] = split_content[split][
                    element_id
                ]["text"].translate(token_translations)

    # Replace double spaces with regular space
    if not keep_spaces:
        for split in split_content:
            for element_id in split_content[split]:
                split_content[split][element_id]["text"] = TWO_SPACES_REGEX.sub(
                    " ", split_content[split][element_id]["text"]
                )

    assert json.loads((output / "split.json").read_text()) == split_content

    # Check "charset.pkl"
    expected_charset = set()
    for values in split_content["train"].values():
        expected_charset.update(set(values["text"]))

    if load_entities:
        expected_charset.update(tokens)
    expected_charset.add("⁇")
    assert set(pickle.loads((output / "charset.pkl").read_bytes())) == expected_charset

    # Check "language_corpus.txt"
    expected_char_language_corpus = """ⓢ C a i l l e t ▁ ▁ ⓕ M a u r i c e ▁ ▁ ⓑ 2 8 . 9 . 0 6
ⓢ R e b o u l ▁ ▁ ⓕ J e a n ▁ ▁ ⓑ 3 0 . 9 . 0 2
ⓢ B a r e y r e ▁ ▁ ⓕ J e a n ▁ ▁ ⓑ 2 8 . 3 . 1 1
ⓢ R o u s s y ▁ ▁ ⓕ J e a n ▁ ▁ ⓑ 4 . 1 1 . 1 4
ⓢ M a r i n ▁ ▁ ⓕ M a r c e l ▁ ▁ ⓑ 1 0 . 8 . 0 6
ⓢ A m i c a l ▁ ▁ ⓕ E l o i ▁ ▁ ⓑ 1 1 . 1 0 . 0 4
ⓢ B i r o s ▁ ▁ ⓕ M a e l ▁ ▁ ⓑ 3 0 . 1 0 . 1 0"""

    expected_word_language_corpus = """ⓢ Caillet ▁ ⓕ Maurice ▁ ⓑ 28 ▁ . ▁ 9 ▁ . ▁ 06
ⓢ Reboul ▁ ⓕ Jean ▁ ⓑ 30 ▁ . ▁ 9 ▁ . ▁ 02
ⓢ Bareyre ▁ ⓕ Jean ▁ ⓑ 28 ▁ . ▁ 3 ▁ . ▁ 11
ⓢ Roussy ▁ ⓕ Jean ▁ ⓑ 4 ▁ . ▁ 11 ▁ . ▁ 14
ⓢ Marin ▁ ⓕ Marcel ▁ ⓑ 10 ▁ . ▁ 8 ▁ . ▁ 06
ⓢ Amical ▁ ⓕ Eloi ▁ ⓑ 11 ▁ . ▁ 10 ▁ . ▁ 04
ⓢ Biros ▁ ⓕ Mael ▁ ⓑ 30 ▁ . ▁ 10 ▁ . ▁ 10"""

    # Transcriptions with worker version are in lowercase
    if transcription_entities_worker_version:
        expected_char_language_corpus = expected_char_language_corpus.lower()
        expected_word_language_corpus = expected_word_language_corpus.lower()
        expected_subword_language_corpus = expected_subword_language_corpus.lower()

    # If we do not load entities, remove tokens
    if not load_entities:
        token_translations = {f"{token} ": "" for token in tokens}
        expected_char_language_corpus = ENTITY_TOKEN_SPACE.sub(
            "", expected_char_language_corpus
        )
        expected_word_language_corpus = ENTITY_TOKEN_SPACE.sub(
            "", expected_word_language_corpus
        )
        expected_subword_language_corpus = ENTITY_TOKEN_SPACE.sub(
            "", expected_subword_language_corpus
        )
    # Replace double spaces with regular space
    if not keep_spaces:
        expected_char_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_char_language_corpus
        )
        expected_word_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_word_language_corpus
        )
        expected_subword_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_subword_language_corpus
        )

    assert (
        output / "language_model" / "corpus_characters.txt"
    ).read_text() == expected_char_language_corpus

    assert (
        output / "language_model" / "corpus_words.txt"
    ).read_text() == expected_word_language_corpus

    assert (
        output / "language_model" / "corpus_subwords.txt"
    ).read_text() == expected_subword_language_corpus

    # Check "language_tokens.txt"
    expected_language_tokens = [
        "▁" if t.isspace() else t for t in sorted(list(expected_charset))
    ]
    expected_language_tokens.append("◌")
    assert (output / "language_model" / "tokens.txt").read_text() == "\n".join(
        expected_language_tokens
    )

    # Check "language_lexicon.txt"
    expected_language_char_lexicon = [f"{t} {t}" for t in expected_language_tokens]
    assert (
        output / "language_model" / "lexicon_characters.txt"
    ).read_text() == "\n".join(expected_language_char_lexicon)

    word_vocab = set([word for word in expected_word_language_corpus.split()])
    expected_language_word_lexicon = [
        f"{word} {' '.join(word)}" for word in sorted(word_vocab)
    ]
    assert (output / "language_model" / "lexicon_words.txt").read_text() == "\n".join(
        expected_language_word_lexicon
    )

    subword_vocab = set(
        [subword for subword in expected_subword_language_corpus.split()]
    )
    expected_language_subword_lexicon = [
        f"{subword} {' '.join(subword)}" for subword in sorted(subword_vocab)
    ]
    assert (
        output / "language_model" / "lexicon_subwords.txt"
    ).read_text() == "\n".join(expected_language_subword_lexicon)


@pytest.mark.parametrize("allow_empty", (True, False))
def test_empty_transcription(allow_empty, mock_database):
    extractor = ArkindexExtractor(
        element_type=["text_line"],
        entity_separators=None,
        allow_empty=allow_empty,
    )
    element_no_transcription = Element(id="unknown")
    if allow_empty:
        assert extractor.extract_transcription(element_no_transcription) == ""
    else:
        with pytest.raises(NoTranscriptionError):
            extractor.extract_transcription(element_no_transcription)


@pytest.mark.parametrize("tokens", (None, EXTRACTION_DATA_PATH / "tokens.yml"))
def test_extract_transcription_no_translation(mock_database, tokens):
    extractor = ArkindexExtractor(
        element_type=["text_line"],
        entity_separators=None,
        tokens=tokens,
    )

    element = Element.get_by_id("test-page_1-line_1")
    # Deleting one of the two transcriptions from the element
    Transcription.get(
        Transcription.element == element,
        Transcription.worker_version_id == "worker_version_id",
    ).delete_instance(recursive=True)

    # Deleting all entities on the element remaining transcription while leaving the transcription intact
    if tokens:
        TranscriptionEntity.delete().where(
            TranscriptionEntity.transcription
            == Transcription.select().where(Transcription.element == element).get()
        ).execute()

    # Early return with only the element transcription text instead of a translation
    assert extractor.extract_transcription(element) == "Coupez  Bouis  7.12.14"


@pytest.mark.parametrize(
    "nestation, xml_output, separators",
    (
        # Non-nested
        (
            "non-nested-id",
            "<root>The <adj>great</adj> king <name>Charles</name> III has eaten \nwith <person>us</person>.</root>",
            None,
        ),
        # Non-nested no text between entities
        (
            "non-nested-id",
            "<root><adj>great</adj> <name>Charles</name>\n<person>us</person></root>",
            ["\n", " "],
        ),
        # Nested
        (
            "nested-id",
            "<root>The great king <fullname><name>Charles</name> III</fullname> has eaten \nwith <person>us</person>.</root>",
            None,
        ),
        # Nested no text between entities
        (
            "nested-id",
            "<root><fullname><name>Charles</name> III</fullname>\n<person>us</person></root>",
            ["\n", " "],
        ),
        # Special characters in entities
        (
            "special-chars-id",
            "<root>The <Arkindex_s_entity>great</Arkindex_s_entity> king <_Name_1_>Charles</_Name_1_> III has eaten \nwith <Person_>us</Person_>.</root>",
            None,
        ),
    ),
)
def test_entities_to_xml(mock_database, nestation, xml_output, separators):
    transcription = Transcription.get_by_id("tr-with-entities")
    assert (
        entities_to_xml(
            text=transcription.text,
            predictions=get_transcription_entities(
                transcription_id="tr-with-entities",
                entity_worker_versions=[nestation],
                supported_types=[
                    "name",
                    "fullname",
                    "person",
                    "adj",
                    "Arkindex's entity",
                    '"Name" (1)',
                    "Person /!\\",
                ],
            ),
            entity_separators=separators,
        )
        == xml_output
    )


@pytest.mark.parametrize(
    "supported_entities, xml_output, separators",
    (
        # <adj> missing, no text between entities
        (
            ["name", "person"],
            "<root><name>Charles</name>\n<person>us</person></root>",
            ["\n", " "],
        ),
        # <adj> missing, text between entities
        (
            ["name", "person"],
            "<root>The great king <name>Charles</name> III has eaten \nwith <person>us</person>.</root>",
            None,
        ),
    ),
)
def test_entities_to_xml_partial_entities(
    mock_database, supported_entities, xml_output, separators
):
    transcription = Transcription.get_by_id("tr-with-entities")
    assert (
        entities_to_xml(
            text=transcription.text,
            predictions=get_transcription_entities(
                transcription_id="tr-with-entities",
                entity_worker_versions=["non-nested-id"],
                supported_types=supported_entities,
            ),
            entity_separators=separators,
        )
        == xml_output
    )


@pytest.mark.parametrize(
    "transcription",
    (
        "Something\n",
        "Something\r",
        "Something\t",
        'Something"',
        "Something'",
        "Something<",
        "Something>",
        "Something&",
    ),
)
def test_entities_to_xml_no_encode(transcription):
    assert (
        entities_to_xml(
            text=transcription,
            # Empty queryset
            predictions=TranscriptionEntity.select().where(TranscriptionEntity.id == 0),
            entity_separators=None,
        )
        == f"<root>{transcription}</root>"
    )
