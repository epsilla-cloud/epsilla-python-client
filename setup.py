#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pyepsilla',
    version= '0.0.6',
    keywords='epsilla',
    author= 'Epsilla Team',
    description='Epsilla Python SDK',
    license='Apache License',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests>=2.19.1'
    ],
    url='https://github.com/epsilla-cloud/pyepsilla',
    project_urls={
        'Source': 'https://github.com/epsilla-cloud/pyepsilla',
    },
)