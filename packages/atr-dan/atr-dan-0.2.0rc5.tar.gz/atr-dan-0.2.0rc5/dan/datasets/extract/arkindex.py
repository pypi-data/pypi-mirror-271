# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import logging
import pickle
import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from uuid import UUID

from tqdm import tqdm

from arkindex_export import Dataset, DatasetElement, Element, open_database
from dan.datasets.extract.db import (
    get_dataset_elements,
    get_elements,
    get_transcription_entities,
    get_transcriptions,
)
from dan.datasets.extract.exceptions import (
    NoTranscriptionError,
    ProcessingError,
    UnknownTokenInText,
)
from dan.datasets.extract.utils import (
    Tokenizer,
    entities_to_xml,
    get_translation_map,
    get_vocabulary,
    normalize_linebreaks,
    normalize_spaces,
)
from dan.utils import LMTokenMapping, parse_tokens

LANGUAGE_DIR = "language_model"  # Subpath to the language model directory.

TRAIN_NAME = "train"
VAL_NAME = "val"
TEST_NAME = "test"
SPLIT_NAMES = [TRAIN_NAME, VAL_NAME, TEST_NAME]

logger = logging.getLogger(__name__)


class ArkindexExtractor:
    """
    Extract data from Arkindex
    """

    def __init__(
        self,
        dataset_ids: List[UUID] | None = None,
        element_type: List[str] = [],
        output: Path | None = None,
        entity_separators: List[str] = ["\n", " "],
        unknown_token: str = "⁇",
        tokens: Path | None = None,
        transcription_worker_versions: List[str | bool] = [],
        entity_worker_versions: List[str | bool] = [],
        keep_spaces: bool = False,
        allow_empty: bool = False,
        subword_vocab_size: int = 1000,
    ) -> None:
        self.dataset_ids = dataset_ids
        self.element_type = element_type
        self.output = output
        self.entity_separators = entity_separators
        self.unknown_token = unknown_token
        self.tokens = parse_tokens(tokens) if tokens else {}
        self.transcription_worker_versions = transcription_worker_versions
        self.entity_worker_versions = entity_worker_versions
        self.allow_empty = allow_empty
        self.mapping = LMTokenMapping()
        self.keep_spaces = keep_spaces
        self.subword_vocab_size = subword_vocab_size

        self.data: Dict = defaultdict(dict)
        self.charset = set()
        self.language_corpus = defaultdict(list)
        self.language_tokens = []
        self.language_lexicon = defaultdict(list)

        # NER extraction
        self.translation_map: Dict[str, str] | None = get_translation_map(self.tokens)

    def translate(self, text: str):
        """
        Use translation map to replace XML tags to actual tokens
        """
        for pattern, repl in self.translation_map.items():
            text = text.replace(pattern, repl)
        return text

    def extract_transcription(self, element: Element):
        """
        Extract the element's transcription.
        If the entities are needed, they are added to the transcription using tokens.
        """
        transcriptions = get_transcriptions(
            element.id, self.transcription_worker_versions
        )
        if len(transcriptions) == 0:
            if self.allow_empty:
                return ""
            raise NoTranscriptionError(element.id)

        transcription = random.choice(transcriptions)
        stripped_text = transcription.text.strip()

        if not self.tokens:
            return stripped_text

        entities = get_transcription_entities(
            transcription.id,
            self.entity_worker_versions,
            supported_types=list(self.tokens),
        )

        if not entities.count():
            return stripped_text

        return self.translate(
            entities_to_xml(
                transcription.text, entities, entity_separators=self.entity_separators
            )
        )

    def format_text(self, text: str, charset: set | None = None):
        if not self.keep_spaces:
            text = normalize_spaces(text)
            text = normalize_linebreaks(text)

        # Replace unknown characters by the unknown token
        if charset is not None:
            unknown_charset = set(text) - charset
            text = text.translate(
                {
                    ord(unknown_char): self.unknown_token
                    for unknown_char in unknown_charset
                }
            )
        return text.strip()

    def process_element(self, dataset_parent: DatasetElement, element: Element):
        """
        Extract an element's data and save it to disk.
        The output path is directly related to the split of the element.
        """
        text = self.extract_transcription(element)

        if self.unknown_token in text:
            raise UnknownTokenInText(element_id=element.id)

        text = self.format_text(
            text,
            # Do not replace unknown characters in train split
            charset=self.charset if dataset_parent.set_name != TRAIN_NAME else None,
        )

        self.data[dataset_parent.set_name][element.id] = {
            "dataset_id": dataset_parent.dataset_id,
            "text": text,
            "image": {
                "iiif_url": element.image.url,
                "polygon": json.loads(element.polygon),
            },
        }

        self.charset = self.charset.union(set(text))

    def process_parent(self, pbar, dataset_parent: DatasetElement):
        """
        Extract data from a parent element.
        """
        parent = dataset_parent.element
        base_description = f"Extracting data from {parent.type} ({parent.id}) for split ({dataset_parent.set_name})"
        pbar.set_description(desc=base_description)
        if self.element_type == [parent.type]:
            try:
                self.process_element(dataset_parent, parent)
            except ProcessingError as e:
                logger.warning(f"Skipping {parent.id}: {str(e)}")
        # Extract children elements
        else:
            children = get_elements(
                parent.id,
                self.element_type,
            )

            nb_children = children.count()
            for idx, element in enumerate(children, start=1):
                # Update description to update the children processing progress
                pbar.set_description(desc=base_description + f" ({idx}/{nb_children})")
                try:
                    self.process_element(dataset_parent, element)
                except ProcessingError as e:
                    logger.warning(f"Skipping {element.id}: {str(e)}")

    def format_lm_files(self) -> None:
        """
        Convert charset to a LM-compatible charset. Ensure that special LM tokens do not appear in the charset.
        """
        logger.info("Preparing language resources")
        # Add unknown token to charset
        self.charset.add(self.unknown_token)

        # Build LM tokens
        for token in sorted(list(self.charset)):
            assert (
                token not in self.mapping.encode.values()
            ), f"Special token {token} is reserved for language modeling."
            self.language_tokens.append(
                self.mapping.encode[token]
            ) if token in self.mapping.encode else self.language_tokens.append(token)
        self.language_tokens.append(self.mapping.ctc.encoded)

        # Build LM corpus
        train_corpus = [
            values["text"].replace(
                self.mapping.linebreak.display, self.mapping.space.display
            )
            for values in self.data[TRAIN_NAME].values()
        ]

        tokenizer = Tokenizer(
            training_corpus=train_corpus,
            charset=self.language_tokens,
            unknown_token=self.unknown_token,
            outdir=self.output / "language_model",
            mapping=self.mapping,
            tokens=self.tokens,
            subword_vocab_size=self.subword_vocab_size,
        )

        if not tokenizer.sentencepiece_model:
            return

        for level, tokenize in (
            ("characters", tokenizer.char_tokenize),
            ("words", tokenizer.word_tokenize),
            ("subwords", tokenizer.subword_tokenize),
        ):
            self.language_corpus[level] = list(map(tokenize, train_corpus))

        # Build LM lexicon
        self.language_lexicon["characters"] = [
            f"{token} {token}" for token in self.language_tokens
        ]
        for level in ["words", "subwords"]:
            self.language_lexicon[level] = [
                f"{token} {tokenizer.char_tokenize(token)}"
                for token in get_vocabulary(self.language_corpus[level])
            ]

    def export(self):
        (self.output / "split.json").write_text(
            json.dumps(
                self.data,
                sort_keys=True,
                indent=4,
            )
        )
        for level in ["characters", "words", "subwords"]:
            (self.output / "language_model" / f"corpus_{level}.txt").write_text(
                "\n".join(self.language_corpus[level])
            )
            (self.output / "language_model" / f"lexicon_{level}.txt").write_text(
                "\n".join(self.language_lexicon[level])
            )
        (self.output / "language_model" / "tokens.txt").write_text(
            "\n".join(self.language_tokens)
        )
        (self.output / "charset.pkl").write_bytes(
            pickle.dumps(sorted(list(self.charset)))
        )

    def run(self):
        # Retrieve the Dataset and its splits from the cache
        for dataset_id in self.dataset_ids:
            dataset = Dataset.get_by_id(dataset_id)
            splits = dataset.sets.split(",")
            if not set(splits).issubset(set(SPLIT_NAMES)):
                logger.warning(
                    f'Dataset {dataset.name} ({dataset.id}) does not have "{TRAIN_NAME}", "{VAL_NAME}" and "{TEST_NAME}" steps'
                )
                continue

            # Extract the train set first to correctly build the `self.charset` variable
            splits.remove(TRAIN_NAME)
            splits.insert(0, TRAIN_NAME)

            # Iterate over the subsets to find the page images and labels.
            for split in splits:
                with tqdm(
                    get_dataset_elements(dataset, split),
                    desc=f"Extracting data from ({dataset_id}) for split ({split})",
                ) as pbar:
                    # Iterate over the pages to create splits at page level.
                    for parent in pbar:
                        self.process_parent(
                            pbar=pbar,
                            dataset_parent=parent,
                        )
                        # Progress bar updates
                        pbar.update()
                        pbar.refresh()

        if not self.data:
            raise Exception(
                "No data was extracted using the provided export database and parameters."
            )

        self.format_lm_files()
        self.export()


def run(
    database: Path,
    dataset_ids: List[UUID],
    element_type: List[str],
    output: Path,
    entity_separators: List[str],
    unknown_token: str,
    tokens: Path,
    transcription_worker_versions: List[str | bool],
    entity_worker_versions: List[str | bool],
    keep_spaces: bool,
    allow_empty: bool,
    subword_vocab_size: int,
):
    assert database.exists(), f"No file found @ {database}"
    open_database(path=database)

    # Create directories
    Path(output, LANGUAGE_DIR).mkdir(parents=True, exist_ok=True)

    ArkindexExtractor(
        dataset_ids=dataset_ids,
        element_type=element_type,
        output=output,
        entity_separators=entity_separators,
        unknown_token=unknown_token,
        tokens=tokens,
        transcription_worker_versions=transcription_worker_versions,
        entity_worker_versions=entity_worker_versions,
        keep_spaces=keep_spaces,
        allow_empty=allow_empty,
        subword_vocab_size=subword_vocab_size,
    ).run()
