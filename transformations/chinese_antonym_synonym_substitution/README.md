# Chinese Antonym (反义词) and Synonym (同义词) Substitution 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese words and characters (sentence, paragraph, etc.) by changing words and characters with its synonyms（同义词）or antonyms（反义词）from a database of synonyms and antonyms.

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Word segmentation is performed on the input text and Chinese words that are picked at random will be replaced with words 
that have similar meaning or opposite meanings (based on the synonyms and antonyms list) to generate perturbations.

## Robustness Evaluation
Code to evaluate the model:
```python evaluate.py -t ChineseAntonymAndSynonymSubtitution -task "TEXT_CLASSIFICATION" -l "zh" -m "clue/roberta_chinese_clue_large" -d "clue" -p 1```
```model_name = "clue/roberta_chinese_clue_large"```
```dataset_name = "clue"```
The accuracy of a RoBERTa model (fine-tuned on CLUE) (model: "clue/roberta_chinese_clue_large") on a subset of CLUE dataset = 67
The accuracy of the same model on the perturbed set = 67

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification, 
text generation, etc.

## Previous Work

1) Database for Synonyms and Antonyms: https://github.com/guotong1988/chinese_dictionary
2) NLPCDA: https://github.com/425776024/nlpcda

## What are the limitations of this transformation?
There could be synonyms and antonyms of Chinese words that are not present within the database.

This perturbation can be improved by providing a larger database of synonyms and antonyms. This will be left as future work for the project.

