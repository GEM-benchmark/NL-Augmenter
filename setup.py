import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        data = f.read()
    return data


setup(
    name="NL-Augmenter",
    version="0.0.1",
    description=("The official repository of transformations."),
    long_description=read("README.md"),
    install_requires=read("requirements.txt"),
    package_data={"": ["*.json", "*.txt", "*.tsv", "*.csv", "*.npz", "*.ckpt"]},
    include_package_data=True,
)
