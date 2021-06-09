# NL-Augmenter 🦎 → 🐍

**Table of Contents**
* [Motivation](#motivation)
* [Definitions](#definitions)
* [Submission review process](#submission-review-process)
    * [Review Criteria for Submissions](#review-criteria-for-submissions)
    * [Writing a good perturbation](#review-criteria-for-submissions)
    * [Evaluating the transformation](#evaluating-the-transformation)
    * [What is the purpose of test.json](#What-is-the-purpose-of-test.json)

## Motivation

## Definitions
Transformations vs Perturbation vs Augmentation 

## Publication of transformations

A paper will be written describing the framework and analyzing the performance of common NLP models. All submitters of accepted transformations will be invited to be co-authors on this paper. The framework itself will provide a final artifact, which we hope will prove useful for data augmentation and generating perturbations and contrast sets to evaluate robustness. 

## Submission review process

Transformations will be subject to a lightweight, public, and non-anonymous review process. Communication will be via discussion on the transformation's pull request. Reviews will focus on technical correctness and completeness, basic clarity of the proposal, and whether the transformation might plausibly generate what it aims to.

Each transformation will receive two reviews. The transformation may be edited in response to the reviews. Final decisions will then be made by a meta-review committee. Authors of transformation submissions may be asked to join the reviewer pool after their own transformation is accepted.

### Review Criteria for Submissions
**Correctness:** Transformations must be valid Python code and must pass tests. 

**Interface:** Participants should ensure that they use the correct interface. The complete list is mentioned [here.](../interfaces) Eg. for tasks like machine translation, a transformation which changes the value of a named entity (Andrew->Jason) might need parallel changes in the output too. And hence, it might be more appropriate to use `SentenceAndTargetOperation` or `SentenceAndTargetsOperation` rather than `SentenceOperation`.

**Applicable Tasks:** We understand that transformations can vary across tasks as well as a single transformation can work for multiple tasks. Hence all the tasks where the transformation is applicable should be specified in the list “tasks”. The list of tasks has been specified [here](tasks/TaskTypes.py).
```python
class ButterFingersPerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    locales = ["en"]
```

**Specificity:** While this is not a necessary criterion, it is highly encouraged to have a specific transformation. Eg. a perturbation which reverses the gender pronouns could give insights about gender bias in models, etc.

**Adding New Libraries:** We welcome addition of libraries which are light and can be installed via pip. Every library should specify the version number associated and be added in requirements.txt. 

**Description:** The `README.md` file should clearly explain what the transformation is attempting to generate as well as the importance of that transformation for the specified tasks.

**Paraphrasers and Data Augmenters:** Besides perturbations, we strongly encourage transformation methods which act like paraphrasers and data augmenters. For non-deterministic approaches, we encourage you to specify metrics which could provide an estimate of the quality of generation. It is preferred to have a high precision transformation generator as compared to a low accuracy one. And hence it's okay to selectively generate.
 
**Test Cases:** At least 5 examples should be added in the file `test.json` as test cases for every added transformation. These examples serve as test cases as well as provide a glimpse of what the transformation takes as input and what it generates.

**Languages other than English:** We also strongly encourage multilingual perturbations. All applicable languages should be specified in the list of “locales”.
 
## Writing a good transformation
Writing a transformation is a creative process. Transformations could be generated both using machine learning as well as rule based models. While there is no hard core rule, a transformation is worth if it can augment training data qualitatively or be able to generate perturbations which could reveal places where models' performance suffers. One of the quick ways to contribute would be to add a copy of any of the existing transformations for a low-resource language.

## Evaluating the transformation
 

## What is the purpose of test.json
The `test.json` simply serves to keep track of the core logic of transformation that you intend. While working with the code to and fro, you don't want to mistakenly change the output of someone else's code. Besides, it also makes reviewing much simpler as it gives a quick look into the examples that your logic generates.   