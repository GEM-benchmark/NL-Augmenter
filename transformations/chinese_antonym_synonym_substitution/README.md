# Chinese Antonym and Synonym Substitution (To be updated) 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese characters (sentence, paragraph, etc.) proportional to noise erupting 
from keyboard typos making errors resulting from Chinese characters that have similiar Pinyin. 

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Few Chinese characters that are picked at random will be replaced with characters 
that have similar pinyin (based on the default Pinyin keyboards in Windows and Mac OS) where the user may accidentally select the wrong character from the returned results. 

It uses a database of 16142 Chinese characters and its associated pinyins to generate the perturbations.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification, 
text generation, etc.

## Previous Work

1) Database for Chinese characters: https://github.com/pwxcoo/chinese-xinhua

## What are the limitations of this transformation?
There could be Chinese characters that are not within the database of 16142 characters since there are over 50000 Chinese characters.
However, the commonly utilized characters in modern Chinese are around 7000 - 8000 characters and most modern Chinese dictionaries will list around 16000 - 20000 characters so the database should cover most cases.

The current implementation does not take into accents in Pinyin which indicates the intonation (such as ā, á, ǎ, and à). This is fine as commonly used Pinyin keyboards
in Windows and MacOS do not take into accents anyways when typing Pinyin. Nevertheless, there are other types of keyboards that take into account the accents in Pinyin. This will be left as future work for the project.

