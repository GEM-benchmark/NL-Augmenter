# Token Replacement Based on Lookup Tables 🦎+ ⌨️ → 🐍
This transformation replaces input tokens with their perturbed versions sampled from a given lookup table of replacement candidates. Lookup tables containing OCR errors and misspellings from prior work are given as examples. Thus, by default, the transformation induces plausible OCR errors and human typos to the input sentence.

Author: [Marcin Namysl](https://github.com/mnamysl/) (m.namysl@gmail.com)

## What type of transformation is this?
This transformation acts like a token-level perturbation. Multiple variations can be easily created via changing parameters or using custom lookup tables. Moreover, multiple lookup tables can be merged together to increase the coverage of available perturbations and consequently the variance of the output.

By default, only the replacement candidates that differ by one edit operation from the original token are taken into account, which already causes large drops in performance of the baseline models (cf. the results of the robustness evaluation in the next section). The replacement probability, the maximum edit distance to the original token, and the minimum length of the original token to be perturbed are the parameters that can be customized by the user.

The default lookup tables already offer fairly large coverage (over 100,000 words). Alternative lookup tables that cover a larger number of words could be easily employed. Moreover, application for languages other than English or in a multi-lingual setting is straightforward. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. It could be used for robustness evaluation as well as for data augmentation.

As a result of applying this transformation, the following preliminary results of the robustness evaluation were obtained:

- The accuracy of the RoBERTa model ("*aychang/roberta-base-imdb*"), evaluated on a subset of 1000 examples from the IMDB sentiment dataset, dropped from 96.0 (original examples) to 55.0 (perturbed examples).
- The average BLEU score of the DistilBART model ("*sshleifer/distilbart-xsum-12-6*"), evaluated on a subset (10%) of XSum dataset, dropped from 15.25 (original examples) to 7.08 (perturbed examples).

## Previous Work

1) The transformation is an adapted and improved version of the lookup table-based noise induction method from the [Noise-Aware Training (NAT) project](https://github.com/mnamysl/nat-acl2020). 

```bibtex
@inproceedings{namysl-etal-2020-nat,
    title = "{NAT}: Noise-Aware Training for Robust Neural Sequence Labeling",
    author = {Namysl, Marcin  and
      Behnke, Sven  and
      K{\"o}hler, Joachim},
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.138",
    doi = "10.18653/v1/2020.acl-main.138",
    pages = "1501--1517",
}
```

2) [ocr.xz](./ocr.xz) is a lookup table created based on 10 million sentences that were sampled from the [1 Billion Word Language Model Benchmark](https://www.statmt.org/lm-benchmark/). As the lookup table  was originally used in the [Noise-Aware Training (NAT) v2](https://github.com/mnamysl/nat-acl2021) project, it covers all tokens from the [CoNLL 2003](https://www.clips.uantwerpen.be/conll2003/ner/) and the [UD English EWT](https://universaldependencies.org/treebanks/en_ewt/index.html) benchmarks. All replacement candidates were ranked based on the edit distance to the corresponding original tokens and the top 100 candidates with the smallest distance were selected. Finally, the dictionary was stored in JSON format and compressed using the [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) algorithm.

```bibtex
@inproceedings{namysl-etal-2021-empirical,
    title = "Empirical Error Modeling Improves Robustness of Noisy Neural Sequence Labeling",
    author = {Namysl, Marcin  and
      Behnke, Sven  and
      K{\"o}hler, Joachim},
    booktitle = "Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.findings-acl.27",
    doi = "10.18653/v1/2021.findings-acl.27",
    pages = "314--329",
}
```

3) [typos.xz](./typos.xz) is a lookup table from the [moe - Misspelling Oblivious Word Embeddings](https://github.com/facebookresearch/moe) project released under the [Attribution-NonCommercial 4.0 International license](https://github.com/facebookresearch/moe/blob/master/LICENSE) ([CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)). Due to the large size of the original data, we performed deduplication and filtered all non-English words using the [NLTK](https://www.nltk.org/)'s dictionary. Finally, the replacement candidates were subsampled by keeping up to 100 entries for each token.

```bibtex
@inproceedings{piktus-etal-2019-misspelling,
    title = "Misspelling Oblivious Word Embeddings",
    author = "Piktus, Aleksandra  and
      Edizel, Necati Bora  and
      Bojanowski, Piotr  and
      Grave, Edouard  and
      Ferreira, Rui  and
      Silvestri, Fabrizio",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/N19-1326",
    doi = "10.18653/v1/N19-1326",
    pages = "3226--3234",
}
```


## What are the limitations of this transformation?
The coverage of the default lookup tables could be suboptimal in the scenarios, where many numerical values or domain-specific vocabularies are used (e.g., Mathematics, Medicine, Chemistry, Law, etc.).
