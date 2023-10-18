#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
# import sys
# # if sys.version_info < (3,10):
# #     sys.exit('Sorry, Python < 3.10 is not supported')

try:
  with open("./pyepsilla/vectordb/version.py") as f:
    version = f.read().split("'")[-2]
except Exception as e:
  print("Error when read version: ", e)

setup(
    name='pyepsilla',
    version=version,
    keywords='epsilla',
    author= 'Epsilla Team',
    description='Epsilla Python SDK',
    long_description='Epsilla Python SDK',
    license='Apache License',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    python_requires='>=3.10.0',
    install_requires=[
        'requests',
        'sentry_sdk',
        'posthog'
    ],
    url='https://github.com/epsilla-cloud/pyepsilla',
    project_urls={
        'Source': 'https://github.com/epsilla-cloud/pyepsilla',
    },
)
