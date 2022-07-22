# Sentence reordering
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly shuffling sentencesin the input text with coreference resolution to reduce ambiguity.

Author name: Zijian Wang (zijwang@hotmail.com)

## What type of a transformation is this?
This transformation could shuffle sentence order in the input text, which could test model robustness.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation.

Benchmark results:

- Sentiment analysis: we run sentiment analysis on a 1% sample of the IMDB dataset. The original accuracy is 956 and the perturbed accuracy is 95.2.
- Text summarization: we run text summarization on a 1% sample of the xsum dataset. The original BLEU is 15.99 and the perturbed BLEU is 9.75.

## Related work

This is very similar to the `Sentence Permutation` noising method in the BART paper.

```bibtex
@inproceedings{lewis2020bart,
  title={BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension},
  author={Lewis, Mike and Liu, Yinhan and Goyal, Naman and Ghazvininejad, Marjan and Mohamed, Abdelrahman and Levy, Omer and Stoyanov, Veselin and Zettlemoyer, Luke},
  booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
  pages={7871--7880},
  year={2020}
}
```

The coreference resolution model is from the following paper

```bibtex
@inproceedings{lee2018higher,
  title={Higher-Order Coreference Resolution with Coarse-to-Fine Inference},
  author={Lee, Kenton and He, Luheng and Zettlemoyer, Luke},
  booktitle={Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers)},
  pages={687--692},
  year={2018}
}
```

We use its [AllenNLP implementation](https://demo.allennlp.org/coreference-resolution).


## What are the limitations of this transformation?

This transformation will only change the input text that has more than one sentence.

There are still cases where coref only could not handle. For example, there could be ellipsis problems as demonstrated by [this paper on narrative reordering](https://arxiv.org/pdf/2104.06669v1.pdf). We leave these as future work for simplicity.
