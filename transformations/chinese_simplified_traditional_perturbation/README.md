# Chinese Simplified （简体）and Traditional （繁体）Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese words and characters (sentence, paragraph, etc.) by changing the words and characters between Simplified and Traditional Chinese.

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Chinese words or characters that are in Simplified Chinese are picked at random will be replaced with words and characters in
Traditional Chinese. This transformation can also be performed in the opposite direction. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification, 
text generation, etc.

## Previous Work

1) Open Chinese Convert: https://github.com/BYVoid/OpenCC

## What are the limitations of this transformation?
Although it can only perform transformation to convert between Simplified and Traditional Chinese for now, however it can easily be extended to perform more transformation such as
Japanese Kanji, character-level and phrase-level conversion, character variant conversion and regional idioms among Mainland China, Taiwan and Hong Kong.

This will be left as future work for the project.

