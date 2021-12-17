# Concept2Sentence (C2S)
This transformation intakes a sentence, its associated integer label, and (optionally) a dataset name that is supported by [`huggingface/datasets`](https://huggingface.co/datasets). It works by extracting keyword concepts from the original sentence, passing them into a BART transformer trained to generate a new, related sentence which reflects the extracted concepts. Providing a dataset allows the function to use `transformers-interpret` to identify the most critical concepts for use in the generative step.

Author name: Fabrice Harel-Canada
Author email: fabricehc@cs.ucla.edu
Author Affiliation: UCLA

## What type of a transformation is this?
This generative transformation contains two primary steps:
- Extract keyword concepts from the input sentence(s).
- Generate a new, related sentence from the extracted concepts.

It is also possible to provide a `target` label and `dataset` name to aid with concept extraction. If the `huggingface_hub` already has models fine-tuned for the given `dataset`, one will be automatically downloaded / loaded from cahche and used to score input saliency for the `target` label - i.e. finding which parts of the sentence are the most important. This helps extract better concepts and generate more semantically comparable outputs. For example:

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
This transformation is one of many from the [Sibyl](https://github.com/fabriceyhc/Sibyl) tool for text and image augmentations (currently in development for conference submission).

## What are the limitations of this transformation?
The underlying BART model was trained on the [`common_gen`](https://huggingface.co/datasets/common_gen) dataset, which itself was sourced from several image captioning datasets. This means that the style of the text outputs are geared towards providing scene descriptions rather than reflecting grammatical structures of the original sentence.

## Example Tests

Since the default configuration of the transformation features elements of randomness for the sake of diversity, a fixed test is not feasible. However, in the interest of illustrating some additional examples, the following code can be used to generate a test.json file.

```python
import json
tf = C2S(max_outputs=1)
test_cases = [("I hate how long loading the models takes to select better keyphrases.", 1, "sst2"),
              ("I really love this movie a lot!", 1, "sst2"),
              ("David Beckham scores 10 goals to win the game for Manchester United.", 1, "ag_news"),
              ("The Pentagon has released the names of the following us service members killed recently in Iraq.", 0, "ag_news"),
              ("America's best airline? Hawaiian Airlines is putting up impressive numbers, including some that really matter to travelers", 2, "ag_news"),]
results = []
for (sentence, target, dataset) in test_cases:
    # uncomment to get better extracted concepts
    # tf = C2S(max_outputs=1, dataset=dataset)
    new_sentence, new_target = tf.generate(sentence, target)
    results.append({
        "class": tf.name(),
        "inputs": {"sentence": sentence, "target": target},
        "outputs": {"new_sentence": new_sentence, "new_target": new_target}
    })
json_file = {"type": tf.name(), "test_cases": results}
print(json.dumps(json_file, indent=2))
```
```json
{
  "type": "C2S",
  "results": [
    {
      "class": "C2S",
      "inputs": {
        "sentence": "I hate how long loading the models takes to select better keyphrases.",
        "target": 1
      },
      "outputs": {
        "new_sentence": "i hate the idea of loading i have to wait a long time.",
        "new_target": 1
      }
    },
    {
      "class": "C2S",
      "inputs": {
        "sentence": "I really love this movie a lot!",
        "target": 1
      },
      "outputs": {
        "new_sentence": "i really love this movie and i really love it.",
        "new_target": 1
      }
    },
    {
      "class": "C2S",
      "inputs": {
        "sentence": "David Beckham scores 10 goals to win the game for Manchester United.",
        "target": 1
      },
      "outputs": {
        "new_sentence": "dramatic scene of a young man playing guitar with a young boy who is learning how to play the guitar.",
        "new_target": 1
      }
    },
    {
      "class": "C2S",
      "inputs": {
        "sentence": "The Pentagon has released the names of the following us service members killed recently in Iraq.",
        "target": 0
      },
      "outputs": {
        "new_sentence": "the car has been released from thepentagon.",
        "new_target": 0
      }
    },
    {
      "class": "C2S",
      "inputs": {
        "sentence": "America's best airline? Hawaiian Airlines is putting up impressive numbers, including some that really matter to travelers",
        "target": 2
      },
      "outputs": {
        "new_sentence": "american Airlines is the best airline in the world.",
        "new_target": 2
      }
    }
  ]
}
```