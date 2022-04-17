# Random Word Deletion
This perturbation randomly remove each word of a sentence or paragraph with a probability p.

Author name: Emile Chapuis and Pierre Colombo
Author email: chapuis.emile@gmail.com and colombo.pierre@gmail.com
Author Affiliation: Telecom Paris - IPP

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Each word of the given text are randomly deleted.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Previous Work
1) There has also been some recent work in the contrast sets of the GEM Benchmark (ACL 2021):
```bibtex
@article{DBLP:journals/corr/DaiL15a,
  author    = {Andrew M. Dai and
               Quoc V. Le},
  title     = {Semi-supervised Sequence Learning},
  journal   = {CoRR},
  volume    = {abs/1511.01432},
  year      = {2015},
  url       = {http://arxiv.org/abs/1511.01432},
  archivePrefix = {arXiv},
  eprint    = {1511.01432},
  timestamp = {Mon, 13 Aug 2018 16:49:17 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/DaiL15a.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
@book{10.5555/3110856,
    author = {Goldberg, Yoav and Hirst, Graeme},
    title = {Neural Network Methods in Natural Language Processing},
    year = {2017},
    isbn = {1627052984},
    publisher = {Morgan & Claypool Publishers},
}


@inproceedings{DBLP:conf/emnlp/WeiZ19,
  author    = {Jason W. Wei and
               Kai Zou},
  editor    = {Kentaro Inui and
               Jing Jiang and
               Vincent Ng and
               Xiaojun Wan},
  title     = {{EDA:} Easy Data Augmentation Techniques for Boosting Performance
               on Text Classification Tasks},
  booktitle = {Proceedings of the 2019 Conference on Empirical Methods in Natural
               Language Processing and the 9th International Joint Conference on
               Natural Language Processing, {EMNLP-IJCNLP} 2019, Hong Kong, China,
               November 3-7, 2019},
  pages     = {6381--6387},
  publisher = {Association for Computational Linguistics},
  year      = {2019},
  url       = {https://doi.org/10.18653/v1/D19-1670},
  doi       = {10.18653/v1/D19-1670},
  timestamp = {Thu, 05 Aug 2021 17:36:17 +0200},
  biburl    = {https://dblp.org/rec/conf/emnlp/WeiZ19.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
## What are the limitations of this transformation?
Some word deletion can alter the meaning of the sentence, e.g. negations.
