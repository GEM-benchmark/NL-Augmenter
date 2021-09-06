## Toxicity filter

## What type of a filter is this?

This filter filters an example text which has a toxicity value matching a particular threshold.
Author: Saqib N. Shamsi

Toxicity labels supported:
* ToxicityTypes.TOXICITY
* ToxicityTypes.SEVERE_TOXICITY
* ToxicityTypes.OBSCENE
* ToxicityTypes.IDENTITY_ATTACK
* ToxicityTypes.INSULT
* ToxicityTypes.THREAT
* ToxicityTypes.SEXUAL_EXPLICIT

## Why is this filter important?
Language generation models which have been trained on data with hate speech can learn to produce samples containing hate speech.

## What are the limitations of this filter?
Since this model uses a model which was trained for toxicity detection, the quality of data the model was trained on and model's performance would affect the accuracy with which toxic text would be detected and filtered.