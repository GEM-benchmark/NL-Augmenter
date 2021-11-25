# Random uppercase transformation
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly adding upper cased letters.

Author name: Pierre Colombo and Emile Chapuis
Author email: colombo.pierre@gmail.com and emile.chapuis@gmail.com
Author Affiliation: Telecom Paris

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few letters picked at random are replaced with uppercased letters. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Previous Work
Standard technique for NLP it is similar to what is proposed in EDA.

```bibtex
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
The transformation's outputs are simple and could induce a huge change if the tokenizer allows uppercased, however if the tokenizer only uses lowercases it will be inefficient.
