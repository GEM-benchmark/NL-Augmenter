## keywords filter

## What type of a filter is this?

This filter filters example which contain a pre-defined set of keywords.
Author: Zhenhao Li

## Why is measuring performance on this split important?
This filter can be used to create splits of a specific domain. Filtering out and testing on examples belonging to a specific domain can provide feedback for improving training data accordingly.

python evaluate.py -f TextContainsKeywordsFilter -p=1
Here is the performance of the model on the filtered set
The accuracy on this subset which has 219 examples= 95.89041095890411

## Related Work

## What are the limitations of this filter?
This filter serves as an example filter. It relies on lexical and purely context-free matching for filtering out examples.