# Emojify 🦎  + ⌨️ → 🐍

This transformation augments the input sentence by swapping words into emojis with similar meanings.
For example, it changes word `movie` to emoji `🎬`.

Author name: Zijie J. Wang

Author email: jayw@gatech.edu

Author Affiliation: Georgia Tech

## What type of a transformation is this?

This transformation acts like a translation to test language models' robustness and generalizability.
In this context, we are translating English words into Emoji unicode.
The transformed sentence has similar structure and semantics to the source sentence.

Some examples:

```
"Apple is looking at buying U.K. startup for $132 billion."

⬇

"🍎 is 👀 at 🛍️ 🇬🇧 startup for $1️⃣3️⃣2️⃣ billion."
```

```
"The quick brown fox jumps over the lazy dog."

⬇

"The quick 🟤 🦊 jumps over the lazy 🐕."
```

```
"Oh, and their movie rolls and the accompanying peanuts and hot sauces were also delicious."

⬇

"Oh, and their 🌱 🧻 and the accompanying 🥜 and 🌡️ sauces were also 😋."
```

## What tasks does it intend to benefit?

This transformation would benefit all tasks that use sentence/paragraph/document as input, such as text classification and question answering.


```python evaluate.py -t ButterFingersPerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6") 
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of same model on the pertubed set = 11.9221

## Previous Work

TODO

## What are the limitations of this transformation?

TODO
