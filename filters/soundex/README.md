## Phonetic Match filter

## What type of a filter is this?
This filter returns texts that contain matching entries to a list of supplied keywords, 
evaluated by reducing each token to a phonetic representation. 

Author: [Richard Plant](https://orcid.org/0000-0002-0239-2090)

## Why is measuring performance on this split important?

This filter can help to create more inclusive domain-related splits by relaxing the need to account for 
incorrect spellings. It can also help to include more texts that include related stem words.

```
python evaluate.py -f PhoneticMatchFilter
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
Loading <imdb> dataset to evaluate <aychang/roberta-base-imdb> model.
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
Applying filtering:
100%|█████████████████████████████████████████████| 1000/1000 [00:09<00:00, 102.63it/s]
Here is the performance of the model on the filtered set
The accuracy on this subset which has 415 examples = 96.0
```
## Related Work

[Lakshmanan & Ravindranath (2020) - A Sentiment Polarity Classifier for YouTube Comments with Code-switching between Tamil, Malayalam and English](https://arxiv.org/abs/2010.03189)

## What are the limitations of this filter?

Allowed values for algorithm are:

* 'soundex' (Default) - [American Soundex](https://en.wikipedia.org/wiki/Soundex)
* 'metaphone' - [Metaphone](https://en.wikipedia.org/wiki/Metaphone)
* 'nysiis' - [NYSIIS (New York State Identification and 
  Intelligence System)](https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System)
* 'match_rating_codex' - [Match Rating Approach](https://en.wikipedia.org/wiki/Match_rating_approach)