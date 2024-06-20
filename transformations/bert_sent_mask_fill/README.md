# BERT Sentence Mask Filling 🦎  + 🎭 → 🐍
This transformation generates similar sentences by applying BERT mask filling to keywords.

Author name: Het Pandya

Author email: hetpandya6797@gmail.com

## What type of a transformation is this?
This transformation augments text using mask filling to replace keywords with other words. For that, the words that can be masked are found using spacy to extract keywords from a sentence. Once the keywords are found, they are replaced with a mask and fed to the BERT model to predict a word in place of the masked word.

## What tasks does it intend to benefit?
This transformation can help generate synthetic data where the number of samples is less in amount.

## What are the limitations of this transformation?
Although, the transformation can generate a healthy amount of similar samples, they will be very simple as compared to the outputs of a paraphraser.