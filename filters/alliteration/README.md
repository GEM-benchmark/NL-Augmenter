## Alliteration filter

**Author: Marie Tolkiehn**\
Center for Data and Computing in Natural Sciences, Universität Hamburg\
marie.tolkiehn@desy.de


## What type of a filter is this?

This filter returns True if any of the input sentences is an alliteration and False otherwise.
By default, stop words are removed and do not count to the alliteration.
However, should the sentence solely consist of stop words, they will not be removed.

A sentence is deemed an alliteration if it contains words starting with the same character or digraph ("ch", "ph", "sh", "th").
The minimum alliteration length then governs how many words starting with the same first phoneme are required to be deemed a valid alliteration.
The default minimum alliteration length is 3.

These alliterative words do not need to appear contiguously in the sentence.
This means that e.g. "Peter Aquarium prepared a pepperoni pizza." is a valid alliteration
as it contains more than (default) 3 alliterative non-stopword words (despite "Aquarium").

## Why is this filter important?
Alliterations attract audiences.
Alliterations are a stylistic device and trope of literature or poetry.
However, alliterations are around us all the time. From newspaper headlines
("Beer Baron Beats Banner" or "Banner Bars Booze (Booze Barred By Banner)" (c) The Simpsons)
over ads ("Taco Tuesdays"), and company/brand names ("Coca Cola", "Bed, Bath & Beyond", "PayPal"),
protagonists ("Peter Pevensie", "Peter Pan", "Bilbo Baggins", "Donald Duck")
and even academic publications, writers often use alliterations to catch the reader's (or listener's) attention,
as through sound repetition, they are catchy and easy to remember.
Alliterations generally sound pleasing and different phonemes create different rhythms and vibes.
For example, alliterations starting with S are often connected to snake-like features,
whereas alliterations with plosives such as P create a particular rhythm.

This filter could check just how prevalent alliterations are in various types of texts and if there are particular areas they are particularly prevalent.
A good language model may then be able to generate synonymous alliterations from non-alliterative texts.

## Robustness Evaluation
### Removing Stopwords (True), minimum alliteration length = 3
Here is the performance of the model on the filtered set:
* **IMDB**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-imdb" -d "imdb" -p 20`\
    The accuracy on this subset which has 612 examples = 95.0

* **SST-2**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-SST-2" -d "sst2" -p 20`\
    The accuracy on this subset which has 17 examples = 88.0

* **QQP** \
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/bert-base-uncased-QQP" -d "qqp" -p 20`\
    The accuracy on this subset which has 31 examples = 97.0

* **MNLI**\
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "roberta-large-mnli" -d "multi_nli" -p 20`\
  The accuracy on this subset which has 128 examples = 91.0


### Not removing stopwords (False), minimum alliteration length = 3
* **IMDB**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-imdb" -d "imdb" -p 20`\
    The accuracy on this subset which has 886 examples = 95.0
* **SST-2**\
  `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-SST-2" -d "sst2" -p 20`\
    The accuracy on this subset which has 34 examples = 97.0
* **QQP** \
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "textattack/bert-base-uncased-QQP" -d "qqp" -p 20`\
    The accuracy on this subset which has 111 examples = 94.0
* **MNLI**\
    `python evaluate.py -f Alliteration -task "TEXT_CLASSIFICATION" -m "roberta-large-mnli" -d "multi_nli" -p 20`\
  The accuracy on this subset which has 233 examples = 92.0\



## Data and code source
Data was fully created by the author.
Only the test case involving "Peter and his famous pickled peppers" first appeared in print in 1813 in John Harris's Peter Piper's Practical Principles of Plain and Perfect Pronunciation.


## What are the limitations of this filter?
There may be phonetic alliterations that are not captured by a graphematic approach. For example, `Phonetic` and `Fine` are phonetic alliterations but not graphematic ones.
This could be ameliorated e.g. by using more sophisticated methods such as a pronouncing dictionary by Carnegie Mellon's to compare each word.