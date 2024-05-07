# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import itertools
import logging
import operator
import re
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Iterator, List

import sentencepiece as spm
from lxml.etree import Element, SubElement, tostring
from nltk import wordpunct_tokenize

from arkindex_export import TranscriptionEntity
from dan.utils import EntityType, LMTokenMapping

logger = logging.getLogger(__name__)

# Replace \t with regular space and consecutive spaces
TRIM_SPACE_REGEX = re.compile(r"[\t ]+")
TRIM_RETURN_REGEX = re.compile(r"[\r\n]+")

# Remove invalid characters to build valid XML tag name
SLUG_PATTERN = re.compile(r"[\W]+")

# Some characters are encoded in XML but we don't want them encoded in the end
ENCODING_MAP = {
    "&#13;": "\r",
    "&lt;": "<",
    "&gt;": ">",
    "&amp;": "&",
}


def normalize_linebreaks(text: str) -> str:
    """
    Remove begin/ending linebreaks.
    Replace \r with regular linebreak and consecutive linebreaks.
    :param text: Text to normalize.
    """
    return TRIM_RETURN_REGEX.sub("\n", text.strip())


def normalize_spaces(text: str) -> str:
    """
    Remove begin/ending spaces.
    Replace \t with regular space and consecutive spaces.
    :param text: Text to normalize.
    """
    return TRIM_SPACE_REGEX.sub(" ", text.strip())


def get_vocabulary(tokenized_text: List[str]) -> set[str]:
    """
    Compute set of vocabulary from tokenzied text.
    :param tokenized_text: List of tokenized text.
    """
    return sorted(set([token for doc in tokenized_text for token in doc.split()]))


@dataclass
class Tokenizer:
    """
    A multi-level tokenizer (char, subword, word), where the subword tokenizer is trained using sentencepiece.
    :param training_corpus: List of training text.
    :param outdir: Path to save the subword tokenizer.
    :param mapping: Mapping between displayed and encoded versions of special characters.
    :param tokens: Start and end tokens used to represent named entities.
    :param subword_vocab_size: Size of the vocabulary size to use to train the subword tokenizer.
    """

    training_corpus: List[str]
    charset: List[str]
    unknown_token: str
    outdir: Path
    mapping: LMTokenMapping
    tokens: EntityType | None = None
    subword_vocab_size: int = 1000
    sentencepiece_model: spm.SentencePieceProcessor = field(init=False)

    @property
    def prefix(self):
        return self.outdir / "subword_tokenizer"

    @property
    def ner_tokens(self) -> List[str] | Iterator[str]:
        if self.tokens is None:
            return []
        return itertools.chain(
            map(operator.attrgetter("start"), self.tokens.values()),
            filter(
                operator.truth, map(operator.attrgetter("end"), self.tokens.values())
            ),
        )

    @property
    def mapping_tokens(self) -> List[str]:
        return [token.encoded for token in self.mapping]

    @property
    def special_tokens(self) -> List[str]:
        return list(set(itertools.chain(self.mapping_tokens, self.ner_tokens)))

    def __post_init__(self) -> None:
        """
        Train a sentencepiece model on the training corpus.
        """
        # Write the corpus in a text file
        logger.info("Training a sentencepiece model for subword tokenization")
        with NamedTemporaryFile(dir=self.outdir, suffix=".txt", mode="w") as tmp:
            tmp.write("\n".join(self.training_corpus))
            tmp.flush()

            try:
                spm.SentencePieceTrainer.train(
                    input=tmp.name,
                    vocab_size=self.subword_vocab_size,
                    model_prefix=self.prefix,
                    user_defined_symbols=self.special_tokens,
                    minloglevel=1,
                )
            except Exception as e:
                logger.warning(
                    f"Failed to train a sentencepiece model for subword tokenization: {e} "
                    "Try again by editing the `--subword-vocab-size` parameter."
                )
                self.sentencepiece_model = None
                return

        # Load the model
        self.sentencepiece_model = spm.SentencePieceProcessor(
            model_file=str(self.prefix.with_suffix(".model"))
        )

    def subword_tokenize(self, text: str) -> str:
        """
        Tokenize into subwords. Sampling is disabled to ensure reproducibility.
        """
        tokens = self.sentencepiece_model.encode(text, out_type=str)
        return " ".join(map("".join, map(self.encode, tokens)))

    def word_tokenize(self, text: str) -> str:
        """
        Tokenize text into a string of space-separated words. Spaces (⎵) and NER tokens are considered as words.
        :param text: Text to be tokenized.
        """
        words = list(map("".join, map(self.encode, wordpunct_tokenize(text))))
        return " ".join(
            [
                word + f" {self.mapping.space.encoded}"
                if (i != len(words) - 1 and word not in self.ner_tokens)
                else word
                for i, word in enumerate(words)
            ]
        )

    def char_tokenize(self, text: str) -> str:
        """
        Tokenize text into a string of space-separated characters.
        :param text: Text to be tokenized.
        """
        return " ".join(
            [
                char if char in self.charset else self.unknown_token
                for char in self.encode(text)
            ]
        )

    def encode(self, text: List[str]) -> List[str]:
        """
        Encode special tokens.
        :param text: Text to be encoded.
        """
        return map(self.mapping.encode_token, text)


def slugify(text: str):
    """
    Replace invalid characters in text to underscores to use it as XML tag.
    """
    return SLUG_PATTERN.sub("_", text)


def get_translation_map(tokens: Dict[str, EntityType]) -> Dict[str, str] | None:
    if not tokens:
        return

    translation_map = {
        # Roots
        "<root>": "",
        "</root>": "",
    }
    # Tokens
    for entity_name, token_type in tokens.items():
        translation_map[f"<{slugify(entity_name)}>"] = token_type.start
        translation_map[f"</{slugify(entity_name)}>"] = token_type.end

    return translation_map


@dataclass
class XMLEntity:
    type: str
    name: str
    offset: int
    length: int
    worker_version: str
    children: List["XMLEntity"] = field(default_factory=list)

    @property
    def end(self) -> int:
        return self.offset + self.length

    def add_child(self, child: TranscriptionEntity):
        self.children.append(
            XMLEntity(
                type=child["type"],
                name=child["name"],
                offset=child["offset"] - self.offset,
                length=child["length"],
                worker_version=child["worker_version"],
            )
        )

    def insert(self, parent: Element):
        e = SubElement(parent, slugify(self.type))

        if not self.children:
            # No children
            e.text = self.name
            return

        offset = 0
        for child in self.children:
            # Add text before entity
            portion_before = self.name[offset : child.offset]
            offset += len(portion_before)
            if len(e):
                e[-1].tail = portion_before
            else:
                e.text = portion_before
            child.insert(e)
            offset += child.length

        # Text after the last entity
        e[-1].tail = self.name[self.children[-1].end : self.end]


def entities_to_xml(
    text: str,
    predictions: List[TranscriptionEntity],
    entity_separators: List[str] | None = None,
) -> str:
    """Represent the transcription and its entities in XML format. Each entity will be exposed with an XML tag.
    Its type will be used to name the tag.

    :param text: The text of the transcription
    :param predictions: The list of entities linked to the transcription
    :param entity_separators: When provided, instead of adding the text between entities, add one separator encountered in this text. The order is kept when looking for separators. Defaults to None
    :return: The representation of the transcription in XML format
    """

    def _find_separator(transcription: str) -> str:
        """
        Find the first entity separator in the provided transcription.
        """
        for separator in entity_separators:
            if separator in transcription:
                return separator
        return ""

    def add_portion(entity_offset: int | None = None):
        """
        Add the portion of text between entities either:
        - after the last node, if there is one before
        - on this node

        If we remove the text between entities, we keep one of the separators provided. Order matters.
        """
        portion = text[offset:entity_offset]

        if entity_separators:
            # Remove the text except the first entity_separator encountered
            portion = _find_separator(portion)

        if len(root):
            root[-1].tail = portion
        else:
            root.text = portion

    entities = iter(predictions)

    # This will mark the ending position of the first-level of entities
    last_end = None
    parsed: List[XMLEntity] = []

    for entity in entities:
        # First entity is not inside any other
        # If offset is too high, no nestation
        if not last_end or entity["offset"] >= last_end:
            parsed.append(XMLEntity(**entity))
            last_end = entity["offset"] + entity["length"]
            continue

        # Nested entity
        parsed[-1].add_child(entity)

    # XML export
    offset = 0
    root = Element("root")

    for entity in parsed:
        add_portion(entity.offset)

        entity.insert(root)

        offset = entity.end

    # Add text after last entity
    add_portion()

    # Cleanup separators introduced when text was removed
    if entity_separators:
        characters = "".join(entity_separators)
        root.text = root.text.lstrip(characters)
        # Strip trailing spaces on last child
        root[-1].tail = root[-1].tail.rstrip(characters)

    encoded_transcription = tostring(root, encoding="utf-8").decode()
    for pattern, repl in ENCODING_MAP.items():
        encoded_transcription = encoded_transcription.replace(pattern, repl)
    return encoded_transcription
