# British to American English and vice versa translation
Author name: Aman Srivastava (amanit0812@gmail.com)

## What type of transformation is this?
This transformation takes a sentence and converts it from british english to american english and vice-versa.
It supports following scenarios:-
* Sentences with British English words :arrow_right: To American English
* Sentences with American English words :arrow_right: To British English
* Sentences with both American English and British English words :arrow_right: Translates American English words to British English words and vice versa.

```
Examples:
1. I Love Pastel Colours > I Love Pastel Colors
2. Carry encyclopedia on vacation > Carry encyclopaedia on holiday
```

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Previous Work and References
Hyperreality - American-British-English-Translator -> Its a command line tool for translation. Master Dictionaries have been taken from here.

## What are the limitations of this transformation?
There is no set standard dictionary available to fetch all the permutations and combinations.


## Robustness Evaluation:-

Evaluation Result 1:-

model: `sshleifer/distilbart-xsum-12-6` <br>
split: `20%` <br>
dataset: `xsum` <br>

| Sentence Type | Predicted BELU Score|
|--------------------|------|
|Original Dataset | 14.877283 |
|Transformed Dataset| 14.489393|