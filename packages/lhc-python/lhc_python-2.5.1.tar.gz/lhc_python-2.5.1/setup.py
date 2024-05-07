import os

from setuptools import setup, find_namespace_packages, Extension


bitap_extension = Extension(
    'lhc.misc.bitap',
    ['src/lib/bitap/bitapmodule.cpp', 'src/lib/bitap/bitap.cpp'],
    include_dirs=['src/lib/bitap'])

digen_extension = Extension(
    'lhc.misc.digen',
    ['src/lib/digen/digenmodule.cpp', 'src/lib/digen/digen.cpp'],
    include_dirs=['src/lib/digen'])

setup(
    ext_modules=[digen_extension, bitap_extension],
)
