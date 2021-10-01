[![Checks](https://github.com/GEM-benchmark/NL-Augmenter/workflows/nl-action/badge.svg)](https://github.com/GEM-benchmark/NL-Augmenter/actions/workflows/nl-action.yml)
[![Forks](https://img.shields.io/github/forks/GEM-benchmark/NL-Augmenter)](https://github.com/GEM-benchmark/NL-Augmenter/network/members)
[![Issues](https://img.shields.io/github/issues/GEM-benchmark/NL-Augmenter)](https://github.com/GEM-benchmark/NL-Augmenter/issues)
[![Pull requests](https://img.shields.io/github/issues-pr/GEM-benchmark/NL-Augmenter)](https://github.com/GEM-benchmark/NL-Augmenter/pulls)
[![Contributors]((https://img.shields.io/github/contributors/GEM-benchmark/NL-Augmenter)](https://github.com/GEM-benchmark/NL-Augmenter/graphs/contributors)
[![License](https://img.shields.io/github/license/GEM-benchmark/NL-Augmenter)](https://opensource.org/licenses/MIT)

# NL-Augmenter 🦎 → 🐍

The NL-Augmenter is a collaborative effort intended to add transformations of datasets dealing with natural language. Transformations augment text datasets in diverse ways, including: randomizing names and numbers, changing style/syntax, [paraphrasing](https://aclanthology.org/J13-3001.pdf), KB-based paraphrasing ... and whatever creative augmentation you contribute. We invite submissions of transformations to this framework by way of GitHub pull request, through August 31, 2021. All submitters of accepted transformations (and filters) will be included as co-authors on a paper announcing this framework.

The framework organizers can be contacted at nl-augmenter@googlegroups.com.

**Submission timeline**

| Due date          | Description                                                                 |
| ------------------ | -----------                                                                 |
| A̶u̶g̶u̶s̶t̶ 3̶1̶, 2̶0̶2̶1̶ | P̶u̶l̶l̶ r̶e̶q̶u̶e̶s̶t̶ m̶u̶s̶t̶ b̶e̶ o̶p̶e̶n̶e̶d̶ t̶o̶ b̶e̶ e̶l̶i̶g̶i̶b̶l̶e̶ f̶o̶r̶ i̶n̶c̶l̶u̶s̶i̶o̶n̶ i̶n̶ t̶h̶e̶ f̶r̶a̶m̶e̶w̶o̶r̶k̶ a̶n̶d̶ a̶s̶s̶o̶c̶i̶a̶t̶e̶d̶ p̶a̶p̶e̶r̶  |
| September 2̶2̶, 30 2021 | Review process for pull request above must be complete           |

A transformation can be revised between the pull request submission and pull request merge deadlines. We will provide reviewer feedback to help with the revisions.

The transformations which are already accepted to NL-Augmenter are summarized in [the transformations folder](transformations). Transformations undergoing review can be seen as [pull requests](https://github.com/GEM-benchmark/NL-Augmenter/pulls).

**Table of contents**

* [Colab notebook](#colab-notebook)
* [Installation](#installation)
* [How do I create a transformation?](#how-do-i-create-a-transformation)
* [How do I create a filter?](#how-do-i-create-a-filter)
* [Motivation](docs/doc.md#motivation)
* [Review Criteria for Accepting Submissions](docs/doc.md#review-criteria-for-submissions)
* [Some Ideas for Transformations](#some-ideas-for-transformations)

## Colab notebook

<a href="https://colab.research.google.com/github/GEM-benchmark/NL-Augmenter/blob/main/notebooks/Write_a_sample_transformation.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> To quickly see transformations and filters in action, run through our [colab notebook](https://colab.research.google.com/github/GEM-benchmark/NL-Augmenter/blob/main/notebooks/Write_a_sample_transformation.ipynb).

## Some Ideas for Transformations
If you need inspiration for what transformations to implement, check out https://github.com/GEM-benchmark/NL-Augmenter/issues/75, where some ideas and previous papers are discussed. So far, contributions have focused on morphological inflections, character level changes, and random noise. The best new pull requests will be dissimilar from these existing contributions.

## Installation

**Requirements**

* Python 3.7

**Instructions**

```bash
# When creating a new transformation, replace this with your forked repository (see below)
git clone https://github.com/GEM-benchmark/NL-Augmenter.git
cd NL-Augmenter
python setup.py sdist
pip install -e .
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
```

## How do I create a transformation?
### Setup

First, [fork the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) in GitHub! :fork_and_knife:
<a href="https://docs.github.com/en/github/getting-started-with-github/fork-a-repo">
<div style="text-align:center"><img src="https://docs.github.com/assets/images/help/repository/fork_button.jpg" alt="fork button" width="500"/></div>
</a>

Your fork will have its own location, which we will call `PATH_TO_YOUR_FORK`.
Next, [clone the forked repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) and create a branch for your transformation, which here we will call **my_awesome_transformation**:
```bash
git clone $PATH_TO_YOUR_FORK
cd NL-Augmenter
git checkout -b my_awesome_transformation
```
We will base our transformation on an existing example.
Create a new transformation directory by copying over an existing transformation. You can choose to copy from other [transformation directories](interfaces) depending on the task you wish to create a transformation for. Check some of the existing [pull requests](https://github.com/GEM-benchmark/NL-Augmenter/pulls?q=is%3Aopen+is%3Apr+label%3Atransformation) [and merged transformations](transformations) first to avoid duplicating efforts or creating transformations too similar to previous ones.
```bash
cd transformations/
cp -r butter_fingers_perturbation my_awesome_transformation
cd my_awesome_transformation
```

### Creating a transformation
1. In the file `transformation.py`, rename the class `ButterFingersPerturbation` to `MyAwesomeTransformation` and choose one of the interfaces from the `interfaces/` folder. See the full list of options [here.](interfaces)
2. Now put all your creativity in implementing the `generate` method. If you intend to use external libraries, add them with their version numbers in [`requirements.txt`](requirements.txt)
3. Update `my_awesome_transformation/README.md` to describe your transformation.

**Testing and evaluating** (Optional)

Once you are done, add at least 5 example pairs as test cases in the file `test.json` so that no one breaks your code inadvertently.

Once the transformation is ready, test it:
```bash
pytest -s --t=my_awesome_transformation
```
If you would like to evaluate your transformation against a common 🤗HuggingFace model, we encourage you to check [evaluation](evaluation)

**Code Styling** To standardized the code we use the [black](https://github.com/psf/black) code formatter which will run at the time of pre-commit.
To use the pre-commit hook, install `pre-commit` with `pip install pre-commit` (should already be installed if you followed the above instructions).
Then run `pre-commit install` to install the hook. On future commits, you should see the black code formatter is run on all python files you've staged for commit.

### Submitting

Once the tests pass and you are happy with the transformation, submit them for review.
First, commit and push your changes:
```bash
git add transformations/my_awesome_transformation/*
git commit -m "Added my_awesome_transformation"
git push --set-upstream origin my_awesome_transformation
```
Finally, [submit a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
The last `git push` command prints a URL that can be copied into a browser to initiate such a pull request.
Alternatively, you can do so from the GitHub website.
<a href="https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request">
<div style="text-align:center"><img src="https://docs.github.com/assets/images/help/pull_requests/pull-request-start-review-button.png" alt="pull request button" width="500"/></div>
</a>

:sparkles: Congratulations, you've submitted a transformation to NL-Augmenter! :sparkles:

## How do I create a filter?

We also accept pull-requests for creating [filters](filters) which identify interesting subpopulations of a dataset. The process to add a new filter is just the same as above. All filter implementations require implementing `.filter` instead of `.generate` and need to be placed in the [filters](filters) folder. So, just the way transformations can transform examples of text, filters can identify whether an example follows some pattern of text! The only difference is that while transformations return another example of the same input format, filters simply return True or False! For step-by-step instructions, follow [these](filters) steps.

## BIG-Bench :chair:
If you are interested in NL-Augmenter, you may also be interested in the [BIG-bench](https://github.com/google/BIG-bench/) large scale collaborative benchmark for language models.

### Most Creative Implementations 🏆

After all pull-requests have been merged, 3 of the [most creative implementations](docs/doc.md#Three-most-creative-Implementations) would be selected and featured on this README page and on the NL-Augmenter [webpage](https://gem-benchmark.com/nl_augmenter).

### License
Some transformations include components released under a different (permissive, open source) license. For license details, refer to the `README.md` and any license files in the transformations's or filter's directory.
