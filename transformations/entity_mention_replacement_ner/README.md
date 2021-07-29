# Replace Named Entities 🦓 ️→ 🐎
This transformation replaces the entity mention with another entity mention of the same entity type e.g. : [PER] John --> Adam , [LOC] Berlin --> Rome, [Disease] Tumour -> Myotonic dystrophy.

Contributor: Usama Yaseen, Siemens AG (usama.yaseen@siemens.com)

## What type of a transformation is this?
This transformation randomly swaps an entity mention with another entity mention of the same entity type.

## What tasks does it intend to benefit?
This transformation would benefit sequence labelling tasks such as named entity recognition.

## Previous Work and References
1) The transformation was proposed by [Dai and Adel, 2020](https://aclanthology.org/2020.coling-main.343/).

```bibtex
@inproceedings{dai-adel-2020-analysis,
    title = "An Analysis of Simple Data Augmentation for Named Entity Recognition",
    author = "Dai, Xiang  and
      Adel, Heike",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2020.coling-main.343",
    doi = "10.18653/v1/2020.coling-main.343",
    pages = "3861--3867",
    abstract = "Simple yet effective data augmentation techniques have been proposed for sentence-level and sentence-pair natural language processing tasks. Inspired by these efforts, we design and compare data augmentation for named entity recognition, which is usually modeled as a token-level sequence labeling problem. Through experiments on two data sets from the biomedical and materials science domains (i2b2-2010 and MaSciP), we show that simple augmentation can boost performance for both recurrent and transformer-based models, especially for small training sets.",
}
```

## What are the limitations of this transformation?
This transformation replicates the context of an entity mention with another entity mention, hence, it cannot generate linguistically diverse sequences. Also, the generated sequence might be factually incorrect as per our knowledge of the world. Nevertheless, exploiting this transformation as a data augmentation strategy has been empirically shown to improve the performance of the underlying sequence (NER) model ([Dai and Adel, 2020](https://aclanthology.org/2020.coling-main.343/)).