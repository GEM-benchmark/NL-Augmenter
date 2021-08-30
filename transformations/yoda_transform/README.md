# Yoda Transformation
This perturbation modifies sentences to flip the clauses such that it reads like "Yoda Speak". For example,
"Much to learn, you still have". For a more in-depth description of "Yoda Speak" linguistically,
see, for example, [this article](https://www.theatlantic.com/entertainment/archive/2015/12/hmmmmm/420798/).

Author names: Ryan Teehan, Vinay Prabhu, Nick Roberts, Sang Han
Author email: rsteehan@gmail.com
Author Affiliation: Charles River Analytics, UnifyID, UW Madison

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Sentences with clauses transformed in this way are
comprehensible by English speakers, but may pose serious difficulty to NL algorithms.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc, but may be especially useful for robustness of POS tagging algorithms. Modifying sentence structure
in this way may expose an algorithm's reliance on spurious correlations in the training data.

```python evaluate.py -t ButterFingersPerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb")
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6")
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of same model on the pertubed set = 11.9221

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
## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
