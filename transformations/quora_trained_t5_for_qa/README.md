# Quora Trained T5 for question paraphrases for QA Task 🦎  + ⌨️ → 🐍
This transformation creates new QA pairs by generating question paraphrases from a T5 model fine-tuned on Quora Question pairs.   

## What type of a transformation is this?
This transformation acts like a paraphrase generator. Generated questions can have a very different surface form from the original question making it a strong paraphrase generator. A T5 model was fine tuned on the Quora Question Pairs dataset and is being used to generate question paraphrases.

## What tasks does it intend to benefit?
This transformation would benefit Question Answering and Question Generation.

```python evaluate.py -t QuoraT5QaPairGenerator -task QUESTION_ANSWERING```


## Previous Work & Citations
The training script is available here: https://github.com/ramsrigouthamg/Paraphrase-any-question-with-T5-Text-To-Text-Transfer-Transformer-
The corresponding HuggingFace model has been sourced from here: https://huggingface.co/ramsrigouthamg/t5_paraphraser 

## What are the limitations of this transformation?
The transformation's outputs only modify the question and not the context and the answers. The model would might be biased towards topics focused in Quora.  
