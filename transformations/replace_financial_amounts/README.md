# Replace Financial amounts 🦎  + ⌨️ → 🐍
This transformation replaces consistently financial amounts throughout a text.
The replacement changes the amount, the writing format as well as the currency of the financial amount.
The change is consistent in regard to:
- the modifier used to change all amounts of the same currency throughout the text.
  - e.g., the sentence `I owe Fred € 20 and I need € 10 for the bus.` might be changed to `I owe Fred 2 906.37 Yen and I need 1 453.19 Yen for the bus.`
- the modifier used to change the amounts so that new amounts are relatively close to the original amount.
- the rate used for a change of currency reflects the actual rate on the day of use based on the forex exchange prices (this rate is fixed when using pytest).
See https://www.forex.com/ie/ for more information about forex.

Author names:
- Maxime Meyer (maxime.meyer@vadesecure.com, Vade)
- Tatiana Ekeinhor (tatiana.ekeinhor@vadesecure.com, Vade)
- Antoine Honoré (antoine.honore@vadesecure.com, Vade)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Generated transformations display high similarity to the 
source sentences i.e. the code outputs highly precise generations. It is a substitution of a financial amount to another financial amount. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Robustness Evaluation
```bash
$ python evaluate.py -t ReplaceFinancialAmount
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
Loading <imdb> dataset to evaluate <aychang/roberta-base-imdb> model.
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
The accuracy on this subset which has 1000 examples = 96.0
Applying transformation:
100%|███████████████████████████████████████████████████████████████████████████████| 1000/1000 [06:21<00:00,  2.62it/s]
Finished transformation! 1000 examples generated from 1000 original examples, with 35 successfully transformed and 965 unchanged (0.035 perturb rate)
Here is the performance of the model on the transformed set
The accuracy on this subset which has 1000 examples = 96.0
```

## Previous Work
1) This perturbation was as part of an augmentation library described by Regina and al. in (Arxiv 2020):
```bibtex
@article{DBLP:journals/corr/abs-2007-02033,
  author    = {Mehdi Regina and
               Maxime Meyer and
               S{\'{e}}bastien Goutal},
  title     = {Text Data Augmentation: Towards better detection of spear-phishing
               emails},
  journal   = {CoRR},
  volume    = {abs/2007.02033},
  year      = {2020},
  url       = {https://arxiv.org/abs/2007.02033},
  archivePrefix = {arXiv},
  eprint    = {2007.02033},
  timestamp = {Fri, 17 Jul 2020 15:39:46 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2007-02033.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## Common currencies
Not all currencies have conversion rate associated. For the moment, only six currencies have a conversion rate associated so that the currency can be changed to one another while keeping the converted amount close to the original amount value.
Those six currencies are: US dollar, Euro, Pound, Yen, Yuan and the Bitcoin.
The bank rate is obtained using the forex exchange prices thanks to the `forex-python` library.

Amounts corresponding to other currencies (e.g.: XAF) have just their amount modified.

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation as a standalone module.
However, combined with other modules, this transformation helps improve the understanding of the context, and generates simple but precise similar sentences (same semantic similarity).

The transformation outputs financial amounts independently of the format expected for the country.
I.e. we might have `12,38 $` or `12.38 $` output by the generator.

The transformation can only change numeric financial amounts (i.e. it will not handle "two dollars" or "14k euros").

Finally, the transformation is case-sensitive i.e., `13 usd` will not be considered as an amount.

### Bank Rate

Currently, the bank rate is fixed and reflects the rate of August 2021.
An improvement to this transformation could be to use a library such as `https://forex-python.readthedocs.io/en/latest/usage.html` to get actualized bank rates.
