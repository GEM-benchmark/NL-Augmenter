# Writing System Replacement ❤️ → 心
This transformation replaces the writing system of the input with another writing system.

Author: Roman Sitelew (sitelewr at gmail dot com)

A few snippets of the code are based on the code from the
[whitespace_perturbation transformation](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/whitespace_perturbation),
authored by Xinyi Wu, and released under the same license (MIT) as the rest of the NL-Augmenter project.

## What type of a transformation is this?
It's a novel transformation that works as follows:

1. There is an input sentence (e.g. "I love potatoes")
2. A new random writing system is generated. For example, a logographic system where the word "love" is written as "蘋"
3. The output is the text in the new writing system. In our example, it's '蚴蘋䗑'

We use [CJK Unified Ideographs](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs)
as the source of characters for the generated writing systems.

Thanks to the enormous diversity of the CJK ideographs (tens of thousands of characters),
we can generate thousands of different writing systems, without running out of characters.

Currently, this transformation can convert the input into the following writing systems:

|writing system type | some real-world languages that use it | "I love potatoes" (a sample output in a generated writing system)      |
|---------------  | ------------------------------------  | -------------------------------------- |
|alphabet         | English, Spanish, Russian             | 之 笓䒉㘔䆇 躓䒉蝲討蝲䒉䆇䁣             |
|syllabary        | Mycenaean Greek, Japanese             | 䃓 熵鏘 㚐料                           |
|partial phonemic | Hebrew,  Arabic                       | 阠㚶乍 渓绌敿                          |
|logographic      | Ancient Egyptian, Oracle bone script  | 驿掩㑇㕶誨                             |

The transformation accepts any textual input, regardless of its language.

## What tasks does it intend to benefit?
This transformation could benefit text classification tasks (especially - language identification tasks).

Trained humans are able to read texts that are written in different writing systems.
For example, Japanese speakers can easily identify these texts as Japanese, and understand their meaning
(all 3 means "hiragana"):

    平仮名
    ひらがな
    ヒラガナ

The ability of ML models to identify and understand a language written in various writing systems could
improve the quality of language identification in general,
and the quality of identification of low-resource languages in particular.

## Robustness Evaluation

We've evaluated this transformation by running the built-in evaluate.py script as follows:
`python3 evaluate.py -t WritingSystemReplacement`

Note: it seems that there is a bug in
[this line](https://github.com/GEM-benchmark/NL-Augmenter/blob/f0111c1587cfa36cd4bd2c9739744e59c2796c26/TestRunner.py#L132)
in TestRunner.py, making the script crash during any test,
which we temporally fixed by replacing the line's right side with `str(package_dir.parent.joinpath(search))`

To speed up the test, we also removed all other transformations from the local NL-Augmenter/transformations dir.

The results of the single run are as follows:

```
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
The accuracy on this subset which has 1000 examples = 96.0
Applying transformation:
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [00:19<00:00, 51.83it/s]
Finished transformation! 1000 examples generated from 1000 original examples, with 1000 successfully transformed and 0 unchanged (1.0 perturb rate)
Here is the performance of the model on the transformed set
The accuracy on this subset which has 1000 examples = 100.0

```

The performance is surprisingly good, considering the dramatic changes made by our transformation.
We are not sure if the results make sense.

According to @Sotwi, in the 3 non-default tests the performance falls significantly, as expected:

    roberta-base-SST-2: 94.0 -> 51.0
    bert-base-uncased-QQP: 92.0 -> 67.0
    roberta-large-mnli: 91.0 -> 43.0

This indicates that both the transformation and the testing pipeline work as intended.

We speculate that the problem in the first test could be caused by some deficiency in
the model `aychang/roberta-base-imdb` and / or the `imdb` dataset.

## What are the limitations of this transformation?

If the input text is too short, the transformed text will not contain enough information
to identify the language of the original text.
For example, if the input is `I love love love`, the output could look like this `人乇乇乇`.
In this example, each unique word was replaced with a randomly selected CJK ideograph.
But no AI could reliably predict the original language from `人乇乇乇`, as almost no linguistic data are preserved
in such a short text.

Thus, for language identification purposes, we would suggest inputs of at least 1k characters.

If the text is long enough, even the meaning could be recovered from the transformed / encrypted text,
e.g. by using standard cryptographic methods.
For example, imagine that the input `I love potatoes... [many more chars after that]`
was transformed into another alphabet like this: `了 乚凸丫丯 尸凸亍人亍凸丯乙...`.
While analyzing the output, one may notice that the character `凸` is very frequent,
and thus might be a common letter (in this case, `o`), making the rest of the decryption process much easier.
We speculate that if a trained cryptographer can extract the meaning from such a ciphertext,
then a language model could do it too.

For the meaning to be reliably recoverable, we would suggest inputs of at least 10k characters.

As @tia-e pointed out, the transformation doesn't fully preserve the syntax of the input.
For example, our transformation sometimes generates writing systems that don't have separators between words
(similarly to Classical Greek, Thai, etc.).
Depending on the generated writing system, a single character could be replaced with several new characters,
and the other way around.
This could make it significantly harder to extract the meaning from the transformed text.

## Future work

It would be interesting to add other types of writing systems, including logosyllabaries, alphasyllabaries, and
the writing systems for sign languages.
Some conlangs (especially, [Ithkuil](https://en.wikipedia.org/wiki/Ithkuil))
could be a great inspiration for further additions.

As suggested by @tia-e, we would like to provide a way to support transformation in the both directions,
with the ability to define the source and the target writing system
(currently, the target system is selected at random, regardless of the source system).

This transformation could help to decipher
the [Voynich manuscript](https://en.wikipedia.org/wiki/Voynich_manuscript),
the [Phaistos Disc](https://en.wikipedia.org/wiki/Phaistos_Disc),
and other undeciphered artifacts.

It could be accomplished as follows:
0. create a corpus featuring hundreds of languages
1. apply this transformation to the corpus' texts, thus obfuscating their writing systems, greatly expanding the corpus
2. train a model on the corpus, to make it capable of identifying the language regardless of the writing system
3. apply the transformation to, say, the Voynich manuscript
4. use the model to predict the language of the transformed manuscript
5. verify the prediction by translating the manuscript as if it was written in the predicted language