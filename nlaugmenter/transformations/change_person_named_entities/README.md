# Change Person Named Entities 👨 ️→ 🐍🧔
This transformation acts like a perturbation which changes the name of the person: John --> Cathy

## What type of a transformation is this?
This transformation acts like a perturbation and makes lexical substitutions.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Previous Work and References
1) The list of names and the implementation of perturbation has been taken from Checklist.
```bibtex
@inproceedings{ribeiro-etal-2020-beyond,
    title = "Beyond Accuracy: Behavioral Testing of {NLP} Models with {C}heck{L}ist",
    author = "Ribeiro, Marco Tulio  and
      Wu, Tongshuang  and
      Guestrin, Carlos  and
      Singh, Sameer",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.442",
    doi = "10.18653/v1/2020.acl-main.442",
    pages = "4902--4912",
    abstract = "Although measuring held-out accuracy has been the primary approach to evaluate generalization, it often overestimates the performance of NLP models, while alternative approaches for evaluating models either focus on individual tasks or on specific behaviors. Inspired by principles of behavioral testing in software engineering, we introduce CheckList, a task-agnostic methodology for testing NLP models. CheckList includes a matrix of general linguistic capabilities and test types that facilitate comprehensive test ideation, as well as a software tool to generate a large and diverse number of test cases quickly. We illustrate the utility of CheckList with tests for three tasks, identifying critical failures in both commercial and state-of-art models. In a user study, a team responsible for a commercial sentiment analysis model found new and actionable bugs in an extensively tested model. In another user study, NLP practitioners with CheckList created twice as many tests, and found almost three times as many bugs as users without it.",
}
```

## What are the limitations of this transformation?
The transformation's outputs are too simple while can still be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
