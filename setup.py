import os

from setuptools import find_packages, setup

from nlaugmenter import __version__
from nlaugmenter.evaluation.TestRunner import OperationRuns
from nlaugmenter.utils.mapper import map_filter, map_transformation

NAME = "nlaugmenter"


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
        NAME + "/" + search + "/" + f
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


def get_default_requirements() -> list:
    """
    Populate the default requirements to be installed for the library.

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
    return filter_requirements(mandatory_requirements)


def filter_requirements(requirements: str) -> list:
    """Filter the requirements, exclude comments, empty strings

    Parameters:
    -----------
    requirements: str,
        string of requirements

    Returns:
    --------
    list
        list of filtered requirements
    """
    requirement_list = requirements.split("\n")
    # Remove all comments and empty string.
    requirement_list = set(
        filter(lambda req: "#" not in req and req != "", requirement_list)
    )
    return list(requirement_list)


def get_extra_requirements() -> dict:
    """
    Get the dict of requirements for all the heavy transformations and filters.
    If a user specifies a heavy transformation or filter, the corresponding requirements
    from the generated dictionary will be picked up and installed along with the default
    requirements.

    The generated dictionary will be of this format:
    {
        'lost_in_translation': ['rouge_score'],
        'mr_value_replacement': ['torchtext==0.9.1'],
        'ocr_perturbation': ['trdg==1.6.0', 'tesserocr>=2.5.2'],
        'pinyin': ['g2pM==0.1.2.5'],
        'punctuation': ['cucco==2.2.1', 'fastpunct==2.0.2'],
        'sentence_reordering': ['allennlp==2.5.0', 'allennlp-models==2.5.0'],
        'synonym_substitution': ['nltk==3.6.2'],
        'token_replacement': ['editdistance>=0.5.3'],
        'transformer_fill': ['torch', 'transformers', 'spacy'],
        'toxicity': ['detoxify==0.2.2']
    }

    Example usage: pip install nl-augmenter[lost_in_translation]

    Returns:
    -------
    dict
        dict of requirements for all the heavy transformations and filters.

    """
    # Dictionary of requirements
    requirements = {}
    # Heavy transformations picked from mapper.py
    for entry in map_transformation["heavy"]:
        file_name = NAME + "/transformations/" + entry + "/requirements.txt"
        if os.path.exists(file_name):
            req_string = read(file_name)
            requirements[entry] = filter_requirements(req_string)
    # Heavy filters picked from mapper.py
    for entry in map_filter["heavy"]:
        file_name = NAME + "/filters/" + entry + "/requirements.txt"
        if os.path.exists(file_name):
            req_string = read(file_name)
            requirements[entry] = filter_requirements(req_string)
    return requirements


setup(
    name=NAME,
    version=__version__,
    description="NL-Augmenter: A Framework for Task-Sensitive Natural Language Augmentation",
    author_email="nl-augmenter@googlegroups.com",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/GEM-benchmark/NL-Augmenter",
    project_urls={
        "Bug Tracker": "https://github.com/GEM-benchmark/NL-Augmenter/issues",
        "Web Page": "https://gem-benchmark.com/nl_augmenter",
    },
    install_requires=get_default_requirements(),
    extras_require=get_extra_requirements(),
    keywords=[
        "augmentation",
        "natural language processing",
        "NLP",
        "filters",
        "deep learning",
        "text processing",
        "machine learning",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["test", "docs"]),
    package_data={
        "": ["*.json", "*.txt", "*.tsv", "*.csv", "*.npz", "*.ckpt"]
    },
    include_package_data=True,
    python_requires=">=3.7",
)
