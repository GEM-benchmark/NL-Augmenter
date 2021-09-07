import os

from setuptools import setup

from TestRunner import OperationRuns


def all_folders():
    folder_names = [
        "transformations/" + f
        for f in list(OperationRuns.get_all_folder_names())
    ]
    folder_names.extend(
        [
            "filters/" + f
            for f in list(OperationRuns.get_all_folder_names("filters"))
        ]
    )
    return folder_names


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        data = f.read()
    return data


def recursive_requirements():
    # (1) read main requirements.txt
    requirements = read("requirements.txt")
    # (1) read all requirements.txt in the folder.
    for folder in all_folders():
        r_file = os.path.join(
            os.path.dirname(__file__), folder + "/requirements.txt"
        )
        if os.path.isfile(r_file):
            with open(r_file,encoding='utf-16') as f:
                requirements += f.read() + "\n"
    return requirements


setup(
    name="NL-Augmenter",
    version="0.0.1",
    description="The official repository of transformations.",
    long_description=read("README.md"),
    install_requires=recursive_requirements(),  # read("requirements.txt"),
    package_data={
        "": ["*.json", "*.txt", "*.tsv", "*.csv", "*.npz", "*.ckpt"]
    },
    include_package_data=True,
)
