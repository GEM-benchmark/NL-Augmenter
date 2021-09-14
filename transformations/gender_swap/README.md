# Gender swap ♀️ ↔️ ♂️
This transformation swaps all gendered words in a given sentence with their counterparts.
By default, names are also randomly swapped.

## What type of a transformation is this?
An example tells it all:
```
Bob wants to become a programmer, as his father. ↔️ Alice wants to become a programmer, as her mother.
```
The word list is taken from [1](https://arxiv.org/abs/1807.11714) and was extended with two possessive pronouns: 'his' and 'her'.
The name list is taken form the CheckList paper [3].


## What tasks does it intend to benefit?
This transformation does not target one particular task – it introduces __gender diversity__ to your data.
If used as data augmentation for training, the transformation might mitigate gender bias, as shown in [2](https://aclanthology.org/2020.emnlp-main.656/).
It also might be used to create a gender-balanced evaluation dataset.
One can use such dataset to expose __gender bias__ of pre-trained models.


## Previous Work

_[1]_ 
```bibtex
@misc{lu2019gender,
      title={Gender Bias in Neural Natural Language Processing}, 
      author={Kaiji Lu and Piotr Mardziel and Fangjing Wu and Preetam Amancharla and Anupam Datta},
      year={2019},
      eprint={1807.11714},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

_[2]_
```bibtex
@article{Dinan2020QueensAP,
  title={Queens Are Powerful Too: Mitigating Gender Bias in Dialogue Generation},
  author={Emily Dinan and Angela Fan and Adina Williams and Jack Urbanek and Douwe Kiela and J. Weston},
  journal={ArXiv},
  year={2020},
  volume={abs/1911.03842}
}
```

_[3]_
```bibtex
@inproceedings{Ribeiro2020BeyondAB,
  title={Beyond Accuracy: Behavioral Testing of NLP models with CheckList},
  author={Marco T{\'u}lio Ribeiro and Tongshuang Wu and Carlos Guestrin and Sameer Singh},
  booktitle={ACL},
  year={2020}
}
```

## What are the limitations of this 
While this transformation handles more complex cases like: 
* retaining original casing (e.g `Brother`➡️`Sister`)
* retaining original punctuation (e.g `he?!`➡️`she?!`),

it does not take sentence meaning and syntax into account.
Thus, resulting sentences might lose meaning or might become ungrammatical.

_Cumbersome case of female possessive pronoun_.
Female possessive pronoun, _her_, that does not take object becomes _hers_.
> That is _her_ bottle. ↔ That bottle is _hers_.

This is not a case for male pronouns:

> That is _his_ bottle. ↔ That bottle is _his_.

Solving this problem requires pronoun resolution which was not implemented.
