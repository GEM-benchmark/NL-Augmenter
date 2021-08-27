# Antonyms Substitute
This transformation aims to substitute words with their antonyms, which facilitates the diversity of the content.

Author name:
- Zhexiong Liu (zhexiong@cs.pitt.edu, University of Pittsburgh)
- Jing Zhang (jing.zhang2@emory.edu, Emory University)

## What type of a transformation is this?
This transformation could introduce semantic diversity by adding antonyms. Specifically, it will help revert the semantics to an opposite position or uses double negation to express the similar semantics.


## What tasks does it intend to benefit?
This augmentation would benefit tasks related to sentiment analysis, contrastive learning and classification, by augmenting the dataset.

## Related Work
Special thanks to @zijwang, whose contribution has inspired this work. The code was adapted from his submission, and the tokenization and POS tagging were adapted from Stanza

```bibtex
@inproceedings{qi2020stanza,
    title={Stanza: A {Python} Natural Language Processing Toolkit for Many Human Languages},
    author={Qi, Peng and Zhang, Yuhao and Zhang, Yuhui and Bolton, Jason and Manning, Christopher D.},
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations",
    year={2020}
}
```

The antonyms are based on WordNet via NLTK

```bibtex
@book{miller1998wordnet,
  title={WordNet: An electronic lexical database},
  author={Miller, George A},
  year={1998},
  publisher={MIT press}
}
@inproceedings{bird2006nltk,
  title={NLTK: the natural language toolkit},
  author={Bird, Steven},
  booktitle={Proceedings of the COLING/ACL 2006 Interactive Presentation Sessions},
  pages={69--72},
  year={2006}
}
```


## What are the limitations of this transformation?
Since the antonyms are generated using WordNet, it would have limitation to augment issues, such as making the text non-grammarly correct.
