# Antonyms Substitute (Double Negation)
This transformation aims to substitute even number of words with their antonyms which would increase the diversity of the given content. Its double negation mechanism does not revert original sentence semantics.

Author name:
- Zhexiong Liu (zhexiong@cs.pitt.edu, University of Pittsburgh)
- Jing Zhang (jing.zhang2@emory.edu, Emory University)

## What type of a transformation is this?
This transformation introduces semantic diversity by replacing even number of adjective/adverb antonyms in given text. We assume that an even number of transforms will remain the semantics in terms of sentiment; however, an odd number of transforms will revert the semantics. Thus, it only applies to the sentence that the number of revertable adjective or adverb in the given sentence is even. We called it double negation.


## What tasks does it intend to benefit?
This augmentation would benefit tasks related to sentiment analysis by augmenting the dataset. The labels for generated sentences would be the semantically similar to their previous one as the double negation mechanism does not change original sentence semantics.

Benchmark results:

Sentiment analysis: we run sentiment analysis on 1000 samples of the IMDB dataset. The original accuracy is 96.0 and the perturbed accuracy is 83.0.


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
