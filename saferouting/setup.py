#!/usr/bin/env python

from distutils.core import setup

setup(
    name="saferouting",
    version="0.1",
    description="Routing with point avoidance.",
    author="Addison Kalanther",
    author_email="addikala@berkeley.edu",
    url="https://github.com/adkala/saferouting",
    packages=["saferouting", "saferouting.graph"],
    package_dir={"saferouting": "./", "saferouting.graph": "./graph"},
)
