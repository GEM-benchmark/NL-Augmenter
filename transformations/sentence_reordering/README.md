# Sentence reordering
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly shuffling sentences in the input text.

Author name: Zijian Wang (zijwang@hotmail.com)

## What type of a transformation is this?
This transformation could shuffle sentence order in the input text, which could test model robustness. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation. 

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


## What are the limitations of this transformation?

This transformation will only change the input text that has more than one sentence.