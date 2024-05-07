# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Dict, List, Optional

import torch
from prettytable import MARKDOWN, PrettyTable
from torch.optim import Adam

from dan.ocr.decoder import GlobalHTADecoder
from dan.ocr.encoder import FCN_Encoder
from dan.ocr.transforms import Preprocessing

METRICS_TABLE_HEADER = {
    "cer": "CER (HTR-NER)",
    "cer_no_token": "CER (HTR)",
    "wer": "WER (HTR-NER)",
    "wer_no_token": "WER (HTR)",
    "wer_no_punct": "WER (HTR no punct)",
    "ner": "NER",
}
REVERSE_HEADER = {column: metric for metric, column in METRICS_TABLE_HEADER.items()}


def update_config(config: dict):
    """
    Complete the fields that are not JSON serializable.
    """

    # .dataset.datasets cast all values to Path
    config["dataset"]["datasets"] = {
        name: Path(path) for name, path in config["dataset"]["datasets"].items()
    }

    # .model.encoder.class = FCN_ENCODER
    config["model"]["encoder"]["class"] = FCN_Encoder

    # .model.decoder.class = GlobalHTADecoder
    config["model"]["decoder"]["class"] = GlobalHTADecoder

    # .model.lm.path to Path
    if config["model"].get("lm", {}).get("path"):
        config["model"]["lm"]["path"] = Path(config["model"]["lm"]["path"])

    # Update preprocessing type
    for prepro in config["training"]["data"]["preprocessings"]:
        prepro["type"] = Preprocessing(prepro["type"])

    # .training.output_folder to Path
    config["training"]["output_folder"] = Path(config["training"]["output_folder"])

    if config["training"]["transfer_learning"]:
        # .training.transfer_learning.encoder[1]
        config["training"]["transfer_learning"]["encoder"][1] = Path(
            config["training"]["transfer_learning"]["encoder"][1]
        )

        # .training.transfer_learning.decoder[1]
        config["training"]["transfer_learning"]["decoder"][1] = Path(
            config["training"]["transfer_learning"]["decoder"][1]
        )

    # Parse optimizers
    for optimizer_setup in config["training"]["optimizers"].values():
        # Only supported optimizer is Adam
        optimizer_setup["class"] = Adam

    # set nb_gpu if not present
    if config["training"]["device"]["nb_gpu"] is None:
        config["training"]["device"]["nb_gpu"] = torch.cuda.device_count()


def create_metrics_table(metrics: List[str]) -> PrettyTable:
    """
    Create a Markdown table to display metrics in (CER, WER, NER, etc)
    for each evaluated split.
    """
    table = PrettyTable(
        field_names=["Split"]
        + [title for metric, title in METRICS_TABLE_HEADER.items() if metric in metrics]
    )
    table.set_style(MARKDOWN)

    return table


def add_metrics_table_row(
    table: PrettyTable, split: str, metrics: Optional[Dict[str, int | float]]
) -> PrettyTable:
    """
    Add a row to an existing metrics Markdown table for the currently evaluated split.
    To create such table please refer to
    [create_metrics_table][dan.ocr.utils.create_metrics_table] function.
    """
    row = [split]
    for column in table.field_names:
        if column not in REVERSE_HEADER:
            continue

        metric_name = REVERSE_HEADER[column]
        metric_value = metrics.get(metric_name)
        row.append(round(metric_value * 100, 2) if metric_value is not None else "−")

    table.add_row(row)
