# NL-Augmenter 🦎 → 🐍

**Table of Contents**
* [Motivation](#motivation)
* [Task Specificity](#task-specificity)
* [Submission review process](#submission-review-process)
    * [Review Criteria for Submissions](#review-criteria-for-submissions)
    * [Writing a good transformation](#Writing-a-good-transformation)
    * [Evaluating the transformation](#evaluating-the-transformation)
    * [Writing a good filter](#Writing-a-good-filter)
    * [What is the purpose of test.json](#What-is-the-purpose-of-test.json)
    * [Three Most Creative Implementations](#Three-Most-Creative-Implementations)


## Motivation
Natural Language Transformation or Augmentation comprises methods for increasing the variety of training data for natural language tasks without having to manually collect additional examples. Most strategies either modify existing data, called transformations, or create synthetic data, for example through counterfactual data augmentation, with the aim of having the extended data act as a regularizer to reduce overfitting or biases when training ML models. However, the space of natural language is discrete and simple perturbations cannot capture the entirety and complexity of natural language phenomena.
Due to this complexity, we all need to work together to ensure that datasets can be properly evaluated. Toward this goal, NL-Augmenter seeks to gather transformations, perturbations, and filters which can generate additional data to serve for training or to test model robustness. Following the success of open collaborative efforts like [BIG-bench](https://github.com/google/BIG-bench) and [many](https://arxiv.org/pdf/2010.02353.pdf) others, we invite submissions via a participant driven repository.

## Task Specificity
NLP tasks often radically differ in their linguistic properties of interest — changing the word “happy” to “very happy” in an input is more relevant for sentiment analysis than for summarization. However, many transformations and filters are relevant to many datasets and hence NL-Augmenter is designed to be flexible enough to encourage [format specific](../interfaces) transformations. Such a mechanism also enables quick and rapid testing of transformations over models (and datasets) which share similar formats. 

## Publication of transformations

A paper will be written describing the framework and analyzing the performance of common NLP models. All submitters of accepted contributions will be invited to be co-authors on this paper. The framework itself will provide a final artifact, which we hope will prove useful for data augmentation and generating evaluation suites to evaluate robustness of models. 

## Submission review process

Transformations will be subject to a lightweight, public, and non-anonymous review process. Communication will be via discussion on the transformation's pull request. Reviews will focus on technical correctness and completeness, basic clarity of the proposal, and whether the transformation plausibly generates what it aims to generate.

Each transformation will receive two reviews and the transformation may be edited in response to the reviews. Final decisions will then be made by a meta-review committee. Authors of transformation submissions may be asked to join the reviewer pool after their own transformation is accepted.

## Review Criteria for Submissions
**Correctness:** Transformations must be valid Python code and must pass tests. 

**Interface:** Participants should ensure that they use the correct interface. The complete list is mentioned [here.](../interfaces) E.g., for tasks like machine translation, a transformation which changes the value of a named entity (Andrew->Jason) might need parallel changes in the output too. And hence, it might be more appropriate to use `SentenceAndTargetOperation` or `SentenceAndTargetsOperation` rather than `SentenceOperation`. Similarly, if a transformation changes the label of a sentence, the interface's generate method should take as input the label too - eg. if your transformation reverses the sentiment, `SentenceAndTargetOperation` would be more appropriate then `SentenceOperation`. If you wish to add transformations for input formats other than those specified, you should add an interface [here.](../interfaces)  

**Applicable Tasks & Keywords:** We understand that transformations can vary across tasks as well as a single transformation can work for multiple tasks. Hence all the tasks where the transformation is applicable should be specified in the list “tasks”. The list of tasks has been specified [here](../tasks/TaskTypes.py). The relevant keywords for the [transformation](../docs/keywords.md) should also be specified.
```python
class ButterFingersPerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]
    keywords = ["morphological", "noise", "rule-based", "high-coverage", "high-precision"]
```

**Specificity:** While this is not a necessary criterion, it is highly encouraged to have a specific transformation. E.g., a perturbation which changes gendered pronouns could give insights about gender bias in models.

**Novelty:** Your transformation must improve the coverage of NL-Augmenter in a meaningful way. The idea behind your transformation need not be novel, but its contribution to the library **must be different from the contributions of earlier submissions**. If you are unsure if your idea would constitute a new contribution, please email the organizers at nl-augmenter@googlegroups.com and we are happy to help.

**Adding New Libraries:** We welcome addition of libraries which are light and can be installed via `pip`. Every library should specify the version number associated and be added in a new [requirements.txt](../transformations/punctuation) in the transformation's own folder. However, we discourage the use of heavy libraries for a few lines of code which could be manually written instead. Please ensure that all libraries have MIT, Apache 2, BSD, or other permissive license. GPL-licensed libraries are not approved for NL-Augmenter. If you are unsure, please email the organizers at nl-augmenter@googlegroups.com. 


**Description:** The `README.md` file should clearly explain what the transformation is attempting to generate as well as the importance of that transformation for the specified tasks. Here is a [sample README](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/gender_culture_diverse_name_two_way).

**Data and code source:** The `README.md` file should have a subsection titled "Data and code provenance", which should describe where data or code came from, or that it was fully created by the author. This section should also disclose the license that any external data or code is released under.

**Paraphrasers and Data Augmenters:** Besides perturbations, we welcome transformation methods that act like paraphrasers and data augmenters. For non-deterministic approaches, we encourage you to specify metrics which can provide an estimate of the generation quality. We prefer high precision transformation generators over low accuracy ones. And hence it's okay if your transformation selectively generates. 
 
**Test Cases:** We recommend you to add at least 5 examples in the file `test.json` as test cases for every added transformation. These examples serve as test cases and provide reviewers a sample of your transformation's output. The format of `test.json` can be borrowed from the sample transformations [here.](../interfaces) A good set of test cases would include good as well as bad generation. Addition of the the test cases is **not mandatory** but is encouraged.

**Evaluating Robustness:** To make a stronger PR, a transformation's potential to act as a robustness tool should be tested via executing [`evaluate.py`](../evaluation) and the corresponding performance should be mentioned in the README. Evaluation should only be skipped in case there is no support in the [evaluation_engine](../evaluation).  

**Languages other than English:** We strongly encourage multilingual perturbations. All applicable languages should be specified in the list of “languages”.

**Decent Programming Practise:** We recommend adding docstrings to help others follow your code with ease. Check the [PEP 257 Docstring Conventions](https://www.python.org/dev/peps/pep-0257/) to get an overview.

All of the above criteria extend to [filters](../filters) too. 
 
## Writing a good transformation
Writing a transformation is a creative process. Transformations could use both machine learning as well as rule based models. While there is no hard and fast rule, a transformation is useful if it can augment training data qualitatively or be able to generate perturbations which could reveal places where models' performance suffers. One of the quick ways to contribute would be to extend any of the existing transformations to a low-resource language.  


## Evaluating the transformation
A transformation is most effective when it can reveal potential failures in a model or act as a data augmenter to generate more training data. With the availability of open source pre-trained models, we seek to provide participants the opportunity to quickly test their implementations for evaluating robustness. For a handful set of NLP tasks, we support a [one line evaluation](../evaluation) of transformations. Depending on the interface/operation you use, our evaluation engine evaluates pre-trained HuggingFace models on task-related datasets. The default choice of models and datasets can be overridden. We currently support evaluation over 🤗HuggingFace models and datasets over HF pipelines.

## Writing a good filter
Filters are qualifying conditions on the input data which help identify informative subpopulations of datasets. Relying on a single train-test split implies that there is an inherent element of randomness that can influence model performance. Instead, writing filters which identify specific properties of the data help make the splitting informative. E.g., a filter which determines if an input sentence is conveyed in "an active voice" might be able to reveal performance differences between active and passive voice sentences.   


## What is the purpose of test.json
The `test.json` simply serves to keep track of the core logic of transformation that you intend. While working with the code to and fro, you don't want to mistakenly change the output of someone else's code. Additionally, it makes reviewing much simpler as it gives a quick look into the examples that your logic generates. Besides, it is good practise to let users know the quality of the outputs the transformation generates. And hence this is also the place where you should display good as well as bad generations.

## Three Most Creative Implementations
 🏆  🏆  🏆 After all pull-requests have been merged, 3 of the most creative implementations would be selected and featured on this README page. The selection would be done by the [organizers of NL-Augmenter](https://gem-benchmark.com/nl_augmenter). The minimum requirement to be featured as "most creative" is novelty of implementation i.e. must be the participant's own work.
