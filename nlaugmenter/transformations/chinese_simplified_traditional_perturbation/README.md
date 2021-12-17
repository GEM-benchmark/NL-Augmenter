# Chinese Simplified （简体）and Traditional （繁体）Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese words and characters (sentence, paragraph, etc.) by changing the words and characters between Simplified and Traditional Chinese as well as other variants of Chinese Characters
such as Japanese Kanji, character-level and phrase-level conversion, character variant conversion and regional idioms among Mainland China, Taiwan and Hong Kong.

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Words/characters that are in Simplified Chinese are picked at random will be replaced with words/characters in
Traditional Chinese. This transformation can be performed in the opposite direction by changing the ```converter_config```.

### List of configurations available from OpenCC:
* s2t.json Simplified Chinese to Traditional Chinese 簡體到繁體
* t2s.json Traditional Chinese to Simplified Chinese 繁體到簡體
* s2tw.json Simplified Chinese to Traditional Chinese (Taiwan Standard) 簡體到臺灣正體
* tw2s.json Traditional Chinese (Taiwan Standard) to Simplified Chinese 臺灣正體到簡體
* s2hk.json Simplified Chinese to Traditional Chinese (Hong Kong variant) 簡體到香港繁體
* hk2s.json Traditional Chinese (Hong Kong variant) to Simplified Chinese 香港繁體到簡體
* s2twp.json Simplified Chinese to Traditional Chinese (Taiwan Standard) with Taiwanese idiom 簡體到繁體（臺灣正體標準）並轉換爲臺灣常用詞彙
* tw2sp.json Traditional Chinese (Taiwan Standard) to Simplified Chinese with Mainland Chinese idiom 繁體（臺灣正體標準）到簡體並轉換爲中國大陸常用詞彙
* t2tw.json Traditional Chinese (OpenCC Standard) to Taiwan Standard 繁體（OpenCC 標準）到臺灣正體
* hk2t.json Traditional Chinese (Hong Kong variant) to Traditional Chinese 香港繁體到繁體（OpenCC 標準）
* t2hk.json Traditional Chinese (OpenCC Standard) to Hong Kong variant 繁體（OpenCC 標準）到香港繁體
* t2jp.json Traditional Chinese Characters (Kyūjitai) to New Japanese Kanji (Shinjitai) 繁體（OpenCC 標準，舊字體）到日文新字體
* jp2t.json New Japanese Kanji (Shinjitai) to Traditional Chinese Characters (Kyūjitai) 日文新字體到繁體（OpenCC 標準，舊字體）
* tw2t.json Traditional Chinese (Taiwan standard) to Traditional Chinese 臺灣正體到繁體（OpenCC 標準）

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification,
text generation, etc.

## Robustness Evaluation
Code to evaluate the model:
```python evaluate.py -t ChineseSimplifiedTraditionalPerturbation -task "TEXT_CLASSIFICATION" -l "zh" -m "clue/roberta_chinese_base" -d "clue" -p 10```
```model_name = "clue/roberta_chinese_base"```
```dataset_name = "clue"```
The accuracy of a RoBERTa model (fine-tuned on CLUE) (model: "clue/roberta_chinese_base") on a subset of CLUE dataset = 60
The accuracy of the same model on the perturbed set = 60

## Previous Work

1) Open Chinese Convert: https://github.com/BYVoid/OpenCC

## What are the limitations of this transformation?
It depends on the implementation by the OpenCC project.

