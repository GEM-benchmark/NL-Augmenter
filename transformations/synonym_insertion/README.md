# Synonym Insertion
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly inserting synonyms of randomly selected words excluding punctuations and stopwords.

Author1 name: Tshephisho Sefara

Author1 email: sefaratj@gmail.com

Author1 Affiliation: Council for Scientific and Industrial Research

Author2 name: Vukosi Marivate

Author2 email: vukosi.marivate@cs.up.ac.za, vima@vima.co.za

Author2 Affiliation: Department of Computer Science, University of Pretoria

## What type of a transformation is this?
This transformation could augment the semantic representation of the sentence as well as test model robustness by inserting synonyms of random words excluding punctuations and stopwords.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation.

Benchmark results:

- Text Classification: we run sentiment analysis on a 1% sample of the IMDB dataset. The original accuracy is 96.0 and the perturbed accuracy is 94.0.
```
Applying transformation:
100%|██████████| 250/250 [00:18<00:00, 13.85it/s]
Finished transformation! 250 examples generated from 250 original examples, with 250 successfully transformed and 0 unchanged (1.0 perturb rate)
Here is the performance of the model on the transformed set
The accuracy on this subset which has 250 examples = 94.0

 {'accuracy': 96.0,
 'dataset_name': 'imdb',
 'model_name': 'aychang/roberta-base-imdb',
 'no_of_examples': 250,
 'pt_accuracy': 94.0,
 'split': 'test[:1%]'}
```
- Text Generation: we run text generation on a 1% sample of the xsum dataset. The original bleu is 16 and the perturbed bleu is 13.85.
```
Applying transformation:
100%|██████████| 113/113 [00:12<00:00,  9.31it/s]
Finished transformation! 113 examples generated from 113 original examples, with 113 successfully transformed and 0 unchanged (1.0 perturb rate)
Here is the performance of the model on the transformed set
Length of Evaluation dataset is 113
Predicted BLEU score = 13.849736846663058
{'bleu': 16.0,
 'dataset_name': 'xsum',
 'model_name': 'sshleifer/distilbart-xsum-12-6',
 'pt_bleu': 13.8,
 'split': 'test[:1%]'}
```

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
