# Chinese Person Named Entities（名字) and Gender （性别） Perturbation  🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese names (sentence, paragraph, etc.) by changing a Chinese name with another Chinese name whilst also performing gender swap if the user choose to do so.

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What does this transformation do?
For a Chinese name that has been identified in the database after segmenting the input text, this transformation will replace it by randomly selects another Chinese name from the database. This can be adjusted to take into account gender when performing the transformation.

## Why is this transformation important?
1. The transformation can allow us to evaluate the biases for language models and its ability to infer implicit gender information when presented with gender-specific names. This can be useful in mitigating representation biases in the input text.

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Chinese Names that are detected in the sentence will be replaced with a random Chinese names from the database that are of the same or opposite gender depending on setting.  

It uses a database of 1.2 million Chinese names and its associated gender to generate the perturbations.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification, 
text generation, etc.

## Previous Work

1) Database for Chinese Names: https://github.com/wainshine/Chinese-Names-Corpus
2) English version of Gender Sensitivity Benchmark: https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/gender_sensitivity_English

## What are the limitations of this transformation?
Chinese names/gender pair that are not within the database of 1.2 million Chinese names will not be considered for perturbations.

The database can be updated with more Chinese names so this will be left as future work for the project.

