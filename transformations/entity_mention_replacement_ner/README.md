# Replace Named Entities 🦓 ️→ 🐎
This transformation replaces the entity mention with another entity mention of the same entity type e.g. : [PER] John --> Adam , [LOC] Berlin --> Rome, [Disease] Tumour -> Myotonic dystrophy.

Contributor: Usama Yaseen, Siemens AG (usama.yaseen@siemens.com)

## What type of a transformation is this?
This transformation randomly swaps an entity mention with another entity mention of the same entity type.

### Example

This transformation expects the reference corpus (list of all token sequences and tag sequences) in the constructor to create a mapping of entity type to entity mentions.

**Corpus**

`"token_sequences": [["Judea", "Pearl", "was", "born", "in", "Tel", "Aviv", "."], ["Demis", "Hassabis", "is", "the", "chief", "executive", "officer", "of", "DeepMind", "."], ["BMW", "is", "headquartered", "in", "Munich", "."]]`

`"tag_sequences": [["B-PER", "I-PER", "O", "O", "O", "B-LOC", "I-LOC", "O"], ["B-PER", "I-PER", "O", "O", "O", "O", "O", "O", "B-ORG", "O"], ["B-ORG", "O", "O", "O", "B-LOC", "O"]]`

**Inputs**

tokens: `["Elon", "Musk", "lives", "in", "San", "Francisco", "."]`

tags: `["B-PER", "I-PER", "O", "O", "B-LOC", "I-LOC", "O"]`

**Outputs**

tokens: `["Judea", "Pearl", "lives", "in", "Tel", "Aviv", "."]`

tags: `["B-PER", "I-PER", "O", "O", "B-LOC", "I-LOC", "O"]`


Note that the entity types in the inputs need to align with the entity types of the corpus, e.g. the following `tokens` and `tags` will result in an error for the above-defined corpus as the entity mention (`headache`) of type `problem` does not align with the corpus (the corpus defined above only recognizes `PER`, `LOC` and `ORG`):

tokens:  `["She", "did", "not", "complain", "of", "headache", "."]`

tags: `["O", "O", "O", "O", "O", "B-problem", "O"]`

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