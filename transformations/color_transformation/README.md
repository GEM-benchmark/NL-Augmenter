# Color Transformation 🦎 → 🐍

This transformation augments the input sentence by randomly replacing colors.

Author name: Seungjae Ryan Lee
Author email: seungjaeryanlee@gmail.com

## What type of a transformation is this?

This transformation searches for colors in the input sentence. Each color is
replaced with a random color.

## What tasks does it intend to benefit?

This perturbation would benefit all tasks which have a sentence / paragraph /
document as input like text classification, text generation, etc. 

## Data and code provenance

The color names are obtained from the 147 extended color keywords specified by
the World Wide Web Consortium (W3C). [1] These include 7 gray/grey variants:
- darkgray/darkgrey,
- darkslategray/darkslategrey,
- dimgray/dimgrey,
- gray/grey,
- lightgray/lightgrey,
- lightslategray/lightgrey, and
- slategray/slategrey

The code was written from scratch by the author of this project.

## What are the limitations of this transformation?

This transformation finds color names by a simple word search, but some color
names have different semantic meaning. Therefore, words that were not intended
to describe color may be transformed. For example, "I am feeling blue" may be
transformed to "I am feeling chocolate."

It is possible for the user to minimize such side effects by specifying a stricter
mapping of colors.

## References

[1] Pemberton, S., &amp; Pettit, B. (2021, August 5). *Css Color Module Level 3*. World Wide Web Consortium (W3C). https://www.w3.org/TR/2021/REC-css-color-3-20210805/. 
