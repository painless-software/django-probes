#!/usr/bin/env python3
"""
Packaging setup to test access to the database
"""
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

import django_probes as package


def read_file(filename):
    """Get the contents of a file"""
    with open(join(abspath(dirname(__file__)), filename)) as file:
        return file.read()


setup(
    name=package.__name__,
    version=package.__version__,
    license=package.__license__,
    author=package.__author__,
    author_email=package.__email__,
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url=package.__url__,
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    keywords=[
        'django',
        'database',
        'probes',
        'docker',
        'kubernetes',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
