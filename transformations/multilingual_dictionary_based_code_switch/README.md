# Multi-lingual code-switch 🦎  + 📕 -> 🐍

Author name: Libo Qin, Fuxuan Wei, Tianbao Xie, Wanxiang Che, Yue Zhang

Author email: {lbqin, fuxuanwei, tianbaoxie, car}@ir.hit.edu.cn, yue.zhang@wias.org.cn

Author Affiliation: Harbin Institute of Technology

## What type of a transformation is this?
This transformation can be seen as a data augmentation framework to generate multi-lingual code-switching data to fine-tune mBERT, which encourages model to align representations from source and multiple target languages once by mixing their context information.

## What tasks does it intend to benefit?
This alignment of different language it brought can benefit a massive of multi-lingual tasks.
As mentioned in the paper, we test this method on tasks including these multi-lingual tasks: 
Natural Language Inference, Sentiment Classification, Document Classification, Dialogue State Tracking (DST), Spoken Language Understanding
We perform t-test for all experiments to measure whether the results from the proposed model are significantly better than the baselines(mBERT and XLM).

## What are the limitations of this transformation?
It is worth noticing that words in the source language can have multiple translations in the target language. In this case, we randomly choose any of the multiple translations as the replacement target language word. Though we cannot guarantee that this is the correct word-to-word translation in the context, we can consider it as one of the data augmented strategy for our tasks. This is verified by our work (CoSDA-ML) [1] and Code-Mixing on Sesame Street [2].

## Previous Work
1) CoSDA-ML: Multi-Lingual Code-Switching Data Augmentation  for Zero-Shot Cross-Lingual NLP

```bibtex
@inproceedings{ijcai2020-533,
  title     = {CoSDA-ML: Multi-Lingual Code-Switching Data Augmentation  for Zero-Shot Cross-Lingual NLP},
  author    = {Qin, Libo and Ni, Minheng and Zhang, Yue and Che, Wanxiang},
  booktitle = {Proceedings of the Twenty-Ninth International Joint Conference on
               Artificial Intelligence, {IJCAI-20}},
  publisher = {International Joint Conferences on Artificial Intelligence Organization},
  editor    = {Christian Bessiere},
  pages     = {3853--3860},
  year      = {2020},
  month     = {7},
  note      = {Main track}
  doi       = {10.24963/ijcai.2020/533},
  url       = {https://doi.org/10.24963/ijcai.2020/533},
}

```

2) Code-Mixing on Sesame Street:

```bibtex
@inproceedings{tan-joty-2021-code-mixing,
    title = "Code-Mixing on Sesame Street: Dawn of the Adversarial Polyglots",
    author = "Tan, Samson  and
      Joty, Shafiq",
    booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jun,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.naacl-main.282",
    doi = "10.18653/v1/2021.naacl-main.282",
    pages = "3596--3616",
    abstract = "Multilingual models have demonstrated impressive cross-lingual transfer performance. However, test sets like XNLI are monolingual at the example level. In multilingual communities, it is common for polyglots to code-mix when conversing with each other. Inspired by this phenomenon, we present two strong black-box adversarial attacks (one word-level, one phrase-level) for multilingual models that push their ability to handle code-mixed sentences to the limit. The former uses bilingual dictionaries to propose perturbations and translations of the clean example for sense disambiguation. The latter directly aligns the clean example with its translations before extracting phrases as perturbations. Our phrase-level attack has a success rate of 89.75{\%} against XLM-R-large, bringing its average accuracy of 79.85 down to 8.18 on XNLI. Finally, we propose an efficient adversarial training scheme that trains in the same number of steps as the original model and show that it creates more language-invariant representations, improving clean and robust accuracy in the absence of lexical overlap without degrading performance on the original examples.",
}
```


3) MUSE bilingual dictionary:

```bibtex
@inproceedings{
lample2018word,
title={Word translation without parallel data},
author={Guillaume Lample and Alexis Conneau and Marc'Aurelio Ranzato and Ludovic Denoyer and Hervé Jégou},
booktitle={International Conference on Learning Representations},
year={2018},
url={https://openreview.net/forum?id=H196sainb},
}
```
4) The idea of learning a mapping function from a source contextualized subword embedding to its target counterpart by using word alignment information

```bibtex
@inproceedings{wang2019cross,
  title={Cross-Lingual BERT Transformation for Zero-Shot Dependency Parsing},
  author={Wang, Yuxuan and Che, Wanxiang and Guo, Jiang and Liu, Yijia and Liu, Ting},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
  pages={5721--5727},
  year={2019}
}
```
