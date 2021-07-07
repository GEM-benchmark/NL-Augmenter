# Mix-Transliteration 🦎  + ⌨️ → 🐍

This transformation converts randomly picks words in the text from their original script to their corresponding english transliteration.
It can be used to train/test multilingual models to improve/evaluate their ability to understand complete or partially transliterated text.

Author name: Tanay Dixit, Mukund Varma T
Author email: tanay.dixit@smail.iitm.ac.in, mukundvarmat@gmail.com

## What type of a transformation is this?

In this transformation we randomly pick words (at least one word in a foreign script) and transliterate it to the English script. 
This ensures that the languages in the input sentence remains the same but is represented differently to expose the model to diverse samples.
Given that Indian languages have diverse scripts (eg: Devanagari, Bengali, Gurmukhi, etc), we choose to transliterate between indic languages using [indic-trans](https://github.com/libindic/indic-trans).

The following are some representative examples:

    Input: कितने साल के हो
    Transformed text: kitne saal ke ho

    Input: உங்களைப் பார்த்து நிறைய நாட்கள் ஆகிவிட்டது
    Transformed text: ungalai paarttu niraiya naatkal aaki vittathu

    Input: My name is Tom और मैं लंदन में रहता हूँ
    Transformed text: My name is Tom aur main landan mein rahata hoon


## What tasks does it intend to benefit?

Multi-lingual datasets generally contain skewed distributions of data across languages, which arises due to the variability in the number of native speakers of a language.
Since the input language remains the same in the transformed text, this transformation can help increase the number of samples (per language) in a multi-lingual corpora. 
Additionally, it might also be interesting to evaluate multi-lingual models on transliterated text to evaluate their understanding of a given language irrespective of its representation.

## Previous Work

There have been attempts to convert all input languages to a common transliterated representation before training multi lingual models for various tasks (Datta et. al). 
This has improved performance by enabling the model to learn a language-agnostic representation. 
This suggests that the same can be used to augment/test multi-lingual models to improve/evaluate their capacity to understand various languages irrespective of its representation. 

## Citations

```bibtex
@inproceedings{Bhat:2014:ISS:2824864.2824872,
    author = {Bhat, Irshad Ahmad and Mujadia, Vandan and Tammewar, Aniruddha and Bhat, Riyaz Ahmad and Shrivastava, Manish}, 
    title = {IIIT-H System Submission for FIRE2014 Shared Task on Transliterated Search}, 
    booktitle = {Proceedings of the Forum for Information Retrieval Evaluation}, 
    series = {FIRE '14}, year = {2015}, 
    isbn = {978-1-4503-3755-7}, location = {Bangalore, India}, 
    pages = {48--53}, numpages = {6}, 
    url = {http://doi.acm.org/10.1145/2824864.2824872}, 
    doi = {10.1145/2824864.2824872}, 
    acmid = {2824872}, 
    publisher = {ACM}, 
    address = {New York, NY, USA}, 
    keywords = {Information Retrieval, Language Identification, Language Modeling, Perplexity, Transliteration},
}
```

```bibtex
@misc{datta2020languageagnostic,
    title={Language-agnostic Multilingual Modeling}, 
    author={Arindrima Datta and Bhuvana Ramabhadran and Jesse Emond and Anjuli Kannan and Brian Roark},
    year={2020},
    eprint={2004.09571},
    archivePrefix={arXiv},
    primaryClass={eess.AS}
}
```

## What are the limitations of this transformation?
The accuracy of the transformation is limited to implementation of the transliterated system and certain spelling discrepancies may exist.
We are assuming that there exists at least one foreign script word in the given input text.