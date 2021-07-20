# Tumblr Text

This transformation adds spaces between all characters.  For example,
the text:

`Hello, how are you?`

becomes:

`H e l l o ,   h o w   a r e   y o u ?`


In the 2010s, this genre of transformation was exploited for aesthetic
effect on social media sites like tumblr.  It also provides a
challenge for NLP tasks, as tumblr text trivially defeats many
tokenization approaches while remaining intelligible to human readers.


Author name: Patrick O'Neill

Author email: patrick.kaileigh.oneill@gmail.com

Author Affiliation: Kensho Technologies

## What type of a transformation is this?
The transformation simply inserts spaces between every pair of
adjacent characters, altering the tokenization while preserving the
sense of the text.

## What tasks does it intend to benefit?
This transformation could be applied in any task that stands to
benefit from robust tokenization.


## What are the limitations of this transformation?
The transformation is fairly trivial and hardly exhausts the potential
for tokenization-resistant transformations.
