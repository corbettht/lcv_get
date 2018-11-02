#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: setup.py
.. moduleauthor:: hank corbett <my_email>

This file is used to create the package we'll publish to PyPI.
"""

import os
import lcv_get
from setuptools import setup, find_packages, Command  # Prefer setuptools over distutils.
from codecs import open  # Use a consistent encoding.
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

# Get the base version from the library.
version=lcv_get.__version__

# If the environment has a build number set...
if os.getenv('buildnum') is not None:
    # ...append it to the version.
    version = "{version}.{buildnum}".format(version=version, buildnum=os.getenv('buildnum'))

setup(
    name='lcv_get',
    description="Internal tool for querying the Evryscope lightcurves table.",
    long_description=long_description,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    install_requires=[
    # Include your dependencies here.
    # Here are a couple of examples...
    # 'numpy>=1.13.3,<2',
    # 'measurement>=1.8.0,<2'
    'click>=6.7,<7',
    'numpy',
    'psycopg2-binary',
  ],
  entry_points="""
    [console_scripts]
    lcv_get=lcv_get.cli:cli
    """,
    python_requires=">=0.0.1",
    license='MIT',
    author='hank corbett',
    author_email='my_email',
    # Use the URL to the github repo.
    url='https://github.com/corbettht/lcv_get',
    download_url=f'https://github.com/corbettht/'
               f'lcv_get/archive/{version}.tar.gz',
    keywords=[
        # Add package keywords here.
    ],
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for.
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries',

      # Pick your license as you wish (should match "license" above).
      'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True
)
