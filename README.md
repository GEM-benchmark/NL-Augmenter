# NL-Augmenter 🦎 → 🐍

The NL-Augmenter is a collaborative effort intended to add transformations of datasets dealing with natural language. Transformations augment text datasets in diverse ways, including: introducing spelling errors, translating to a different language, randomizing names and numbers, paraphrasing ... and whatever creative augmentation you contribute. We invite submissions of transformations to this framework by way of GitHub pull request, through September 1, 2021. All submitters of accepted transformations (and filters) will be included as co-authors on a paper announcing this framework. 

The framework organizers can be contacted at nl-augmenter@googlegroups.com.

**Submission timeline**

| Due date          | Description                                                                 |
| ------------------ | -----------                                                                 |
|  July 25, 2021   | Pull request must be opened to be invited as a reviewer and be included in the framework & associated paper |
|  August 15, 2021   | Review process for pull request above must be complete to be invited as a reviewer and be included in the framework & associated paper |
| August 31, 2021 | Pull request must be opened to be eligible for inclusion in the framework and associated paper  |
| September 22, 2021 | Review process for pull request above must be complete           |

A transformation can be revised between the pull request submission and pull request merge deadlines. We will provide reviewer feedback to help with the revisions.

The transformations which are already accepted to NL-Augmenter are summarized in [this table](transformations/README.md). Transformations undergoing review can be seen as [pull requests](https://github.com/GEM-benchmark/NL-Augmenter/pulls).

**Table of contents**

* [Colab notebook](#colab-notebook)
* [Installation](#installation)
* [How do I create a transformation?](#how-do-i-create-a-transformation)
* [How do I create a filter?](#how-do-i-create-a-filter)
* [Motivation](docs/doc.md#motivation)
* [Review Criteria for Accepting Submissions](docs/doc.md#review-criteria-for-submissions)

## Colab notebook

<a href="https://colab.research.google.com/github/GEM-benchmark/NL-Augmenter/blob/main/notebooks/Write_a_sample_transformation.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> To quickly see transformations and filters in action, run through our [colab notebook](https://colab.research.google.com/github/GEM-benchmark/NL-Augmenter/blob/main/notebooks/Write_a_sample_transformation.ipynb).

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
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
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
Create a new transformation directory by copying over an existing transformation. You can choose to copy from other [transformation directories](interfaces) depending on the task you wish to create a transformation for. We strongly suggest you to look at some of the other [transformations](transformations) first.
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

### Most Creative Implementations 🏆

After all pull-requests have been merged, 3 of the [most creative implementations](docs/doc.md#Three-most-creative-Implementations) would be selected and featured on this README page and on the NL-Augmenter [webpage](https://gem-benchmark.com/nl_augmenter).
