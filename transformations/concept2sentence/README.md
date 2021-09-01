# Concept2Sentence (C2S)
This transformation intakes a sentence, its associated integer label, and (optionally) a dataset name that is supported by [`huggingface/datasets`](https://huggingface.co/datasets). It works by extracting keyword concepts from the original sentence, passing them into a BART transformer trained to generate a new, related sentence which reflects the extracted concepts. Providing a dataset allows the function to use `transformers-interpret` to identify the most critical concepts for use in the generative step. 

Author name: Fabrice Harel-Canada
Author email: fabricehc@cs.ucla.edu
Author Affiliation: UCLA

## What type of a transformation is this?
This generative transformation contains two primary steps:
- Extract keyword concepts from the input sentence.
- Generate a new, related sentence from the concepts.

```
Original Sentence: "a disappointment for those who love alternate versions of the bard, particularly ones that involve deep fryers and hamburgers."
Original Label: 0 # (sst2 dataset 0=negative, 1=positive)


Extracted Concepts: ['disappointment', 'for']
New Sentence: "A man is waiting for someone to give him a look of disappointment."
New Label: 0
```

Underneath the hood, this transform makes use of the [Sibyl](https://github.com/fabriceyhc/Sibyl) tool, which is capable of also transforming the label as well. However, this particular implementation of C2S generates new text that is invariant (INV) with respect to the label. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence as input like text classification (especially topic classification and sentiment analysis).

The accuracy of an XLNet model fine-tuned on "ag_news" with / without this transformation is 89.13 / 92.29
The accuracy of an XLNet model fine-tuned on "sst2" with / without this transformation is 88.85 / 93.14

## Previous Work
This transformation is one of many from the [Sibyl](https://github.com/fabriceyhc/Sibyl) tool for text and image augmentations (currently in development for submission). 

## What are the limitations of this transformation?
The underlying BART model was trained on the [`common_gen`](https://huggingface.co/datasets/common_gen) dataset, which itself was sourced from several image captioning datasets. This means that the style of the text outputs are geared towards providing scene descriptions rather than reflecting grammatical structures of the original sentence. 
