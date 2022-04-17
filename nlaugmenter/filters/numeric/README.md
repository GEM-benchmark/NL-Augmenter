## Numeric filter

## What type of filter is this?

This filter filters example which contain a numeric value, so that utterraces with or without numeric values can be evaluated separately.   <br>
+ Author: Suchitra Dubey
+ Email: suchitra27288@gmail.com
+ Affiliation: Acko

## Why is measuring performance on this split important?
In the tasks like textual entailment, question answering etc. where a quantity (number) could directly affect
the final label/response, we can use this split to measure the performance separately on utterances containing
numeric values.

### How to use this filter?
`python evaluate.py -f TextContainsNumericFilter -p=1` <br>

### Evaluation Results #1
model: `textattack/bert-base-uncased-snli` <br>
split: `20%` <br>
dataset: `snli` <br>

| Sentence Type | Number of samples| EM|
|--------------------|------|--------|
|All| 1000| 89.0|
|Non-Numeric | 757| 90.0|
|Numeric|243| 88.0|

### Evaluation Results #2
model: `roberta-large-mnli` <br>
split: `20%` <br>
dataset: `multi_nli` <br>

| Sentence Type | Number of samples| EM|
|--------------------|------|--------|
|All| 1000| 91.0|
|Non-Numeric | 747| 92.0|
|Numeric|253| 89.0|
## Related Work

## What are the limitations of this filter?
This filter relies on lexical and purely context-free
matching for filtering out examples.