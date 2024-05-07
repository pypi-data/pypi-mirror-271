# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

from operator import itemgetter

import pytest

from arkindex_export import Dataset, DatasetElement, Element
from dan.datasets.extract.arkindex import TRAIN_NAME
from dan.datasets.extract.db import (
    get_dataset_elements,
    get_elements,
    get_transcription_entities,
    get_transcriptions,
)


def test_get_dataset_elements(mock_database):
    """
    Assert dataset elements retrieval output against verified results
    """
    dataset_elements = get_dataset_elements(
        dataset=Dataset.select().get(),
        split=TRAIN_NAME,
    )

    # ID verification
    assert all(
        isinstance(dataset_element, DatasetElement)
        for dataset_element in dataset_elements
    )
    assert [dataset_element.element.id for dataset_element in dataset_elements] == [
        "train-page_1",
        "train-page_2",
    ]


def test_get_elements(mock_database):
    """
    Assert elements retrieval output against verified results
    """
    elements = get_elements(
        parent_id="train-page_1",
        element_type=["text_line"],
    )

    # ID verification
    assert all(isinstance(element, Element) for element in elements)
    assert [element.id for element in elements] == [
        "train-page_1-line_1",
        "train-page_1-line_2",
        "train-page_1-line_3",
        "train-page_1-line_4",
    ]


@pytest.mark.parametrize(
    "worker_versions",
    ([False], ["worker_version_id"], [], [False, "worker_version_id"]),
)
def test_get_transcriptions(worker_versions, mock_database):
    """
    Assert transcriptions retrieval output against verified results
    """
    element_id = "train-page_1-line_1"
    transcriptions = get_transcriptions(
        element_id=element_id,
        transcription_worker_versions=worker_versions,
    )

    expected_transcriptions = []
    if not worker_versions or False in worker_versions:
        expected_transcriptions.append(
            {
                "text": "Caillet  Maurice  28.9.06",
                "worker_version_id": None,
            }
        )

    if not worker_versions or "worker_version_id" in worker_versions:
        expected_transcriptions.append(
            {
                "text": "caillet  maurice  28.9.06",
                "worker_version_id": "worker_version_id",
            }
        )

    assert (
        sorted(
            [
                {
                    "text": transcription.text,
                    "worker_version_id": transcription.worker_version.id
                    if transcription.worker_version
                    else None,
                }
                for transcription in transcriptions
            ],
            key=itemgetter("text"),
        )
        == expected_transcriptions
    )


@pytest.mark.parametrize("worker_version", (False, "worker_version_id", None))
@pytest.mark.parametrize(
    "supported_types", (["surname"], ["surname", "firstname", "birthdate"])
)
def test_get_transcription_entities(worker_version, mock_database, supported_types):
    transcription_id = "train-page_1-line_1" + (worker_version or "")
    entities = get_transcription_entities(
        transcription_id=transcription_id,
        entity_worker_versions=[worker_version],
        supported_types=supported_types,
    )

    expected_entities = [
        {
            "name": "Caillet",
            "type": "surname",
            "offset": 0,
            "length": 7,
        },
        {
            "name": "Maurice",
            "type": "firstname",
            "offset": 9,
            "length": 7,
        },
        {
            "name": "28.9.06",
            "type": "birthdate",
            "offset": 18,
            "length": 7,
        },
    ]

    expected_entities = list(
        filter(lambda ent: ent["type"] in supported_types, expected_entities)
    )
    for entity in expected_entities:
        if worker_version:
            entity["name"] = entity["name"].lower()
        entity["worker_version"] = worker_version or None

    assert (
        sorted(
            entities,
            key=itemgetter("offset"),
        )
        == expected_entities
    )
