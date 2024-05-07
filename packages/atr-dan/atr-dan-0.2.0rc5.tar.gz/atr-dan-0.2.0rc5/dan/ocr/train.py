# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import json
import logging
import random
from copy import deepcopy

import numpy as np
import torch
import torch.multiprocessing as mp

from dan.ocr.manager.training import Manager
from dan.ocr.mlflow import MLFLOW_AVAILABLE
from dan.ocr.utils import update_config
from dan.utils import MLflowNotInstalled

if MLFLOW_AVAILABLE:
    import mlflow

    from dan.ocr.mlflow import make_mlflow_request, start_mlflow_run


logger = logging.getLogger(__name__)


def train(rank, params, mlflow_logging=False):
    torch.manual_seed(0)
    torch.cuda.manual_seed(0)
    np.random.seed(0)
    random.seed(0)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

    params["training"]["device"]["ddp_rank"] = rank
    model = Manager(params)
    model.load_model()

    if params["dataset"]["tokens"] is not None:
        if "ner" not in params["training"]["metrics"]["train"]:
            params["training"]["metrics"]["train"].append("ner")
        if "ner" not in params["training"]["metrics"]["eval"]:
            params["training"]["metrics"]["eval"].append("ner")

    if mlflow_logging:
        logger.info("MLflow logging enabled")

    model.train(mlflow_logging=mlflow_logging)


def serialize_config(config):
    """
    Make every field of the configuration JSON-Serializable and remove sensitive information.

    - Classes are transformed using their name attribute
    - Functions are casted to strings
    """
    # Create a copy of the original config without erase it
    serialized_config = deepcopy(config)

    # Remove credentials to the config
    serialized_config["mlflow"]["s3_endpoint_url"] = ""
    serialized_config["mlflow"]["tracking_uri"] = ""
    serialized_config["mlflow"]["aws_access_key_id"] = ""
    serialized_config["mlflow"]["aws_secret_access_key"] = ""

    # Get the name of the class
    serialized_config["model"]["models"]["encoder"] = serialized_config["model"][
        "models"
    ]["encoder"].__name__
    serialized_config["model"]["models"]["decoder"] = serialized_config["model"][
        "models"
    ]["decoder"].__name__
    serialized_config["training"]["optimizers"]["all"]["class"] = serialized_config[
        "training"
    ]["optimizers"]["all"]["class"].__name__

    # Cast the functions to str
    serialized_config["dataset"]["config"]["augmentation"] = str(
        serialized_config["dataset"]["config"]["augmentation"]
    )
    serialized_config["training"]["nb_gpu"] = str(
        serialized_config["training"]["nb_gpu"]
    )

    return serialized_config


def start_training(config, mlflow_logging: bool) -> None:
    if (
        config["training"]["device"]["use_ddp"]
        and config["training"]["device"]["force"] in [None, "cuda"]
        and torch.cuda.is_available()
    ):
        mp.spawn(
            train,
            args=(config, mlflow_logging),
            nprocs=config["training"]["device"]["nb_gpu"],
        )
    else:
        train(0, config, mlflow_logging)


def run(config: dict):
    """
    Main program, training a new model, using a valid configuration
    """
    names = list(config["dataset"]["datasets"].keys())
    # We should only have one dataset
    assert len(names) == 1, f"Found {len(names)} datasets but only one is expected"

    dataset_name = names.pop()
    update_config(config)

    if config.get("mlflow") and not MLFLOW_AVAILABLE:
        logger.error(
            "Cannot log to MLflow. Please install the `mlflow` extra requirements."
        )
        raise MLflowNotInstalled()

    if not config.get("mlflow"):
        start_training(config, mlflow_logging=False)
    else:
        labels_path = config["dataset"]["datasets"][dataset_name] / "labels.json"
        with start_mlflow_run(config["mlflow"]) as (run, created):
            if created:
                logger.info(f"Started MLflow run with ID ({run.info.run_id})")
            else:
                logger.info(f"Resumed MLflow run with ID ({run.info.run_id})")

            make_mlflow_request(
                mlflow_method=mlflow.set_tags, tags={"Dataset": dataset_name}
            )
            # Get the labels json file
            labels_artifact = json.loads(labels_path.read_text())

            # Log MLflow artifacts
            for artifact, filename in [
                (serialize_config(config), "config.json"),
                (labels_artifact, "labels.json"),
            ]:
                make_mlflow_request(
                    mlflow_method=mlflow.log_dict,
                    dictionary=artifact,
                    artifact_file=filename,
                )
            start_training(config, mlflow_logging=True)
