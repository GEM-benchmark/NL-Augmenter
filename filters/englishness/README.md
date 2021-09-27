# Englishness Filter
This filter identifies passages that contain uniquely British spellings, vocabulary, or slang.

Author names:
- Jamie Simon (james.simon@berkeley.edu, UC Berkeley)
- Chandan Singh (chandan_singh@berkeley.edu, UC Berkeley)
- Sajant Anand (sajant@berkeley.edu, UC Berkeley)
- Roy Rinberg (royrinberg@gmail.com, Columbia University)  

## Filter overview
The vast majority of English text on the Internet is written with American vocaublary and spelling, but we should aim for language models to work equally well on British English. To that end, this filter aims to help identify text that is written in unambiguously British English. We achieve this with a simple count of words with British spelling (e.g. 'honour'), unambiguously British vocabulary (e.g. 'lorry' or 'sellotape'), and British slang (e.g. 'knackered' or 'odds and sods'). The number of required British words and phrases is provided as an argument to the filter. This filter is specialized to the dialects of England and does not intend to include vocabulary unique to Scotland, Wales, or Northern Ireland.

## What tasks does it intend to benefit?
We expect virtually all NLP tasks to exhibit some bias towards American English, which we hope this filter helps mitigate.

## Previous work
Translation between American and British English has been the subject of a slew of open-source projects in recent years. We used the dictionary of [one of these projects](https://github.com/hyperreality/American-British-English-Translator) to generate our list of distinctly British spellings. Regional differences in English have been the subject of study for centuries, and we agglomerated the rest of our British vocabulary from numerous webpages offering shorter lists.

## What are the limitations of this filter?
This filter just naively selects for the presence of British vocabulary, ignoring subtler stylistic and grammatical differences between the two dialects, so it will inevitably fail to identify passages that a knowledgeable human would recognize as British English. Furthermore, in addition to these false negatives, this filter is prone to false positives, as Americans occasionally still find use for certain British spellings (as with the space shuttle Endeavour), and certain British terms like 'dynamo' and 'the fuzz' still have some trace presence in American English. It is also worth noting that British spellings and slang (e.g. "uni" for "college") are also used in other non-American English speaking countries like Australia, so this is ultimately more of a filter for uniquely non-American English than for specifically British English.

## Filter evaluation
Running `evaluate.py` on this filter yields the following output:

```
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
Applying filtering:
100% 1000/1000 [09:47<00:00,  1.70it/s]
Here is the performance of the model on the filtered set
The accuracy on this subset which has 193 examples = 96.0
```