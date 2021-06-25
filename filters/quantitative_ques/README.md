## Quantitative question filter

## What type of a filter is this?

This filter is used to identify the quantitative questions

## Why is measuring performance on this split important?
This filter can be used to sepearte out quantiative questions, it helps to analyse models performance on questions which require numerical understanding.It is also usefull to study possible biases in question generation.

python evaluate.py -f TextContainsKeywordsFilter -p=1  
Here is the performance of the model on the filtered set
The accuracy on this subset which has 219 examples= 95.89041095890411

## Related Work

## What are the limitations of this filter?
This filter serves as an example filter. It relies on lexical and purely context-free matching for filtering out examples. 