# Spell-checker based word perturbation
This transformation helps add noise to a sentence using a spell-checker.
This can make the model adapt to noise via randomly incorrect words.

Author name: P Reddy Gurunatha Swamy (Email: gurunathpr at gmail)

## What type of a transformation is this?
This transformation replaces words in text given a specified probability using a spell-checker via pyenchant   
library to generate similar words with spelling variations. This would help in making a model more robust to   
spelling variations in text.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. It can switch languages by changing language input to the spell-checker.

## Previous Work
1) Used PyEnchant spell-checker from [here](https://pypi.org/project/pyenchant/)

2) This spell-checker based transformation was previously used in the following paper for data-augmentation:
```bibtex
@inproceedings{awasthi-etal-2019-parallel,
    title = "Parallel Iterative Edit Models for Local Sequence Transduction",
    author = "Awasthi, Abhijeet  and
      Sarawagi, Sunita  and
      Goyal, Rasna  and
      Ghosh, Sabyasachi  and
      Piratla, Vihari",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1435",
    doi = "10.18653/v1/D19-1435",
    pages = "4259--4269",
}
```


## What are the limitations of this transformation?
These are simple transformations with spelling variations and the meanings of replacement words may not be similar to usage of the original word. 
