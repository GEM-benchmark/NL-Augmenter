# Random Swap
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly swapping words which are close to each other in a sentence.

Author1 name: Tshephisho Sefara

Author1 email: [sefaratj@gmail.com](mailto:sefaratj@gmail.com)

Author1 Affiliation: Council for Scientific and Industrial Research

Author2 name: Vukosi Marivate

Author2 email: [vukosi.marivate@cs.up.ac.za](mailto:vukosi.marivate@cs.up.ac.za), [vima@vima.co.za](mailto:vima@vima.co.za)

Author2 Affiliation: Department of Computer Science, University of Pretoria

## What type of a transformation is this?
This transformation could augment the semantic representation of the sentence as well as test model robustness by swapping words.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation.

Benchmark results:

- Text Classification: we run sentiment analysis on a 1% sample of the IMDB dataset. The original accuracy is 96.0 and the perturbed accuracy is 96.0.
```
{'accuracy': 96.0,
 'dataset_name': 'imdb',
 'model_name': 'aychang/roberta-base-imdb',
 'no_of_examples': 250,
 'pt_accuracy': 96.0,
 'split': 'test[:1%]'}
```
- Text summarization: we run text summarization on a 1% sample of the xsum dataset. The original bleu is 15.99 and the perturbed bleu is 16.1.
```
{'bleu': 15.989230311212195,
 'dataset_name': 'xsum',
 'model_name': 'sshleifer/distilbart-xsum-12-6',
 'pt_bleu': 16.09338711985113,
 'split': 'test[:1%]'}
```
## Related Work
This perturbation is adapted from our TextAugment library https://github.com/dsfsi/textaugment
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




## What are the limitations of this transformation?
The transformation's outputs may change the meaning of the sentence by adding grammatical errors. 
