#!/usr/bin/env python
import os
dir = 'transformations/mix_transliteration'

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

import numpy


extensions = [
    Extension(
        dir.replace("/",".") + ".utils.viterbi",
        [
            os.path.join(dir,"utils/viterbi.pyx")
        ],
        include_dirs=[numpy.get_include()]
    ),
]

print(dir.replace("/",".") + ".utils.viterbi",  os.path.join(dir,"utils/viterbi.pyx"))

setup(
    ext_modules=cythonize(extensions)
)
