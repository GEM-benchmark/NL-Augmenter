## Alliteration filter

**Author: Marie Tolkiehn**\
Center for Data and Computing in Natural Sciences, Universität Hamburg\
marie.tolkiehn@desy.de


## What type of a filter is this?

This filter returns True if a sentence is an alliteration and False otherwise.
There is an option to remove stopwords from the sentences, and the default is True (remove stopwords). However, should the sentence solely consist of stop words, will they not be removed

If the input contains more than one sentence, only the first sentence is used and filtered.


## Robustness Evaluation
### Removing Stopwords (True)
Here is the performance of the model on the filtered set:
* **IMDB**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-imdb" -d "imdb" -p 20`\
    The accuracy on this subset which has 24 examples = 100.0
* **SST-2**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-SST-2" -d "sst2" -p 20`\
    The accuracy on this subset which has 4 examples = 100.0
* **QQP** \
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/bert-base-uncased-QQP" -d "qqp" -p 20`\
    The accuracy on this subset which has 28 examples = 96.0
* **MNLI**\
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "roberta-large-mnli" -d "multi_nli" -p 20`\
  The accuracy on this subset which has 77 examples = 91.0

### Not removing stopwords (False)
* **IMDB**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-imdb" -d "imdb" -p 20`\
    The accuracy on this subset which has 8 examples = 100.0
* **SST-2**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-SST-2" -d "sst2" -p 20`\
    The accuracy on this subset which has 1 examples = 100.0
* **QQP** \
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/bert-base-uncased-QQP" -d "qqp" -p 20`\
    The accuracy on this subset which has 1 examples = 100.0
* **MNLI**\
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "roberta-large-mnli" -d "multi_nli" -p 20`\
  The accuracy on this subset which has 22 examples = 91.0


## Data and code source
Data was fully created by the author.
Only the test case involving "Peter and his famous pickled peppers" first appeared in print in 1813 in John Harris's Peter Piper's Practical Principles of Plain and Perfect Pronunciation.


## What are the limitations of this filter?
There may be phonetic alliterations that are not captured by a graphematic approach. For example, `Phonetic` and `Fine` are phonetic alliterations but not graphematic ones.
This could be ameliorated e.g. by using more sophisticated methods such as a pronouncing dictionary by Carnegie Mellon's to compare each word.