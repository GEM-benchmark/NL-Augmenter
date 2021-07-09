## unicode filter

## What type of a filter is this?

This filter filters examples which contain characters outside of a given encoding (by default ascii).
Author: Jan Pfister

## Why is measuring performance on this split important?
This filter can be used to find datapoints containing e.g. non-ascii unicode characters. Filtering out and testing on examples containing these characters can provide feedback for improving models accordingly as most models are trained on plain English text mostly containing ascii characters. Sometimes non-ascii character are even explicitly stripped away.
The same applies for e.g. German models.

## What are the limitations of this filter?
It does not filter for specific characters but only checks for the existence of any character outside the encoding.

## Performance
```
% python evaluate.py -f TextEncodingFilter
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
Loading <imdb> dataset to evaluate <aychang/roberta-base-imdb> model.
Reusing dataset imdb (/Users/janpf/.cache/huggingface/datasets/imdb/plain_text/1.0.0/e3c66f1788a67a89c7058d97ff62b6c30531e05b549de56d3ab91891f0561f9a)
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
Applying filtering:
100%|███████████████████████████████████████████████████████████████████████████| 5000/5000 [00:00<00:00, 307180.50it/s]
Here is the performance of the model on the filtered set
The accuracy on this subset which has 453 examples= 95.14348785871965
```
