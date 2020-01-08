#!/usr/bin/env python
import sys
from os import path
from setuptools import setup, find_packages
from codecs import open

version = '1.6.1'

working_directory = path.abspath(path.dirname(__file__))
with open(path.join(working_directory, 'steamworks/__init__.py'), encoding = 'utf-8') as f:
    for line in f.readlines():
        if '__version__' in line:
            version = line.split("'")[1]
            break

setup(
    name = 'steamworks',
    version = version,
    description = 'Interact with Steamworks API',
    long_description = 'Interact with Steamworks API',
    url = 'https://github.com/Gramps/SteamworksPy',
    author = 'GP Garcia',
    author_email = '',
    license = 'MIT',
    classifiers = [
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    keywords = 'steamworks sdk valve steamapi api',
    packages = ['steamworks'] + ['steamworks.' + package for package in find_packages(where = 'steamworks')],
    install_requires = [],
    extras_require = {},
    zip_safe = True
)