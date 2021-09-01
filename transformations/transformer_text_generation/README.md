# Transformer-based Text Generation
We use generative pretrained language model (e.g., GPT-2) to generate next word(s) in a sequence based on preceding word(s).

## What type of a transformation is this?
Given a generative pretrained language model, we generate next word(s) in a sequence based on the prefix of the original text. For SST-2 and IMDB datasets, the code points to fine-tuned models, respectively, ```jmamou/gpt2-medium-IMDB``` and ```jmamou/gpt2-medium-SST-2```.
In order to generate a sample preserving the label of the original sample, we fine-tuned ```gpt2-medium``` for labeled text generation tasks. If the sentiment label of the orignial text is not provided, we first run sentiment classification to get a pseudo-label using respectively, ```textattack/roberta-base-imdb``` and ```textattack/roberta-base-SST-2```.

In addition, we support general purpose text generation using ```gpt2-medium``` pretrained model.


## What tasks does it intend to benefit?
This transformation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation and text tagging. In addition, this approach has been successfully used to augment data for distillation.

```python evaluate.py -t TransformerTextGeneration -task TEXT_CLASSIFICATION```
```model_name = "textattack/roberta-base-SST-2" -d sst2```


## Previous Work
Our approach follows previous work on data augmentation for distillation
```bibtex
@inproceedings{tang-etal-2019-natural,
    title = "Natural Language Generation for Effective Knowledge Distillation",
    author = "Tang, Raphael  and
      Lu, Yao  and
      Lin, Jimmy",
    booktitle = "Proceedings of the 2nd Workshop on Deep Learning Approaches for Low-Resource NLP (DeepLo 2019)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D19-6122",
    doi = "10.18653/v1/D19-6122",
    pages = "202--208",
    abstract = "Knowledge distillation can effectively transfer knowledge from BERT, a deep language representation model, to traditional, shallow word embedding-based neural networks, helping them approach or exceed the quality of other heavyweight language representation models. As shown in previous work, critical to this distillation procedure is the construction of an unlabeled transfer dataset, which enables effective knowledge transfer. To create transfer set examples, we propose to sample from pretrained language models fine-tuned on task-specific text. Unlike previous techniques, this directly captures the purpose of the transfer set. We hypothesize that this principled, general approach outperforms rule-based techniques. On four datasets in sentiment classification, sentence similarity, and linguistic acceptability, we show that our approach improves upon previous methods. We outperform OpenAI GPT, a deep pretrained transformer, on three of the datasets, while using a single-layer bidirectional LSTM that runs at least ten times faster.",
}
```
