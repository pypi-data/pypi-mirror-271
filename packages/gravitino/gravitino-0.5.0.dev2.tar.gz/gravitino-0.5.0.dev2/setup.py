"""
Copyright 2024 Datastrato Pvt Ltd.
This software is licensed under the Apache License version 2.
"""

from setuptools import find_packages, setup


setup(
    name="gravitino",
    description="Python lib/client for Gravitino",
    version="0.5.0.dev2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/datastrato/gravitino",
    author="datastrato",
    python_requires=">=3.8",
    packages=find_packages(include=["gravitino", ".*"]),
    include_package_data=True,
    package_data={"": ["assets/*"]},
    install_requires=open("requirements.txt").read(),
    extras_require={
        "dev": open("requirements-dev.txt").read(),
    },
)
