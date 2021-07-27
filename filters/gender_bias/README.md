## gender bias filter

## What type of a filter is this?

This filter filters a subset of text corpus to measure gender fairness in regards of a female gender representation.
It is based on a pre-defined set personal pronouns, corresponding to the female and male genders accordingly.
Two utility methods - flag_sentences() and count_genders() give supplementary information to the boolean value returned by the filter() method.

Author: Anna Shvets
Company: Fablab by Inetum in Paris

## Why is measuring performance on this split important?
This filter can be used to define whether the female gender is sufficiently represented in a tested subset of sentences.
Being currently implemented for English language, this filter is potentially language-agnostic, since does not rely on any external dependencies.

## Related Work
While the problematics of the gender fairness is an active domain of research in NLP, the current code represents an original implementation.

## What are the limitations of this filter?
The filter result is based exclusively on the personal pronouns, therefore the gender representation is calculated using only this parameter.