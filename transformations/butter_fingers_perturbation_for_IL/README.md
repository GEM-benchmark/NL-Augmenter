# Butter Fingers Perturbation For Indian Languages 🦎 + ⌨️ → 🦚
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.), which is proportional to noise erupting from keyboard typos resulting in common spelling errors. We have expanded the existing implementation for English ([source](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/butter_fingers_perturbation)) to a few Indian Languages: Bangla, Gujarati, Hindi, Kannada, Malayalam, Oriya, Punjabi, Tamil, and Telugu.

#### Author (1)
- Name: KV Aditya Srivatsa
- Email: k.v.aditya@research.iiit.ac.in
- Affiliation: Language Technologies Research Center, Kohli Center on Intelligent Systems,International Institute of Information Technology, Hyderabad

#### Author (2)
- Name: Mukund Choudhary
- Email: mukund.choudhary@research.iiit.ac.in
- Affiliation: Brain, Cognition, and Computation Lab, International Institute of Information Technology, Hyderabad

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness of text-based models. In this, a few letters are picked at random and are replaced with letters which are at keyboard positions near the source letter (refer to subsection below for more details). Generated transformations display high similarity to the source sentences but with the addition of controlled noise i.e. the code generates highly precise transformations.

### Keyboard choice & Future Work
Currently our implementation considers the InScript keyboard ([source](https://en.wikipedia.org/wiki/InScript_keyboard)) which is decreed as a standard for Indian Languages. The mapping for letters "near" another is concluded from the same layout as well. We intend to exapnd this support to Gboard (mobile devices), other non QWERTY format keyboards, or other Indian Language input layouts.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have text (a sentence/paragraph/document) as input like text classification, text generation, etc. 

## What are the limitations of this transformation?
The transformation's outputs are too simplistic to be used for data augmentation. Unlike a paraphraser, it is not capable of generating linguistically diverse text. It is not modifying a (linguistic) feature of the input (text), rather just creating some noise that is supposed to mirror typos in a naturalistic setting.

## Robustness Evaluation
Our transformation aims at a set of Indian Languages. These languages are not covered by the the currently proposed robustness evaluation method, which can only evaluate transformations in English. Thus, it was not possible to evaluate our transformation using the same.

## Previous Work
1) Butter Finger implementation borrowed from this code https://github.com/alexyorke/butter-fingers

2) There has also been some recent work in the contrast sets of the GEM Benchmark (ACL 2021):
```bibtex
@article{DBLP:journals/corr/abs-2102-01672,
  title     = {The {GEM} Benchmark: Natural Language Generation, its Evaluation and
               Metrics},
  journal   = {CoRR},
  volume    = {abs/2102.01672},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.01672},
  archivePrefix = {arXiv},
  eprint    = {2102.01672},
  timestamp = {Tue, 16 Feb 2021 16:58:52 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2102-01672.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

3) There has been some recent work in NoiseQA too:
```bibtex
@inproceedings{ravichander-etal-2021-noiseqa,
    title = "{N}oise{QA}: Challenge Set Evaluation for User-Centric Question Answering",
    author = "Ravichander, Abhilasha  and
      Dalmia, Siddharth  and
      Ryskina, Maria  and
      Metze, Florian  and
      Hovy, Eduard  and
      Black, Alan W",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume",
    month = apr,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2021.eacl-main.259",
    pages = "2976--2992",
    abstract = "When Question-Answering (QA) systems are deployed in the real world, users query them through a variety of interfaces, such as speaking to voice assistants, typing questions into a search engine, or even translating questions to languages supported by the QA system. While there has been significant community attention devoted to identifying correct answers in passages assuming a perfectly formed question, we show that components in the pipeline that precede an answering engine can introduce varied and considerable sources of error, and performance can degrade substantially based on these upstream noise sources even for powerful pre-trained QA models. We conclude that there is substantial room for progress before QA systems can be effectively deployed, highlight the need for QA evaluation to expand to consider real-world use, and hope that our findings will spur greater community interest in the issues that arise when our systems actually need to be of utility to humans.",
}
```
