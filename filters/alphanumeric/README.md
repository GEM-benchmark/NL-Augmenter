## Alphanumeric Characters Filter

## What type of filter is this?

This transformation filters text that contains characters which are non-alphanumeric and not common punctuation.
The alphabetical characters are determined by the 26 letters of the English alphabet.

Author: Mo Tiwari
Author Email: motiwari@stanford.edu
Author Affiliation: Stanford University

## Why is measuring performance on this split important?
This filter can be used to a) select text with only characters from a standard alphabet and 
b) remove characters that are specifically meant to circumvent filters e.g. text that uses 
`buy some pi//s` if the string `buy some pills` triggers spam filters 

This is of import in domains such as profanity detection and spam, where bad actors may attempt to work around existing filters by using characters that can be easily mistaken for others.

## Related Work

N/A 

## What are the limitations of this filter?
- Currently, the filter only permits characters as defined by the English alphabet. 
The filter could be extended to handle the characters from other alphabets via the `args`
provided.