# Emoji Icon Transformation
This perturbation adds noise to text sources (sentence, paragraph, etc.) containing emoji or icons.

Author name: Marco Di Giovanni
Author email: marco.digiovanni@polimi.it
Author Affiliation: Politecnico di Milano and University of Bologna

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness.
We can select to convert emojis to similar icons (e.g., "🙂" -> ":)" ) or icons to similar emojis (e.g., ":)" -> "🙂" )
Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations.

## What tasks does it intend to benefit?
This perturbation would benefit tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.
However, only sentences containing icons or emojis are perturbed.
It would mainly benefit texts from social networks or texts from messaging platforms.

## References

https://en.wikipedia.org/wiki/List_of_emoticons

## What are the limitations of this transformation?
- The transformation's outputs are very simple and does not affect formal texts.
- It is implemented such that you can convert emoji2icon or icon2emoji but not both (although this could be fixed).
