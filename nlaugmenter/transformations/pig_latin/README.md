# Pig Latin cipher :nose: → :pig_nose:
This transformation translates the original text into pig latin.
Pig Latin is a well-known deterministic transformation of English words, and can be viewed as a cipher which can be deciphered by a human with relative ease. The resulting sentences are completely unlike examples typically used in language model training. As such, and in a similar fashion to the Simple Ciphers augmentation, this augmentation change the input into inputs which are difficult for a language model to interpret, while being relatively easy for a human to interpret.

Authors:

Nicholas Roberts nick11roberts@cs.wisc.edu Vinay Prabhu vinay@unify.id Sang Han sanghan@protonmail.com Ryan Teehan rsteehan@gmail.com

## What type of a transformation is this?
This transformation modifies text by translating it into Pig Latin, which makes the input sequence much harder for a language model to interpret, while maintaining meaning and ease-of-decipherability by a human. In other words, no information is lost. In order for a language model to be robust to translation to Pig Latin, it must tolerate significant (yet consistent and deterministic) word-level manipulations. On the other hand, many of the characters constituting the Pig Latin translation of each word remain the same, albeit in a different order or with additional characters. This in turn suggests that the choice of character/subword/word-level tokenization may play an important role in robustness to Pig Latin translation. Notably, this is distinct from simply translating English sentences to another language, as it would be reasonable to expect an English-speaking human annotator to ascertain the meaning of a sentence in Pig Latin.

[The rules of Pig Latin can be found here!](https://en.wikipedia.org/wiki/Pig_Latin)

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Previous Work
[Google Voice Search works when speaking in Pig Latin. ](https://ai.googleblog.com/2011/04/ig-pay-atin-lay-oice-vay-earch-say.html)

## What are the limitations of this transformation?
Pig Latin is a relatively simple transformation, but deciphering the resulting sentences requires knowledge of its rules as well as of consonants and vowels. Large enough datasets may contain examples of Pig Latin.

## Evaluation

Using the same evaluation procedure as shown in [the leaderboard](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/evaluation), text classification models are substantially less robust to the PigLatin transform than all of the leading transformations for evaluating robustness.

| Transformation              | roberta-base-SST-2   | bert-base-uncased-QQP   | roberta-large-mnli   | roberta-base-imdb   |
|:----------------------------|:---------------------|:------------------------|:---------------------|:--------------------|
| **PigLatin**       | **94.0->60.0 (-34.0)**   | **92.0->68.0 (-24.0)**      | **91.0->50.0 (-41.0)**   | **95.0->32.0 (-63.0)**  |
| BackTranslation             | 94.0->91.0 (-3.0)    | 92.0->90.0 (-2.0)       | 91.0->87.0 (-4.0)    | 95.0->92.0 (-3.0)   |
| ButterFingersPerturbation   | 94.0->89.0 (-5.0)    | 92.0->89.0 (-3.0)       | 91.0->88.0 (-3.0)    | 95.0->93.0 (-2.0)   |
| ChangePersonNamedEntities   | 94.0->94.0 (0.0)     | 92.0->92.0 (0.0)        | 91.0->89.0 (-2.0)    | 95.0->95.0 (0.0)    |
| CloseHomophonesSwap         | 94.0->91.0 (-3.0)    | 92.0->88.0 (-4.0)       | 91.0->89.0 (-2.0)    | 95.0->96.0 (1.0)    |
| DiscourseMarkerSubstitution | 94.0->94.0 (0.0)     | 92.0->92.0 (0.0)        | 91.0->91.0 (0.0)     | 95.0->95.0 (0.0)    |
| MixedLanguagePerturbation   | 94.0->90.0 (-4.0)    | 92.0->86.0 (-6.0)       | 91.0->86.0 (-5.0)    | 95.0->91.0 (-4.0)   |
| PunctuationWithRules        | 94.0->94.0 (0.0)     | 92.0->92.0 (0.0)        | 91.0->91.0 (0.0)     | 95.0->90.0 (-5.0)   |
| ReplaceNumericalValues      | 94.0->94.0 (0.0)     | 92.0->92.0 (0.0)        | 91.0->90.0 (-1.0)    | 95.0->95.0 (0.0)    |
| SentenceReordering          | 94.0->95.0 (1.0)     | 92.0->93.0 (1.0)        | nan                  | 95.0->94.0 (-1.0)   |