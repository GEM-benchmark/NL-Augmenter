# Emojify 🦎  + ⌨️ → 🐍

This transformation augments the input sentence by swapping words into emojis with similar meanings.
For example, it changes word `"movie"` to emoji `"🎬"`.

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
"Oh, and their spring rolls and the accompanying peanuts and hot sauces were also delicious."

⬇

"Oh, and their 🌱 🧻 and the accompanying 🥜 and 🌡️ sauces were also 😋."
```

## What tasks does it intend to benefit?

This transformation would benefit all tasks that use sentence/paragraph/document as input, such as text classification, summarization, and question answering.

```shell
python evaluate.py -t EmojifyTransformation -task TEXT_CLASSIFICATION --model "aychang/roberta-base-imdb"
```

The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") on a subset of IMDB sentiment dataset = 96.0%.
The accuracy of the same model on the perturbed set = 95.0%.

## Data and code provenance

We create the english-to-emoji dictionary `emoji_dict.json` based on the open-source project (MIT license) [emojilib](https://github.com/muan/emojilib).
We write the transformation code from scratch for NL-Augmenter.

## Previous Work

Emojis, introduced in 1997 as a set of pictograms used in digital messaging, have been deeply integrated into our everyday communication.
More than 10% of tweets and more than 35% of Instagram posts include one or more emojis in 2015 (Cruse, 2015; Instagram Engineering, 2015).
Given the ubiquitousness of emojis, there is a growing body of work researching the linguistic and cultural aspects of emojis (Chandra Guntuku et al., 2019) and how we can leverage the use of emojis to help solve NLP tasks (Eisner et al., 2016).
Recently, researchers have also developed an emoji-based benchmark to evaluate large language model's understanding of emojis ([Big Bench](https://github.com/google/BIG-bench/tree/56a2db6a8d27151401c2a6cb677f54e2252d3ae5/bigbench/benchmark_tasks/emoji-movie)).
However, to our best knowledge, there is no prior work that evaluates NLP model robustness by changing English words to their corresponding emojis.

- Chandra Guntuku, S., Li, M., Tay, L., & Ungar, L. H. (2019). Studying Cultural Differences in Emoji Usage across the East and the West. Proceedings of the International AAAI Conference on Web and Social Media, 13(01), 226–235.
- Cruse, J. (2015, November 18). Emoji usage in TV conversation. https://blog.twitter.com/en_us/a/2015/emoji-usage-in-tv-conversation.html
- Eisner, B., Rocktäschel, T., Augenstein, I., Bosnjak, M., & Riedel, S. (2016). emoji2vec: Learning Emoji Representations from their Description. Proceedings of The Fourth International Workshop on Natural Language           Processing for Social Media, 48–54. https://doi.org/10.18653/v1/W16-6208
- Instagram Engineering. (2015, May 1). Emojineering Part 1: Machine Learning for Emoji Trends. https://instagram-engineering.com/emojineering-part-1-machine-learning-for-emoji-trendsmachine-learning-for-emoji-trends-7f5f9cb979ad

## What are the limitations of this transformation?

- The one-to-one mapping between English words and emojis is not perfect, due to the complexity of English words.
- We translate English word to emoji word by word. This design choice is likely to make mistakes when translating compound words. For example, the words `"spring roll"` is currently translated to `"🌱 🧻"`.
- The emoji version in our dataset is at [version 13.0](https://emojipedia.org/emoji-13.0/). Newer emojis such as `😵‍💫` and `❤️‍🩹` (from [version 13.1](https://emojipedia.org/emoji-13.1/)) are not included in this transformation.
