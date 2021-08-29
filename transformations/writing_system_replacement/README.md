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
3. The output is the text in the new writing system. In out example, it's '蚴蘋䗑'

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

As a useful side effect, it could help to decipher the [Voynich manuscript](https://en.wikipedia.org/wiki/Voynich_manuscript),
the [Phaistos Disc](https://en.wikipedia.org/wiki/Phaistos_Disc), and other undeciphered artifacts.

## What are the limitations of this transformation?

If the input text is too short, the transformed text will not contain enough information 
to identify the language of the original text. 
For example, there is not enough information to decipher '驿掩㑇㕶誨', 
where each word of the original English input was replaced with a random CJK ideograph.
Thus, for language identification purposes, we would suggest inputs of 1000 characters or more. 