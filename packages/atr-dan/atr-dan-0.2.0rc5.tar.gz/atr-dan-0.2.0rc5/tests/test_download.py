# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import logging
from operator import attrgetter, methodcaller
from pathlib import Path

import pytest
from PIL import Image, ImageChops

from dan.datasets.download.images import IIIF_FULL_SIZE, ImageDownloader
from dan.datasets.download.utils import download_image
from line_image_extractor.image_utils import BoundingBox
from tests import FIXTURES

EXTRACTION_DATA_PATH = FIXTURES / "extraction"


@pytest.mark.parametrize(
    "max_width, max_height, width, height, resize",
    (
        (1000, 2000, 900, 800, IIIF_FULL_SIZE),
        (1000, 2000, 1100, 800, "1000,"),
        (1000, 2000, 1100, 2800, ",2000"),
        (1000, 2000, 2000, 3000, "1000,"),
    ),
)
def test_get_iiif_size_arg(max_width, max_height, width, height, resize):
    assert (
        ImageDownloader(max_width=max_width, max_height=max_height).get_iiif_size_arg(
            width=width, height=height
        )
        == resize
    )


def test_download(split_content, monkeypatch, tmp_path):
    # Mock download_image so that it simply opens it with Pillow
    monkeypatch.setattr(
        "dan.datasets.download.images.download_image", lambda url: Image.open(url)
    )

    output = tmp_path / "download"
    output.mkdir(parents=True, exist_ok=True)
    (output / "split.json").write_text(json.dumps(split_content))

    def mock_build_image_url(polygon, image_url, *args, **kwargs):
        # During tests, the image URL is its local path
        return image_url

    extractor = ImageDownloader(
        output=output,
        image_extension=".jpg",
    )
    # Mock build_image_url to simply return the path to the image
    extractor.build_iiif_url = mock_build_image_url
    extractor.run()

    # Check files
    IMAGE_DIR = output / "images"
    TEST_DIR = IMAGE_DIR / "test" / "dataset_id"
    TRAIN_DIR = IMAGE_DIR / "train" / "dataset_id"
    VAL_DIR = IMAGE_DIR / "val" / "dataset_id"

    expected_paths = [
        # Images of test folder
        TEST_DIR / "test-page_1-line_1.jpg",
        TEST_DIR / "test-page_1-line_2.jpg",
        TEST_DIR / "test-page_1-line_3.jpg",
        TEST_DIR / "test-page_2-line_1.jpg",
        TEST_DIR / "test-page_2-line_2.jpg",
        TEST_DIR / "test-page_2-line_3.jpg",
        # Images of train folder
        TRAIN_DIR / "train-page_1-line_1.jpg",
        TRAIN_DIR / "train-page_1-line_2.jpg",
        TRAIN_DIR / "train-page_1-line_3.jpg",
        TRAIN_DIR / "train-page_1-line_4.jpg",
        TRAIN_DIR / "train-page_2-line_1.jpg",
        TRAIN_DIR / "train-page_2-line_2.jpg",
        TRAIN_DIR / "train-page_2-line_3.jpg",
        # Images of val folder
        VAL_DIR / "val-page_1-line_1.jpg",
        VAL_DIR / "val-page_1-line_2.jpg",
        VAL_DIR / "val-page_1-line_3.jpg",
        output / "labels.json",
        output / "split.json",
    ]
    assert sorted(filter(methodcaller("is_file"), output.rglob("*"))) == expected_paths

    # Check "labels.json"
    expected_labels = {
        "test": {
            "images/test/dataset_id/test-page_1-line_1.jpg": "ⓢCou⁇e⁇  ⓕBouis  ⓑ⁇.12.14",
            "images/test/dataset_id/test-page_1-line_2.jpg": "ⓢ⁇outrain  ⓕA⁇ol⁇⁇e  ⓑ9.4.13",
            "images/test/dataset_id/test-page_1-line_3.jpg": "ⓢ⁇abale  ⓕ⁇ran⁇ais  ⓑ26.3.11",
            "images/test/dataset_id/test-page_2-line_1.jpg": "ⓢ⁇urosoy  ⓕBouis  ⓑ22⁇4⁇18",
            "images/test/dataset_id/test-page_2-line_2.jpg": "ⓢColaiani  ⓕAn⁇els  ⓑ28.11.1⁇",
            "images/test/dataset_id/test-page_2-line_3.jpg": "ⓢRenouar⁇  ⓕMaurice  ⓑ2⁇.⁇.04",
        },
        "train": {
            "images/train/dataset_id/train-page_1-line_1.jpg": "ⓢCaillet  ⓕMaurice  ⓑ28.9.06",
            "images/train/dataset_id/train-page_1-line_2.jpg": "ⓢReboul  ⓕJean  ⓑ30.9.02",
            "images/train/dataset_id/train-page_1-line_3.jpg": "ⓢBareyre  ⓕJean  ⓑ28.3.11",
            "images/train/dataset_id/train-page_1-line_4.jpg": "ⓢRoussy  ⓕJean  ⓑ4.11.14",
            "images/train/dataset_id/train-page_2-line_1.jpg": "ⓢMarin  ⓕMarcel  ⓑ10.8.06",
            "images/train/dataset_id/train-page_2-line_2.jpg": "ⓢAmical  ⓕEloi  ⓑ11.10.04",
            "images/train/dataset_id/train-page_2-line_3.jpg": "ⓢBiros  ⓕMael  ⓑ30.10.10",
        },
        "val": {
            "images/val/dataset_id/val-page_1-line_1.jpg": "ⓢMonar⁇  ⓕBouis  ⓑ29⁇⁇⁇04",
            "images/val/dataset_id/val-page_1-line_2.jpg": "ⓢAstier  ⓕArt⁇ur  ⓑ11⁇2⁇13",
            "images/val/dataset_id/val-page_1-line_3.jpg": "ⓢ⁇e ⁇lie⁇er  ⓕJules  ⓑ21⁇11⁇11",
        },
    }

    assert json.loads((output / "labels.json").read_text()) == expected_labels

    # Check cropped images
    for expected_path in expected_paths:
        if expected_path.suffix != ".jpg":
            continue

        assert ImageChops.difference(
            Image.open(
                EXTRACTION_DATA_PATH / "images" / "text_line" / expected_path.name
            ),
            Image.open(expected_path),
        )


def test_download_image_error(monkeypatch, caplog, capsys):
    task = {
        "split": "train",
        "polygon": [],
        "image_url": "deadbeef",
        "destination": Path("/dev/null"),
    }
    monkeypatch.setattr(
        "dan.datasets.download.images.polygon_to_bbox",
        lambda polygon: BoundingBox(0, 0, 0, 0),
    )

    extractor = ImageDownloader(image_extension=".jpg")

    # Add the key in data
    extractor.data[task["split"]][str(task["destination"])] = "deadbeefdata"

    # Build a random task
    extractor.download_images([task])

    # Key should have been removed
    assert str(task["destination"]) not in extractor.data[task["split"]]

    # Check error log
    assert len(caplog.record_tuples) == 1
    _, level, msg = caplog.record_tuples[0]
    assert level == logging.ERROR
    assert msg == "Failed to download 1 image(s)."

    # Check stdout
    captured = capsys.readouterr()
    assert captured.out == "deadbeef: Image URL must be HTTP(S) for element null\n"


def test_download_image_error_try_max(responses, caplog):
    # An image's URL
    url = (
        "https://blabla.com/iiif/2/image_path.jpg/231,699,2789,3659/full/0/default.jpg"
    )
    fixed_url = (
        "https://blabla.com/iiif/2/image_path.jpg/231,699,2789,3659/max/0/default.jpg"
    )

    # Fake responses error
    responses.add(
        responses.GET,
        url,
        status=400,
    )
    # Correct response with max
    responses.add(
        responses.GET,
        fixed_url,
        status=200,
        body=next((FIXTURES / "prediction" / "images").iterdir()).read_bytes(),
    )

    image = download_image(url)

    assert image
    # We try 3 times with the first URL
    # Then the first try with the new URL is successful
    assert len(responses.calls) == 4
    assert list(map(attrgetter("request.url"), responses.calls)) == [url] * 3 + [
        fixed_url
    ]

    # Check error log
    assert len(caplog.record_tuples) == 2

    # We should only have WARNING levels
    assert set(level for _, level, _ in caplog.record_tuples) == {logging.WARNING}
