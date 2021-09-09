# Diacritic Removal 
This perturbation removes the diacritics on characters in a sentence.

# What are Diacritics?

From Merriam Webster: Diacritics are marks placed above or below (or sometimes next to) a letter in a word to indicate a particular pronunciation — in regard to accent, tone, or stress — as well as meaning, especially when a homograph exists without the marked letter or letters. 

For example, the breve ( ˘ ) is the rounded curved (diacritic) mark that is used by some dictionaries in pronunciations to indicate that a vowel is short, as in \kŭt\ for cut, or in poetic scansion to show that a syllable is unstressed in verse. Another example is the haček ( ˇ ), whose name includes the inverted pointed circumflex over the 'c,' that is used in Baltic and Slavonic languages to indicate a change in pronunciation, e.g. the last name of the Czech author Karel Čapek bears the diacritic.

Author: Vikas Raunak (viraunak@microsoft.com)

## What type of a transformation is this?
This transformation removes the accented characters or diacritics on characters, and replaces them with their non-accented versions.

## What tasks does it intend to benefit?
This can simplify the dataset to be used for any task, especially which rely on constructing the embeddings from scratch, since often these rare characters with diacritics lead to poorly formed embeddings. 

## Previous Work
No specific research question is entailed here, except that accented characters might be among the rarest of characters, so it would be inetersting to see how much performance gain one can get by replacing them.

## What are the limitations of this transformation?
The transformation is very simple, it just replaces the accented characters. Howver, one has to be careful to not apply it on chemical formulas or phycial units, since those cases diacritics are super important.
