# Chinese Person Named Entities（名字) and Gender （性别） Perturbation  🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese names (sentence, paragraph, etc.) by changing a Chinese name with another Chinese name whilst also performing gender swap if the user choose to do so.

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What does this transformation do?
For Chinese names that has been identified though Named Entity Recognition (NER), this transformation will replace it by randomly selects another Chinese name from a database of Chinese Names. This can be adjusted to take into account of gender when performing the transformation.

## Why is this transformation important?
The transformation can allow us to evaluate the biases for language models and its ability to infer implicit gender information when presented with gender-specific names. This can be useful in mitigating representation biases in the input text.

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Chinese Names that are detected in the sentence will be replaced with a random Chinese names from the database that are of the same or opposite gender depending on setting.  

It uses CLUENER for Named Entity Recognition, database of 1.2 million Chinese names and its associated gender to generate the perturbations.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification, 
text generation, etc.

## Robustness Evaluation
Code to evaluate the model:
```python evaluate.py -t ChinesePersonNamedEntitiesAndGender -task "TEXT_CLASSIFICATION" -l "zh" -m "clue/roberta_chinese_base" -d "clue" -p 1```
```model_name = "clue/roberta_chinese_base"```
```dataset_name = "clue"```
The accuracy of a RoBERTa model (fine-tuned on CLUE) (model: "clue/roberta_chinese_base") on a subset of CLUE dataset = 67
The accuracy of the same model on the perturbed set = 67

## Previous Work

1) Database for Chinese Names: https://github.com/wainshine/Chinese-Names-Corpus
2) English version of Gender Sensitivity Benchmark: https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/gender_sensitivity_English
3) CLUENER2020 for Chinese Named Entity Recognition: https://huggingface.co/uer/roberta-base-finetuned-cluener2020-chinese

```bibtex

@article{xu2020cluener2020,
  title={CLUENER2020: Fine-grained Name Entity Recognition for Chinese},
  author={Xu, Liang and Dong, Qianqian and Yu, Cong and Tian, Yin and Liu, Weitang and Li, Lu and Zhang, Xuanwei},
  journal={arXiv preprint arXiv:2001.04351},
  year={2020}
 }
 
@article{zhao2019uer,
  title={UER: An Open-Source Toolkit for Pre-training Models},
  author={Zhao, Zhe and Chen, Hui and Zhang, Jinbin and Zhao, Xin and Liu, Tao and Lu, Wei and Chen, Xi and Deng, Haotang and Ju, Qi and Du, Xiaoyong},
  journal={EMNLP-IJCNLP 2019},
  pages={241},
  year={2019}
}
```

## What are the limitations of this transformation?
Chinese Names that are recognized by the CLUENER model will be selected for perturbation. Chinese names/gender pair that are also not within the database of 1.2 million Chinese names will not be considered for perturbations. 

The NER model can be changed and the database can be updated with more Chinese names so this will be left as future work for the project.

