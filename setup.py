#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pyepsilla',
    version= '0.1.7',
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
