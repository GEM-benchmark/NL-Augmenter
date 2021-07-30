# Multi-lingual code-switch 🦎  + 📕 -> 🐍

Author name: Libo Qin, Fuxuan Wei, Tianbao Xie, Wanxiang Che, Yue Zhang

Author email: {lbqin, fuxuanwei, tianbaoxie, car}@ir.hit.edu.cn yue.zhang@wias.org.cn

Author Affiliation: Harbin Institute of Technology

## What type of a transformation is this?
This transformation can be seen as a data augmentation framework to generate multi-lingual code-switching data to fine-tune mBERT, which encourages model to align representations from source and multiple target languages once by mixing their context information.

## What tasks does it intend to benefit?
This alignment of different language it brought can benefit a massive of multi-lingual tasks.
As mentioned in the paper, we test this method on tasks including these multi-lingual tasks: 
Natural Language Inference, Sentiment Classification, Document Classification, Dialogue State Tracking (DST), Spoken Language Understanding
We perform t-test for all experiments to measure whether the results from the proposed model are significantly better than the baselines(mBERT and XLM).

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
@article{tan2021code,
  title={Code-Mixing on Sesame Street: Dawn of the Adversarial Polyglots},
  author={Tan, Samson and Joty, Shafiq},
  journal={arXiv preprint arXiv:2103.09593},
  year={2021}
}
```


3) MUSE bilingual dictionary:

```bibtex
@article{conneau2017word,
  title={Word translation without parallel data},
  author={Conneau, Alexis and Lample, Guillaume and Ranzato, Marc'Aurelio and Denoyer, Ludovic and J{\'e}gou, Herv{\'e}},
  journal={arXiv preprint arXiv:1710.04087},
  year={2017}
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