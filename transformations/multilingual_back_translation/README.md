# Multilingual Back Translation
This transformation translates a given sentence from a given language into a pivot language and then back to the original language.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
This transformation is a simple paraphraser that works on 100 different languages thanks to the m2m100 many-to-many translation model. The user only needs to speciffy the source and target language. It is possible to select the same language as source and pivot, in which case the many-to-many translation model will perform a "Direct Translation" from the source language to itslef (while this is faster the output sentences are usualy very similar or identical to the original ones).

## What tasks does it intend to benefit?
This transformations works to increase the data for any task that has input texts.

## What are the limitations of this transformation?
The outputs dependend on the accuracy of the translation model.