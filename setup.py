# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from findsecbugs_parser.version import __version__

setup(
    name='findsecbugs-parser',
    version=__version__,
    author='amon',
    author_email='amon@nandynarwhals.org',
    description='Parses FindSecBugs XML output.',
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
        'setuptools',
    ],
    tests_require=[
        'pytest',
        'tox<=2.9.1',
    ],
    install_requires=[
        'Sphinx>=1.7.0',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    url='https://github.com/nnamon/findsecbugs-python-parser'
)
