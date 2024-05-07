#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import fnmatch
from setuptools import setup, find_packages


def find_files(directory):
    matches = []

    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*'):
            matches.append(os.path.join(root, filename))

    return matches


setup(name="cosolvkit",
      version='0.4.2',
      description="CosolvKit",
      author="Niccolo Bruciaferri, Jerome Eberhardt",
      author_email="forli@scripps.edu",
      url="https://github.com/forlilab/cosolvkit",
      packages=find_packages(),
      scripts=["scripts/create_cosolvent_system.py",
               "scripts/post_simulation_processing.py"],
      package_data={"cosolvkit" : ["data/*"]},
      data_files=[("", ["README.md", "LICENSE"]),
                  ("scripts", find_files("scripts"))],
      include_package_data=True,
      zip_safe=False,
      python_requires=">=3.9, <3.12",
      license="LGPL-2.1",
      keywords=["molecular modeling", "drug design",
                "cosolvent", "MD simulations"],
      classifiers=["Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                   "Operating System :: Unix",
                   "Operating System :: MacOS",
                   "Topic :: Scientific/Engineering"]
)
