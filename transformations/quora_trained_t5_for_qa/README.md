# Quora Trained T5 for question paraphrases for QA Task ❓️ → 🐍❔
This transformation creates new QA pairs by generating question paraphrases from a T5 model fine-tuned on Quora Question pairs.   

## What type of a transformation is this?
This transformation acts like a paraphrase generator. Generated questions can have a very different surface form from the original question making it a strong paraphrase generator. A T5 model was fine tuned on the Quora Question Pairs dataset and is being used to generate question paraphrases.

## What tasks does it intend to benefit?
This transformation would benefit Question Answering and Question Generation.

Robustness Evaluation:
```python evaluate.py -t QuoraT5QaPairGenerator -task QUESTION_ANSWERING```

Here is the performance of the model mrm8488/bert-tiny-5-finetuned-squadv2 on the validation[:20%] split of the squad dataset
The accuracy on a subset of squad = 60.31220435193945
The accuracy on its perturbed set generated from = 47.161778618732264

## Previous Work & Citations
The training script is available here: https://github.com/ramsrigouthamg/Paraphrase-any-question-with-T5-Text-To-Text-Transfer-Transformer-
The corresponding HuggingFace model has been sourced from here: https://huggingface.co/ramsrigouthamg/t5_paraphraser 

## What are the limitations of this transformation?
The transformation's outputs only modify the question and not the context and the answers. The model might be biased towards topics focused in Quora.
