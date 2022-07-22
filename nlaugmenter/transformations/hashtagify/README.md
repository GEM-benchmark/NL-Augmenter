# Hashtagify

This transformation adapts an input sentence by identifying named entities and other common words and turning them into hashtags, as often used in social media.

Authors: [Shahab Raji](mailto:shahab.raji@rutgers.edu) (Rutgers University) and [Gerard de Melo](http://gerard.demelo.org/) (Hasso Plattner Institute / University of Potsdam)


## How does the transformation work?

Hashtagify uses named entity recognition and part-of-speech tagging to turn certain words or phrases in the sentence into hashtags. This transformation converts the sentence to a social media style text to support the generalizability of NLP models.

In more detail, Hashtagify identifies named entities, nouns, and verbs and adds the hash character "#" prefix to turn them into hashtags. The hashtags are added to each candidate word according to a fixed probability. Stopwords are not hashtagged. Multi-word named entities are handled by removing the spaces and capitalizing the first letter of each word. The syntactic and semantic structure of the sentence is preserved during the transformation.

Examples:

```
New Delhi is among the many famous places in India.
```

to

```
#NewDelhi is among the many famous places in India.
```


## Target Tasks

This transformation can be used for augmenting the text in classification and generation tasks.


## Limitations

- Non-neural NER models sometimes fail to identify the named entities correctly. A fine-tuned model based on the input data can be used to improve the performance of the NER model.
- Hashtags are sometimes added to unusual words or based on some trends.

