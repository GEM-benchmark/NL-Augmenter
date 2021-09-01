# Diacritic Removal 
This perturbation removes the diacritics on characters in a sentence.

Author: Vikas Raunak (viraunak@microsoft.com)

## What type of a transformation is this?
This transformation removes the accented characters or diacritics on characters, and replaces them with their non-accented versions.

## What tasks does it intend to benefit?
This can simplify the dataset to be used for any task, especially which rely on constructing the embeddings from scratch, since often these rare characters with diacritics lead to poorly formed embeddings. 

## Previous Work
No specific research question is entailed here, except that accented characters might be among the rarest of characters, so it would be inetersting to see how much performance gain one can get by replacing them.

## What are the limitations of this transformation?
The transformation is very simple, it just replaces the accented characters. Howver, one has to be careful to not apply it on chemical formulas or phycial units, since those cases diacritics are super important.
