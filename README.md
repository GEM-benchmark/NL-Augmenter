# A Repository of Perturbations and Adversaries 🦎 → 🐍

The Perturbation Repository is a collaborative effort intended to accumulate all transformations operating over tasks dealing with natural language. We invite submissions of perturbations and transformations via pull requests to this GitHub repository. 
Every contribution of a perturbation should either add noise to the input or paraphrase or transform the input. 

# Tasks
All the supported interfaces can be looked up here: [interfaces](interfaces)
```python
class TaskType(enum.Enum):
    TEXT_CLASSIFICATION = 1,
    TEXT_TO_TEXT_GENERATION = 2,
    TEXT_TAGGING = 3,
    DIALOGUE_TO_TEXT = 4,
    TABLE_TO_TEXT = 5,
    RDF_TO_TEXT = 6,
    RDF_TO_RDF = 7
```

**Table of contents**

* [Installation](#installation)
* [How do I create a perturbation?](#how-do-i-create-a-perturbation)
* [Creating a programmatic task](#creating-a-programmatic-task)
* [Review Criteria for Accepting Submissions](#review-criteria)

## Installation
```bash
# When creating a new transformation, replace this with your forked repository (see below)
git clone https://github.com/GEM-benchmark/GEM-special-test-sets.git
cd GEM-special-test-sets
python setup.py sdist
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
```

```bash
python main.py
```
Running it for the first time will take a while (depending on your internet speed) since the translation models need to be downloaded.

After you make any change, run test_main.py once to ensure that your changes don't regress anything.

```bash
python test_main.py
```
 
And for any new logic, add the appropriate test case so that no one else breaks the changes. 

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
cd GEM-special-test-sets
git checkout -b my_awesome_transformation
```
We will base our transformation on an existing example.
Create a new transformation directory by copying over an existing transformation:
```bash
cd transformation/
cp -r butter_fingers_perturbation my_awesome_transformation
cd my_awesome_transformation
```

### Creating a transformation
1. Rename the class `ButterFingersPerturbation` to `MyAwesomeTransformation`
2. Choose one of the perturbation interfaces from the `interfaces` folder eg. `SentenceTransformation`, `SentenceAndTargetTransformation`, etc.
3. Now put all your creativity in implementing the `generate` method. If you intend to use external libraries, add them with their version numbers in `requirements.txt`
4. Once done add at least 5 example pairs as test cases in the file `test.json`.

**Testing and evaluating**

Once the transformation is ready, test it:
```bash
pytest
```

### Submitting

Once the tests pass and you are happy with the transformation, submit your transformation for review.
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

:sparkles: Congratulations, you've submitted a transformation to the perturbation repository! :sparkles:

## Review Criteria for Accepting Submissions

**Correctness:** Transformations must be valid Python code and must pass tests. 

**Output:** Participants should ensure that they use the correct interface. Eg. for tasks like machine translation, perturbations like named entity changes might need parallel changes in the output. 

**Specificity:** While this is not a necessary criterion, it is highly encouraged to have a specific perturbation. Eg. reversing the gender pronouns could give insights about gender bias in models, etc.

**Adding New Libraries:** We welcome addition of new libraries which can be installed via pip. Every library should specify the version number associated. 

However, we encourage you to avoid adding new libraries which are heavy or from which only a small part of the code is used.
  
**Applicable Tasks:** Perturbations can vary across tasks as well as work differently for different types of inputs. Hence all the tasks where the perturbation is applicable should be specified in the list “tasks”. The list of tasks has been specified [here](tasks/TaskTypes.py).
```python
class ButterFingersPerturbation(SentenceTransformation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]
```

**Description:** The `README.md` file should clearly explain what the perturbation is attempting to generate as well as the importance of that perturbation for the specified tasks.

**Accuracy:** We also encourage perturbation methods which act like paraphrasers or data augmenters. For such methods, the paraphrasing accuracy must be specified. It is preferred to have a high precision transformer rather than a low accuracy one. Paraphrasers with low accuracy would be selected on a case-by-case basis.
 
**Test Cases:** At least 5 examples (text or data) should be added in the file `test.json` as test cases for every added perturbation.

**Languages other than English:** We strongly encourage multilingual perturbations. All applicable languages should be specified in the list of “locales”.
 
