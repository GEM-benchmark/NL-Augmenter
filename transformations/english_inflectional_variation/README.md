# Inflectional Perturbation for English
This perturbation adds variation to the inflections of English words.

## Transformation Type
This transformation is a perturbation to test a model's ability to handle inflectional variation. In English, each inflection generally maps to a grammatical category in the Penn Treebank. For each content word in the sentence, we first lemmatise it before randomly sampling a valid category and reinflecting the word according to the new category. The sampling process for each word is constrained using its UD POS tag to maintain the original sense for polysemous words. The semantics of the perturbed words should be preserved.

## Supported Tasks
This perturbation can be used for any English task.

## Limitations
This perturbation will likely modify the number of characters in the word; extra care is needed when using this to generate training data for span classification tasks (e.g., question answering).


## Previous Work
This perturbation is adapted from the `Morpheus` adversarial attack.
```
@inproceedings{tan-etal-2020-morphin,
    title = "It{'}s Morphin{'} Time! {C}ombating Linguistic Discrimination with Inflectional Perturbations",
    author = "Tan, Samson  and
      Joty, Shafiq  and
      Kan, Min-Yen  and
      Socher, Richard",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.263",
    doi = "10.18653/v1/2020.acl-main.263",
    pages = "2920--2935",
}
```