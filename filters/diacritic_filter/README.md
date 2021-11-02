## Diacritics filter

## What type of a filter is this?

This filter checks whether any character in the sentence has a diacritic.

From Merriam-Webster: Diacritics are marks placed above or below (or sometimes next to) a letter in a word to indicate a particular pronunciation -- in regard to accent, tone, or stress — 
as well as meaning, especially when a homograph exists without the marked letter or letters. For example, pâte refers to clay whereas pate refers to the head, 
and résumé or resumé is used for a work history versus resume, which means "to begin again."

Author: Vikas Raunak (viraunak@microsoft.com)

## Why is measuring performance on this split important?
Neural Sequence models have discrete vocabularies and commonly use subword segmentation techniques to achieve an ‘open vocabulary.’ [1] 
This filter can be used to create splits of the dataet where the sentences have diacritics.
Accented characters are typically among the rarer characters (& will likely result in different subword representations) and checking the model performance on such a split would be useful with respect to model robustness.

## Related Work

[1] Robust Open-Vocabulary Translation from Visual Text Representations https://arxiv.org/pdf/2104.08211.pdf

## What are the limitations of this filter?
For the intended purpose of filtering sentences with diacritics, it doesn't have any limitations (unless Python2 is used!).
