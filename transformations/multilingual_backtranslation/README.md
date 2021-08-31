## Multilingual backtranslation

This perturbation is very similar to [backtranslation](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/back_translation), significantly more general as it supports multilingual through backtranslation and supports backtranslation (back and forth) for up to 232 language codes and 201 unique languages. By this, it means that 201 languages has at least one other language paired with itself, such that there exists two MarianMT models, one for translating to the intermediate language and one for translating back to the original language.

## What type of a transformation is this?

As noted by the authors of the backtranslation module in this package, backtranslation can act as a light paraphraser and can act beneficially for many tasks, in particular text classification.

## Previous Work
Zhenhao Li and Lucia Specia. 2019.  Improving neural machine translation robustness via data augmentation:  Beyond backtranslation.
Amane Sugiyama and Naoki Yoshinaga. 2019.   Data augmentation using back-translation for context-aware neural machine translation.
Xie Q. et al. 2020. Unsupervised Data Augmentation for Consistency Training

## Reference to the models

The models used here are produced and uploaded by [HELSINKI-NLP](https://huggingface.co/Helsinki-NLP).

## Important note regarding the quality

Since a lot of models here are made available, the quality has not been ensured for all the models. It should be noted that a quality check should perhaps be made before using this on a large scale when using a new language pairing.