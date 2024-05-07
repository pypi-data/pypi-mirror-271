#!/usr/bin/env python
# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def parse_requirements_line(line) -> str:
    # Special case for git requirements
    if line.startswith("git+http"):
        assert "@" in line, "Branch should be specified with suffix (ex: @master)"
        assert (
            "#egg=" in line
        ), "Package name should be specified with suffix (ex: #egg=kraken)"
        package_name: str = line.split("#egg=")[-1]
        return f"{package_name} @ {line}"
    # Special case for submodule requirements
    elif line.startswith("-e"):
        package_path: str = line.split(" ")[-1]
        package = Path(package_path).resolve()
        return f"{package.name} @ file://{package}"
    else:
        return line


def parse_requirements(filename: str) -> List[str]:
    path = Path(__file__).parent.resolve() / filename
    assert path.exists(), f"Missing requirements: {path}"
    return list(
        map(parse_requirements_line, map(str.strip, path.read_text().splitlines()))
    )


setup(
    name="atr-dan",
    version=Path("VERSION").read_text(),
    description="Teklia DAN",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Teklia",
    author_email="contact@teklia.com",
    url="https://gitlab.teklia.com/atr/dan",
    python_requires=">=3.10",
    install_requires=parse_requirements("requirements.txt"),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "teklia-dan=dan.cli:main",
        ]
    },
    extras_require={
        "docs": parse_requirements("doc-requirements.txt"),
        "mlflow": parse_requirements("mlflow-requirements.txt"),
    },
    license="CeCILL-C",
    license_files=(
        "LICENSE",
        "LICENCE",
    ),
)
