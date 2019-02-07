#!/usr/bin/env python3
"""
Packaging setup to test access to the database
"""

from os.path import abspath, dirname, join
from setuptools import setup
import probes as package


def read_file(filename):
    """Get the contents of a file"""
    here = abspath(dirname(__file__))
    with open(join(here, filename), encoding='utf-8') as file:
        return file.read()


setup(
    name=package.__name__,
    version=package.__version__,
    license=package.__license__,
    author=package.__author__,
    author_email=package.__email__,
    description='Test whether access to the database is possible',
    long_description=read_file('README.rst'),
    url='https://github.com/vshn/python-hatchbuck',
    install_requires=read_file('requirements.txt'),
    include_package_data=True,
    keywords=['django', 'DB', 'probes'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Programming Language :: Python'
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
