#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 10):
    print("Suggest to use Python >= 3.10")


setup(
    name="pyepsilla",
    version=open("./pyepsilla/vectordb/version.py").read().split('"')[-2],
    keywords="epsilla",
    author="Epsilla Team",
    author_email="info@epsilla.com",
    description="Epsilla Python SDK",
    long_description="Epsilla Python SDK",
    license="Apache License",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "sentry_sdk", "posthog", "pydantic"],
    url="https://github.com/epsilla-cloud/epsilla-python-client",
    project_urls={
        "Source": "https://github.com/epsilla-cloud/epsilla-python-client",
    },
)
