# Synonym Substitution
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly substituting words with their synonyms. 

Author name: Zijian Wang (zijwang@hotmail.com)

## What type of a transformation is this?
This transformation could augment the semantic representation of the sentence as well as test model robustness by substituting words with their synonyms. 


## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation. 

Benchmark results:

- Sentiment analysis: we run sentiment analysis on a 10% sample of the IMDB dataset. The original accuracy is 96.0 and the perturbed accuracy is 93.36.

- Text summarization: we run text summarization on a 10% sample of the xsum dataset. The original bleu is 15.25 and the perturbed bleu is 12.27.

## Related Work
The tokenization and POS tagging were done using Stanza

```bibtex
@inproceedings{qi2020stanza,
    title={Stanza: A {Python} Natural Language Processing Toolkit for Many Human Languages},
    author={Qi, Peng and Zhang, Yuhao and Zhang, Yuhui and Bolton, Jason and Manning, Christopher D.},
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations",
    year={2020}
}
```

The synonyms are based on WordNet via NLTK

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
The space of synonyms depends on WordNet and could be limited.
