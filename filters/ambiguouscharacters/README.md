## Ambiguous Characters Filter

## What type of a filter is this?

This filter filters sentences that contain ambiguous characters.
(Aside: `Buffalo buffalo buffalo Buffalo buffalo Buffalo buffalo buffalo --> Filter filters filter filter filters filter filters filter`?)

Author: Mo Tiwari
Author Email: motiwari@stanford.edu
Author Affiliation: Stanford University

## Why is measuring performance on this split important?
This filter can be used to either a) select text with ambiguous characters, or b) select text that contains only unambiguous characters.
This is of import in domains such as profanity detection and spam, where bad actors may attempt to work around existing filters by using characters that can be easily mistaken for others.

For example, "Buy some piIIs here" actually contains two capital `I`s for `l`s.

This feature is also common in password managers, e.g. as a setting to avoid ambiguous characters when generating
passwords.

## Related Work

N/A 

## What are the limitations of this filter?
- The usefulness of the filter depends on font in which the initial text was rendered; future work could accept the 
source font as an argument
- The filter is also primarily useful for the English language.