## polarity filter

## What type of a filter is this?

This filter filters a transformed text if it does not retain the same polarity as an original text.

Author: Maria Obedkova

## Why is measuring performance on this split important?

This filter helps not to distort training data during augmentation for sentiment analysis-related tasks.
While generating new data for a sentiment analysis task, it is important to make sure that generated data is labelled correctly.
If a newly generated example does not retain the same polarity as an original one, we might want to exclude it from the final training data or relabel it.

Especially, when dealing with distributional approaches for data augmentation, it is crucial to check if polarity does not shift on generated examples.
This filter helps to identify those polarity-changing transformations.

## Related Work

[spaCyTextBlob](https://github.com/SamEdwardes/spaCyTextBlob)

## What are the limitations of this filter?

This filter purely relies on polarity scores provided by the TextBlob library.
OOV words and inconsistent polarity scoring may occur.

The current implementation works only for English but potentially this filter can be extended to other languages with libraries like
[textblob-de](https://textblob-de.readthedocs.io/en/latest/), [textblob-fr](https://github.com/sloria/textblob-fr), etc.