# Shuffle within segments
Shuffle within segments (SiS): We first split the token sequence into segments of the same label. Thus, each segment corresponds to either a mention or a sequence of out-of-mention tokens. For example, a sentence `She did not complain of headache or any other neurological symptoms .` with tags `O O O O O B-problem O B-problem I-problem I-problem I-problem O` is split into five segments: [She did not complain of], [headache], [or], [any other neurological symptoms], [.]. Then for each segment, we use a binomial distribution to randomly
decide whether it should be shuffled. If yes, the order of the tokens within the segment is shuffled while the label order is kept unchanged.

The source of the idea: https://arxiv.org/abs/2010.11683

## What type of a transformation is this?
This transformation shuffles the tokens in the sentence without breaking the sequences of the labels.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, and most importantly, a tagging task.
This would help augment data for a NER task by keeping the labels still aligned.

## What are the limitations of this transformation?
It is possible that shuffling could change the meaning of the sentence, the meaning the entity itself or have negative effect for NLU tasks.

## Evaluation

Here is the performance of the model dslim/bert-base-NER on the test[:20%] split of the 

Dataset({
    features: ['id', 'tokens', 'pos_tags', 'chunk_tags', 'ner_tags'],
    num_rows: 691
})

The average accuracy on a subset of conll2003 = 81.3640468775567

The average accuracy on its perturbed set = 70.13742999132477

## Previous Work
This perturbation is adapted from the following paper:
```
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
}
```