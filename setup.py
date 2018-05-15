#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages

import skeppa


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

package_exclude = ("tests*", "examples*")
packages = find_packages(exclude=package_exclude)

# Handle requirements
install_requires = [
    "Fabric==1.10.2",
    "PyCrypto==2.6.1",
    "Jinja2==2.8",
    "PyYAML==3.11",
    "six==1.10.0",
]

# Convert markdown to rst
try:
    from pypandoc import convert
    long_description = convert("README.md", "rst")
except:
    long_description = ""


setup(
    name="skeppa",
    version=skeppa.__version__,
    description=("A docker deployment tool based on fabric and "
                 "docker-compose"),
    long_description=long_description,
    author="Marteinn",
    author_email="martin@marteinn.se",
    url="https://github.com/marteinn/skeppa",
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "skeppa = skeppa.scripts.skeppa:main",
        ]
    },
    license="MIT",
    zip_safe=False,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
    ),
)
