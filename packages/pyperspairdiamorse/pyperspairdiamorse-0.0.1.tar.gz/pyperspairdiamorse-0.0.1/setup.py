#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from setuptools import setup, Extension, find_packages
import pip


version = "0.0.1"
libName = "pyperspairdiamorse"

file_dir_path = os.path.dirname(os.path.realpath(__file__))


def package_files(directory):
    return [os.path.join(p, f) for p, d, files in os.walk(directory) for f in files]


with open("README.md", "r") as fh:
    long_description = fh.read()
short_description = "Cross-platform C++ library of persistent pair extractor using the diamorse approach"

language = "c++"
extra_compile_args = ["-O3", "-w", "-std=c++11"]
installRequiresList = ["numpy"]
entry_points_Command = {
    "main": [
        "persistance_pair_extractor=pyperspairdiamorse.extract",
    ]
}
license = "GPLv3"
author = "Andrey S. Zubov, Kirill M. Gerke, Andrey A. Ananev"
author_email = "andrey.ananev@phystech.edu"

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Education",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Programming Language :: C++",
    "Programming Language :: Python :: 3 :: Only",
]

packages = find_packages("src", include=["pyperspairdiamorse*"]) + ["baselib"]

os.environ["CXX"] = "g++"
os.environ["CC"] = "gcc"

pip.main(["install", "numpy"])


class get_numpy_include(object):
    """Defer numpy.get_include() until after numpy is installed."""

    def __str__(self):
        import numpy

        return numpy.get_include()


pyperspairdiamorse_module = Extension(
    libName,
    sources=["./src/pyperspairdiamorse/pyperspairdiamorse.cpp"],
    language=language,
    extra_compile_args=extra_compile_args,
    include_dirs=["./src/baselib/include/", get_numpy_include()],
)
setup(
    name=libName,
    version=version,
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    license=license,
    packages=packages,
    package_dir={"": "src"},
    package_data={
        "baselib": ["./src/*.cpp", "./include/*.hpp"],
    },
    classifiers=classifiers,
    ext_modules=[pyperspairdiamorse_module],
    setup_requires=installRequiresList,
    install_requires=installRequiresList,
    entry_points=entry_points_Command,
)
