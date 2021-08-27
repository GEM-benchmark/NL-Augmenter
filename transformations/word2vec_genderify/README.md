# Gender-ify nouns 

This perturbation takes nouns finds their word2vec representation, and then adds the man-vector, and the woman-vector and finds the closest word to the (<noun> + <man/woman>)-vector.

Author names:
- Chandan Singh (chandan_singh@berkeley.edu, UC Berkeley)
- Jamie Simon (james.simon@berkeley.edu, UC Berkeley)
- Sajant Anand (sajant@berkeley.edu, UC Berkeley)
- Roy Rinberg (royrinberg@gmail.com, Columbia University)

## Extra:

You need to run `python -m spacy download en_core_web_sm` before running.

## What type of a transformation is this?

This transformation acts like a perturbation to test robustness. It will transform 1 sentence into a similar sentence that makes grammatical sense, and likely makes good logical sense too. The transformations display relatively high similarity to the source sentences. 

## How it works:

1. Find all the nouns in a sentence. 
2. For each noun, find the word2vec vector for that noun, and add `man`-vector and add `woman` vector. Replace the noun with the closest word to the new (word + man)-vector.

Caveats:
1. Make sure that singular nouns remain singular, and plural nouns remain plural.
2. Often the closest word-vector to (<woman> + <word>) is <woman>. So, some words (like woman or man) are explicitly ignored.

## What tasks does it intend to benefit? 

This transformation could be used to improve datasets for models that seek to improve their implicit bias (i.e. if the dataset comes from a source that always uses the masculine or the feminine version of nouns). 

Further, this same model can be used to add other kinds of words (beyond "man" and "woman") to each of the nouns. Which may allow for a more balanced dataset with regards to equitable vocab expression - i.e. add "young" and "old" vectors to all nouns or "fast" and "slow".

## What are the limitations of this transformation?

The transformation relies on the accuracy of word2vec, and that word2vec vector addition preserves analogy well. This process is hard to predict and edge-cases are difficult to account for with hard-and-fast rules. This transformation does not check whether the transformed sentence makes logical sense; while most cases it works, it's difficult to ensure.

A foreign name like "Dev" which is someone's name, may be interpreted as a developer, and changed like a noun.

## References

* Radim Rehurek , Gensim, Topic Modelling for Humans, [https://radimrehurek.com/gensim/index.html](https://radimrehurek.com/gensim/index.html)

```
@inproceedings{rehurek_lrec,
      title = {{Software Framework for Topic Modelling with Large Corpora}},
      author = {Radim {\v R}eh{\r u}{\v r}ek and Petr Sojka},
      booktitle = {{Proceedings of the LREC 2010 Workshop on New
      Challenges for NLP Frameworks}},
      pages = {45--50},
      year = 2010,
      month = May,
      day = 22,
      publisher = {ELRA},
      address = {Valletta, Malta},
      note={\url{http://is.muni.cz/publication/884893/en}},
      language={English}
}
```






