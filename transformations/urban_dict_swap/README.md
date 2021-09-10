# Urban Thesaurus Swap
This perturbation randomly picks nouns from the input source to convert to related terms drawn from the
[Urban Dictionary](https://www.urbandictionary.com/) resource.

Author name: Richard Plant

Author email: r.plant@napier.ac.uk

Author Affiliation: Edinburgh Napier University

## What type of a transformation is this?
This transformation can be applied to an input text to produce semantically-similar output texts in order to generate
more robust test sets. We first select nouns at random, then query the Urban Thesaurus website to obtain a list of
related terms to swap in.

## What tasks does it intend to benefit?
This perturbation is intended to benefit tasks with a sentence/document input for which the researcher desires an
expanded test set to evaluate robustness.

## Robustness Evaluation

Automatic evaluation was carried out using the 
[`evaluate.py`](https://github.com/GEM-benchmark/NL-Augmenter/blob/main/evaluate.py) script with the following models. 
All evaluations carried out for the Text Classification task type. 

For more evaluation details, please see [here](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/evaluation).

| Transformation              | roberta-base-SST-2   | bert-base-uncased-QQP   | roberta-large-mnli   | roberta-base-imdb   |
|:----------------------------|:---------------------|:------------------------|:---------------------|:--------------------|
| UrbanThesaurusSwap          | 94.0->92.0 (-2.0)    | 92.0->90.0 (-2.0)       | 91.0->90.0 (-1.0)    | 95.0->94.0 (-1.0)   |

## Previous Work

This transformation relies on the [Urban Thesaurus](https://urbanthesaurus.org/) website.

Prior research leveraging Urban Dictionary:

[Wilson et al. (2020)](https://aclanthology.org/2020.lrec-1.586/)
```bibtex
@inproceedings{wilson-etal-2020-urban,
    title = "Urban Dictionary Embeddings for Slang {NLP} Applications",
    author = "Wilson, Steven  and
      Magdy, Walid  and
      McGillivray, Barbara  and
      Garimella, Kiran  and
      Tyson, Gareth",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.586",
    pages = "4764--4773",
    abstract = "The choice of the corpus on which word embeddings are trained can have a sizable effect on the learned representations, the types of analyses that can be performed with them, and their utility as features for machine learning models. To contribute to the existing sets of pre-trained word embeddings, we introduce and release the first set of word embeddings trained on the content of Urban Dictionary, a crowd-sourced dictionary for slang words and phrases. We show that although these embeddings are trained on fewer total tokens (by at least an order of magnitude compared to most popular pre-trained embeddings), they have high performance across a range of common word embedding evaluations, ranging from semantic similarity to word clustering tasks. Further, for some extrinsic tasks such as sentiment analysis and sarcasm detection where we expect to require some knowledge of colloquial language on social media data, initializing classifiers with the Urban Dictionary Embeddings resulted in improved performance compared to initializing with a range of other well-known, pre-trained embeddings that are order of magnitude larger in size.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

## What are the limitations of this transformation?

This transformation relies on the information returned by the Urban Thesaurus website, which is dependent on the
reliability of the Urban Dictionary. As a crowdsourced resource, this may be extremely variable.

The returned terms are also not always direct synonyms. Setting a confidence score threshold should mitigate this
somewhat, since higher-scoring terms are expected to be more relevant to the query term. However, while semantic
similarity should be preserved, this cannot be guaranteed.

Since the Urban Dictionary contains a great deal of profanity and offensive content, care should be taken with results.