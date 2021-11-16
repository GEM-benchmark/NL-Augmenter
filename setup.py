import os
from test.mapper import map_filter, map_transformation

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
        search + "/" + f
        for f in list(
            OperationRuns.get_all_folder_names(search, transformation_type)
        )
    ]
    return folder_names


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        data = f.read()
    return data


def recursive_requirements(search: str, transformation_type: str) -> str:
    # (1) read all requirements.txt in the folder.
    requirements = ""
    for folder in all_folders(search, transformation_type):
        r_file = os.path.join(
            os.path.dirname(__file__), folder + "/requirements.txt"
        )
        if os.path.isfile(r_file):
            with open(r_file) as f:
                requirements += f.read() + "\n"
    return requirements


def get_default_requirements(transformation_type: str) -> list:
    """
    Populate the default requirements to be installed for the library

    Parameters
    ----------
    transformation_type: str,
        type of transformation, light or heavy.

    Returns:
    -------
    list
        list of requirements.
    """
    # Get the default requirements (light transformations and light filters)
    # (1) read main requirements.txt
    mandatory_requirements = read("requirements.txt")
    # (2) read requirements for light transformations
    mandatory_requirements += recursive_requirements(
        "transformations", "light"
    )
    # (3) read requirements for light filters
    mandatory_requirements += recursive_requirements(
        "filters", "light"
    )  # light filters
    return mandatory_requirements


def get_extra_requirements() -> dict:
    """
    Get the dict of requirements for all the heavy transformations and filters.
    If a user specifies a heavy transformation or filter, the corresponding requirements
    from the generated dictionary will be picked up and installed along with the default
    requiremens.

    Returns:
    -------
    dict
        dict of requirements for all the heavy transformations and filters.

    """
    # Dictionary of requirements
    requirements = {}
    # Heavy transformations picked from test/mapper.py
    for entry in map_transformation["heavy"]:
        requirements[entry] = recursive_requirements(
            "transformations/" + entry, "heavy"
        )
    # Heavy filters picked from test/mapper.py
    for entry in map_filter["heavy"]:
        requirements[entry] = recursive_requirements(
            "filters/" + entry, "heavy"
        )
    return requirements


setup(
    name="NL-Augmenter",
    version="0.0.1",
    description="The official repository of transformations.",
    long_description=read("README.md"),
    install_requires=get_default_requirements("light"),
    extras_require=get_extra_requirements(),
    package_data={
        "": ["*.json", "*.txt", "*.tsv", "*.csv", "*.npz", "*.ckpt"]
    },
    include_package_data=True,
)
