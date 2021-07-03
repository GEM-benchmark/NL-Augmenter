## Numeric filter

## What type of filter is this?

This filter filters example which contain a numeric value.
Author: Suchitra Dubey
Email: suchitra27288@gmail.com
Affiliation:

## Why is measuring performance on this split important?
This filter can be used to create splits. Filtering out and testing on examples 
contain numeric values can provide feedback for improving training data 
accordingly.

python evaluate.py -f TextContainsNumericFilter -p=1

## Related Work

## What are the limitations of this filter?
This filter serves as an example filter. It relies on lexical and purely context-free
matching for filtering out examples. 