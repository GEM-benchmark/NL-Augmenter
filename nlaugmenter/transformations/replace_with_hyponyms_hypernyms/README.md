# Replace nouns with hyponyms or hypernyms 👨 ️→ 🐍🧔
This perturbation replaces common nouns with other related words that are either hyponyms or hypernyms. Hyponyms of a word are more specific in meaning (such as a sub-class of the word), eg: 'spoon' is a hyponym of 'cutlery'. Hypernyms are related words with a broader meaning (such as a generic category /super-class of the word), eg: 'colour' is a hypernym of 'red'. Not every word will have a hypernym or hyponym.

Contributors: Ananya B. Sai, Tanay Dixit (Indian Institute of Technology, Madras)

## What type of a transformation is this?
This transformation acts like a perturbation and makes lexical substitutions using the hyponyms or hypernyms of the common nouns in a sentence when possible (i.e., when atleast one noun in the sentence has a hyponym or hypernym).

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. Since the transformation is only dealing with the hyponyms and hypernyms of nouns, it can be used to augment or benchmark performance on tasks like sentiment classification. For example, 'United Airlines has horrible service' -> 'United Airlines has horrible seating' (using hyponym replacement) or 'United Airlines has horrible quality' (using hypernym replacement).

## Previous Work and References
1) The implementation of this perturbation uses Checklist.
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
While the transformation can be used for data augmentation or to check for performance difference in tasks like sentiment classification, it has to be cautiously used. Since the transformation does affect meaning of a sentence, it is not applicable to tasks like paraphrases [unless, we only want to augment the negative (i.e., not paraphrases) class]. Even for the task of sentiment classification, while the sentiment is usually preserved in case of hyponym/hypernym replacement of only the nouns in a sentence, it is possible that a hypernym would change a positive or negative sentiment to neutral (especially when abstract nouns are involved).
