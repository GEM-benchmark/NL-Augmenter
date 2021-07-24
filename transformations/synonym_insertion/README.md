# Synonym Insertion
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly inserting synonyms of randomly selected words excluding punctuations and stopwords.

Author1 name: Tshephisho Sefara

Author1 email: sefarat@gmail.com

Author1 Affiliation: Council for Scientific and Industrial Research

Author2 name: Vukosi Marivate

Author2 email: vima@vima.co.za

Author2 Affiliation: University of Pretoria

## What type of a transformation is this?
This transformation could augment the semantic representation of the sentence as well as test model robustness by inserting synonyms of random words excluding punctuations and stopwords.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation.

Benchmark results:

- Text Classification: we run sentiment analysis on a 1% sample of the IMDB dataset. The original accuracy is 96.0 and the perturbed accuracy is 94.0.
```{'accuracy': 96.0,
 'dataset_name': 'imdb',
 'model_name': 'aychang/roberta-base-imdb',
 'no_of_examples': 250,
 'pt_accuracy': 94.0,
 'split': 'test[:1%]'}
```
- Text summarization: we run text summarization on a 1% sample of the xsum dataset. The original bleu is 15.99 and the perturbed bleu is ???.

## Related Work
This perturbation is adapted from our TextAugmentation library https://github.com/dsfsi/textaugment
```bibtex
@inproceedings{marivate2020improving,
  title={Improving short text classification through global augmentation methods},
  author={Marivate, Vukosi and Sefara, Tshephisho},
  booktitle={International Cross-Domain Conference for Machine Learning and Knowledge Extraction},
  pages={385--399},
  year={2020},
  organization={Springer}
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
The space of synonyms depends on WordNet and could be limited. The transformation might introduce non-grammatical segments.
