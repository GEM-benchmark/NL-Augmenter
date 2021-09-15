import os

from setuptools import setup

from TestRunner import OperationRuns


def all_folders(search: str, transformation_type: str) -> list:
    """
    Get all folder names for either the transformations or filters

    Parameters:
    -----------
    search: str,
        search term, can be either 'transformations' or 'filters'.
    transformation_type: str,
        if 'transformations' is the search term then specify what type is it (light or heavy).

    Returns:
    --------
    list of folder names.

    """
    folder_names = [
        "transformations/" + f
        for f in list(
            OperationRuns.get_all_folder_names(search, transformation_type)
        )
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


def recursive_requirements(search: str, transformation_type: str) -> str:
    # (1) read main requirements.txt
    requirements = read("requirements.txt")

    # (1) read all requirements.txt in the folder.
    for folder in all_folders(search, transformation_type):
        r_file = os.path.join(
            os.path.dirname(__file__), folder + "/requirements.txt"
        )
        if os.path.isfile(r_file):
            with open(r_file) as f:
                requirements += f.read() + "\n"
    return requirements


setup(
    name="NL-Augmenter",
    version="0.0.1",
    description="The official repository of transformations.",
    long_description=read("README.md"),
    install_requires=recursive_requirements(
        "transformations", "light"
    ),  # read("requirements.txt") for light transformations and all filters
    package_data={
        "": ["*.json", "*.txt", "*.tsv", "*.csv", "*.npz", "*.ckpt"]
    },
    include_package_data=True,
)
