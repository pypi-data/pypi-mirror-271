# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from typing import List

from arkindex_export import Image
from arkindex_export.models import (
    Dataset,
    DatasetElement,
    Element,
    Entity,
    EntityType,
    Transcription,
    TranscriptionEntity,
)
from arkindex_export.queries import list_children


def get_dataset_elements(
    dataset: Dataset,
    split: str,
):
    """
    Retrieve dataset elements in a specific split from an SQLite export of an Arkindex corpus
    """
    query = (
        DatasetElement.select()
        .join(Element)
        .join(Image, on=(DatasetElement.element.image == Image.id))
        .where(
            DatasetElement.dataset == dataset,
            DatasetElement.set_name == split,
        )
    )

    return query


def get_elements(
    parent_id: str,
    element_type: List[str],
):
    """
    Retrieve elements from an SQLite export of an Arkindex corpus
    """
    # And load all the elements found in the CTE
    query = (
        list_children(parent_id=parent_id)
        .join(Image)
        .where(Element.type.in_(element_type))
    )

    return query


def build_worker_version_filter(ArkindexModel, worker_versions: List[str | bool]):
    """
    `False` worker version means `manual` worker_version -> null field.
    """
    condition = None
    for worker_version in worker_versions:
        condition |= (
            ArkindexModel.worker_version == worker_version
            if worker_version
            else ArkindexModel.worker_version.is_null()
        )
    return condition


def get_transcriptions(
    element_id: str, transcription_worker_versions: List[str | bool]
) -> List[Transcription]:
    """
    Retrieve transcriptions from an SQLite export of an Arkindex corpus
    """
    query = Transcription.select(
        Transcription.id, Transcription.text, Transcription.worker_version
    ).where((Transcription.element == element_id))

    if transcription_worker_versions:
        query = query.where(
            build_worker_version_filter(
                Transcription, worker_versions=transcription_worker_versions
            )
        )
    return query


def get_transcription_entities(
    transcription_id: str,
    entity_worker_versions: List[str | bool],
    supported_types: List[str],
) -> List[TranscriptionEntity]:
    """
    Retrieve transcription entities from an SQLite export of an Arkindex corpus
    """
    query = (
        TranscriptionEntity.select(
            EntityType.name.alias("type"),
            Entity.name.alias("name"),
            TranscriptionEntity.offset,
            TranscriptionEntity.length,
            TranscriptionEntity.worker_version,
        )
        .join(Entity, on=TranscriptionEntity.entity)
        .join(EntityType, on=Entity.type)
        .where(
            TranscriptionEntity.transcription == transcription_id,
            EntityType.name.in_(supported_types),
        )
    )

    if entity_worker_versions:
        query = query.where(
            build_worker_version_filter(
                TranscriptionEntity, worker_versions=entity_worker_versions
            )
        )

    return query.order_by(
        TranscriptionEntity.offset, TranscriptionEntity.length.desc()
    ).dicts()
