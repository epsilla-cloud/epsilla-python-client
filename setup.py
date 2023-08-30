#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, ".")
from setuptools import setup, find_packages
from pyepsilla.vectordb.version import __version__

setup(
    name='pyepsilla',
    version=__version__,
    keywords='epsilla',
    author= 'Epsilla Team',
    description='Epsilla Python SDK',
    long_description='Epsilla Python SDK',
    license='Apache License',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests>=2.19.1',
        'sentry_sdk'
    ],
    url='https://github.com/epsilla-cloud/pyepsilla',
    project_urls={
        'Source': 'https://github.com/epsilla-cloud/pyepsilla',
    },
)
