## Ambiguous Characters Filter

## What type of a filter is this?

This filter filters sentences that contain ambiguous characters.

Author: Mo Tiwari
Author Email: motiwari@stanford.edu
Author Affiliation: Stanford University

## Why is measuring performance on this split important?
This filter can be used to either a) select text with ambiguous characters, or b) select text that contains only unambiguous characters.
This is of import in domains such as profanity detection and spam, where bad actors may attempt to work around existing filters by using characters that can be easily mistaken for others.

For example, "Buy some piIIs here" actually contains two capital `I`s for `l`s.

## Related Work

N/A 

## What are the limitations of this filter?
- The filter depends on font; fonts may have different sets of ambiguous characters 